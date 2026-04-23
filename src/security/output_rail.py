# src/security/output_rail.py

class OutputValidator:
    def __init__(self):
        self.banned_terms = ["competitor_product_x", "confidential", "internal_use_only"]

    def validate(self, response_text: str) -> str:
        """
        Checks output for banned terms. Returns the text or a canned refusal.
        """
        lower_text = response_text.lower()

        for term in self.banned_terms:
            if term in lower_text:
                # Log this security event!
                print(f"SECURITY ALERT: Model generated banned term '{term}'")
                return "I apologize, but I cannot answer that question."

        return response_text