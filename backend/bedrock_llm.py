"""
AWS Bedrock LLM Integration Module
Handles credit memo generation using Claude/Sonnet models via AWS Bedrock
"""

import os
import json
import boto3
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockLLMClient:
    """Client for interacting with AWS Bedrock LLMs"""

    def __init__(self, region: Optional[str] = None):
        """
        Initialize the Bedrock client

        Args:
            region: AWS region. If not provided, reads from AWS_REGION env var or defaults to us-east-1
        """
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')

        try:
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

    def generate_credit_memo(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, Any],
        borrower_info: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generate a credit memo narrative using AWS Bedrock LLM

        Args:
            financial_data: Extracted financial metrics from documents
            ratios: Calculated financial ratios (DSCR, leverage, etc.)
            borrower_info: Optional borrower information (name, industry, etc.)

        Returns:
            Generated credit memo text

        Raises:
            Exception: If Bedrock API call fails
        """
        if not self.bedrock_runtime:
            return self._generate_mock_memo(financial_data, ratios, borrower_info)

        # Prepare prompt for credit memo generation
        prompt = self._create_memo_prompt(financial_data, ratios, borrower_info)

        # Use Claude 3 Sonnet model
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

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
                "temperature": 0.7,
                "top_p": 0.9
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
        borrower_info: Optional[Dict[str, str]]
    ) -> str:
        """Create the prompt for credit memo generation"""

        borrower_name = borrower_info.get('name', 'the borrower') if borrower_info else 'the borrower'
        borrower_industry = borrower_info.get('industry', 'their industry') if borrower_info else 'their industry'

        prompt = f"""You are an experienced credit analyst preparing a credit memo for loan underwriting.

Based on the following financial information, write a comprehensive credit memo analyzing the creditworthiness of {borrower_name} operating in {borrower_industry}.

FINANCIAL DATA:
{json.dumps(financial_data, indent=2)}

CALCULATED RATIOS:
{json.dumps(ratios, indent=2)}

Please structure the credit memo with the following sections:

1. EXECUTIVE SUMMARY
   - Brief overview of the borrower and loan request
   - Key strengths and concerns
   - Recommendation (subject to further due diligence)

2. FINANCIAL ANALYSIS
   - Revenue and profitability trends
   - Asset and liability composition
   - Cash flow analysis

3. RISK ASSESSMENT
   - Debt Service Coverage Ratio (DSCR) analysis
   - Leverage analysis
   - Liquidity analysis
   - Key risk factors

4. STRENGTHS
   - Positive factors supporting creditworthiness

5. CONCERNS
   - Risk factors and areas requiring attention

6. RECOMMENDATION
   - Preliminary lending recommendation with conditions

Write in a professional, analytical tone appropriate for bank credit committee review. Be specific and reference the actual numbers provided."""

        return prompt

    def _generate_mock_memo(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, Any],
        borrower_info: Optional[Dict[str, str]]
    ) -> str:
        """Generate a mock credit memo when AWS Bedrock is not available"""

        borrower_name = borrower_info.get('name', 'ABC Corporation') if borrower_info else 'ABC Corporation'

        memo = f"""CREDIT MEMO - {borrower_name}
[MOCK MEMO - AWS Bedrock credentials not configured]

EXECUTIVE SUMMARY
This credit memo provides an analysis of {borrower_name}'s financial position based on the provided financial statements.

FINANCIAL HIGHLIGHTS:
- Revenue: {financial_data.get('revenue', 'N/A')}
- Net Income: {financial_data.get('net_income', 'N/A')}
- Total Assets: {financial_data.get('total_assets', 'N/A')}
- Total Debt: {financial_data.get('total_debt', 'N/A')}

KEY RATIOS:
- DSCR: {ratios.get('dscr', 'N/A')}
- Leverage Ratio: {ratios.get('leverage_ratio', 'N/A')}
- Current Ratio: {ratios.get('current_ratio', 'N/A')}
- Quick Ratio: {ratios.get('quick_ratio', 'N/A')}

RISK ASSESSMENT:
[Detailed analysis would be generated by AWS Bedrock Claude model]

RECOMMENDATION:
[Lending recommendation would be generated based on comprehensive financial analysis]

---
Note: This is a mock memo. Configure AWS Bedrock credentials to generate AI-powered credit memos.
"""
        return memo


def test_client():
    """Test function to verify Bedrock connectivity"""
    try:
        client = BedrockLLMClient()
        if client.bedrock_runtime:
            print("✓ AWS Bedrock client ready")
            return True
        else:
            print("⚠ AWS Bedrock client initialized but credentials not configured")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    test_client()
