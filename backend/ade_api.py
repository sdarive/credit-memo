"""
LandingAI ADE (Agentic Document Extraction) API Integration Module
Uses the official Python library for simplified, type-safe extraction
"""

import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class FinancialDataSchema(BaseModel):
    """
    Pydantic schema for extracting financial data from documents
    This provides type safety and clear field definitions for ADE extraction
    """

    # Company Information
    company_name: Optional[str] = Field(
        None,
        description="Company name, business name, or borrower name"
    )

    # Income Statement Items
    revenue: Optional[float] = Field(
        None,
        description="Total revenue, sales, or gross income for the period"
    )

    net_income: Optional[float] = Field(
        None,
        description="Net income, net profit, or bottom line profit after all expenses"
    )

    operating_income: Optional[float] = Field(
        None,
        description="Operating income or income from operations before interest and taxes"
    )

    ebit: Optional[float] = Field(
        None,
        description="EBIT - Earnings Before Interest and Taxes"
    )

    ebitda: Optional[float] = Field(
        None,
        description="EBITDA - Earnings Before Interest, Taxes, Depreciation, and Amortization"
    )

    interest_expense: Optional[float] = Field(
        None,
        description="Interest expense or interest paid on debt"
    )

    # Balance Sheet Items
    total_assets: Optional[float] = Field(
        None,
        description="Total assets on the balance sheet"
    )

    current_assets: Optional[float] = Field(
        None,
        description="Current assets - assets convertible to cash within one year"
    )

    cash_and_equivalents: Optional[float] = Field(
        None,
        description="Cash and cash equivalents"
    )

    accounts_receivable: Optional[float] = Field(
        None,
        description="Accounts receivable or trade receivables"
    )

    inventory: Optional[float] = Field(
        None,
        description="Inventory value"
    )

    total_liabilities: Optional[float] = Field(
        None,
        description="Total liabilities on the balance sheet"
    )

    current_liabilities: Optional[float] = Field(
        None,
        description="Current liabilities - liabilities due within one year"
    )

    total_debt: Optional[float] = Field(
        None,
        description="Total debt, total borrowings, or long-term debt plus short-term debt"
    )

    # Equity
    total_equity: Optional[float] = Field(
        None,
        description="Total equity, shareholders' equity, or net worth"
    )

    # Cash Flow Items
    debt_service: Optional[float] = Field(
        None,
        description="Total debt service - principal and interest payments for the period"
    )


class LandingAIClient:
    """
    Client for LandingAI Agentic Document Extraction (ADE)
    Uses the official Python library for type-safe, efficient extraction
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LandingAI client

        Args:
            api_key: LandingAI API key. If not provided, reads from LANDINGAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv('LANDINGAI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "LandingAI API key not provided. "
                "Set LANDINGAI_API_KEY environment variable or pass api_key parameter."
            )

        # Set environment variable for the library
        os.environ['VISION_AGENT_API_KEY'] = self.api_key

        # Import and initialize the library client
        try:
            from landingai_ade import LandingAIADE
            self.client = LandingAIADE()
            print("✓ LandingAI ADE Python library initialized")
        except ImportError:
            raise ImportError(
                "landingai-ade library not installed. "
                "Install it with: pip install landingai-ade"
            )

        # Store parsed results for potential re-extraction
        self._last_parse_result = None

    def extract_financials(self, file_path: str) -> Dict[str, Any]:
        """
        Extract financial data from a document using parse + extract workflow

        Args:
            file_path: Path to the financial document (PDF, Word, Excel, etc.)

        Returns:
            Dictionary containing:
                - extracted_data: Structured financial data
                - metadata: Processing metadata (credits, duration, etc.)
                - markdown: Parsed markdown (for debugging/re-extraction)
                - chunks: Parsed chunks with grounding data

        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If API call fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            print(f"📄 Processing document: {os.path.basename(file_path)}")

            # Step 1: Parse document into structured markdown
            print("  → Parsing document with LandingAI ADE...")
            with open(file_path, 'rb') as f:
                parse_result = self.client.parse(document=f)

            # Store for potential re-extraction
            self._last_parse_result = parse_result

            # Log parsing results
            page_count = getattr(parse_result.metadata, 'page_count', 'N/A')
            parse_duration = getattr(parse_result.metadata, 'duration_ms', 0)
            parse_credits = getattr(parse_result.metadata, 'credit_usage', 0)

            print(f"  ✓ Parsed {page_count} page(s) in {parse_duration}ms")
            print(f"  ✓ Parse credits used: {parse_credits}")

            # Step 2: Extract structured financial data using Pydantic schema
            print("  → Extracting financial data...")
            # Convert Pydantic schema to JSON schema string
            schema_json = json.dumps(FinancialDataSchema.model_json_schema())
            extract_result = self.client.extract(
                markdown=parse_result.markdown,
                schema=schema_json
            )

            # Log extraction results
            extract_duration = getattr(extract_result.metadata, 'duration_ms', 0)
            extract_credits = getattr(extract_result.metadata, 'credit_usage', 0)

            print(f"  ✓ Extraction completed in {extract_duration}ms")
            print(f"  ✓ Extract credits used: {extract_credits}")

            # Get extraction result (already a dict when using JSON schema)
            extracted_data = extract_result.extraction if isinstance(extract_result.extraction, dict) else extract_result.extraction.dict()

            # Count non-null fields
            extracted_fields = [k for k, v in extracted_data.items() if v is not None]
            print(f"  ✓ Extracted {len(extracted_fields)} fields: {', '.join(extracted_fields[:5])}{'...' if len(extracted_fields) > 5 else ''}")

            # Prepare complete result
            result = {
                'extracted_data': extracted_data,
                'metadata': {
                    'parse_duration_ms': parse_duration,
                    'extract_duration_ms': extract_duration,
                    'total_duration_ms': parse_duration + extract_duration,
                    'parse_credits': parse_credits,
                    'extract_credits': extract_credits,
                    'total_credits': parse_credits + extract_credits,
                    'page_count': page_count,
                    'parse_job_id': getattr(parse_result.metadata, 'job_id', None),
                    'extract_job_id': getattr(extract_result.metadata, 'job_id', None),
                    'extracted_field_count': len(extracted_fields)
                },
                'markdown': parse_result.markdown,  # Store for debugging
                'chunks': parse_result.chunks  # Store for visual grounding
            }

            return result

        except Exception as e:
            print(f"  ✗ Error during extraction: {e}")

            # Provide helpful error messages
            error_msg = str(e)
            if '401' in error_msg or 'unauthorized' in error_msg.lower():
                raise Exception(
                    "Authentication failed. Please check your LANDINGAI_API_KEY. "
                    "Get your API key at: https://va.landing.ai/settings/api-key"
                )
            elif '429' in error_msg or 'rate limit' in error_msg.lower():
                raise Exception(
                    "Rate limit exceeded. Please wait a few minutes before trying again. "
                    "Request more credits via Discord if needed."
                )
            elif '422' in error_msg:
                raise Exception(
                    "Schema validation error. The extraction schema may not match the document content."
                )
            else:
                raise Exception(f"LandingAI ADE error: {error_msg}")

    def extract_from_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Extract financial data from file bytes (useful for web uploads)

        Args:
            file_bytes: File content as bytes
            filename: Original filename (for content-type detection)

        Returns:
            Dictionary with extracted data and metadata
        """
        # Save bytes to temporary file
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        try:
            # Extract using file path
            result = self.extract_financials(temp_path)
            return result
        finally:
            # Clean up temporary file
            try:
                os.remove(temp_path)
            except:
                pass

    def parse_financial_data(self, extraction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse extraction result into format compatible with existing financial_calcs module

        Args:
            extraction_result: Result from extract_financials()

        Returns:
            Structured dictionary with financial metrics (legacy format for compatibility)
        """
        extracted = extraction_result.get('extracted_data', {})

        # Map to legacy format expected by financial_calcs.py
        parsed_data = {
            'revenue': extracted.get('revenue'),
            'net_income': extracted.get('net_income'),
            'operating_income': extracted.get('operating_income'),
            'ebit': extracted.get('ebit'),
            'ebitda': extracted.get('ebitda'),
            'total_assets': extracted.get('total_assets'),
            'total_liabilities': extracted.get('total_liabilities'),
            'total_debt': extracted.get('total_debt'),
            'total_equity': extracted.get('total_equity'),
            'current_assets': extracted.get('current_assets'),
            'current_liabilities': extracted.get('current_liabilities'),
            'cash_and_equivalents': extracted.get('cash_and_equivalents'),
            'accounts_receivable': extracted.get('accounts_receivable'),
            'inventory': extracted.get('inventory'),
            'interest_expense': extracted.get('interest_expense'),
            'debt_service': extracted.get('debt_service'),

            # Add metadata for audit trail
            'extraction_metadata': extraction_result.get('metadata'),
            'company_name': extracted.get('company_name')
        }

        return parsed_data

    def re_extract_with_custom_schema(self, custom_schema: BaseModel) -> Dict[str, Any]:
        """
        Re-extract data from last parsed document using a custom schema
        This is efficient because it reuses the parsed markdown without re-parsing

        Args:
            custom_schema: Custom Pydantic model for extraction

        Returns:
            Dictionary with newly extracted data

        Raises:
            ValueError: If no document has been parsed yet
        """
        if not self._last_parse_result:
            raise ValueError(
                "No document has been parsed yet. Call extract_financials() first."
            )

        print("  → Re-extracting with custom schema (reusing parsed markdown)...")

        # Convert Pydantic schema to JSON schema string
        schema_json = json.dumps(custom_schema.model_json_schema())
        extract_result = self.client.extract(
            markdown=self._last_parse_result.markdown,
            schema=schema_json
        )

        return extract_result.extraction if isinstance(extract_result.extraction, dict) else extract_result.extraction.dict()


def test_client():
    """Test function to verify API connectivity and library installation"""
    try:
        print("\n" + "="*60)
        print("Testing LandingAI ADE Python Library Integration")
        print("="*60 + "\n")

        # Test 1: Check environment variable
        api_key = os.getenv('LANDINGAI_API_KEY')
        if not api_key:
            print("✗ LANDINGAI_API_KEY not found in environment")
            print("  Set it with: export LANDINGAI_API_KEY=your_key_here")
            return False

        print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}")

        # Test 2: Initialize client
        client = LandingAIClient()
        print("✓ Client initialized successfully")

        # Test 3: Check for sample documents
        test_files = [
            'uploads/sample_financial_statement.pdf',
            '../datasets/Sample-Enhanced-Memo.pdf'
        ]

        test_file = None
        for f in test_files:
            if os.path.exists(f):
                test_file = f
                break

        if test_file:
            print(f"\n📄 Found test document: {test_file}")
            print("   Run with a document path to test extraction:")
            print(f"   python ade_api.py {test_file}")
        else:
            print("\n⚠ No test documents found")
            print("   Upload a financial PDF to test extraction")

        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60 + "\n")

        return True

    except ImportError as e:
        print(f"✗ Error: {e}")
        print("\n  Install the library with:")
        print("  pip install landingai-ade")
        return False
    except ValueError as e:
        print(f"✗ Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # If file path provided as argument, test extraction
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        print("\n" + "="*60)
        print(f"Testing Extraction: {os.path.basename(file_path)}")
        print("="*60 + "\n")

        try:
            client = LandingAIClient()
            result = client.extract_financials(file_path)

            print("\n" + "="*60)
            print("Extraction Results")
            print("="*60 + "\n")

            # Display extracted data
            extracted = result['extracted_data']
            print("📊 Extracted Financial Data:")
            for key, value in extracted.items():
                if value is not None:
                    if isinstance(value, float) and key != 'company_name':
                        print(f"  {key:.<30} ${value:,.2f}")
                    else:
                        print(f"  {key:.<30} {value}")

            # Display metadata
            print("\n📈 Processing Metadata:")
            metadata = result['metadata']
            print(f"  Total processing time: {metadata['total_duration_ms']}ms")
            print(f"  Total credits used: {metadata['total_credits']}")
            print(f"  Fields extracted: {metadata['extracted_field_count']}")

            # Show markdown preview (first 500 chars)
            print("\n📝 Markdown Preview:")
            markdown = result['markdown'][:500]
            print(f"  {markdown}...")

            print("\n✓ Extraction test completed successfully!")

        except Exception as e:
            print(f"\n✗ Extraction failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Run basic connectivity test
        test_client()
