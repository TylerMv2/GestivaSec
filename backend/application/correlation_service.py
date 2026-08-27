"""
Gestiva Security (GestivaSec V1) — SPRINT 7: Multi-Event Correlation Engine Application Service
Correlates independent Findings over Sliding Time-Windows into High-Priority Attack Chains mapped to MITRE ATT&CK.
"""
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from backend.domain.detection_rule import Finding
from backend.domain.correlation import AttackChain, AttackChainNode, CorrelationRule
from backend.infrastructure.sliding_window_buffer import SlidingWindowBuffer

_ATTACK_CHAINS_STORE: List[AttackChain] = []
_CORRELATION_RULES_STORE: List[CorrelationRule] = [CorrelationRule()]
_SLIDING_WINDOW_BUFFER = SlidingWindowBuffer(window_minutes=15)

class CorrelationEngineService:
    def __init__(self, buffer: Optional[SlidingWindowBuffer] = None):
        self.buffer = buffer or _SLIDING_WINDOW_BUFFER

    def _map_mitre_phase(self, rule_id: str) -> str:
        """Maps rule ID to MITRE Kill Chain Phase."""
        rule_id_upper = rule_id.upper()
        if "RECON" in rule_id_upper or "GEOIP" in rule_id_upper:
            return "RECONNAISSANCE"
        elif "BRUTE" in rule_id_upper or "AUTH" in rule_id_upper:
            return "EXPLOITATION"
        elif "PRIV" in rule_id_upper or "ESCALATION" in rule_id_upper:
            return "PRIVILEGE_ESCALATION"
        return "EXFILTRATION"

    def _calculate_explainable_score(self, related_findings: List[Finding], stages: set, asset_id: Optional[str], target_ip: str) -> (int, float, List[str]):
        score = 40
        reasons = []
        if asset_id:
            score += 20
            reasons.append("+ Target Asset UUID correlated")
        if target_ip:
            score += 15
            reasons.append("+ Common Source IP correlated")
        if len(related_findings) >= 3:
            score += 15
            reasons.append(f"+ High event density ({len(related_findings)} findings within window)")
        if len(stages) >= 2:
            score += 10
            reasons.append(f"+ Multi-phase MITRE attack sequence ({len(stages)} stages)")
        
        score = min(score, 100)
        confidence = min(0.50 + (len(stages) * 0.15), 0.98)
        return score, confidence, reasons

    async def process_finding(self, finding: Finding) -> Optional[AttackChain]:
        """Correlates new finding against sliding window buffer per Asset UUID / IP."""
        self.buffer.add_finding(finding)
        related_findings = self.buffer.get_findings_for_asset(finding.asset_id, finding.source_ip)

        # Threshold: Require at least 2 distinct findings to trigger an Attack Chain Sequence
        if len(related_findings) < 2:
            return None

        # Build / Update AttackChain
        now = datetime.now(timezone.utc)
        target_ip = finding.source_ip
        asset_id = finding.asset_id

        # Check existing active chain for asset/IP
        existing_chain = None
        for chain in _ATTACK_CHAINS_STORE:
            if chain.organization_id == finding.organization_id and chain.status == "ACTIVE":
                if (asset_id and chain.asset_id == asset_id) or (chain.target_ip == target_ip):
                    existing_chain = chain
                    break

        nodes = []
        stages = set()
        timeline = []
        for f in related_findings:
            phase = self._map_mitre_phase(f.rule_id)
            stages.add(phase)
            node = AttackChainNode(
                finding_id=f.finding_id,
                rule_id=f.rule_id,
                rule_title=f.rule_title,
                severity=f.severity,
                mitre_phase=phase,
                asset_id=f.asset_id,
                source_ip=f.source_ip
            )
            nodes.append(node)
            timeline.append({
                "timestamp": f.created_at.isoformat() if hasattr(f, 'created_at') else now.isoformat(),
                "type": "FINDING",
                "id": f.finding_id,
                "title": f.rule_title,
                "severity": f.severity,
                "phase": phase
            })

        score, confidence, reasons = self._calculate_explainable_score(related_findings, stages, asset_id, target_ip)

        if existing_chain:
            existing_chain.nodes = nodes
            existing_chain.kill_chain_stages = list(stages)
            existing_chain.correlation_score = score
            existing_chain.confidence_score = confidence
            existing_chain.explainable_reasons = reasons
            existing_chain.timeline = timeline
            existing_chain.last_seen = now
            return existing_chain
        else:
            new_chain = AttackChain(
                organization_id=finding.organization_id,
                asset_id=asset_id,
                target_ip=target_ip,
                chain_title=f"Correlated Multi-Stage Attack Sequence ({len(stages)} MITRE Phases)",
                severity="P1_CRITICAL",
                status="ACTIVE",
                correlation_score=score,
                confidence_score=confidence,
                explainable_reasons=reasons,
                nodes=nodes,
                kill_chain_stages=list(stages),
                timeline=timeline,
                first_seen=now,
                last_seen=now
            )
            _ATTACK_CHAINS_STORE.append(new_chain)

            # Auto-promote P1 Critical Attack Chains to Incident Cases (Sprint 8)
            try:
                from backend.application.incident_case_service import IncidentCaseApplicationService
                case_service = IncidentCaseApplicationService()
                await case_service.create_case(
                    organization_id=new_chain.organization_id,
                    title=new_chain.chain_title,
                    description=f"Correlated MITRE Attack Sequence on target IP {target_ip}",
                    severity="P1_CRITICAL",
                    asset_id=asset_id,
                    target_ip=target_ip,
                    attack_chain_id=new_chain.chain_id
                )
            except Exception:
                pass

            return new_chain

    def get_attack_chain(self, chain_id: str) -> Optional[AttackChain]:
        for c in _ATTACK_CHAINS_STORE:
            if c.chain_id == chain_id:
                return c
        return None

    def list_attack_chains(self, organization_id: str, limit: int = 50) -> List[AttackChain]:
        """Returns active attack chains for tenant (BR-0004)."""
        filtered = [c for c in _ATTACK_CHAINS_STORE if c.organization_id == organization_id]
        return filtered[-limit:]

    def get_chain_timeline(self, chain_id: str) -> Optional[List[Dict[str, Any]]]:
        chain = self.get_attack_chain(chain_id)
        if chain:
            return chain.timeline
        return None

    def close_attack_chain(self, chain_id: str) -> Optional[AttackChain]:
        chain = self.get_attack_chain(chain_id)
        if chain:
            chain.status = "RESOLVED"
            return chain
        return None

    def list_rules(self, organization_id: str) -> List[CorrelationRule]:
        return [r for r in _CORRELATION_RULES_STORE if r.organization_id == organization_id or r.organization_id == "00000000-0000-0000-0000-000000000001"]

    def add_rule(self, rule: CorrelationRule) -> CorrelationRule:
        _CORRELATION_RULES_STORE.append(rule)
        return rule
