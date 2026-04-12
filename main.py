#!/usr/bin/env python3
"""
Local ingestion script to test text splitting
Reads a file from the current directory and prints chunks created by LangChain text splitter
"""

import os
import sys
from pathlib import Path
from typing import List

from langchain_text_splitters import Language, RecursiveCharacterTextSplitter


def parse_markdown_file(file_path: Path) -> List[str]:
    """Read and parse a markdown file into chunks using LangChain text splitter."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Initialize the splitter with Markdown-specific rules
    # chunk_size=1000: Target ~1000 characters per chunk (approx 200-300 tokens)
    # chunk_overlap=100: Keep 100 chars of context from the previous chunk
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN,
        chunk_size=1000,
        chunk_overlap=200
    )

    # The splitter returns LangChain 'Document' objects
    raw_chunks = splitter.create_documents([text])

    # Extract just the text content from each chunk
    chunks = [chunk.page_content for chunk in raw_chunks]

    return chunks

def main():
    """Main function to read a file and print chunks."""
    file_path = "Nimble_guide.MD"

    print(f"📄 Reading file: {file_path}")

    chunks = parse_markdown_file(file_path)

    print(f"📊 Created {len(chunks)} chunks")
    print("=" * 80)

    # Print each chunk with metadata
    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Length: {len(chunk)} characters")
        print(f"Content:\n{chunk}")
        print("-" * 40)

    print(f"\n✅ Total chunks: {len(chunks)}")
    print(f"📄 File: {file_path}")
    print(f"📏 Total characters: {sum(len(chunk) for chunk in chunks)}")

if __name__ == "__main__":
    main()
