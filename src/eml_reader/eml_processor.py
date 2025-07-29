"""EML file processing using Python's standard library email module.

This module provides comprehensive EML file parsing and analysis capabilities using
Python's built-in email module. It extracts structured data from EML files including
headers, body content, attachments, and metadata.

Features:
- Complete email header analysis with common and custom headers
- Body content extraction for both text and HTML formats
- Attachment analysis with file details and metadata
- Message metadata extraction including threading information
- Summary generation for quick overview of email content
- Support for multipart messages and various email formats
- Robust error handling and encoding support
- Cross-platform compatibility

The EMLProcessor class provides a clean interface for parsing EML content from
files, strings, or file-like objects, returning structured data that can be
easily consumed by web interfaces, APIs, or other applications.
"""

import email
import email.policy
from email.message import Message
from pathlib import Path
from typing import Any, BinaryIO
from datetime import datetime


class EMLProcessor:
    """Process EML files using Python's standard library email module."""

    def __init__(self) -> None:
        """Initialize the EML processor."""
        # Use the default policy which handles most email formats correctly
        self.policy = email.policy.default

    def parse_eml_content(self, content: str | bytes) -> dict[str, Any]:
        """Parse EML content and extract structured data.

        Args:
            content: EML content as string or bytes

        Returns:
            Dictionary containing parsed email data

        Raises:
            ValueError: If content cannot be parsed as valid email
        """
        try:
            # Parse the email content
            if isinstance(content, str):
                message = email.message_from_string(content, policy=self.policy)
            else:
                message = email.message_from_bytes(content, policy=self.policy)

            return self._extract_email_data(message)

        except Exception as e:
            raise ValueError(f"Failed to parse EML content: {e}")

    def parse_eml_file(self, file_path: Path | str) -> dict[str, Any]:
        """Parse EML file and extract structured data.

        Args:
            file_path: Path to the EML file

        Returns:
            Dictionary containing parsed email data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file cannot be parsed as valid email
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"EML file not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            return self.parse_eml_content(content)

        except Exception as e:
            raise ValueError(f"Failed to parse EML file {file_path}: {e}")

    def parse_eml_file_object(self, file_obj: BinaryIO) -> dict[str, Any]:
        """Parse EML from a file-like object.

        Args:
            file_obj: File-like object containing EML data

        Returns:
            Dictionary containing parsed email data

        Raises:
            ValueError: If content cannot be parsed as valid email
        """
        try:
            content = file_obj.read()
            return self.parse_eml_content(content)

        except Exception as e:
            raise ValueError(f"Failed to parse EML from file object: {e}")

    def _extract_email_data(self, message: Message) -> dict[str, Any]:
        """Extract structured data from an email message.

        Args:
            message: Parsed email message object

        Returns:
            Dictionary containing extracted email data
        """
        # Extract basic headers
        headers = self._extract_headers(message)

        # Extract body content
        body_data = self._extract_body(message)

        # Extract attachments
        attachments = self._extract_attachments(message)

        # Extract metadata
        metadata = self._extract_metadata(message)

        return {
            "headers": headers,
            "body": body_data,
            "attachments": attachments,
            "metadata": metadata,
            "raw_size": len(str(message)),
        }

    def _extract_headers(self, message: Message) -> dict[str, Any]:
        """Extract email headers.

        Args:
            message: Parsed email message object

        Returns:
            Dictionary containing header information
        """
        headers = {}

        # Common headers to extract
        common_headers = [
            "from",
            "to",
            "cc",
            "bcc",
            "subject",
            "date",
            "message-id",
            "reply-to",
            "return-path",
            "sender",
            "in-reply-to",
            "references",
            "content-type",
            "content-transfer-encoding",
            "mime-version",
        ]

        for header in common_headers:
            value = message.get(header)
            if value:
                headers[header] = value

        # Get all headers (including custom ones)
        all_headers = dict(message.items())

        return {"common": headers, "all": all_headers, "count": len(all_headers)}

    def _extract_body(self, message: Message) -> dict[str, Any]:
        """Extract email body content.

        Args:
            message: Parsed email message object

        Returns:
            Dictionary containing body information
        """
        body_data = {
            "text": None,
            "html": None,
            "content_type": message.get_content_type(),
            "encoding": message.get_content_charset(),
        }

        # Handle multipart messages
        if message.is_multipart():
            for part in message.walk():
                if part.is_multipart():
                    continue

                content_type = part.get_content_type()
                content_disposition = part.get("content-disposition", "")

                # Skip attachments (they're handled separately)
                if "attachment" in content_disposition.lower():
                    continue

                # Extract text content
                if content_type == "text/plain":
                    try:
                        body_data["text"] = part.get_content()
                    except Exception:
                        body_data["text"] = part.get_payload(decode=True).decode(
                            "utf-8", errors="ignore"
                        )

                # Extract HTML content
                elif content_type == "text/html":
                    try:
                        body_data["html"] = part.get_content()
                    except Exception:
                        body_data["html"] = part.get_payload(decode=True).decode(
                            "utf-8", errors="ignore"
                        )
        else:
            # Single part message
            content_type = message.get_content_type()

            if content_type == "text/plain":
                try:
                    body_data["text"] = message.get_content()
                except Exception:
                    body_data["text"] = message.get_payload(decode=True).decode(
                        "utf-8", errors="ignore"
                    )

            elif content_type == "text/html":
                try:
                    body_data["html"] = message.get_content()
                except Exception:
                    body_data["html"] = message.get_payload(decode=True).decode(
                        "utf-8", errors="ignore"
                    )

        return body_data

    def _extract_attachments(self, message: Message) -> list[dict[str, Any]]:
        """Extract email attachments.

        Args:
            message: Parsed email message object

        Returns:
            List of attachment dictionaries
        """
        attachments = []

        for part in message.walk():
            if part.is_multipart():
                continue

            content_disposition = part.get("content-disposition", "")

            if "attachment" in content_disposition.lower():
                attachment = {
                    "filename": part.get_filename(),
                    "content_type": part.get_content_type(),
                    "size": len(part.get_payload(decode=True) or b""),
                    "content_id": part.get("content-id"),
                    "content_disposition": content_disposition,
                }
                attachments.append(attachment)

        return attachments

    def _extract_metadata(self, message: Message) -> dict[str, Any]:
        """Extract email metadata.

        Args:
            message: Parsed email message object

        Returns:
            Dictionary containing metadata
        """
        metadata = {
            "is_multipart": message.is_multipart(),
            "content_type": message.get_content_type(),
            "content_charset": message.get_content_charset(),
            "content_encoding": message.get("content-transfer-encoding"),
            "mime_version": message.get("mime-version"),
        }

        # Try to parse date
        date_header = message.get("date")
        if date_header:
            try:
                # Parse email date format
                parsed_date = email.utils.parsedate_to_datetime(date_header)
                metadata["date_parsed"] = parsed_date.isoformat()
                metadata["date_timestamp"] = parsed_date.timestamp()
            except Exception:
                metadata["date_parsed"] = None
                metadata["date_timestamp"] = None

        # Extract message ID info
        message_id = message.get("message-id")
        if message_id:
            metadata["message_id"] = message_id.strip("<>")

        # Extract thread info
        in_reply_to = message.get("in-reply-to")
        references = message.get("references")

        if in_reply_to:
            metadata["in_reply_to"] = in_reply_to.strip("<>")

        if references:
            # Parse multiple references
            ref_list = [ref.strip("<>") for ref in references.split()]
            metadata["references"] = ref_list

        return metadata

    def get_summary(self, eml_data: dict[str, Any]) -> dict[str, Any]:
        """Get a summary of the EML data.

        Args:
            eml_data: Parsed EML data dictionary

        Returns:
            Summary dictionary
        """
        headers = eml_data.get("headers", {}).get("common", {})

        return {
            "subject": headers.get("subject", "No Subject"),
            "from": headers.get("from", "Unknown Sender"),
            "to": headers.get("to", "Unknown Recipient"),
            "cc": headers.get("cc", "N/A"),
            "bcc": headers.get("bcc", "N/A"),
            "date": headers.get("date", "Unknown Date"),
            "has_attachments": len(eml_data.get("attachments", [])) > 0,
            "attachment_count": len(eml_data.get("attachments", [])),
            "has_html": bool(eml_data.get("body", {}).get("html")),
            "has_text": bool(eml_data.get("body", {}).get("text")),
            "size_bytes": eml_data.get("raw_size", 0),
        }
