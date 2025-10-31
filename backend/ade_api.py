"""
LandingAI ADE (Agentic Document Extraction) API Integration Module
Handles document upload and extraction of financial data
"""

import os
import requests
from typing import Dict, Any, Optional
import json


class LandingAIClient:
    """Client for interacting with LandingAI's ADE API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LandingAI client

        Args:
            api_key: LandingAI API key. If not provided, reads from LANDINGAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv('LANDINGAI_API_KEY')
        if not self.api_key:
            raise ValueError("LandingAI API key not provided. Set LANDINGAI_API_KEY environment variable.")

        self.base_url = "https://va.landing.ai/api/ade"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def extract_financials(self, file_path: str) -> Dict[str, Any]:
        """
        Extract financial data from a document using LandingAI ADE

        Args:
            file_path: Path to the financial document (PDF, Word, Excel, etc.)

        Returns:
            Dictionary containing extracted financial data and metadata

        Raises:
            requests.exceptions.RequestException: If API call fails
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'rb') as file:
                files = {'document': file}
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    files=files,
                    timeout=60  # 60 second timeout for large documents
                )

                response.raise_for_status()
                return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error calling LandingAI API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def extract_from_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Extract financial data from file bytes (useful for web uploads)

        Args:
            file_bytes: File content as bytes
            filename: Original filename (for content-type detection)

        Returns:
            Dictionary containing extracted financial data and metadata
        """
        try:
            files = {'document': (filename, file_bytes)}
            response = requests.post(
                self.base_url,
                headers=self.headers,
                files=files,
                timeout=60
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error calling LandingAI API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def parse_financial_data(self, ade_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse ADE response to extract key financial metrics

        Args:
            ade_response: Raw response from ADE API

        Returns:
            Structured dictionary with financial metrics
        """
        # This will need to be customized based on actual ADE response format
        # Placeholder implementation
        parsed_data = {
            'revenue': None,
            'net_income': None,
            'total_assets': None,
            'total_liabilities': None,
            'total_debt': None,
            'cash_and_equivalents': None,
            'operating_income': None,
            'debt_service': None,
            'raw_data': ade_response
        }

        # TODO: Add logic to extract specific fields from ADE response
        # This will depend on the structure of documents and ADE's output format

        return parsed_data


def test_client():
    """Test function to verify API connectivity"""
    try:
        client = LandingAIClient()
        print("✓ LandingAI client initialized successfully")
        print(f"✓ API endpoint: {client.base_url}")
        return True
    except ValueError as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    test_client()
