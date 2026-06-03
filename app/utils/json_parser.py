import json
import re


def safe_json_loads(text):

    try:
        return json.loads(text)
    except Exception:
        # extract JSON from messy response
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Invalid JSON from LLM")