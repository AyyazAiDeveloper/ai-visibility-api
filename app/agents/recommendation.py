import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ContentRecommendationAgent:

    def generate_recommendations(self, query, domain):

        prompt = f"""
You are an SEO content strategist.

Given:

Query: {query}
Target Domain: {domain}

Task:
Generate content recommendations to improve visibility.

Return ONLY JSON:

{{
  "recommendations": [
    {{
      "content_type": "blog_post",
      "title": "",
      "rationale": "",
      "target_keywords": ["", ""],
      "priority": "high/medium/low"
    }}
  ]
}}

Rules:
- Must be actionable
- Must target SEO ranking improvement
- Must include keywords
- Must include comparison or informational intent
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert SEO strategist."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content