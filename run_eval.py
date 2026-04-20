import asyncio
import csv

from main import db
from src.generation import generate_answer
from src.judge import FaithfulnessJudge, RelevanceJudge
from src.retrieval import retrieve_chunks


def load_golden_dataset():
    rows = []
    with open("golden_dataset.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((row["query"], row["expected_id"]))
    return rows


async def main():
    results = []

    await db.connect()
    try:
        dataset = load_golden_dataset()

        faith_judge = FaithfulnessJudge()
        rel_judge = RelevanceJudge()

        print("Starting Evaluation Run...")

        for query in dataset:
            print("QUERY IS", query)
            chunks = await retrieve_chunks(query[0])
            context_text = [c.page_content for c in chunks]

            generated_output = generate_answer(query, chunks)
            answer_text = generated_output["answer"]

            faith_result = faith_judge.evaluate(context_text, answer_text)
            rel_result = rel_judge.evaluate(query, answer_text)

            results.append({
                "query": query,
                "faithfulness": faith_result["score"],
                "relevance": rel_result["score"],
            })

            print(
                f"Query: {query} | "
                f"Faith: {faith_result['score']} | "
                f"Rel: {rel_result['score']}"
            )

        avg_faith = sum(r["faithfulness"] for r in results) / len(results)
        avg_rel = sum(r["relevance"] for r in results) / len(results)

        print(f"\nFinal Score -> Faithfulness: {avg_faith:.2f}, Relevance: {avg_rel:.2f}")

        if avg_faith < 0.9:
            print("❌ FAILED: Faithfulness below 0.9 threshold.")
            raise SystemExit(1)
        else:
            print("✅ PASSED: Ready for Deployment.")
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())