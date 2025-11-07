"""
Credit Memo Generator - Flask Backend Application
Orchestrates document upload, ADE extraction, financial analysis, and memo generation
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import traceback
import tempfile
from datetime import datetime

from ade_api import LandingAIClient
from bedrock_llm import BedrockLLMClient
from financial_calcs import FinancialCalculator
from word_generator import generate_credit_memo_docx

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = 'uploads'
# LandingAI ADE supported formats only (Excel not supported by ADE API)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
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
    health_status = {
        'status': 'healthy',
        'services': {
            'ade_api': ade_client is not None,
            'bedrock_llm': bedrock_client is not None and bedrock_client.bedrock_runtime is not None,
            'rag_knowledge_base': bedrock_client is not None and getattr(bedrock_client, 'rag_enabled', False)
        }
    }

    # Add RAG stats if available
    if bedrock_client and getattr(bedrock_client, 'rag_enabled', False):
        try:
            if bedrock_client.rag_retriever:
                rag_stats = bedrock_client.rag_retriever.get_knowledge_base_stats()
                health_status['rag_stats'] = {
                    'total_chunks': rag_stats.get('total_chunks', 0),
                    'score_distribution': rag_stats.get('score_distribution', {})
                }
        except:
            pass

    return jsonify(health_status)


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

        # Step 3: Generate credit memo using AWS Bedrock (with RAG if enabled)
        print("Generating credit memo with AWS Bedrock...")
        use_rag = request.form.get('use_rag', 'true').lower() == 'true'

        if bedrock_client:
            memo = bedrock_client.generate_credit_memo(
                financial_data,
                ratios,
                borrower_info,
                use_rag=use_rag
            )
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

        # Provide user-friendly error messages
        error_message = str(e)
        if '402' in error_message or 'Payment Required' in error_message or 'insufficient' in error_message.lower():
            error_message = 'LandingAI API credits exhausted. Please use the "Use Test Data" button to see a demo, or request more credits from LandingAI Discord.'
        elif '429' in error_message or 'Too Many Requests' in error_message:
            error_message = 'LandingAI API rate limit exceeded. Please wait a few minutes and try again, or use the "Use Test Data" button to see the demo.'
        elif '401' in error_message or 'Unauthorized' in error_message:
            error_message = 'LandingAI API authentication failed. Please check your API key.'
        elif '404' in error_message:
            error_message = 'LandingAI API endpoint not found. Please check the API configuration.'
        else:
            error_message = f'Error processing document: {error_message}'

        return jsonify({
            'error': error_message
        }), 500


@app.route('/upload-multiple', methods=['POST'])
def upload_multiple_documents():
    """
    Upload and process multiple financial documents

    Expected form data:
        - documents: Multiple file uploads
        - borrower_name (optional): Name of borrower
        - borrower_industry (optional): Industry of borrower

    Returns:
        JSON array with results for each document
    """
    print("=" * 60)
    print("📥 RECEIVED MULTI-FILE UPLOAD REQUEST")
    print("=" * 60)
    try:
        # Check if files are in request
        if 'documents' not in request.files:
            print("❌ No 'documents' field in request")
            return jsonify({'error': 'No documents provided'}), 400

        files = request.files.getlist('documents')
        print(f"📄 Received {len(files)} file(s)")

        if not files or len(files) == 0:
            print("❌ No files in upload")
            return jsonify({'error': 'No files selected'}), 400

        borrower_info = {
            'name': request.form.get('borrower_name', 'Unknown Borrower'),
            'industry': request.form.get('borrower_industry', 'Not specified')
        }
        print(f"👤 Borrower: {borrower_info['name']} | Industry: {borrower_info['industry']}")

        results = []

        for i, file in enumerate(files, 1):
            print(f"\n📄 Processing file {i}/{len(files)}: {file.filename}")
            if file.filename == '':
                continue

            if not allowed_file(file.filename):
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'error': f'File type not allowed'
                })
                continue

            try:
                # Save file temporarily
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                print(f"Processing document: {filename}")

                # Extract, calculate, and generate memo
                if not ade_client:
                    results.append({
                        'filename': filename,
                        'success': False,
                        'error': 'LandingAI API not configured'
                    })
                    continue

                ade_response = ade_client.extract_financials(filepath)
                financial_data = ade_client.parse_financial_data(ade_response)
                ratios = financial_calc.calculate_all_ratios(financial_data)

                if bedrock_client:
                    memo = bedrock_client.generate_credit_memo(financial_data, ratios, borrower_info)
                else:
                    memo = "AWS Bedrock not configured."

                results.append({
                    'filename': filename,
                    'success': True,
                    'borrower_info': borrower_info,
                    'financial_data': financial_data,
                    'ratios': ratios,
                    'memo': memo
                })

                # Clean up
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Warning: Could not delete temporary file: {e}")

            except Exception as e:
                print(f"Error processing {file.filename}: {e}")
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'processed': len([r for r in results if r.get('success')]),
            'failed': len([r for r in results if not r.get('success')]),
            'results': results
        })

    except Exception as e:
        print(f"Error processing multiple documents: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing documents: {str(e)}'
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

        # Generate memo (with RAG if enabled)
        # Default to False for test data to speed up demo recording
        use_rag = request.json.get('use_rag', False) if request.json else False

        if bedrock_client:
            memo = bedrock_client.generate_credit_memo(
                sample_data,
                ratios,
                borrower_info,
                use_rag=use_rag
            )
        else:
            memo = "AWS Bedrock not configured. Please set up AWS credentials to generate AI-powered memos."

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


@app.route('/download-word', methods=['POST'])
def download_word():
    """
    Generate and download Word document version of credit memo

    Expected JSON body:
        - financial_data: Dict of extracted financial data
        - ratios: Dict of calculated ratios
        - memo: Generated memo text (optional)
        - borrower_info: Dict with borrower details
    """
    try:
        data = request.get_json()

        financial_data = data.get('financial_data', {})
        ratios = data.get('ratios', {})
        memo_text = data.get('memo', '')
        borrower_info = data.get('borrower_info', {})

        # Generate safe filename
        borrower_name = borrower_info.get('name', 'credit_memo')
        safe_name = "".join(c for c in borrower_name if c.isalnum() or c in (' ', '_')).replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"credit_memo_{safe_name}_{timestamp}.docx"

        # Create temporary file
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, filename)

        # Generate Word document
        generate_credit_memo_docx(
            extracted_data=financial_data,
            ratios=ratios,
            memo_narrative=memo_text,
            borrower_info=borrower_info,
            output_filename=output_path
        )

        # Send file
        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error generating Word document: {e}")
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to generate Word document',
            'details': str(e)
        }), 500


@app.route('/test-word', methods=['GET'])
def test_word():
    """
    Test Word generation with sample data
    Generates a Word document and returns it for download
    """
    try:
        # Sample data matching the test data from word_generator.py
        test_data = {
            'financial_data': {
                'revenue': 5000000,
                'net_income': 400000,
                'ebitda': 600000,
                'total_assets': 3000000,
                'total_liabilities': 1200000,
                'current_assets': 1500000,
                'current_liabilities': 500000,
                'total_debt': 1000000,
                'interest_expense': 50000
            },
            'ratios': {
                'dscr': 1.71,
                'debt_to_ebitda': 1.67,
                'current_ratio': 3.00,
                'quick_ratio': 2.00,
                'net_income_margin': 8.0,
                'interest_coverage': 12.00,
                'leverage_ratio': 0.33,
                'working_capital': 1000000,
                'dso': 73,
                'interpretations': {
                    'dscr': 'Strong - Excellent debt coverage',
                    'debt_to_ebitda': 'Strong - Low leverage',
                    'current_ratio': 'Strong liquidity position',
                    'quick_ratio': 'Good immediate liquidity',
                    'net_income_margin': 'Moderate profitability',
                    'interest_coverage': 'Strong - Excellent coverage',
                    'leverage_ratio': 'Low leverage - Conservative',
                    'working_capital': 'Positive - Good operational liquidity',
                    'dso': 'Slow collections - Risk concern'
                }
            },
            'memo': 'Test credit memo narrative',
            'borrower_info': {
                'name': 'Test Company Inc.',
                'industry': 'Manufacturing',
                'loan_amount': 750000,
                'loan_type': 'Commercial Term Loan',
                'purpose': 'Equipment acquisition and working capital',
                'loan_officer': 'Jennifer Martinez',
                'credit_analyst': 'David Chen'
            }
        }

        # Use the download_word function logic
        borrower_name = test_data['borrower_info']['name']
        safe_name = "".join(c for c in borrower_name if c.isalnum() or c in (' ', '_')).replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_credit_memo_{safe_name}_{timestamp}.docx"

        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, filename)

        generate_credit_memo_docx(
            extracted_data=test_data['financial_data'],
            ratios=test_data['ratios'],
            memo_narrative=test_data['memo'],
            borrower_info=test_data['borrower_info'],
            output_filename=output_path
        )

        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error in test-word: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Error: {str(e)}'
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'name': 'Credit Memo Generator API',
        'version': '2.0.0',
        'status': 'running',
        'features': {
            'ade_extraction': 'LandingAI document extraction',
            'bedrock_llm': 'AWS Bedrock Claude/Sonnet models',
            'rag_knowledge_base': 'RAG-enhanced memo generation with semantic search',
            'word_export': 'Professional Word document generation'
        },
        'endpoints': {
            '/health': 'GET - Health check and service status',
            '/upload': 'POST - Upload and process financial document (supports use_rag param)',
            '/test-extraction': 'POST - Test with sample data (supports use_rag param)',
            '/download-word': 'POST - Generate and download Word document',
            '/test-word': 'GET - Test Word generation with sample data'
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
    app.run(debug=False, host='0.0.0.0', port=5001)
