# Credit Memo Generator

**Automated credit analysis powered by LandingAI's ADE API and AWS Bedrock**

Built for the LandingAI Financial AI Hackathon Championship 2025

---

## Overview

An intelligent financial agent that automates credit memo generation for bank loan underwriting. The system combines:
- **LandingAI's Agentic Document Extraction (ADE)** for parsing financial documents
- **AWS Bedrock** (Claude/Sonnet models) for generating narrative credit analysis
- **Advanced financial ratio calculations** for credit risk assessment

### Features

- Upload borrower financial documents (PDF, Word, Excel, CSV)
- AI-powered document parsing and data extraction
- Automatic calculation of 9 key credit analysis ratios:
  1. Debt Service Coverage Ratio (DSCR)
  2. Total Debt to EBITDA
  3. Current Ratio
  4. Quick Ratio (Acid Test)
  5. Net Income Margin
  6. Interest Coverage Ratio
  7. Leverage Ratio
  8. Working Capital
  9. Days Sales Outstanding (DSO)
- AI-generated credit memo narratives
- Interactive results dashboard with visual ratio indicators
- Editable, downloadable credit memos

---

## Tech Stack

**Backend:**
- Flask (Python REST API)
- LandingAI ADE API
- AWS Bedrock (Claude/Sonnet models)
- Python financial calculations module

**Frontend:**
- React
- Modern responsive UI
- Real-time document processing

**Data:**
- HuggingFace public financial datasets for testing and validation

---

## Project Structure

```
landing-ai-hackathon/
├── backend/
│   ├── app.py                 # Flask REST API
│   ├── ade_api.py            # LandingAI ADE integration
│   ├── bedrock_llm.py        # AWS Bedrock LLM integration
│   ├── financial_calcs.py    # Financial ratio calculations
│   ├── requirements.txt       # Python dependencies
│   └── uploads/              # Temporary file storage
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Upload.js     # Document upload component
│   │   │   ├── Results.js    # Financial dashboard
│   │   │   └── MemoEditor.js # Memo viewer/editor
│   │   ├── App.js            # Main application
│   │   └── App.css
│   ├── package.json
│   └── public/
├── datasets/
│   └── financial_datasets_exploration.ipynb
├── .env                      # Environment variables (API keys)
├── .env.example              # Template for environment variables
├── CLAUDE.md                 # Development guide
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- LandingAI account with ADE API key
- AWS account with Bedrock access (optional, has fallback mode)

### 1. Clone and Navigate

```bash
cd landing-ai-hackathon
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start the React development server
npm start
```

The frontend will open automatically at `http://localhost:3000`

### 4. Configure API Keys

Your LandingAI API key is already configured in `.env`.

For AWS Bedrock (optional but recommended):
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

---

## Usage

### Basic Workflow

1. **Open the application** at `http://localhost:3000`

2. **Enter borrower information** (optional):
   - Borrower name
   - Industry

3. **Upload a financial document**:
   - Supported formats: PDF, Word (.doc, .docx), Excel (.xlsx, .xls), CSV
   - Max file size: 16MB

4. **Or use test data**:
   - Click "Use Test Data" to see the system in action with sample financial data

5. **View results**:
   - Financial data extracted by LandingAI ADE
   - 9 calculated credit ratios with interpretations
   - Color-coded ratio indicators (green/yellow/red)

6. **Review credit memo**:
   - AI-generated narrative credit analysis
   - Edit the memo if needed
   - Download as text file or copy to clipboard

### API Endpoints

**Backend API** (`http://localhost:5000`):

- `GET /health` - Health check and service status
- `POST /upload` - Upload and process financial document
  - Form data: `document` (file), `borrower_name` (optional), `borrower_industry` (optional)
- `POST /test-extraction` - Test with sample data
  - JSON: `{"borrower_name": "...", "borrower_industry": "..."}`

---

## Financial Ratios Explained

### 1. Debt Service Coverage Ratio (DSCR)
- **Formula**: Net Operating Income / Total Debt Service
- **Interpretation**: Ability to cover debt payments from operating income
- **Healthy**: ≥ 1.25

### 2. Total Debt to EBITDA
- **Formula**: Total Debt / EBITDA
- **Interpretation**: Leverage and repayment capacity
- **Healthy**: ≤ 2.0

### 3. Current Ratio
- **Formula**: Current Assets / Current Liabilities
- **Interpretation**: Short-term liquidity
- **Healthy**: ≥ 2.0

### 4. Quick Ratio (Acid Test)
- **Formula**: (Current Assets - Inventory) / Current Liabilities
- **Interpretation**: Immediate liquidity without inventory
- **Healthy**: ≥ 1.0

### 5. Net Income Margin
- **Formula**: (Net Income / Sales) × 100
- **Interpretation**: Profitability
- **Healthy**: ≥ 10%

### 6. Interest Coverage Ratio
- **Formula**: EBIT / Interest Expense
- **Interpretation**: Ability to pay interest on debt
- **Healthy**: ≥ 3.0

### 7. Leverage Ratio
- **Formula**: Total Debt / Total Assets
- **Interpretation**: Proportion of debt in capital structure
- **Healthy**: ≤ 0.3

### 8. Working Capital
- **Formula**: Current Assets - Current Liabilities
- **Interpretation**: Liquidity for daily operations
- **Healthy**: Positive value

### 9. Days Sales Outstanding (DSO)
- **Formula**: (Accounts Receivable / Total Credit Sales) × 365
- **Interpretation**: Efficiency in collecting receivables
- **Healthy**: ≤ 45 days

---

## Development

### Running Tests

Test the financial calculator:
```bash
cd backend
python financial_calcs.py
```

Test LandingAI ADE connectivity:
```bash
python ade_api.py
```

Test AWS Bedrock connectivity:
```bash
python bedrock_llm.py
```

### Exploring Datasets

Open the Jupyter notebook:
```bash
cd datasets
jupyter notebook financial_datasets_exploration.ipynb
```

---

## Hackathon Requirements

### Mandatory Components ✓
- [x] **LandingAI ADE API integration** - Required for document extraction
- [x] **LLM integration** - AWS Bedrock with Claude/Sonnet models
- [x] **Intelligent agentic analysis** - Multi-step workflow: extraction → calculation → memo generation

### Judging Criteria Focus
- **Problem clarity**: Clear focus on credit memo automation for lending
- **ADE integration depth**: Comprehensive financial data extraction
- **Accuracy**: 9 standard credit analysis ratios with interpretations
- **Usability**: Clean, professional UI with editing capabilities
- **Feasibility**: Production-ready architecture, 90-day pilot path ready

---

## Demo Preparation

For the 4-minute demo on November 15:

1. **Show document upload** (10 sec)
2. **Demonstrate AI extraction** (30 sec)
3. **Highlight 9 calculated ratios** with visual indicators (45 sec)
4. **Show AI-generated credit memo** (45 sec)
5. **Demonstrate editing and download** (30 sec)
6. **Explain architecture** and production readiness (60 sec)

---

## Troubleshooting

### Backend Issues

**LandingAI API errors:**
- Check API key in `.env` file
- Verify account has remaining credits at https://va.landing.ai
- Request additional credits via Discord if needed

**AWS Bedrock errors:**
- Verify AWS credentials: `aws configure list`
- Check Bedrock is enabled in your region
- System will use mock memos if Bedrock is unavailable

**Port already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 5000
- Check CORS is enabled (flask-cors installed)
- Clear browser cache

**Module not found:**
```bash
cd frontend
npm install
```

---

## Resources

- **LandingAI ADE Playground**: https://va.landing.ai/my/playground/ade
- **AWS Bedrock Docs**: https://docs.aws.amazon.com/bedrock/
- **Hackathon Discord**: https://discord.gg/ySHxDU7Brd
- **HuggingFace Datasets**:
  - AdaptLLM/finance-tasks
  - gbharti/finance-alpaca
  - PatronusAI/financebench
  - JanosAudran/financial-reports-sec

---

## License

Built for the LandingAI Financial AI Hackathon Championship 2025

---

## Next Steps

### Before Submission (Nov 10, 11:59 PM ET)

- [ ] Test with real financial documents
- [ ] Verify AWS Bedrock integration with your credentials
- [ ] Record 4-minute demo video
- [ ] Submit via Google Form: https://forms.gle/q682wg7ZWLnNUqQL6

### For Production

- [ ] Add user authentication
- [ ] Implement data persistence (database)
- [ ] Add batch processing for multiple documents
- [ ] Create audit trail for compliance
- [ ] Add more comprehensive error handling
- [ ] Implement caching for repeated analyses
- [ ] Add export to PDF format
- [ ] Deploy to cloud infrastructure (AWS/GCP)

---

**Questions or issues?** Check the hackathon Discord or review CLAUDE.md for development guidance.
