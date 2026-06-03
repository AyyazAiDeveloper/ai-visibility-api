import os
import random
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class VisibilityScoringAgent:

    def score_query(self, query, domain):

        prompt = f"""
You are an SEO analytics expert.

Given:
Query: {query}
Target Domain: {domain}

Task:
Estimate:

1. search_volume (0–10000)
2. competitive_difficulty (0–100)
3. domain_visible (true/false)
4. visibility_position (1–10 or null)
5. opportunity_score (0–1 float)

Rules:
- Be realistic
- If competition is high, opportunity is lower
- If domain likely not present → opportunity increases

Return ONLY JSON:
{{
  "search_volume": 0,
  "competitive_difficulty": 0,
  "domain_visible": false,
  "visibility_position": null,
  "opportunity_score": 0.0
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You return structured SEO metrics."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content