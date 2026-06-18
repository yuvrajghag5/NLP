from config.settings import (
    COMPANY_NAME,
    DEFAULT_CEO_QUESTION
)

from rag.rag_chain import generate_ceo_briefing


class AICEOAgent:
    def __init__(self, company_name=COMPANY_NAME):
        self.company_name = company_name

    def run(self, question=DEFAULT_CEO_QUESTION):
        print("\nAI CEO Agent Started")
        print("=" * 80)
        print("Company:", self.company_name)
        print("CEO Question:", question)
        print("=" * 80)

        briefing = generate_ceo_briefing(question=question)

        if briefing is None:
            print("\nAI CEO Agent failed.")
            print("Reason: CEO briefing could not be generated.")
            return None

        print("\nAI CEO Agent Completed Successfully")
        print("=" * 80)

        return briefing

    def display_briefing(self, briefing):
        if briefing is None:
            return

        print("\nFINAL CEO BRIEFING")
        print("=" * 80)
        print(briefing.get("answer", "No answer generated."))
        print("=" * 80)

    def display_sources(self, briefing):
        if briefing is None:
            return

        sources = briefing.get("sources_used", [])

        if not sources:
            print("\nNo sources found in briefing.")
            return

        print("\nSOURCES USED")
        print("=" * 80)

        for source in sources:
            print("Source ID:", source.get("source_id", ""))
            print("Type:", source.get("type", ""))
            print("Title:", source.get("title", ""))
            print("Source:", source.get("source", ""))
            print("Publisher:", source.get("publisher", ""))
            print("URL:", source.get("url", ""))
            print("-" * 80)


def main():
    agent = AICEOAgent()

    briefing = agent.run()

    agent.display_briefing(briefing)

    agent.display_sources(briefing)


if __name__ == "__main__":
    main()