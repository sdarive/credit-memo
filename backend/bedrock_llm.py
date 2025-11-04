"""
AWS Bedrock LLM Integration Module
Handles credit memo generation using Claude/Sonnet models via AWS Bedrock
Enhanced with RAG (Retrieval-Augmented Generation) capabilities
"""

import os
import json
import boto3
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError

# Import RAG retriever (optional - gracefully handle if not available)
try:
    from rag_retrieval import RAGRetriever
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("⚠ RAG module not available - credit memos will be generated without knowledge base context")


class BedrockLLMClient:
    """Client for interacting with AWS Bedrock LLMs"""

    def __init__(self, region: Optional[str] = None, enable_rag: bool = True):
        """
        Initialize the Bedrock client

        Args:
            region: AWS region. If not provided, reads from AWS_REGION env var or defaults to us-east-1
            enable_rag: Enable RAG (Retrieval-Augmented Generation) for knowledge base context
        """
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')

        try:
            # Get credentials from environment variables
            aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

            if aws_access_key and aws_secret_key:
                # Explicitly pass credentials
                self.bedrock_runtime = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=self.region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                # Fall back to default credential chain
                self.bedrock_runtime = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=self.region
                )
            print(f"✓ AWS Bedrock client initialized in region: {self.region}")
        except NoCredentialsError:
            print("⚠ AWS credentials not configured. Please set up AWS credentials.")
            print("   Run: aws configure")
            print("   Or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
            self.bedrock_runtime = None

        # Initialize RAG retriever if available and enabled
        self.rag_retriever = None
        self.rag_enabled = enable_rag and RAG_AVAILABLE

        if self.rag_enabled:
            try:
                self.rag_retriever = RAGRetriever()
                if self.rag_retriever.connected:
                    print("✓ RAG knowledge base connected")
                else:
                    print("⚠ RAG retriever initialized but database not connected")
                    self.rag_enabled = False
            except Exception as e:
                print(f"⚠ RAG initialization failed: {e}")
                self.rag_enabled = False

    def generate_credit_memo(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, Any],
        borrower_info: Optional[Dict[str, str]] = None,
        use_rag: bool = True
    ) -> str:
        """
        Generate a credit memo narrative using AWS Bedrock LLM
        Enhanced with RAG for knowledge base context

        Args:
            financial_data: Extracted financial metrics from documents
            ratios: Calculated financial ratios (DSCR, leverage, etc.)
            borrower_info: Optional borrower information (name, industry, etc.)
            use_rag: Use RAG to retrieve similar examples from knowledge base

        Returns:
            Generated credit memo text

        Raises:
            Exception: If Bedrock API call fails
        """
        if not self.bedrock_runtime:
            return self._generate_mock_memo(financial_data, ratios, borrower_info)

        # Retrieve RAG context if enabled
        rag_context = None
        if use_rag and self.rag_enabled and self.rag_retriever:
            try:
                print("  Retrieving similar credit memos from knowledge base...")
                rag_context = self.rag_retriever.retrieve_similar_memos(
                    financial_data=financial_data,
                    ratios=ratios,
                    borrower_info=borrower_info or {},
                    limit=3
                )
            except Exception as e:
                print(f"  ⚠ RAG retrieval failed: {e}")
                rag_context = None

        # Prepare prompt for credit memo generation
        prompt = self._create_memo_prompt(financial_data, ratios, borrower_info, rag_context)

        # Use Claude 4.5 Haiku model via US cross-region inference profile
        model_id = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

        try:
            # Prepare request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            }

            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body)
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            memo_text = response_body['content'][0]['text']

            return memo_text

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"AWS Bedrock Error [{error_code}]: {error_message}")

            # Return mock memo on error
            return self._generate_mock_memo(financial_data, ratios, borrower_info)

        except Exception as e:
            print(f"Error generating memo: {e}")
            return self._generate_mock_memo(financial_data, ratios, borrower_info)

    def _create_memo_prompt(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, Any],
        borrower_info: Optional[Dict[str, str]],
        rag_context: Optional[str] = None
    ) -> str:
        """Create the prompt for credit memo generation with optional RAG context"""

        borrower_name = borrower_info.get('name', 'the borrower') if borrower_info else 'the borrower'
        borrower_industry = borrower_info.get('industry', 'their industry') if borrower_info else 'their industry'

        # Build prompt with RAG context if available
        rag_section = ""
        if rag_context:
            rag_section = f"""

KNOWLEDGE BASE CONTEXT (Similar Credit Memos):
The following are examples of similar credit memos from our knowledge base. Use these as references for style, structure, and analysis approach, but tailor your analysis to the specific borrower's financial data.

{rag_context}

---

"""

        prompt = f"""You are an experienced credit analyst preparing a credit memo for loan underwriting at a commercial bank.

IMPORTANT: This memo must follow the bank's approved template structure and be grounded in the extracted financial data provided below. Each assertion should reference specific data points for audit trail and regulatory compliance.
{rag_section}
BORROWER INFORMATION:
- Name: {borrower_name}
- Industry: {borrower_industry}

EXTRACTED FINANCIAL DATA (from uploaded documents):
{json.dumps(financial_data, indent=2)}

CALCULATED CREDIT RATIOS:
{json.dumps(ratios, indent=2)}

TEMPLATE STRUCTURE:
Generate a comprehensive credit memo following this bank-approved template, adhering to the "5 Cs of Credit" framework (Character, Capacity, Capital, Collateral, Conditions):

1. EXECUTIVE SUMMARY
   - Borrower overview and industry context
   - Loan request summary (note: specific loan details to be added by analyst)
   - Key credit strengths (2-3 bullets with specific metrics)
   - Primary concerns (2-3 bullets with specific metrics)
   - Preliminary recommendation with conditions

2. FINANCIAL ANALYSIS (CAPACITY & CAPITAL)
   - Revenue trends and profitability metrics (cite specific figures from financial data)
   - Asset composition and quality (reference balance sheet data)
   - Liability structure and debt levels (reference extracted debt figures)
   - Cash flow adequacy (reference operating income and cash positions)

3. CREDIT RISK ASSESSMENT
   - **Debt Service Coverage**: Analyze DSCR of {ratios.get('dscr', 'N/A')} against benchmark of 1.25+
   - **Leverage Analysis**: Analyze Debt/EBITDA of {ratios.get('debt_to_ebitda', 'N/A')} and Leverage Ratio of {ratios.get('leverage_ratio', 'N/A')}
   - **Liquidity Position**: Analyze Current Ratio of {ratios.get('current_ratio', 'N/A')} and Quick Ratio of {ratios.get('quick_ratio', 'N/A')}
   - **Profitability**: Analyze Net Income Margin of {ratios.get('net_income_margin', 'N/A')}%
   - **Risk Factors**: Identify specific concerns from the data

4. STRENGTHS (CHARACTER, CAPACITY, CAPITAL)
   - List 3-5 positive credit factors with specific supporting data
   - Reference actual financial metrics and ratios
   - Industry position and competitive advantages

5. CONCERNS & RISK MITIGANTS (CONDITIONS)
   - List 3-5 areas of concern with specific data points
   - Suggested covenants or monitoring requirements
   - Required additional documentation or due diligence

6. RECOMMENDATION
   - Preliminary credit decision (Approve with Conditions / Needs Further Review / Decline)
   - Suggested loan terms and structure (to be finalized by credit committee)
   - Required conditions precedent
   - Ongoing monitoring requirements

FORMATTING REQUIREMENTS:
- Use professional banking terminology
- Cite specific numbers and data points (e.g., "Revenue of ${financial_data.get('revenue', 'N/A'):,}")
- Include ratio values with interpretations (e.g., "DSCR of X indicates [strong/adequate/weak] debt service capability")
- Maintain objective, analytical tone suitable for credit committee review
- Note data sources as "per uploaded financial documents" for audit trail
- Flag any missing critical data points that require follow-up

Write a complete, actionable credit memo that a loan officer can review, edit, and present to the credit committee."""

        return prompt

    def _generate_mock_memo(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, Any],
        borrower_info: Optional[Dict[str, str]]
    ) -> str:
        """Generate a mock credit memo when AWS Bedrock is not available"""

        borrower_name = borrower_info.get('name', 'ABC Corporation') if borrower_info else 'ABC Corporation'
        borrower_industry = borrower_info.get('industry', 'Not specified') if borrower_info else 'Not specified'

        # Format numbers safely
        def format_currency(value):
            if value is None or value == 'N/A':
                return 'N/A'
            if isinstance(value, (int, float)):
                return f"${value:,.0f}"
            return str(value)

        def format_ratio(ratio_value, ratio_name=None):
            if ratio_value is None or ratio_value == 'N/A':
                return 'N/A'
            if isinstance(ratio_value, (int, float)):
                formatted = f"{ratio_value:.2f}"
                # Add interpretation if available
                if ratio_name and isinstance(ratios.get('interpretations'), dict):
                    interpretation = ratios.get('interpretations', {}).get(ratio_name)
                    if interpretation:
                        return f"{formatted} ({interpretation})"
                return formatted
            return str(ratio_value)

        memo = f"""CREDIT MEMO - {borrower_name}
[MOCK TEMPLATE - Configure AWS Bedrock for AI-generated analysis]

════════════════════════════════════════════════════════════════════════

1. EXECUTIVE SUMMARY

Borrower: {borrower_name}
Industry: {borrower_industry}
Date: [Current Date]

This credit memo analyzes the creditworthiness of {borrower_name} based on financial documents uploaded to the system.

Key Strengths:
• Revenue base of {format_currency(financial_data.get('revenue', 'N/A'))} per uploaded financial statements
• Total assets of {format_currency(financial_data.get('total_assets', 'N/A'))} providing collateral capacity
• [Additional strengths would be identified by AI analysis]

Primary Concerns:
• Total debt of {format_currency(financial_data.get('total_debt', 'N/A'))} requires debt service analysis
• [Additional concerns would be identified by AI analysis]

Preliminary Recommendation: Subject to further due diligence and credit committee review

════════════════════════════════════════════════════════════════════════

2. FINANCIAL ANALYSIS (CAPACITY & CAPITAL)

Revenue & Profitability (per uploaded documents):
- Total Revenue: {format_currency(financial_data.get('revenue', 'N/A'))}
- Net Income: {format_currency(financial_data.get('net_income', 'N/A'))}
- Operating Income: {format_currency(financial_data.get('operating_income', 'N/A'))}
- EBITDA: {format_currency(financial_data.get('ebitda', 'N/A'))}

Balance Sheet Position:
- Total Assets: {format_currency(financial_data.get('total_assets', 'N/A'))}
- Current Assets: {format_currency(financial_data.get('current_assets', 'N/A'))}
- Total Liabilities: {format_currency(financial_data.get('total_liabilities', 'N/A'))}
- Total Equity: {format_currency(financial_data.get('total_equity', 'N/A'))}

[AI would provide trend analysis and industry comparison here]

════════════════════════════════════════════════════════════════════════

3. CREDIT RISK ASSESSMENT

Debt Service Coverage: DSCR = {format_ratio(ratios.get('dscr'), 'dscr')}
- Benchmark: 1.25+ considered healthy
- [AI analysis of debt service capability]

Leverage Analysis:
- Debt to EBITDA: {format_ratio(ratios.get('debt_to_ebitda'), 'debt_to_ebitda')} (Target: ≤2.0)
- Leverage Ratio: {format_ratio(ratios.get('leverage_ratio'), 'leverage_ratio')} (Target: ≤0.3)
- [AI analysis of leverage position]

Liquidity Position:
- Current Ratio: {format_ratio(ratios.get('current_ratio'), 'current_ratio')} (Target: ≥2.0)
- Quick Ratio: {format_ratio(ratios.get('quick_ratio'), 'quick_ratio')} (Target: ≥1.0)
- Working Capital: {format_currency(ratios.get('working_capital'))}

Profitability Metrics:
- Net Income Margin: {format_ratio(ratios.get('net_income_margin'), 'net_income_margin')} (Target: ≥10%)
- Interest Coverage: {format_ratio(ratios.get('interest_coverage'), 'interest_coverage')} (Target: ≥3.0)

════════════════════════════════════════════════════════════════════════

4. STRENGTHS (5 Cs: CHARACTER, CAPACITY, CAPITAL)

[AI would identify specific strengths with supporting data:]
• Financial strength indicators from uploaded documents
• Positive ratio performance in key areas
• Industry position and competitive advantages
• Management capability and track record

════════════════════════════════════════════════════════════════════════

5. CONCERNS & RISK MITIGANTS (CONDITIONS)

[AI would identify specific concerns with supporting data:]
• Areas requiring attention based on ratio analysis
• Missing financial documentation requiring follow-up
• Industry or market condition risks
• Suggested loan covenants and monitoring requirements

════════════════════════════════════════════════════════════════════════

6. RECOMMENDATION

Preliminary Credit Decision: [To be determined by AI analysis]

Suggested Conditions:
• [AI would suggest specific loan conditions and covenants]
• Quarterly financial reporting requirements
• Ongoing monitoring of key financial ratios

Required Documentation:
• [AI would flag missing critical documents]

════════════════════════════════════════════════════════════════════════

NOTE: This is a template-based mock memo. Configure AWS Bedrock credentials to generate comprehensive AI-powered credit analysis with detailed narrative, industry insights, and specific recommendations.

Data Source: Per uploaded financial documents (audit trail available)
Generated: Automated Credit Memo Generator v1.0
"""
        return memo


    def cleanup(self):
        """Cleanup resources (close RAG connections)"""
        if self.rag_retriever:
            try:
                self.rag_retriever.close()
            except:
                pass


def test_client():
    """Test function to verify Bedrock connectivity and RAG integration"""
    try:
        print("\n" + "="*60)
        print("Testing AWS Bedrock Client with RAG")
        print("="*60 + "\n")

        client = BedrockLLMClient()

        print("\n1. Bedrock Runtime Status:")
        if client.bedrock_runtime:
            print("   ✓ AWS Bedrock client ready")
        else:
            print("   ⚠ AWS Bedrock client initialized but credentials not configured")

        print("\n2. RAG Status:")
        if client.rag_enabled:
            print("   ✓ RAG knowledge base enabled and connected")

            # Get knowledge base stats
            if client.rag_retriever:
                stats = client.rag_retriever.get_knowledge_base_stats()
                print(f"   Total chunks in KB: {stats.get('total_chunks', 'N/A')}")
        else:
            print("   ⚠ RAG not available (database not connected or module not installed)")

        client.cleanup()

        print("\n" + "="*60)
        print("✓ Test complete!")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    test_client()
