"""Email threading analysis and conversation tracking module.

This module provides sophisticated email threading analysis capabilities, including
automatic thread detection, timeline generation, participant tracking, and
engagement metrics calculation. It uses email headers like Message-ID, In-Reply-To,
and References to build conversation trees and analyze email relationships.

Classes:
- EmailThreadAnalyzer: Analyzes individual emails for threading information
- ThreadManager: Manages collections of threads and provides thread-level insights

Features:
- Automatic thread detection using email headers
- Thread timeline generation with chronological ordering
- Response time analysis between messages
- Participant tracking with message counts
- Engagement scoring based on content and activity
- Thread depth calculation (capped at 15 levels)
- Subject analysis for thread continuation detection
- Thread ID generation using content hashing
- Comprehensive thread metadata and statistics

The module integrates seamlessly with the EML processor to provide automatic
thread analysis for all processed emails.
"""

import hashlib
import re
from datetime import datetime
from typing import Any


class EmailThreadAnalyzer:
    """Analyzes email threads and conversation relationships."""

    def __init__(self) -> None:
        """Initialize the email thread analyzer."""
        self.thread_cache: dict[str, dict[str, Any]] = {}

    def analyze_thread(self, eml_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze threading information for a single email.

        Args:
            eml_data: Parsed EML data dictionary

        Returns:
            Dictionary containing threading analysis results
        """
        metadata = eml_data.get("metadata", {})
        headers = eml_data.get("headers", {}).get("common", {})

        thread_analysis = {
            "thread_id": self._generate_thread_id(eml_data),
            "message_id": metadata.get("message_id"),
            "in_reply_to": metadata.get("in_reply_to"),
            "references": metadata.get("references", []),
            "subject_thread": self._analyze_subject_thread(headers.get("subject", "")),
            "thread_depth": self._calculate_thread_depth(metadata),
            "is_reply": bool(metadata.get("in_reply_to")),
            "is_forward": self._detect_forward(headers.get("subject", "")),
            "is_root": self._is_root_message(metadata),
            "thread_participants": self._extract_thread_participants(headers),
            "thread_position": self._calculate_thread_position(metadata),
            "response_time": None,  # Will be calculated when thread context is available
            "engagement_indicators": self._calculate_engagement_indicators(eml_data),
        }

        return thread_analysis

    def _generate_thread_id(self, eml_data: dict[str, Any]) -> str:
        """Generate a unique thread identifier.

        Args:
            eml_data: Parsed EML data dictionary

        Returns:
            Unique thread identifier string
        """
        metadata = eml_data.get("metadata", {})
        headers = eml_data.get("headers", {}).get("common", {})

        # Priority order for thread ID generation
        if metadata.get("in_reply_to"):
            # Use In-Reply-To header for reply chains
            return f"thread_{self._hash_string(metadata['in_reply_to'])}"

        elif metadata.get("references"):
            # Use first reference for thread continuity
            return f"thread_{self._hash_string(metadata['references'][0])}"

        elif metadata.get("message_id"):
            # Use Message-ID for new threads
            return f"thread_{self._hash_string(metadata['message_id'])}"

        else:
            # Fallback to subject-based threading
            subject = headers.get("subject", "")
            normalized_subject = self._normalize_subject(subject)
            return f"thread_{self._hash_string(normalized_subject)}"

    def _hash_string(self, text: str) -> str:
        """Create a hash of a string for consistent thread IDs.

        Args:
            text: String to hash

        Returns:
            Hash string
        """
        return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]

    def _analyze_subject_thread(self, subject: str) -> dict[str, Any]:
        """Analyze subject line for threading patterns.

        Args:
            subject: Email subject line

        Returns:
            Dictionary containing subject analysis
        """
        normalized = self._normalize_subject(subject)

        return {
            "original": subject,
            "normalized": normalized,
            "has_re_prefix": subject.lower().startswith("re:"),
            "has_fw_prefix": subject.lower().startswith(("fw:", "fwd:")),
            "has_aw_prefix": subject.lower().startswith("aw:"),
            "prefix_count": self._count_subject_prefixes(subject),
            "is_thread_continuation": self._is_thread_continuation(subject),
        }

    def _normalize_subject(self, subject: str) -> str:
        """Remove common prefixes and normalize subject for threading.

        Args:
            subject: Email subject line

        Returns:
            Normalized subject string
        """
        if not subject:
            return ""

        # Remove common prefixes
        prefixes = ["re:", "fw:", "fwd:", "aw:", "fwd:", "fwd:"]
        normalized = subject.lower().strip()

        for prefix in prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix) :].strip()

        return normalized

    def _count_subject_prefixes(self, subject: str) -> int:
        """Count the number of subject prefixes (Re:, Fw:, etc.).

        Args:
            subject: Email subject line

        Returns:
            Number of prefixes
        """
        if not subject:
            return 0

        prefixes = ["re:", "fw:", "fwd:", "aw:"]
        count = 0
        normalized = subject.lower().strip()

        for prefix in prefixes:
            if normalized.startswith(prefix):
                count += 1
                normalized = normalized[len(prefix) :].strip()

        return count

    def _is_thread_continuation(self, subject: str) -> bool:
        """Check if subject indicates thread continuation.

        Args:
            subject: Email subject line

        Returns:
            True if subject indicates thread continuation
        """
        if not subject:
            return False

        normalized = subject.lower().strip()
        return normalized.startswith(("re:", "aw:"))

    def _calculate_thread_depth(self, metadata: dict[str, Any]) -> int:
        """Calculate how deep this message is in the thread.

        Args:
            metadata: Email metadata

        Returns:
            Thread depth (0 for root messages)
        """
        references = metadata.get("references", [])
        depth = len(references)

        # Cap depth at a reasonable maximum to avoid unrealistic values
        # Most email threads don't go deeper than 10-15 levels
        return min(depth, 15)

    def _detect_forward(self, subject: str) -> bool:
        """Detect if this is a forwarded message.

        Args:
            subject: Email subject line

        Returns:
            True if message appears to be forwarded
        """
        if not subject:
            return False

        normalized = subject.lower().strip()
        return normalized.startswith(("fw:", "fwd:"))

    def _is_root_message(self, metadata: dict[str, Any]) -> bool:
        """Check if this is a root message in a thread.

        Args:
            metadata: Email metadata

        Returns:
            True if this is a root message
        """
        return not metadata.get("in_reply_to") and not metadata.get("references")

    def _extract_thread_participants(self, headers: dict[str, Any]) -> list[str]:
        """Extract all participants in the thread.

        Args:
            headers: Email headers

        Returns:
            List of participant email addresses
        """
        participants = set()

        # Extract email addresses from various header fields
        for field in ["from", "to", "cc", "bcc"]:
            if headers.get(field):
                addresses = self._extract_email_addresses(headers[field])
                participants.update(addresses)

        return list(participants)

    def _extract_email_addresses(self, header_value: str) -> list[str]:
        """Extract email addresses from header value.

        Args:
            header_value: Header field value

        Returns:
            List of email addresses
        """
        if not header_value:
            return []

        # Email regex pattern
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_pattern, header_value)

        return list(set(emails))  # Remove duplicates

    def _calculate_thread_position(self, metadata: dict[str, Any]) -> int:
        """Calculate position in thread based on references.

        Args:
            metadata: Email metadata

        Returns:
            Position in thread (1-based)
        """
        # For a single email, position is always 1
        # In a real thread context, this would be calculated differently
        return 1

    def _calculate_engagement_indicators(
        self, eml_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Calculate engagement indicators for the email.

        Args:
            eml_data: Parsed EML data

        Returns:
            Dictionary containing engagement indicators
        """
        body = eml_data.get("body", {})
        headers = eml_data.get("headers", {}).get("common", {})

        # Calculate content length
        text_content = body.get("text", "")
        html_content = body.get("html", "")
        total_content_length = len(text_content) + len(html_content)

        # Count recipients
        recipient_count = 0
        for field in ["to", "cc", "bcc"]:
            if headers.get(field):
                recipient_count += len(self._extract_email_addresses(headers[field]))

        # Check for attachments
        has_attachments = bool(eml_data.get("attachments"))

        return {
            "content_length": total_content_length,
            "recipient_count": recipient_count,
            "has_attachments": has_attachments,
            "has_html": bool(html_content),
            "has_text": bool(text_content),
            "engagement_score": self._calculate_simple_engagement_score(
                total_content_length, recipient_count, has_attachments
            ),
        }

    def _calculate_simple_engagement_score(
        self, content_length: int, recipient_count: int, has_attachments: bool
    ) -> float:
        """Calculate a simple engagement score.

        Args:
            content_length: Length of email content
            recipient_count: Number of recipients
            has_attachments: Whether email has attachments

        Returns:
            Engagement score (0-100)
        """
        score = 0

        # Content length factor (0-40 points)
        if content_length > 1000:
            score += 40
        elif content_length > 500:
            score += 30
        elif content_length > 100:
            score += 20
        else:
            score += 10

        # Recipient count factor (0-30 points)
        if recipient_count > 10:
            score += 30
        elif recipient_count > 5:
            score += 20
        elif recipient_count > 1:
            score += 15
        else:
            score += 10

        # Attachment factor (0-30 points)
        if has_attachments:
            score += 30

        return min(score, 100)


class ThreadManager:
    """Manages email thread collections and relationships."""

    def __init__(self) -> None:
        """Initialize the thread manager."""
        self.threads: dict[str, list[dict[str, Any]]] = {}
        self.thread_metadata: dict[str, dict[str, Any]] = {}
        self.analyzer = EmailThreadAnalyzer()

    def add_email_to_thread(self, eml_data: dict[str, Any]) -> str:
        """Add an email to its appropriate thread.

        Args:
            eml_data: Parsed EML data

        Returns:
            Thread ID of the email
        """
        # Analyze the email for threading information
        thread_analysis = self.analyzer.analyze_thread(eml_data)
        thread_id = thread_analysis["thread_id"]

        # Initialize thread if it doesn't exist
        if thread_id not in self.threads:
            self.threads[thread_id] = []
            self.thread_metadata[thread_id] = {
                "created": datetime.now(),
                "participants": set(),
                "subject": thread_analysis["subject_thread"]["normalized"],
                "message_count": 0,
                "last_activity": None,
                "root_message_id": None,
                "max_depth": 0,
            }

        # Add email to thread
        thread_entry = {
            "email_data": eml_data,
            "thread_analysis": thread_analysis,
            "added_at": datetime.now(),
        }

        self.threads[thread_id].append(thread_entry)

        # Update thread metadata
        self._update_thread_metadata(thread_id, eml_data, thread_analysis)

        return thread_id

    def _update_thread_metadata(
        self, thread_id: str, eml_data: dict[str, Any], thread_analysis: dict[str, Any]
    ) -> None:
        """Update thread metadata with new email information.

        Args:
            thread_id: Thread identifier
            eml_data: Parsed EML data
            thread_analysis: Thread analysis results
        """
        metadata = self.thread_metadata[thread_id]
        headers = eml_data.get("headers", {}).get("common", {})

        # Update message count
        metadata["message_count"] = len(self.threads[thread_id])

        # Update participants
        participants = thread_analysis.get("thread_participants", [])
        metadata["participants"].update(participants)

        # Update last activity
        metadata["last_activity"] = datetime.now()

        # Update max depth
        current_depth = thread_analysis.get("thread_depth", 0)
        metadata["max_depth"] = max(metadata["max_depth"], current_depth)

        # Update root message ID if this is a root message
        if thread_analysis.get("is_root"):
            metadata["root_message_id"] = eml_data.get("metadata", {}).get("message_id")

    def get_thread_summary(self, thread_id: str) -> dict[str, Any] | None:
        """Get summary information for a specific thread.

        Args:
            thread_id: Thread identifier

        Returns:
            Thread summary dictionary or None if thread doesn't exist
        """
        if thread_id not in self.threads:
            return None

        thread_emails = self.threads[thread_id]
        metadata = self.thread_metadata[thread_id]

        if not thread_emails:
            return None

        # Get the first email for basic info
        first_email = thread_emails[0]["email_data"]
        headers = first_email.get("headers", {}).get("common", {})

        # Calculate engagement metrics
        engagement = self._calculate_thread_engagement(thread_emails)

        return {
            "thread_id": thread_id,
            "message_count": metadata["message_count"],
            "participants": list(metadata["participants"]),
            "subject": metadata["subject"],
            "created": metadata["created"].isoformat(),
            "last_activity": metadata["last_activity"].isoformat()
            if metadata["last_activity"]
            else None,
            "max_depth": metadata["max_depth"],
            "root_message_id": metadata["root_message_id"],
            "engagement": engagement,
        }

    def get_thread_timeline(self, thread_id: str) -> list[dict[str, Any]]:
        """Get chronological timeline of messages in a thread.

        Args:
            thread_id: Thread identifier

        Returns:
            List of timeline entries for the thread
        """
        if thread_id not in self.threads:
            return []

        thread_emails = self.threads[thread_id]

        # Sort emails by date
        sorted_emails = sorted(
            thread_emails,
            key=lambda x: x["email_data"].get("metadata", {}).get("date_timestamp", 0),
        )

        timeline = []
        for i, thread_entry in enumerate(sorted_emails):
            email_data = thread_entry["email_data"]
            thread_analysis = thread_entry["thread_analysis"]
            metadata = email_data.get("metadata", {})

            # Calculate response time
            response_time = None
            if i > 0:
                response_time = self._calculate_response_time(sorted_emails, i)

            timeline_entry = {
                "position": i + 1,
                "is_root": thread_analysis.get("is_root", False),
                "is_latest": i == len(sorted_emails) - 1,
                "email_data": email_data,
                "thread_analysis": thread_analysis,
                "response_time": response_time,
            }

            timeline.append(timeline_entry)

        return timeline

    def _calculate_response_time(
        self, sorted_emails: list[dict[str, Any]], current_index: int
    ) -> dict[str, Any] | None:
        """Calculate response time to the previous message.

        Args:
            sorted_emails: List of sorted thread emails
            current_index: Index of current email

        Returns:
            Response time information or None
        """
        if current_index == 0:
            return None

        current_email = sorted_emails[current_index]["email_data"]
        previous_email = sorted_emails[current_index - 1]["email_data"]

        current_timestamp = current_email.get("metadata", {}).get("date_timestamp")
        previous_timestamp = previous_email.get("metadata", {}).get("date_timestamp")

        if not current_timestamp or not previous_timestamp:
            return None

        response_seconds = current_timestamp - previous_timestamp

        return {
            "seconds": response_seconds,
            "formatted": self._format_duration(response_seconds),
            "is_quick": response_seconds < 3600,  # Less than 1 hour
            "is_same_day": response_seconds < 86400,  # Less than 24 hours
        }

    def _format_duration(self, seconds: float) -> str:
        """Format duration in a human-readable way.

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours}h"
        else:
            days = int(seconds / 86400)
            return f"{days}d"

    def _calculate_thread_engagement(
        self, thread_emails: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Calculate engagement metrics for the entire thread.

        Args:
            thread_emails: List of thread email entries

        Returns:
            Dictionary containing engagement metrics
        """
        if not thread_emails:
            return {
                "avg_engagement_score": 0,
                "total_messages": 0,
                "avg_response_time": None,
                "activity_level": "inactive",
            }

        # Calculate average engagement score
        total_score = 0
        response_times = []

        for i, thread_entry in enumerate(thread_emails):
            email_data = thread_entry["email_data"]
            engagement = email_data.get("thread_analysis", {}).get(
                "engagement_indicators", {}
            )
            total_score += engagement.get("engagement_score", 0)

            # Calculate response time if not the first message
            if i > 0:
                response_time = self._calculate_response_time(thread_emails, i)
                if response_time:
                    response_times.append(response_time["seconds"])

        avg_engagement = total_score / len(thread_emails)
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else None
        )

        return {
            "avg_engagement_score": round(avg_engagement, 2),
            "total_messages": len(thread_emails),
            "avg_response_time": self._format_duration(avg_response_time)
            if avg_response_time
            else None,
            "activity_level": self._calculate_activity_level(
                len(thread_emails), avg_engagement
            ),
        }

    def _calculate_activity_level(
        self, message_count: int, avg_engagement: float
    ) -> str:
        """Calculate activity level based on message count and engagement.

        Args:
            message_count: Number of messages in thread
            avg_engagement: Average engagement score

        Returns:
            Activity level string
        """
        if message_count >= 10 and avg_engagement >= 70:
            return "very_active"
        elif message_count >= 5 and avg_engagement >= 50:
            return "active"
        elif message_count >= 3:
            return "moderate"
        elif message_count >= 1:
            return "low"
        else:
            return "inactive"

    def get_all_threads(self) -> list[dict[str, Any]]:
        """Get summaries for all threads.

        Returns:
            List of all thread summaries
        """
        summaries = []
        for thread_id in self.threads:
            summary = self.get_thread_summary(thread_id)
            if summary:
                summaries.append(summary)

        return summaries

    def search_threads(self, query: str) -> list[dict[str, Any]]:
        """Search threads by subject or participant.

        Args:
            query: Search query string

        Returns:
            List of matching thread summaries
        """
        query_lower = query.lower()
        matching_threads = []

        for thread_id in self.threads:
            summary = self.get_thread_summary(thread_id)
            if not summary:
                continue

            # Search in subject
            if query_lower in summary["subject"].lower():
                matching_threads.append(summary)
                continue

            # Search in participants
            for participant in summary["participants"]:
                if query_lower in participant.lower():
                    matching_threads.append(summary)
                    break

        return matching_threads
