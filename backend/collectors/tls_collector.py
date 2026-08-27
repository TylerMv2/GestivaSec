import ssl
import socket
import datetime
from OpenSSL import crypto
from backend.collectors.base import BaseCollector
from backend.models.service import Service
from backend.models.certificate import Certificate

class TLSCollector(BaseCollector):
    name = "TLSCollector"

    def _get_tls_details(self, hostname: str, port: int) -> dict:
        """
        Connects via SSL/TLS and retrieves certificate details.
        Does not break encryption; retrieves publicly visible TLS handshake info.
        """
        context = ssl.create_default_context()
        # Allow checking even if expired (to record details)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        details = {
            "version": "Unknown",
            "cipher": "Unknown",
            "issuer": "Unknown",
            "algorithm": "Unknown",
            "valid_from": None,
            "valid_to": None,
            "days_remaining": 0,
            "status": "Unknown"
        }
        
        try:
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher_info = ssock.cipher()
                    if cipher_info:
                        details["cipher"] = cipher_info[0]
                        details["version"] = cipher_info[1]
                    
                    # Fetch binary cert to parse detailed attributes with pyOpenSSL / cryptography
                    bin_cert = ssock.getpeercert(binary_form=True)
                    if bin_cert:
                        x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, bin_cert)
                        
                        # Extract issuer
                        issuer_components = x509.get_issuer().get_components()
                        issuer_parts = [f"{k.decode('utf-8')}={v.decode('utf-8')}" for k, v in issuer_components]
                        details["issuer"] = ", ".join(issuer_parts)
                        
                        # Extract signature algorithm
                        details["algorithm"] = x509.get_signature_algorithm().decode('utf-8')
                        
                        # Parse validity dates
                        # Format: YYYYMMDDHHMMSSZ
                        not_before_str = x509.get_notBefore().decode('utf-8')
                        not_after_str = x509.get_notAfter().decode('utf-8')
                        
                        valid_from = datetime.datetime.strptime(not_before_str, "%Y%m%d%H%M%SZ")
                        valid_to = datetime.datetime.strptime(not_after_str, "%Y%m%d%H%M%SZ")
                        
                        details["valid_from"] = valid_from
                        details["valid_to"] = valid_to
                        
                        now = datetime.datetime.utcnow()
                        delta = valid_to - now
                        days = delta.days
                        details["days_remaining"] = days
                        
                        if days < 0:
                            details["status"] = "Expired"
                        elif days < 30:
                            details["status"] = "Expiring"
                        else:
                            details["status"] = "Valid"
                            
            return details
        except Exception as e:
            logger.error(f"Error fetching TLS details for {hostname}:{port}: {e}")
            return None

    def run(self):
        if not self.is_enabled():
            return

        # Scan services on port 443 (HTTPS)
        tls_services = self.db.query(Service).filter(Service.port == 443).all()
        
        for service in tls_services:
            host = service.host
            # Use hostname for SNI, fallback to IP if hostname not available
            target_host = host.hostname if host.hostname else host.ip
            
            tls_data = self._get_tls_details(target_host, service.port)
            
            if tls_data:
                # Find or create certificate record
                cert = self.db.query(Certificate).filter(
                    Certificate.service_id == service.id,
                    Certificate.host_id == host.id
                ).first()
                
                if not cert:
                    cert = Certificate(
                        service_id=service.id,
                        host_id=host.id,
                        domain=target_host
                    )
                    self.db.add(cert)
                
                cert.issuer = tls_data["issuer"]
                cert.signature_algorithm = tls_data["algorithm"]
                cert.valid_from = tls_data["valid_from"]
                cert.valid_to = tls_data["valid_to"]
                cert.days_remaining = tls_data["days_remaining"]
                cert.status = tls_data["status"]
                cert.cipher_suite = tls_data["cipher"]
                cert.tls_version = tls_data["version"]
                cert.updated_at = datetime.datetime.utcnow()
                
                # Check status and trigger alerts
                alert_source = f"TLS_{service.id}"
                if cert.status == "Expired":
                    self.raise_alert(
                        host_id=host.id,
                        level="Critical",
                        source=alert_source,
                        description=f"TLS Certificate for {target_host} has EXPIRED ({cert.days_remaining} days remaining)."
                    )
                elif cert.status == "Expiring":
                    self.raise_alert(
                        host_id=host.id,
                        level="Warning",
                        source=alert_source,
                        description=f"TLS Certificate for {target_host} is EXPIRING SOON ({cert.days_remaining} days remaining)."
                    )
                else:
                    self.resolve_alerts(host.id, alert_source)
                
                self.log_message(
                    host_id=host.id,
                    ip=host.ip,
                    message=f"TLS details updated for {target_host}. TLS Version: {cert.tls_version}. Status: {cert.status}. Days remaining: {cert.days_remaining}",
                    level="Info",
                    service="TLS"
                )
            else:
                self.log_message(
                    host_id=host.id,
                    ip=host.ip,
                    message=f"Could not check TLS status on port {service.port}.",
                    level="Warn",
                    service="TLS"
                )
            
            self.db.commit()

if __name__ == "__main__":
    collector = TLSCollector()
    try:
        collector.run()
    finally:
        collector.close()
