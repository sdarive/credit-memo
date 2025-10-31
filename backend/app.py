"""
Credit Memo Generator - Flask Backend Application
Orchestrates document upload, ADE extraction, financial analysis, and memo generation
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import traceback

from ade_api import LandingAIClient
from bedrock_llm import BedrockLLMClient
from financial_calcs import FinancialCalculator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xlsx', 'xls', 'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize clients
try:
    ade_client = LandingAIClient()
    print("✓ LandingAI client initialized")
except ValueError as e:
    print(f"⚠ LandingAI client initialization failed: {e}")
    ade_client = None

try:
    bedrock_client = BedrockLLMClient()
    print("✓ AWS Bedrock client initialized")
except Exception as e:
    print(f"⚠ AWS Bedrock client initialization failed: {e}")
    bedrock_client = None

financial_calc = FinancialCalculator()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'ade_api': ade_client is not None,
            'bedrock_llm': bedrock_client is not None and bedrock_client.bedrock_runtime is not None
        }
    })


@app.route('/upload', methods=['POST'])
def upload_document():
    """
    Upload and process a financial document

    Expected form data:
        - document: File upload
        - borrower_name (optional): Name of borrower
        - borrower_industry (optional): Industry of borrower

    Returns:
        JSON with extracted data, calculated ratios, and generated memo
    """
    try:
        # Check if file is in request
        if 'document' not in request.files:
            return jsonify({'error': 'No document file provided'}), 400

        file = request.files['document']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        # Get optional borrower information
        borrower_info = {
            'name': request.form.get('borrower_name', 'Unknown Borrower'),
            'industry': request.form.get('borrower_industry', 'Not specified')
        }

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"Processing document: {filename}")

        # Step 1: Extract financial data using LandingAI ADE
        if not ade_client:
            return jsonify({
                'error': 'LandingAI API client not configured. Please set LANDINGAI_API_KEY environment variable.'
            }), 500

        print("Extracting data with LandingAI ADE...")
        ade_response = ade_client.extract_financials(filepath)
        financial_data = ade_client.parse_financial_data(ade_response)

        print("✓ Data extraction complete")

        # Step 2: Calculate financial ratios
        print("Calculating financial ratios...")
        ratios = financial_calc.calculate_all_ratios(financial_data)
        print("✓ Ratio calculations complete")

        # Step 3: Generate credit memo using AWS Bedrock
        print("Generating credit memo with AWS Bedrock...")
        if bedrock_client:
            memo = bedrock_client.generate_credit_memo(financial_data, ratios, borrower_info)
        else:
            memo = "AWS Bedrock not configured. Please set up AWS credentials to generate AI-powered memos."
        print("✓ Memo generation complete")

        # Clean up uploaded file
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Warning: Could not delete temporary file: {e}")

        # Return results
        return jsonify({
            'success': True,
            'borrower_info': borrower_info,
            'financial_data': financial_data,
            'ratios': ratios,
            'memo': memo,
            'filename': filename
        })

    except Exception as e:
        print(f"Error processing document: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing document: {str(e)}'
        }), 500


@app.route('/test-extraction', methods=['POST'])
def test_extraction():
    """
    Test ADE extraction with sample data (for development/testing)

    Returns:
        Mock financial data and calculated ratios
    """
    try:
        # Sample financial data for testing (includes all fields for 9 key ratios)
        sample_data = {
            'revenue': 5000000,
            'net_income': 400000,
            'operating_income': 500000,
            'ebit': 550000,
            'ebitda': 600000,
            'debt_service': 350000,
            'total_debt': 2000000,
            'total_assets': 5000000,
            'total_equity': 3000000,
            'total_liabilities': 2000000,
            'current_assets': 1500000,
            'current_liabilities': 800000,
            'inventory': 300000,
            'accounts_receivable': 400000,
            'interest_expense': 100000,
            'cash_and_equivalents': 500000
        }

        borrower_info = {
            'name': request.json.get('borrower_name', 'Test Company Inc.'),
            'industry': request.json.get('borrower_industry', 'Manufacturing')
        }

        # Calculate ratios
        ratios = financial_calc.calculate_all_ratios(sample_data)

        # Generate memo
        if bedrock_client:
            memo = bedrock_client.generate_credit_memo(sample_data, ratios, borrower_info)
        else:
            memo = bedrock_client._generate_mock_memo(sample_data, ratios, borrower_info) if bedrock_client else "Bedrock not configured"

        return jsonify({
            'success': True,
            'borrower_info': borrower_info,
            'financial_data': sample_data,
            'ratios': ratios,
            'memo': memo,
            'note': 'This is test data, not from a real document'
        })

    except Exception as e:
        print(f"Error in test extraction: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Error: {str(e)}'
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'name': 'Credit Memo Generator API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/health': 'GET - Health check',
            '/upload': 'POST - Upload and process financial document',
            '/test-extraction': 'POST - Test with sample data'
        }
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Credit Memo Generator - Backend Server")
    print("="*60)
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Max file size: {MAX_FILE_SIZE / 1024 / 1024}MB")
    print(f"Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print("="*60 + "\n")

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
