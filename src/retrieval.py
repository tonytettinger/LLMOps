import json
from dataclasses import dataclass
from typing import Dict, List

from main import DocumentChunk, db, get_embedding


@dataclass
class RetrievedChunk:
    id: str
    page_content: str
    metadata: Dict[str, str]

async def retrieve_chunks(query: str, k: int = 5) -> List[DocumentChunk]:
    query_embedding = get_embedding(query)
    query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, content, metadata
            FROM document_chunks
            ORDER BY embedding <=> $1::vector
            LIMIT $2
            """,
            query_embedding_str,
            k,
        )

    chunks = []
    for row in rows:
        metadata = row["metadata"]
        if isinstance(metadata, str):
            metadata = json.loads(metadata)

        chunks.append(
            RetrievedChunk(
                id=row["id"],
                page_content=row["content"],
                metadata=metadata,
            )
        )

    return chunks