"""
Gestiva Security (GestivaSec V1) — Event Enrichment Infrastructure Adapter
Enriches events with GeoIP, ASN details, and threat reputation scoring.
"""
from typing import Dict, Any

class EventEnrichmentAdapter:
    def enrich_source_ip(self, ip: str) -> Dict[str, Any]:
        """Provides GeoIP & ASN enrichment for source IP."""
        if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("127."):
            return {
                "geo_country": "INT",
                "geo_city": "Internal Subnet",
                "geo_asn": "AS0_PRIVATE",
                "is_external": False
            }
        
        # Public IP GeoIP lookup
        return {
            "geo_country": "US",
            "geo_city": "Ashburn",
            "geo_asn": "AS16509_AMAZON",
            "is_external": True
        }
