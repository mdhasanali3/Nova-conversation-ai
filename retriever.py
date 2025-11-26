class ProductRetriever:
    def __init__(self):
        self.knowledge_base = {
            "lead generation": "Our platform automates lead generation with AI-powered tools that score and qualify leads in real-time.",
            "sales automation": "We offer end-to-end sales automation including email sequences, follow-ups, and CRM integration.",
            "company size": "We support companies from 10 to 10,000+ employees with scalable solutions.",
            "timeline": "Implementation typically takes 2-4 weeks depending on integration complexity.",
            "pricing": "Custom pricing based on team size and features. Contact us for a quote."
        }

    def retrieve(self, query):
        query_lower = query.lower()
        results = []

        for key, value in self.knowledge_base.items():
            if key in query_lower:
                results.append(value)

        if results:
            return " ".join(results)
        return "Our sales team can provide more specific information based on your needs."

    def get_context(self, answers):
        context = []
        for answer in answers:
            retrieved = self.retrieve(answer)
            if retrieved:
                context.append(retrieved)
        return " ".join(context)
