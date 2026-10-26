"""Terminal chat: python -m copilot.cli"""

from .answer import Copilot
from .feedback import log_interaction


def main() -> None:
    bot = Copilot()
    print("API Docs Copilot — ask about the Staylane Partner API (type 'quit' to exit)\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        if not q:
            continue
        a = bot.ask(q)
        print(f"\nCopilot: {a.text}\n")
        for i, c in enumerate(a.sources, 1):
            print(f"  [{i}] {c.label}")
        rating = input("\nHelpful? (y/n/enter to skip): ").strip().lower()
        log_interaction(a, {"y": "up", "n": "down"}.get(rating))
        print("-" * 60)


if __name__ == "__main__":
    main()
