"""
Text Chunking and Embedding Module for RAG
Handles chunking of credit memo narratives and embedding generation
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np


class TextChunker:
    """Handles text chunking for semantic search"""

    @staticmethod
    def chunk_text(text: str, max_length: int = 500) -> List[str]:
        """
        Split long text into manageable chunks for semantic search

        Args:
            text: Text to chunk
            max_length: Maximum chunk length in characters

        Returns:
            List of text chunks
        """
        if not text or len(text) <= max_length:
            return [text] if text else []

        # Split by sentences
        sentences = text.split('. ')
        chunks = []
        current = ""

        for sentence in sentences:
            # Add period back if it was removed
            if not sentence.endswith('.'):
                sentence += '.'

            # Check if adding this sentence exceeds max_length
            if len(current) + len(sentence) < max_length:
                current += sentence + " "
            else:
                # Save current chunk and start new one
                if current:
                    chunks.append(current.strip())
                current = sentence + " "

        # Add remaining text
        if current:
            chunks.append(current.strip())

        return chunks

    @staticmethod
    def chunk_dataframe(
        df: pd.DataFrame,
        text_column: str,
        id_column: str,
        max_length: int = 300,
        additional_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Chunk text in a DataFrame and create new rows for each chunk

        Args:
            df: Source DataFrame
            text_column: Column containing text to chunk
            id_column: Column containing unique IDs
            max_length: Maximum chunk length
            additional_columns: Additional columns to preserve in output

        Returns:
            New DataFrame with chunked text
        """
        chunked_records = []

        for _, row in df.iterrows():
            text = row[text_column]
            chunks = TextChunker.chunk_text(text, max_length=max_length)

            for idx, chunk in enumerate(chunks):
                record = {
                    'chunk_id': f"{row[id_column]}-{idx+1}",
                    'original_id': row[id_column],
                    'chunk_index': idx + 1,
                    'chunk_text': chunk,
                    'chunk_length': len(chunk)
                }

                # Add additional columns
                if additional_columns:
                    for col in additional_columns:
                        if col in row:
                            record[col] = row[col]

                chunked_records.append(record)

        return pd.DataFrame(chunked_records)


class EmbeddingGenerator:
    """Handles embedding generation for semantic search"""

    def __init__(self, model_name: str = 'all-mpnet-base-v2'):
        """
        Initialize embedding generator

        Args:
            model_name: Sentence transformer model name
                       Options:
                         - 'all-mpnet-base-v2': Best quality (768 dims)
                         - 'all-MiniLM-L6-v2': Fast and efficient (384 dims)
                         - 'all-distilroberta-v1': Good balance (768 dims)
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✓ Model loaded. Embedding dimension: {self.embedding_dim}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Input text

        Returns:
            Embedding vector as list of floats
        """
        if not text:
            return [0.0] * self.embedding_dim

        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def generate_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts efficiently

        Args:
            texts: List of input texts
            batch_size: Batch size for processing
            show_progress: Show progress bar

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        print(f"Generating embeddings for {len(texts)} texts...")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )

        print(f"✓ Generated {len(embeddings)} embeddings")

        return embeddings.tolist()

    def add_embeddings_to_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str,
        embedding_column: str = 'embedding',
        batch_size: int = 32
    ) -> pd.DataFrame:
        """
        Add embeddings to DataFrame

        Args:
            df: Source DataFrame
            text_column: Column containing text to embed
            embedding_column: Name for new embedding column
            batch_size: Batch size for processing

        Returns:
            DataFrame with embeddings added
        """
        texts = df[text_column].fillna('').tolist()

        embeddings = self.generate_embeddings_batch(
            texts,
            batch_size=batch_size,
            show_progress=True
        )

        df[embedding_column] = embeddings

        return df


def process_credit_memos_for_rag(
    input_csv: str,
    output_dir: str = 'rag_data',
    text_column: str = 'risk_analysis',
    id_column: str = 'memo_id',
    max_chunk_length: int = 300,
    embedding_model: str = 'all-mpnet-base-v2'
) -> Dict[str, Any]:
    """
    Complete pipeline: chunk credit memos and generate embeddings

    Args:
        input_csv: Path to input CSV with credit memos
        output_dir: Directory for output files
        text_column: Column containing text to chunk
        id_column: Column with unique IDs
        max_chunk_length: Maximum chunk length
        embedding_model: Sentence transformer model name

    Returns:
        Dictionary with processing results
    """
    print("\n" + "="*60)
    print("Processing Credit Memos for RAG Knowledge Base")
    print("="*60 + "\n")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Load data
    print(f"1. Loading credit memos from: {input_csv}")
    df = pd.read_csv(input_csv)
    print(f"   ✓ Loaded {len(df)} memos")

    # Step 2: Chunk text
    print(f"\n2. Chunking text (max length: {max_chunk_length} chars)")
    chunker = TextChunker()

    additional_cols = ['title', 'borrower', 'loan_type', 'score', 'recommendation']
    df_chunks = chunker.chunk_dataframe(
        df,
        text_column=text_column,
        id_column=id_column,
        max_length=max_chunk_length,
        additional_columns=additional_cols
    )
    print(f"   ✓ Created {len(df_chunks)} chunks from {len(df)} memos")

    # Save chunked data
    chunks_csv = os.path.join(output_dir, "credit_memo_risk_chunks.csv")
    df_chunks.to_csv(chunks_csv, index=False)
    print(f"   ✓ Saved chunks to: {chunks_csv}")

    # Step 3: Generate embeddings
    print(f"\n3. Generating embeddings (model: {embedding_model})")
    embedder = EmbeddingGenerator(model_name=embedding_model)

    df_chunks = embedder.add_embeddings_to_dataframe(
        df_chunks,
        text_column='chunk_text',
        embedding_column='embedding'
    )

    # Save with embeddings
    embeddings_csv = os.path.join(output_dir, "credit_memo_chunks_with_embeddings.csv")
    df_chunks.to_csv(embeddings_csv, index=False)
    print(f"   ✓ Saved embeddings to: {embeddings_csv}")

    # Step 4: Generate statistics
    print("\n" + "="*60)
    print("Processing Statistics:")
    print("="*60)
    print(f"Original memos: {len(df)}")
    print(f"Total chunks: {len(df_chunks)}")
    print(f"Avg chunks per memo: {len(df_chunks) / len(df):.2f}")
    print(f"Embedding dimension: {embedder.embedding_dim}")
    print(f"\nChunk length statistics:")
    print(f"  Min: {df_chunks['chunk_length'].min()} chars")
    print(f"  Max: {df_chunks['chunk_length'].max()} chars")
    print(f"  Mean: {df_chunks['chunk_length'].mean():.0f} chars")

    # Risk score distribution
    print(f"\nChunks by risk score:")
    for score in sorted(df_chunks['score'].unique()):
        count = len(df_chunks[df_chunks['score'] == score])
        print(f"  Score {score}: {count} chunks")

    print("\n" + "="*60)
    print("✓ RAG processing complete!")
    print("="*60 + "\n")

    return {
        'original_memos': len(df),
        'total_chunks': len(df_chunks),
        'chunks_csv': chunks_csv,
        'embeddings_csv': embeddings_csv,
        'embedding_dimension': embedder.embedding_dim,
        'model_name': embedder.model_name
    }


if __name__ == "__main__":
    # Test the chunking and embedding pipeline
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "rag_data/credit_memo_dataset_diverse.csv"

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("\nUsage:")
        print("  python rag_chunking.py <input_csv>")
        print("\nExample:")
        print("  python rag_chunking.py rag_data/credit_memo_dataset_diverse.csv")
        sys.exit(1)

    # Process memos
    results = process_credit_memos_for_rag(
        input_csv=input_file,
        output_dir='rag_data',
        max_chunk_length=300,
        embedding_model='all-mpnet-base-v2'
    )

    # Display sample
    print("\nSample Chunks:")
    print("="*60)
    df_chunks = pd.read_csv(results['chunks_csv'])
    for i in range(min(3, len(df_chunks))):
        row = df_chunks.iloc[i]
        print(f"\nChunk {i+1}: {row['chunk_id']}")
        print(f"  Score: {row['score']}")
        print(f"  Length: {row['chunk_length']} chars")
        print(f"  Text: {row['chunk_text'][:150]}...")
