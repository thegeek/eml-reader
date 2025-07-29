"""Resource management for the EML Reader application.

This module provides comprehensive resource management for the EML Reader application,
including cross-platform application data directory management, configuration file
handling, and SSL certificate generation.

Features:
- Cross-platform application data directory management
- Configuration file creation and management using TOML format
- SSL certificate and private key generation for HTTPS support
- Certificate validation and expiration checking
- Resource structure verification and bootstrap commands
- Secure file permissions and access control
- Platform-specific directory handling (Windows, macOS, Linux)

The ResourceManager class provides a unified interface for managing all application
resources, ensuring consistent behavior across different operating systems and
providing secure, configurable SSL certificate generation for web server security.
"""

import ipaddress
import os
import platform
import stat
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import toml
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


class ResourceManager:
    """Manages application resources and configuration."""

    def __init__(self) -> None:
        """Initialize the resource manager."""
        self.app_name = "eml-reader"
        self.resource_dir = self._get_app_data_dir()
        self.config_file = self.resource_dir / "config.toml"
        self.ssl_dir = self.resource_dir / "ssl"
        self.ssl_cert_file = self.ssl_dir / "server.crt"
        self.ssl_key_file = self.ssl_dir / "server.key"

    def _get_app_data_dir(self) -> Path:
        """Get the application data directory for the current OS.

        Returns:
            Path to the application data directory
        """
        system = platform.system().lower()

        if system == "windows":
            app_data = os.environ.get("APPDATA")
            if not app_data:
                raise RuntimeError("APPDATA environment variable not found")
            return Path(app_data) / self.app_name

        elif system == "darwin":  # macOS
            home = Path.home()
            return home / "Library" / "Application Support" / self.app_name

        elif system == "linux":
            home = Path.home()
            return home / ".local" / "share" / self.app_name

        else:
            raise RuntimeError(f"Unsupported operating system: {system}")

    def create_resource_structure(self) -> None:
        """Create the resource directory structure."""
        try:
            # Create main resource directory
            self.resource_dir.mkdir(parents=True, exist_ok=True)

            # Create SSL directory
            self.ssl_dir.mkdir(parents=True, exist_ok=True)

            print(f"✅ Created resource directory: {self.resource_dir}")
            print(f"✅ Created SSL directory: {self.ssl_dir}")

        except Exception as e:
            raise RuntimeError(f"Failed to create resource structure: {e}")

    def get_default_config(self) -> dict[str, Any]:
        """Get the default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "server": {
                "host": "localhost",
                "port": 8443,
                "ssl_enabled": True,
                "file_upload_size_limit": 5 * 1024 * 1024,  # 5MB default
            },
            "ssl": {
                "cert_file": str(self.ssl_cert_file.relative_to(self.resource_dir)),
                "key_file": str(self.ssl_key_file.relative_to(self.resource_dir)),
                "days_valid": 365,
                "country": "US",
                "state": "CA",
                "locality": "San Francisco",
                "organization": "EML Reader",
                "common_name": "localhost",
            },
            "logging": {"level": "INFO", "file": "eml-reader.log"},
        }

    def load_config(self) -> dict[str, Any]:
        """Load configuration from file.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            toml.TomlDecodeError: If config file is invalid
        """
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        with open(self.config_file, "r", encoding="utf-8") as f:
            return toml.load(f)

    def save_config(self, config: dict[str, Any]) -> None:
        """Save configuration to file.

        Args:
            config: Configuration dictionary to save
        """
        # Ensure resource directory exists
        self.resource_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, "w", encoding="utf-8") as f:
            toml.dump(config, f)

        print(f"✅ Configuration saved to: {self.config_file}")

    def generate_ssl_certificate(
        self,
        days_valid: int = 365,
        country: str = "US",
        state: str = "CA",
        locality: str = "San Francisco",
        organization: str = "EML Reader",
        common_name: str = "localhost",
    ) -> None:
        """Generate a self-signed SSL certificate and private key.

        Args:
            days_valid: Number of days the certificate is valid
            country: Country code for certificate
            state: State/province for certificate
            locality: City/locality for certificate
            organization: Organization name for certificate
            common_name: Common name for certificate
        """
        try:
            # Ensure SSL directory exists
            self.ssl_dir.mkdir(parents=True, exist_ok=True)

            # Generate private key
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

            # Create certificate
            subject = issuer = x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                ]
            )

            cert = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(private_key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.utcnow())
                .not_valid_after(datetime.utcnow() + timedelta(days=days_valid))
                .add_extension(
                    x509.SubjectAlternativeName(
                        [
                            x509.DNSName(common_name),
                            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                            x509.IPAddress(ipaddress.IPv6Address("::1")),
                        ]
                    ),
                    critical=False,
                )
                .sign(private_key, hashes.SHA256())
            )

            # Save private key
            with open(self.ssl_key_file, "wb") as f:
                f.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )

            # Set restrictive permissions on private key (Unix-like systems)
            if platform.system().lower() != "windows":
                os.chmod(self.ssl_key_file, stat.S_IRUSR | stat.S_IWUSR)

            # Save certificate
            with open(self.ssl_cert_file, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

            print(f"✅ SSL certificate generated:")
            print(f"   Certificate: {self.ssl_cert_file}")
            print(f"   Private key: {self.ssl_key_file}")
            print(f"   Valid for: {days_valid} days")
            print(f"   Common name: {common_name}")

        except Exception as e:
            raise RuntimeError(f"Failed to generate SSL certificate: {e}")

    def check_ssl_certificate(self) -> dict[str, Any]:
        """Check SSL certificate validity and expiration.

        Returns:
            Dictionary with certificate status information
        """
        result = {
            "cert_exists": False,
            "key_exists": False,
            "cert_valid": False,
            "expires_in_days": None,
            "errors": [],
        }

        try:
            # Check if files exist
            result["cert_exists"] = self.ssl_cert_file.exists()
            result["key_exists"] = self.ssl_key_file.exists()

            if not result["cert_exists"]:
                result["errors"].append("Certificate file not found")
                return result

            if not result["key_exists"]:
                result["errors"].append("Private key file not found")
                return result

            # Load and validate certificate
            with open(self.ssl_cert_file, "rb") as f:
                cert_data = f.read()

            cert = x509.load_pem_x509_certificate(cert_data)

            # Check expiration
            now = datetime.utcnow()
            expires = cert.not_valid_after.replace(tzinfo=None)

            if now > expires:
                result["errors"].append("Certificate has expired")
                return result

            days_until_expiry = (expires - now).days
            result["expires_in_days"] = days_until_expiry
            result["cert_valid"] = True

            if days_until_expiry < 30:
                result["errors"].append(
                    f"Certificate expires in {days_until_expiry} days"
                )

        except Exception as e:
            result["errors"].append(f"Certificate validation failed: {e}")

        return result

    def check_resource_structure(self) -> dict[str, Any]:
        """Check if the resource structure is properly set up.

        Returns:
            Dictionary with structure status information
        """
        result = {
            "resource_dir_exists": False,
            "ssl_dir_exists": False,
            "config_exists": False,
            "config_valid": False,
            "ssl_status": {},
            "errors": [],
            "warnings": [],
        }

        try:
            # Check directories
            result["resource_dir_exists"] = self.resource_dir.exists()
            result["ssl_dir_exists"] = self.ssl_dir.exists()
            result["config_exists"] = self.config_file.exists()

            if not result["resource_dir_exists"]:
                result["errors"].append("Resource directory does not exist")

            if not result["ssl_dir_exists"]:
                result["errors"].append("SSL directory does not exist")

            if not result["config_exists"]:
                result["errors"].append("Configuration file does not exist")
            else:
                # Try to load config
                try:
                    config = self.load_config()
                    result["config_valid"] = True
                except Exception as e:
                    result["errors"].append(f"Configuration file is invalid: {e}")

            # Check SSL certificate
            result["ssl_status"] = self.check_ssl_certificate()
            result["errors"].extend(result["ssl_status"]["errors"])

        except Exception as e:
            result["errors"].append(f"Structure check failed: {e}")

        return result
