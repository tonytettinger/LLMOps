import csv
import os

import psycopg2
from dotenv import load_dotenv

from main import get_embedding

load_dotenv()


def load_golden_dataset():
    rows = []
    with open("golden_dataset.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((row["query"], row["expected_id"]))
    return rows


def run_retrieval_eval(k=3):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    try:
        with conn.cursor() as cursor:
            dataset = load_golden_dataset()
            hits = 0

            for query, expected_id in dataset:
                query_vec = get_embedding(query)
                query_vec_str = "[" + ",".join(map(str, query_vec)) + "]"

                cursor.execute(
                    """
                    SELECT id, 1 - (embedding <=> %s::vector) AS similarity
                    FROM document_chunks
                    ORDER BY embedding <=> %s::vector ASC
                    LIMIT %s;
                    """,
                    (query_vec_str, query_vec_str, k),
                )

                results = cursor.fetchall()
                retrieved_ids = [row[0] for row in results]

                if expected_id in retrieved_ids:
                    hits += 1
                    print(f"✅ Query: '{query}' found correct chunk.")
                else:
                    print(f"❌ Query: '{query}' missed. Got: {retrieved_ids}")

            hit_rate = hits / len(dataset)
            print(f"Final Hit Rate@{k}: {hit_rate:.2f}")

            if hit_rate < 0.9:
                raise Exception("Retrieval quality below threshold! Do not deploy.")
    finally:
        conn.close()


if __name__ == "__main__":
    run_retrieval_eval(k=3)