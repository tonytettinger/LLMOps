# Setup notes

## Database creation instructions

-- Run this once to enable vector operations in the database

```CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_chunks (
id UUID PRIMARY KEY,
content TEXT NOT NULL,
metadata JSONB, -- Stores source, page number, etc.
embedding vector(1536) -- Must match our model dimensions
);
```

-- Create an HNSW index for fast approximate nearest neighbor search

```
CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);
```
