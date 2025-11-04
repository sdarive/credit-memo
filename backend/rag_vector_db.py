"""
Vector Database Utilities for RAG Knowledge Base
Handles PostgreSQL with pgvector for semantic search
"""

import os
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import json
from dotenv import load_dotenv


class VectorDatabase:
    """Manages PostgreSQL with pgvector for semantic search"""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize vector database connection

        Args:
            host: PostgreSQL host (or use POSTGRES_HOST env var)
            port: PostgreSQL port (or use POSTGRES_PORT env var, default: 5432)
            database: Database name (or use POSTGRES_DB env var)
            user: Database user (or use POSTGRES_USER env var)
            password: Database password (or use POSTGRES_PASSWORD env var)
        """
        load_dotenv()

        self.host = host or os.getenv('POSTGRES_HOST', 'localhost')
        self.port = port or int(os.getenv('POSTGRES_PORT', 5432))
        self.database = database or os.getenv('POSTGRES_DB', 'credit_memo_kb')
        self.user = user or os.getenv('POSTGRES_USER', 'postgres')
        self.password = password or os.getenv('POSTGRES_PASSWORD', '')

        self.conn = None
        self.embedding_dimension = None

    def connect(self) -> bool:
        """
        Establish connection to PostgreSQL

        Returns:
            True if connection successful
        """
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.conn.autocommit = False
            print(f"✓ Connected to PostgreSQL at {self.host}:{self.port}/{self.database}")
            return True
        except psycopg2.Error as e:
            print(f"✗ Database connection failed: {e}")
            print(f"\nConnection parameters:")
            print(f"  Host: {self.host}")
            print(f"  Port: {self.port}")
            print(f"  Database: {self.database}")
            print(f"  User: {self.user}")
            print(f"\nMake sure PostgreSQL is running and credentials are correct.")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Disconnected from database")

    def setup_database(self, embedding_dim: int = 768) -> bool:
        """
        Set up database schema with pgvector extension

        Args:
            embedding_dim: Dimension of embedding vectors (default: 768 for all-mpnet-base-v2)

        Returns:
            True if setup successful
        """
        if not self.conn:
            print("✗ Not connected to database")
            return False

        self.embedding_dimension = embedding_dim

        try:
            cur = self.conn.cursor()

            print(f"\nSetting up vector database (dimension: {embedding_dim})...")

            # Step 1: Enable pgvector extension
            print("  1. Enabling pgvector extension...")
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            print("     ✓ pgvector extension enabled")

            # Step 2: Create table
            print("  2. Creating memo_kb_chunks table...")
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS memo_kb_chunks (
                id SERIAL PRIMARY KEY,
                chunk_id VARCHAR(32) UNIQUE NOT NULL,
                original_id VARCHAR(16) NOT NULL,
                chunk_index INT NOT NULL,
                title TEXT,
                borrower VARCHAR(255),
                loan_type VARCHAR(255),
                chunk_text TEXT NOT NULL,
                chunk_length INT,
                score INT,
                recommendation TEXT,
                embedding VECTOR({embedding_dim}),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cur.execute(create_table_sql)
            print("     ✓ Table created")

            # Step 3: Create indexes
            print("  3. Creating indexes...")

            # Index on chunk_id for fast lookups
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunk_id
                ON memo_kb_chunks(chunk_id);
            """)

            # Index on original_id for finding all chunks of a memo
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_original_id
                ON memo_kb_chunks(original_id);
            """)

            # Index on score for filtering by risk level
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_score
                ON memo_kb_chunks(score);
            """)

            # Vector index using HNSW for fast similarity search
            cur.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_embedding_hnsw
                ON memo_kb_chunks
                USING hnsw (embedding vector_cosine_ops);
            """)

            print("     ✓ Indexes created")

            # Commit changes
            self.conn.commit()
            cur.close()

            print("\n✓ Database setup complete!")
            return True

        except psycopg2.Error as e:
            print(f"\n✗ Database setup failed: {e}")
            self.conn.rollback()
            return False

    def insert_chunks(self, df: pd.DataFrame, batch_size: int = 100) -> int:
        """
        Insert chunked credit memos with embeddings into database

        Args:
            df: DataFrame with columns: chunk_id, original_id, chunk_index,
                title, borrower, loan_type, chunk_text, chunk_length, score,
                recommendation, embedding
            batch_size: Batch size for insertions

        Returns:
            Number of rows inserted
        """
        if not self.conn:
            print("✗ Not connected to database")
            return 0

        try:
            cur = self.conn.cursor()

            print(f"\nInserting {len(df)} chunks into database...")

            # Prepare data for insertion
            records = []
            for _, row in df.iterrows():
                # Convert embedding list to PostgreSQL array format
                embedding = row['embedding']
                if isinstance(embedding, str):
                    # Parse string representation of list
                    embedding = json.loads(embedding)

                record = (
                    row.get('chunk_id'),
                    row.get('original_id'),
                    int(row.get('chunk_index', 0)),
                    row.get('title'),
                    row.get('borrower'),
                    row.get('loan_type'),
                    row.get('chunk_text'),
                    int(row.get('chunk_length', 0)),
                    int(row.get('score', 0)),
                    row.get('recommendation'),
                    embedding
                )
                records.append(record)

            # Insert in batches
            insert_sql = """
                INSERT INTO memo_kb_chunks
                (chunk_id, original_id, chunk_index, title, borrower, loan_type,
                 chunk_text, chunk_length, score, recommendation, embedding)
                VALUES %s
                ON CONFLICT (chunk_id) DO UPDATE SET
                    chunk_text = EXCLUDED.chunk_text,
                    embedding = EXCLUDED.embedding;
            """

            total_inserted = 0
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                execute_values(cur, insert_sql, batch)
                total_inserted += len(batch)

                if (i + batch_size) % (batch_size * 5) == 0:
                    print(f"  Inserted {total_inserted}/{len(records)}...")

            self.conn.commit()
            cur.close()

            print(f"✓ Inserted {total_inserted} chunks")
            return total_inserted

        except psycopg2.Error as e:
            print(f"✗ Insert failed: {e}")
            self.conn.rollback()
            return 0

    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        score_filter: Optional[int] = None,
        borrower_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using vector similarity

        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results
            score_filter: Optional filter by risk score
            borrower_filter: Optional filter by borrower type

        Returns:
            List of matching chunks with similarity scores
        """
        if not self.conn:
            print("✗ Not connected to database")
            return []

        try:
            cur = self.conn.cursor()

            # Build query with optional filters
            where_clauses = []
            params = []

            if score_filter is not None:
                where_clauses.append("score = %s")
                params.append(score_filter)

            if borrower_filter:
                where_clauses.append("borrower ILIKE %s")
                params.append(f"%{borrower_filter}%")

            where_sql = ""
            if where_clauses:
                where_sql = "WHERE " + " AND ".join(where_clauses)

            # Query using cosine distance (1 - cosine similarity)
            query_sql = f"""
                SELECT
                    chunk_id,
                    original_id,
                    title,
                    borrower,
                    loan_type,
                    chunk_text,
                    score,
                    recommendation,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM memo_kb_chunks
                {where_sql}
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
            """

            # Add embedding twice (for SELECT and ORDER BY) plus other params
            all_params = [query_embedding] + params + [query_embedding, limit]

            cur.execute(query_sql, all_params)

            results = []
            for row in cur.fetchall():
                results.append({
                    'chunk_id': row[0],
                    'original_id': row[1],
                    'title': row[2],
                    'borrower': row[3],
                    'loan_type': row[4],
                    'chunk_text': row[5],
                    'score': row[6],
                    'recommendation': row[7],
                    'similarity': float(row[8])
                })

            cur.close()
            return results

        except psycopg2.Error as e:
            print(f"✗ Search failed: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics

        Returns:
            Dictionary with database statistics
        """
        if not self.conn:
            return {}

        try:
            cur = self.conn.cursor()

            # Total chunks
            cur.execute("SELECT COUNT(*) FROM memo_kb_chunks;")
            total_chunks = cur.fetchone()[0]

            # Chunks by score
            cur.execute("""
                SELECT score, COUNT(*)
                FROM memo_kb_chunks
                GROUP BY score
                ORDER BY score;
            """)
            score_distribution = {row[0]: row[1] for row in cur.fetchall()}

            # Top borrowers
            cur.execute("""
                SELECT borrower, COUNT(*) as count
                FROM memo_kb_chunks
                GROUP BY borrower
                ORDER BY count DESC
                LIMIT 10;
            """)
            top_borrowers = {row[0]: row[1] for row in cur.fetchall()}

            cur.close()

            return {
                'total_chunks': total_chunks,
                'score_distribution': score_distribution,
                'top_borrowers': top_borrowers,
                'embedding_dimension': self.embedding_dimension
            }

        except psycopg2.Error as e:
            print(f"✗ Failed to get statistics: {e}")
            return {}

    def clear_database(self) -> bool:
        """
        Clear all data from the knowledge base table

        Returns:
            True if successful
        """
        if not self.conn:
            return False

        try:
            cur = self.conn.cursor()
            cur.execute("TRUNCATE TABLE memo_kb_chunks RESTART IDENTITY;")
            self.conn.commit()
            cur.close()
            print("✓ Database cleared")
            return True
        except psycopg2.Error as e:
            print(f"✗ Clear failed: {e}")
            self.conn.rollback()
            return False


def load_knowledge_base_from_csv(
    csv_path: str,
    db_host: Optional[str] = None,
    db_port: Optional[int] = None,
    db_name: Optional[str] = None,
    db_user: Optional[str] = None,
    db_password: Optional[str] = None,
    embedding_dim: int = 768
) -> bool:
    """
    Complete pipeline: Load chunks from CSV into vector database

    Args:
        csv_path: Path to CSV with embeddings
        db_host, db_port, db_name, db_user, db_password: Database credentials
        embedding_dim: Embedding dimension

    Returns:
        True if successful
    """
    print("\n" + "="*60)
    print("Loading Knowledge Base into Vector Database")
    print("="*60 + "\n")

    # Load CSV
    print(f"1. Loading data from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"   ✓ Loaded {len(df)} chunks")

    # Initialize database
    print(f"\n2. Connecting to database...")
    db = VectorDatabase(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )

    if not db.connect():
        return False

    # Setup schema
    print(f"\n3. Setting up database schema...")
    if not db.setup_database(embedding_dim=embedding_dim):
        db.disconnect()
        return False

    # Insert chunks
    print(f"\n4. Inserting chunks...")
    inserted = db.insert_chunks(df)

    if inserted == 0:
        db.disconnect()
        return False

    # Show statistics
    print(f"\n5. Database statistics:")
    stats = db.get_statistics()
    print(f"   Total chunks: {stats.get('total_chunks', 0)}")
    print(f"   Risk score distribution: {stats.get('score_distribution', {})}")

    db.disconnect()

    print("\n" + "="*60)
    print("✓ Knowledge base loaded successfully!")
    print("="*60 + "\n")

    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "rag_data/credit_memo_chunks_with_embeddings.csv"

    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        print("\nUsage:")
        print("  python rag_vector_db.py <csv_path>")
        print("\nExample:")
        print("  python rag_vector_db.py rag_data/credit_memo_chunks_with_embeddings.csv")
        sys.exit(1)

    # Load knowledge base
    success = load_knowledge_base_from_csv(
        csv_path=csv_file,
        embedding_dim=768  # all-mpnet-base-v2 dimension
    )

    if success:
        print("\nYou can now use the RAG module for semantic search!")
    else:
        print("\n✗ Failed to load knowledge base")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is installed and running")
        print("  2. Create database: createdb credit_memo_kb")
        print("  3. Install pgvector extension")
        print("  4. Check environment variables or connection parameters")
