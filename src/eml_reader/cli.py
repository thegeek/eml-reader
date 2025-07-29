"""Command-line interface for the EML Reader application.

This module provides a comprehensive CLI for processing EML files, managing the web
server, and analyzing email threads. It uses Click for command-line argument
parsing and provides both individual file processing and batch operations.

Commands:
- server: Start the web server with optional SSL support
- bootstrap: Initialize application resources and SSL certificates
- process: Parse and analyze individual EML files
- config-file-size: Configure maximum file upload size
- threads: Email threading analysis commands
  - analyze: Analyze email threads in directories
  - search: Search threads by subject or participant
  - show: Show detailed thread information

The CLI supports various output formats including JSON, pretty-printed JSON,
and summary mode for quick overviews of email content.
"""

import asyncio
import click
import json
from pathlib import Path
from typing import Any
from datetime import datetime

from .server import run_server
from .resource import ResourceManager
from .eml_processor import EMLProcessor


@click.group()
@click.version_option()
def cli() -> None:
    """EML Reader - A tool for reading and processing EML files."""
    pass


@cli.group()
def bootstrap() -> None:
    """Bootstrap commands for initial setup and verification."""
    pass


@bootstrap.command()
@click.option(
    "--days",
    "-d",
    default=365,
    type=int,
    help="Number of days the SSL certificate is valid",
)
@click.option("--country", default="US", help="Country code for certificate")
@click.option("--state", default="CA", help="State/province for certificate")
@click.option(
    "--locality", default="San Francisco", help="City/locality for certificate"
)
@click.option(
    "--organization", default="EML Reader", help="Organization name for certificate"
)
@click.option("--common-name", default="localhost", help="Common name for certificate")
def init(
    days: int,
    country: str,
    state: str,
    locality: str,
    organization: str,
    common_name: str,
) -> None:
    """Initialize the EML reader resource structure and SSL certificate.

    This command creates the necessary directories, configuration file,
    and generates a self-signed SSL certificate for the server.
    """
    try:
        click.echo("🚀 Initializing EML Reader resources...")

        # Create resource manager
        resource_mgr = ResourceManager()

        # Create directory structure
        click.echo("📁 Creating directory structure...")
        resource_mgr.create_resource_structure()

        # Generate default configuration
        click.echo("⚙️  Creating default configuration...")
        config = resource_mgr.get_default_config()
        resource_mgr.save_config(config)

        # Generate SSL certificate
        click.echo("🔐 Generating SSL certificate...")
        resource_mgr.generate_ssl_certificate(
            days_valid=days,
            country=country,
            state=state,
            locality=locality,
            organization=organization,
            common_name=common_name,
        )

        click.echo("\n✅ Bootstrap completed successfully!")
        click.echo(f"📂 Resource directory: {resource_mgr.resource_dir}")
        click.echo(f"🔧 Configuration file: {resource_mgr.config_file}")
        click.echo(f"🔒 SSL certificate: {resource_mgr.ssl_cert_file}")
        click.echo(f"🔑 SSL private key: {resource_mgr.ssl_key_file}")
        click.echo("\n🎉 You can now start the server with:")
        click.echo("   eml-reader server")

    except Exception as e:
        click.echo(f"❌ Bootstrap failed: {e}", err=True)
        raise click.Abort()


@bootstrap.command()
def check() -> None:
    """Check the EML reader resource structure and SSL certificate.

    This command verifies that all necessary files and directories
    exist and are properly configured.
    """
    try:
        click.echo("🔍 Checking EML Reader resources...")

        # Create resource manager
        resource_mgr = ResourceManager()

        # Check structure
        status = resource_mgr.check_resource_structure()

        # Display results
        click.echo(
            f"\n📂 Resource Directory: {'✅' if status['resource_dir_exists'] else '❌'}"
        )
        if status["resource_dir_exists"]:
            click.echo(f"   Path: {resource_mgr.resource_dir}")

        click.echo(f"📁 SSL Directory: {'✅' if status['ssl_dir_exists'] else '❌'}")
        if status["ssl_dir_exists"]:
            click.echo(f"   Path: {resource_mgr.ssl_dir}")

        click.echo(
            f"⚙️  Configuration File: {'✅' if status['config_exists'] else '❌'}"
        )
        if status["config_exists"]:
            click.echo(f"   Path: {resource_mgr.config_file}")
            click.echo(f"   Valid: {'✅' if status['config_valid'] else '❌'}")

        # SSL certificate status
        ssl_status = status["ssl_status"]
        click.echo(f"🔒 SSL Certificate: {'✅' if ssl_status['cert_exists'] else '❌'}")
        if ssl_status["cert_exists"]:
            click.echo(f"   Path: {resource_mgr.ssl_cert_file}")

        click.echo(f"🔑 SSL Private Key: {'✅' if ssl_status['key_exists'] else '❌'}")
        if ssl_status["key_exists"]:
            click.echo(f"   Path: {resource_mgr.ssl_key_file}")

        if ssl_status["cert_valid"]:
            click.echo(f"✅ Certificate Valid: Yes")
            if ssl_status["expires_in_days"] is not None:
                click.echo(f"📅 Expires in: {ssl_status['expires_in_days']} days")

        # Display errors and warnings
        if status["errors"]:
            click.echo(f"\n❌ Errors:")
            for error in status["errors"]:
                click.echo(f"   - {error}")

        if status["warnings"]:
            click.echo(f"\n⚠️  Warnings:")
            for warning in status["warnings"]:
                click.echo(f"   - {warning}")

        # Overall status
        if not status["errors"]:
            click.echo(f"\n✅ All checks passed! EML Reader is ready to use.")
        else:
            click.echo(
                f"\n❌ Some issues found. Run 'eml-reader bootstrap init' to fix them."
            )
            raise click.Abort()

    except Exception as e:
        click.echo(f"❌ Check failed: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("size_mb", type=int)
def config_file_size(size_mb: int) -> None:
    """Configure the maximum file upload size limit.

    This command updates the configuration file to set the maximum
    file size that can be uploaded to the server.

    Args:
        size_mb: Maximum file size in megabytes
    """
    try:
        click.echo(f"⚙️  Configuring file upload size limit to {size_mb}MB...")

        # Create resource manager
        resource_mgr = ResourceManager()

        # Load current config or create default
        try:
            config = resource_mgr.load_config()
        except FileNotFoundError:
            config = resource_mgr.get_default_config()

        # Update the file size limit
        if "server" not in config:
            config["server"] = {}

        config["server"]["file_upload_size_limit"] = size_mb * 1024 * 1024

        # Save the updated configuration
        resource_mgr.save_config(config)

        click.echo(f"✅ File upload size limit set to {size_mb}MB")
        click.echo(f"📁 Configuration saved to: {resource_mgr.config_file}")
        click.echo(f"🔄 Restart the server for changes to take effect")

    except Exception as e:
        click.echo(f"❌ Configuration failed: {e}", err=True)
        raise click.Abort()


@cli.group()
def threads() -> None:
    """Thread analysis commands for email conversation tracking."""
    pass


@threads.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def analyze(directory: Path, output: Path | None, pretty: bool) -> None:
    """Analyze email threads in a directory of EML files.

    This command processes all EML files in the specified directory
    and analyzes their threading relationships.

    Args:
        directory: Directory containing EML files
        output: Output JSON file path (optional)
        pretty: Pretty print JSON output
    """
    try:
        click.echo(f"🧵 Analyzing email threads in: {directory}")

        # Find all EML files
        eml_files = list(directory.glob("*.eml"))
        if not eml_files:
            click.echo("❌ No EML files found in directory", err=True)
            raise click.Abort()

        click.echo(f"📧 Found {len(eml_files)} EML files")

        # Process all files
        processor = EMLProcessor()
        processed_count = 0

        for eml_file in eml_files:
            try:
                click.echo(f"  Processing: {eml_file.name}")
                processor.parse_eml_file(eml_file)
                processed_count += 1
            except Exception as e:
                click.echo(f"  ⚠️  Skipping {eml_file.name}: {e}")

        # Get thread analysis
        all_threads = processor.get_all_threads()

        click.echo(f"\n📊 Thread Analysis Results:")
        click.echo(f"  Total threads: {len(all_threads)}")
        click.echo(f"  Total messages: {sum(t['message_count'] for t in all_threads)}")
        click.echo(
            f"  Average thread size: {sum(t['message_count'] for t in all_threads) / len(all_threads):.1f} messages"
        )

        # Show top threads by message count
        top_threads = sorted(
            all_threads, key=lambda x: x["message_count"], reverse=True
        )[:5]
        click.echo(f"\n🏆 Top 5 Threads by Message Count:")
        for i, thread in enumerate(top_threads, 1):
            click.echo(
                f"  {i}. {thread['subject'][:50]}... ({thread['message_count']} messages)"
            )

        if output:
            result = {
                "analysis_date": datetime.now().isoformat(),
                "directory": str(directory),
                "files_processed": processed_count,
                "total_threads": len(all_threads),
                "threads": all_threads,
            }

            with open(output, "w", encoding="utf-8") as f:
                if pretty:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(result, f, ensure_ascii=False)

            click.echo(f"\n✅ Thread analysis saved to: {output}")

        click.echo(f"\n✅ Thread analysis completed successfully!")

    except Exception as e:
        click.echo(f"❌ Thread analysis failed: {e}", err=True)
        raise click.Abort()


@threads.command()
@click.argument("query", type=str)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def search(query: str, output: Path | None, pretty: bool) -> None:
    """Search threads by subject or participant.

    This command searches through analyzed threads for matches
    in subject lines or participant email addresses.

    Args:
        query: Search query string
        output: Output JSON file path (optional)
        pretty: Pretty print JSON output
    """
    try:
        click.echo(f"🔍 Searching threads for: '{query}'")

        # Note: This would need a persistent thread database in a real implementation
        # For now, we'll show how the search would work
        click.echo("⚠️  Note: Thread search requires previously analyzed threads.")
        click.echo(
            "   Use 'eml-reader threads analyze <directory>' first to analyze threads."
        )

        # Example search results structure
        search_results = {
            "query": query,
            "search_date": datetime.now().isoformat(),
            "results": [],
            "total_matches": 0,
        }

        if output:
            with open(output, "w", encoding="utf-8") as f:
                if pretty:
                    json.dump(search_results, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(search_results, f, ensure_ascii=False)

            click.echo(f"✅ Search results saved to: {output}")

        click.echo(f"\n✅ Thread search completed!")

    except Exception as e:
        click.echo(f"❌ Thread search failed: {e}", err=True)
        raise click.Abort()


@threads.command()
@click.argument("thread_id", type=str)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def show(thread_id: str, output: Path | None, pretty: bool) -> None:
    """Show detailed information about a specific thread.

    This command displays detailed information about a thread
    including timeline and participant analysis.

    Args:
        thread_id: Thread identifier
        output: Output JSON file path (optional)
        pretty: Pretty print JSON output
    """
    try:
        click.echo(f"🧵 Showing thread details for: {thread_id}")

        # Note: This would need a persistent thread database in a real implementation
        # For now, we'll show how the command would work
        click.echo("⚠️  Note: Thread details require previously analyzed threads.")
        click.echo(
            "   Use 'eml-reader threads analyze <directory>' first to analyze threads."
        )

        # Example thread details structure
        thread_details = {
            "thread_id": thread_id,
            "summary": None,
            "timeline": [],
            "participants": [],
            "engagement_metrics": {},
        }

        if output:
            with open(output, "w", encoding="utf-8") as f:
                if pretty:
                    json.dump(thread_details, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(thread_details, f, ensure_ascii=False)

            click.echo(f"✅ Thread details saved to: {output}")

        click.echo(f"\n✅ Thread details retrieved!")

    except Exception as e:
        click.echo(f"❌ Thread details failed: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("eml_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output JSON file path"
)
@click.option("--summary", "-s", is_flag=True, help="Show only summary information")
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
def process(eml_file: Path, output: Path | None, summary: bool, pretty: bool) -> None:
    """Process an EML file and display the results.

    This command parses an EML file and extracts all available information
    including headers, body content, attachments, and metadata.
    """
    try:
        click.echo(f"📧 Processing EML file: {eml_file}")

        # Create EML processor
        processor = EMLProcessor()

        # Process the file
        eml_data = processor.parse_eml_file(eml_file)
        summary_data = processor.get_summary(eml_data)

        # Display summary
        click.echo(f"\n📋 Summary:")
        click.echo(f"   Subject: {summary_data['subject']}")
        click.echo(f"   From: {summary_data['from']}")
        click.echo(f"   To: {summary_data['to']}")
        click.echo(f"   Date: {summary_data['date']}")
        click.echo(f"   Attachments: {summary_data['attachment_count']}")
        click.echo(f"   Size: {summary_data['size_bytes']} bytes")
        click.echo(f"   Has HTML: {summary_data['has_html']}")
        click.echo(f"   Has Text: {summary_data['has_text']}")

        if summary:
            # Show only summary data
            result_data = summary_data
        else:
            # Show full data
            result_data = eml_data

        # Output to file or display
        if output:
            with open(output, "w", encoding="utf-8") as f:
                if pretty:
                    json.dump(result_data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(result_data, f, ensure_ascii=False)
            click.echo(f"\n✅ Results saved to: {output}")
        else:
            # Display to console
            click.echo(f"\n📄 Full Data:")
            if pretty:
                click.echo(json.dumps(result_data, indent=2, ensure_ascii=False))
            else:
                click.echo(json.dumps(result_data, ensure_ascii=False))

        click.echo(f"\n✅ EML file processed successfully!")

    except FileNotFoundError as e:
        click.echo(f"❌ File not found: {e}", err=True)
        raise click.Abort()
    except ValueError as e:
        click.echo(f"❌ Invalid EML file: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Processing failed: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--host", "-h", default="localhost", help="Server host address")
@click.option("--port", "-p", default=8443, type=int, help="Server port number")
@click.option(
    "--cert",
    type=click.Path(exists=True, path_type=Path),
    help="Path to SSL certificate file for HTTPS",
)
@click.option(
    "--key",
    type=click.Path(exists=True, path_type=Path),
    help="Path to SSL private key file for HTTPS",
)
def server(host: str, port: int, cert: Path | None, key: Path | None) -> None:
    """Start the EML reader web server.

    The server supports both HTTP and HTTPS modes. For HTTPS, provide both
    --cert and --key options. For HTTP, omit both options.
    """
    if (cert and not key) or (key and not cert):
        raise click.UsageError("Both --cert and --key must be provided for HTTPS mode")

    if cert and key:
        click.echo(f"🔒 Starting HTTPS server on {host}:{port}")
        click.echo(f"   Certificate: {cert}")
        click.echo(f"   Private key: {key}")
    else:
        click.echo(f"🌐 Starting HTTP server on {host}:{port}")

    try:
        asyncio.run(run_server(host, port, cert, key))
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped by user")
    except Exception as e:
        click.echo(f"❌ Server error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
