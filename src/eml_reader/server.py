"""Web server implementation for the EML Reader application.

This module provides an asynchronous web server built with aiohttp that serves
the EML Reader web interface and API endpoints. It includes HTTPS support with
auto-generated SSL certificates and comprehensive error handling.

Routes:
- GET /: Welcome page with API documentation
- GET /upload: EML file upload interface
- GET /api/status: Server status and version information
- POST /api/process: Process EML content and return structured data
- GET /api/threads: List all analyzed email threads
- GET /api/threads/{thread_id}: Get detailed thread information
- GET /api/threads/search/{query}: Search threads by subject or participant

Features:
- Async request handling for high performance
- HTTPS support with auto-generated SSL certificates
- Configurable file upload size limits
- JSON API responses with proper error handling
- Cross-platform compatibility
- Thread analysis integration
"""

import asyncio
import ssl
from pathlib import Path
from aiohttp import web, ClientSession
from typing import Any

from .resource import ResourceManager
from .html import WELCOME_PAGE, UPLOAD_PAGE, ERROR_PAGE_TEMPLATE, NOT_FOUND_PAGE
from .eml_processor import EMLProcessor


class EMLServer:
    """Async web server for EML processing."""

    def __init__(self, host: str = "localhost", port: int = 8443) -> None:
        """Initialize the EML server.

        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.resource_mgr = ResourceManager()

        # Load configuration for file size limit
        try:
            config = self.resource_mgr.load_config()
            self.file_size_limit = config.get("server", {}).get(
                "file_upload_size_limit", 5 * 1024 * 1024
            )
        except Exception:
            # Fallback to default if config can't be loaded
            self.file_size_limit = 5 * 1024 * 1024

        # Configure application with file upload support from config
        self.app = web.Application(
            client_max_size=self.file_size_limit,
        )

        self.eml_processor = EMLProcessor()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up the application routes."""
        # Main HTML pages
        self.app.router.add_get("/", self._handle_root)
        self.app.router.add_get("/upload", self._handle_upload_page)

        # API routes
        self.app.router.add_get("/api/status", self._handle_api_status)
        self.app.router.add_post("/api/process", self._handle_api_process_eml)
        self.app.router.add_get("/api/threads", self._handle_api_threads)
        self.app.router.add_get(
            "/api/threads/{thread_id}", self._handle_api_thread_details
        )
        self.app.router.add_get(
            "/api/threads/search/{query}", self._handle_api_thread_search
        )

    async def _handle_root(self, request: web.Request) -> web.Response:
        """Handle the root endpoint with HTML page.

        Args:
            request: The incoming request

        Returns:
            HTML response with welcome page
        """
        return web.Response(text=WELCOME_PAGE, content_type="text/html")

    async def _handle_upload_page(self, request: web.Request) -> web.Response:
        """Handle the upload page endpoint.

        Args:
            request: The incoming request

        Returns:
            HTML response with upload page
        """
        return web.Response(text=UPLOAD_PAGE, content_type="text/html")

    async def _handle_api_status(self, request: web.Request) -> web.Response:
        """Handle the API status endpoint.

        Args:
            request: The incoming request

        Returns:
            JSON response with server status
        """
        return web.json_response(
            {"status": "running", "service": "EML Reader Server", "version": "0.1.0"}
        )

    async def _handle_api_process_eml(self, request: web.Request) -> web.Response:
        """Handle EML processing requests.

        Args:
            request: The incoming request with EML data

        Returns:
            JSON response with processing results
        """
        try:
            # Check if it's a file upload or JSON content
            if request.content_type and "multipart/form-data" in request.content_type:
                # Handle file upload
                data = await request.post()
                file = data.get("file")

                if not file:
                    return web.json_response({"error": "No file provided"}, status=400)

                # Read file content
                eml_content = file.file.read()
                filename = file.filename

                # Process the EML content
                try:
                    eml_data = self.eml_processor.parse_eml_content(eml_content)
                    summary = self.eml_processor.get_summary(eml_data)

                    result = {
                        "status": "processed",
                        "message": f"EML file '{filename}' processed successfully",
                        "filename": filename,
                        "summary": summary,
                        "data": eml_data,
                        "raw_eml": eml_content.decode("utf-8", errors="replace"),
                    }

                    return web.json_response(result)

                except ValueError as e:
                    return web.json_response(
                        {"error": f"Invalid EML file: {e}"}, status=400
                    )

            else:
                # Handle JSON content
                data = await request.json()
                eml_content = data.get("eml_content", "")

                if not eml_content:
                    return web.json_response(
                        {"error": "No EML content provided"}, status=400
                    )

                # Process the EML content
                try:
                    eml_data = self.eml_processor.parse_eml_content(eml_content)
                    summary = self.eml_processor.get_summary(eml_data)

                    result = {
                        "status": "processed",
                        "message": "EML content processed successfully",
                        "summary": summary,
                        "data": eml_data,
                        "raw_eml": eml_content,
                    }

                    return web.json_response(result)

                except ValueError as e:
                    return web.json_response(
                        {"error": f"Invalid EML content: {e}"}, status=400
                    )

        except Exception as e:
            return web.json_response(
                {"error": f"Processing failed: {str(e)}"}, status=500
            )

    async def _handle_api_threads(self, request: web.Request) -> web.Response:
        """Handle thread listing requests.

        Args:
            request: The incoming request

        Returns:
            JSON response with thread summaries
        """
        try:
            all_threads = self.eml_processor.get_all_threads()

            return web.json_response(
                {
                    "status": "success",
                    "thread_count": len(all_threads),
                    "threads": all_threads,
                }
            )

        except Exception as e:
            return web.json_response(
                {"error": f"Thread listing failed: {str(e)}"}, status=500
            )

    async def _handle_api_thread_details(self, request: web.Request) -> web.Response:
        """Handle thread details requests.

        Args:
            request: The incoming request with thread_id parameter

        Returns:
            JSON response with thread details
        """
        try:
            thread_id = request.match_info.get("thread_id")
            if not thread_id:
                return web.json_response({"error": "Thread ID required"}, status=400)

            thread_summary = self.eml_processor.get_thread_summary(thread_id)
            if not thread_summary:
                return web.json_response({"error": "Thread not found"}, status=404)

            thread_timeline = self.eml_processor.get_thread_timeline(thread_id)

            return web.json_response(
                {
                    "status": "success",
                    "thread_id": thread_id,
                    "summary": thread_summary,
                    "timeline": thread_timeline,
                }
            )

        except Exception as e:
            return web.json_response(
                {"error": f"Thread details failed: {str(e)}"}, status=500
            )

    async def _handle_api_thread_search(self, request: web.Request) -> web.Response:
        """Handle thread search requests.

        Args:
            request: The incoming request with query parameter

        Returns:
            JSON response with search results
        """
        try:
            query = request.match_info.get("query")
            if not query:
                return web.json_response({"error": "Search query required"}, status=400)

            search_results = self.eml_processor.search_threads(query)

            return web.json_response(
                {
                    "status": "success",
                    "query": query,
                    "result_count": len(search_results),
                    "results": search_results,
                }
            )

        except Exception as e:
            return web.json_response(
                {"error": f"Thread search failed: {str(e)}"}, status=500
            )

    def create_ssl_context(self, cert_path: Path, key_path: Path) -> ssl.SSLContext:
        """Create SSL context for HTTPS.

        Args:
            cert_path: Path to the SSL certificate file
            key_path: Path to the SSL private key file

        Returns:
            Configured SSL context

        Raises:
            FileNotFoundError: If certificate or key files don't exist
        """
        if not cert_path.exists():
            raise FileNotFoundError(f"Certificate file not found: {cert_path}")
        if not key_path.exists():
            raise FileNotFoundError(f"Private key file not found: {key_path}")

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(cert_path, key_path)
        return ssl_context

    async def start(
        self, cert_path: Path | None = None, key_path: Path | None = None
    ) -> None:
        """Start the web server.

        Args:
            cert_path: Path to SSL certificate file (optional for HTTP)
            key_path: Path to SSL private key file (optional for HTTP)
        """
        # If no certificates provided, try to use generated ones
        if not cert_path and not key_path:
            try:
                # Check if generated certificates exist
                if (
                    self.resource_mgr.ssl_cert_file.exists()
                    and self.resource_mgr.ssl_key_file.exists()
                ):
                    cert_path = self.resource_mgr.ssl_cert_file
                    key_path = self.resource_mgr.ssl_key_file
                    print(f"🔒 Using generated SSL certificates")
                else:
                    print(f"⚠️  No SSL certificates found, running in HTTP mode")
                    print(
                        f"   Run 'eml-reader bootstrap init' to generate certificates"
                    )
            except Exception as e:
                print(f"⚠️  Could not load generated certificates: {e}")
                print(f"   Running in HTTP mode")

        if cert_path and key_path:
            ssl_context = self.create_ssl_context(cert_path, key_path)
            runner = web.AppRunner(self.app)
            await runner.setup()
            site = web.TCPSite(runner, self.host, self.port, ssl_context=ssl_context)
            await site.start()
            print(f"🚀 HTTPS server running on https://{self.host}:{self.port}")
        else:
            runner = web.AppRunner(self.app)
            await runner.setup()
            site = web.TCPSite(runner, self.host, self.port)
            await site.start()
            print(f"🚀 HTTP server running on http://{self.host}:{self.port}")

        print("📧 EML Reader Server is ready to process requests!")
        print("   - GET  / : Welcome page")
        print("   - GET  /upload : Upload EML file")
        print("   - GET  /api/status : Server status")
        print("   - POST /api/process : Process EML content")
        print("   - GET  /api/threads : List all threads")
        print("   - GET  /api/threads/{id} : Get thread details")
        print("   - GET  /api/threads/search/{query} : Search threads")
        print(f"   - Max file size: {self.file_size_limit // (1024 * 1024)}MB")

        # Keep the server running
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            await runner.cleanup()


async def run_server(
    host: str, port: int, cert_path: Path | None = None, key_path: Path | None = None
) -> None:
    """Run the EML server.

    Args:
        host: Server host address
        port: Server port number
        cert_path: Path to SSL certificate file
        key_path: Path to SSL private key file
    """
    server = EMLServer(host, port)
    await server.start(cert_path, key_path)
