# src/security/input_rail.py
import re
from typing import Tuple


class PIIScrubber:
    def __init__(self):
        # Regex for email addresses
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # Regex for phone numbers (simple US format)
        self.phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'

    def scrub(self, text: str) -> Tuple[str, bool]:
        """
        Returns (scrubbed_text, was_modified)
        """
        scrubbed = text
        was_modified = False

        # Redact Emails
        if re.search(self.email_pattern, scrubbed):
            scrubbed = re.sub(self.email_pattern, "<EMAIL_REDACTED>", scrubbed)
            was_modified = True

        # Redact Phones
        if re.search(self.phone_pattern, scrubbed):
            scrubbed = re.sub(self.phone_pattern, "<PHONE_REDACTED>", scrubbed)
            was_modified = True

        return scrubbed, was_modified