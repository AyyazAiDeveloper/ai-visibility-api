from app.agents.discovery import QueryDiscoveryAgent
from app.agents.scoring import VisibilityScoringAgent
from app.agents.recommendation import ContentRecommendationAgent
from app.utils.json_parser import safe_json_loads


class PipelineService:

    def __init__(self):
        self.discovery = QueryDiscoveryAgent()
        self.scoring = VisibilityScoringAgent()
        self.recommendation = ContentRecommendationAgent()

    def run(self, profile):

        # =========================
        # STEP 1 — Generate Queries
        # =========================
        raw_queries = self.discovery.generate_queries(
            profile.name,
            profile.domain,
            profile.industry,
            profile.competitors
        )

        queries = safe_json_loads(raw_queries).get("queries", [])

        scored_queries = []
        recommendations = []

        # =========================
        # STEP 2 — Score Queries
        # =========================
        for q in queries:

            score_raw = self.scoring.score_query(q, profile.domain)
            score = safe_json_loads(score_raw)

            score["query_text"] = q
            scored_queries.append(score)

        # =========================
        # STEP 3 — Sort by Opportunity Score
        # =========================
        scored_queries.sort(
            key=lambda x: x.get("opportunity_score", 0),
            reverse=True
        )

        top_queries = scored_queries[:3]

        # =========================
        # STEP 4 — Generate Recommendations
        # =========================
        for q in top_queries:

            rec_raw = self.recommendation.generate_recommendations(
                q["query_text"],
                profile.domain
            )

            rec = safe_json_loads(rec_raw)

            recommendations.append(rec)

        # =========================
        # FINAL OUTPUT
        # =========================
        return {
            "queries": scored_queries,
            "top_queries": top_queries,
            "recommendations": recommendations
        }