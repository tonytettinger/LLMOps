# src/generation.py
from typing import Any, List

from litellm import completion

from src.prompt_manager import PromptManager

# Initialize manager
pm = PromptManager()

def generate_answer(user_query: str, context_chunks: List[Any]):
    # 1. Render the Prompt
    # We pass the list of chunk objects directly to the template
    system_message = pm.render_prompt(
        "support_v1.j2",
        user_query=user_query,
        context_chunks=context_chunks
    )

    # 2. Call the Model
    response = completion(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": system_message}
            # Note: For some providers, you might split this into 'system' and 'user' roles.
            # But putting the whole structured block in 'user' is a robust pattern for generic models.
        ],
        response_format={"type": "json_object"}, # <--- ENFORCE JSON
        temperature=0.1 # Low temperature for factual grounding
    )

    # 3. Parse and Return
    raw_content = response.choices[0].message.content
    return pm.parse_response(raw_content)