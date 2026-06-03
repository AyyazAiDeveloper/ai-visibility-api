import os
from openai import OpenAI


class QueryDiscoveryAgent:

    def generate_queries(self, name, domain, industry, competitors):

        # Create client INSIDE function (SAFE)
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise Exception("OPENAI_API_KEY not found. Check .env loading.")

        client = OpenAI(api_key=api_key)

        prompt = f"""
You are an SEO research expert.

Business:
- Name: {name}
- Domain: {domain}
- Industry: {industry}
- Competitors: {competitors}

Task:
Generate 10-15 high-intent SEO questions.

Return ONLY JSON:
{{
  "queries": ["example 1", "example 2"]
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate structured SEO queries."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content