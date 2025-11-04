"""
RAG Retrieval Module
Integrates semantic search with knowledge base for context-aware credit memo generation
"""

import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from rag_vector_db import VectorDatabase
from dotenv import load_dotenv


class RAGRetriever:
    """
    Retrieval-Augmented Generation (RAG) retriever for credit memos
    Combines query embedding with semantic search to retrieve relevant context
    """

    def __init__(
        self,
        embedding_model: str = 'all-mpnet-base-v2',
        db_host: Optional[str] = None,
        db_port: Optional[int] = None,
        db_name: Optional[str] = None,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None
    ):
        """
        Initialize RAG retriever

        Args:
            embedding_model: Sentence transformer model name
            db_host, db_port, db_name, db_user, db_password: Database connection params
        """
        load_dotenv()

        print("Initializing RAG retriever...")

        # Initialize embedding model
        print(f"  Loading embedding model: {embedding_model}...")
        self.model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"  ✓ Model loaded (dimension: {self.embedding_dim})")

        # Initialize database connection
        print(f"  Connecting to vector database...")
        self.db = VectorDatabase(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        self.connected = self.db.connect()

        if self.connected:
            print("✓ RAG retriever initialized")
        else:
            print("⚠ RAG retriever initialized but database connection failed")
            print("  Semantic search will not be available")

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query

        Args:
            query: Query text

        Returns:
            Embedding vector
        """
        if not query:
            return [0.0] * self.embedding_dim

        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
        score_filter: Optional[int] = None,
        borrower_filter: Optional[str] = None,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context chunks for a query

        Args:
            query: Query text (e.g., "What are good examples of strong DSCR analysis?")
            limit: Maximum number of results
            score_filter: Filter by risk score (1-5)
            borrower_filter: Filter by borrower type
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of relevant chunks with metadata
        """
        if not self.connected:
            print("⚠ Database not connected, cannot retrieve context")
            return []

        # Generate query embedding
        query_embedding = self.embed_query(query)

        # Perform semantic search
        results = self.db.semantic_search(
            query_embedding=query_embedding,
            limit=limit * 2,  # Get more results to filter by threshold
            score_filter=score_filter,
            borrower_filter=borrower_filter
        )

        # Filter by similarity threshold
        filtered_results = [
            r for r in results
            if r.get('similarity', 0) >= similarity_threshold
        ]

        # Limit results
        return filtered_results[:limit]

    def format_context_for_llm(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        include_metadata: bool = True
    ) -> str:
        """
        Format retrieved context for LLM prompt

        Args:
            retrieved_chunks: List of retrieved chunks
            include_metadata: Include metadata in formatted output

        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return "No relevant examples found in knowledge base."

        context_parts = []

        for i, chunk in enumerate(retrieved_chunks, 1):
            part = f"--- Example {i} ---\n"

            if include_metadata:
                part += f"Memo ID: {chunk['original_id']}\n"
                part += f"Title: {chunk['title']}\n"
                part += f"Borrower Type: {chunk['borrower']}\n"
                part += f"Loan Type: {chunk['loan_type']}\n"
                part += f"Risk Score: {chunk['score']}/5\n"
                part += f"Similarity: {chunk['similarity']:.3f}\n\n"

            part += f"Risk Analysis:\n{chunk['chunk_text']}\n"

            if include_metadata and chunk.get('recommendation'):
                part += f"\nRecommendation: {chunk['recommendation']}\n"

            context_parts.append(part)

        return "\n".join(context_parts)

    def retrieve_similar_memos(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, Any],
        borrower_info: Dict[str, str],
        limit: int = 3
    ) -> str:
        """
        Retrieve similar credit memos based on financial profile

        Args:
            financial_data: Extracted financial data
            ratios: Calculated financial ratios
            borrower_info: Borrower information
            limit: Number of similar memos to retrieve

        Returns:
            Formatted context string
        """
        # Build query from financial profile
        query_parts = []

        # Add borrower info
        borrower_industry = borrower_info.get('industry', 'business')
        query_parts.append(f"{borrower_industry}")

        # Add financial strength indicators
        dscr = ratios.get('dscr')
        if dscr:
            if dscr >= 1.5:
                query_parts.append("strong debt service coverage")
            elif dscr >= 1.25:
                query_parts.append("adequate debt service coverage")
            else:
                query_parts.append("weak debt service coverage")

        current_ratio = ratios.get('current_ratio')
        if current_ratio:
            if current_ratio >= 2.0:
                query_parts.append("strong liquidity")
            elif current_ratio >= 1.5:
                query_parts.append("adequate liquidity")
            else:
                query_parts.append("liquidity concerns")

        leverage = ratios.get('leverage_ratio')
        if leverage:
            if leverage <= 0.3:
                query_parts.append("low leverage")
            elif leverage <= 0.5:
                query_parts.append("moderate leverage")
            else:
                query_parts.append("high leverage")

        # Create query
        query = " ".join(query_parts)

        print(f"\n  RAG Query: {query}")

        # Retrieve similar memos
        results = self.retrieve_context(
            query=query,
            limit=limit,
            similarity_threshold=0.4  # Lower threshold for financial profile matching
        )

        if results:
            print(f"  ✓ Retrieved {len(results)} similar memos (avg similarity: {sum(r['similarity'] for r in results) / len(results):.3f})")
        else:
            print(f"  ⚠ No similar memos found")

        return self.format_context_for_llm(results, include_metadata=True)

    def retrieve_by_keywords(
        self,
        keywords: List[str],
        limit: int = 5,
        score_filter: Optional[int] = None
    ) -> str:
        """
        Retrieve context based on keywords

        Args:
            keywords: List of keywords to search
            limit: Maximum results
            score_filter: Filter by risk score

        Returns:
            Formatted context string
        """
        query = " ".join(keywords)

        results = self.retrieve_context(
            query=query,
            limit=limit,
            score_filter=score_filter,
            similarity_threshold=0.5
        )

        return self.format_context_for_llm(results)

    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base

        Returns:
            Dictionary with statistics
        """
        if not self.connected:
            return {'status': 'disconnected'}

        stats = self.db.get_statistics()
        stats['status'] = 'connected'
        stats['embedding_model'] = self.model.get_sentence_embedding_dimension()

        return stats

    def close(self):
        """Close database connection"""
        if self.db:
            self.db.disconnect()


def test_rag_retrieval():
    """Test RAG retrieval with sample queries"""
    print("\n" + "="*60)
    print("Testing RAG Retrieval")
    print("="*60 + "\n")

    # Initialize retriever
    retriever = RAGRetriever()

    if not retriever.connected:
        print("✗ Cannot test - database not connected")
        return False

    # Get statistics
    print("\n1. Knowledge Base Statistics:")
    stats = retriever.get_knowledge_base_stats()
    print(f"   Total chunks: {stats.get('total_chunks', 0)}")
    print(f"   Score distribution: {stats.get('score_distribution', {})}")

    # Test query 1: Strong cash flow examples
    print("\n2. Test Query: Strong cash flow and low leverage")
    results = retriever.retrieve_context(
        query="strong historical cash flow and low leverage",
        limit=3
    )

    if results:
        print(f"   ✓ Found {len(results)} results")
        for i, r in enumerate(results, 1):
            print(f"   {i}. {r['title']} (similarity: {r['similarity']:.3f})")
    else:
        print("   ⚠ No results found")

    # Test query 2: Risk concerns
    print("\n3. Test Query: Business risk and concerns")
    results = retriever.retrieve_context(
        query="revenue concentration risk and liquidity concerns",
        limit=3
    )

    if results:
        print(f"   ✓ Found {len(results)} results")
        for i, r in enumerate(results, 1):
            print(f"   {i}. {r['title']} (similarity: {r['similarity']:.3f})")
    else:
        print("   ⚠ No results found")

    # Test formatted context
    print("\n4. Sample Formatted Context:")
    print("="*60)
    context = retriever.format_context_for_llm(results[:1], include_metadata=True)
    print(context)

    retriever.close()

    print("\n" + "="*60)
    print("✓ RAG retrieval test complete!")
    print("="*60 + "\n")

    return True


if __name__ == "__main__":
    test_rag_retrieval()
