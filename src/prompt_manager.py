import json
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.security.output_rail import OutputValidator


class PromptManager:
    def __init__(self, template_dir: str = "src/prompts"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['xml']) # Security against injection in XML tags
        )

    def render_prompt(self, template_name: str, **kwargs) -> str:
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """Safe JSON parsing helper with markdown fallback."""
        cleaned_response_text = OutputValidator().validate(response_text)
        try:
            return json.loads(cleaned_response_text)
        except json.JSONDecodeError:
            cleaned = cleaned_response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)