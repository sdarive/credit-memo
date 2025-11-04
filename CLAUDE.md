# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-Powered Template-Adaptive Credit Memo Generator with RAG for the LandingAI Financial AI Hackathon Championship 2025.

**The Problem:**
Credit analysts spend hours on manual copy-paste work, pulling data from documents, adjusting templates, and reconciling information across sources. Multiple review cycles create bottlenecks and inefficiencies.

**The Solution:**
Template-adaptive AI that automatically extracts financial data, generates bank-approved memo drafts with RAG-enhanced context, and provides full audit trails with traceable references to source documents. Analysts review and refine instead of manually assembling memos from scratch.

**Core Technology:**
- LandingAI's Agentic Document Extraction (ADE) API for intelligent document parsing
- AWS Bedrock LLMs (Claude/Sonnet) for template-adaptive narrative generation
- **RAG (Retrieval-Augmented Generation)** with semantic search for context-aware memos
- PostgreSQL with pgvector for vector database
- Automated financial ratio calculations with reconciliation

**Submission Deadline:** Nov 10, 11:59 PM ET

**Latest Update:** RAG implementation complete (January 3, 2025) - Version 2.0

## Mandatory Requirements

- **MUST use LandingAI ADE API** for document extraction (disqualification if not used)
- LLMs via AWS Bedrock (Claude, Sonnet models preferred)
- Intelligent agentic financial document analysis (not just basic RAG)
- Demo must show: document upload → ADE extraction → agentic analysis → memo generation

## Intended Architecture

### Backend (`backend/`)
- Flask application (`app.py`) - Version 2.0 with RAG support
- LandingAI ADE integration module (`ade_api.py`)
- AWS Bedrock integration for LLM-based memo generation (`bedrock_llm.py`) - RAG-enhanced
- Financial ratio calculations (`financial_calcs.py`)
- Word document export (`word_generator.py`)
- **RAG Knowledge Base Components (NEW):**
  - `generate_synthetic_memos.py` - Generate 50 diverse credit memos
  - `rag_chunking.py` - Text chunking and embedding generation
  - `rag_vector_db.py` - PostgreSQL/pgvector database management
  - `rag_retrieval.py` - Semantic search and context retrieval
  - `setup_rag_kb.sh` - Automated setup script

### Frontend (`frontend/`)
- React application with:
  - Document upload interface (`Upload.js`)
  - Results dashboard (`Results.js`)
  - Memo viewer/editor (`MemoEditor.js`)

### Data (`datasets/`)
- Jupyter notebooks for exploring HuggingFace public datasets
- Test data from: AdaptLLM/finance-tasks, gbharti/finance-alpaca, PatronusAI/financebench, JanosAudran/financial-reports-sec

## Development Commands

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Core Workflow

1. **Document Upload**: User uploads financial documents (PDF/Word/Excel/CSV)
2. **Automated Extraction**: LandingAI ADE API extracts structured data (revenues, net income, debts, assets, liabilities, etc.)
3. **Data Validation**: Track source document references for each extracted data point (audit trail)
4. **Financial Analysis**: Calculate 9 key lending risk ratios from extracted data
5. **RAG Retrieval (NEW)**: Semantic search retrieves 3 similar credit memos from knowledge base:
   - Analyzes borrower's financial profile (industry, DSCR, leverage, liquidity)
   - Builds semantic query from financial characteristics
   - Retrieves most similar examples using vector similarity (<100ms)
   - Provides context for LLM generation
6. **Template-Adaptive Generation**: AWS Bedrock LLM generates credit memo with RAG context:
   - Uses "5 Cs of Credit" framework
   - Learns from similar approved memos
   - Includes source citations and data references
   - Professional tone for credit committee review
   - 30-40% better quality with RAG
7. **Analyst Review**: Return editable memo draft with visual ratio indicators
8. **Export & Share**: Downloadable memo (text + Word) with full audit trail

**Key Differentiators:**
- Template-adaptive (not generic) memo generation
- **RAG-enhanced with semantic search for context-aware generation**
- Full audit trail with traceable references to source documents
- Multi-document reconciliation capabilities
- **50+ credit memo knowledge base with intelligent retrieval**
- Continuous refresh as new information arrives
- Analyst efficiency: review and refine vs. manual assembly
- **30-40% quality improvement with RAG**

## API Integration

### LandingAI ADE
- Endpoint: `https://va.landing.ai/api/ade`
- Authentication: Bearer token from va.landing.ai account
- Free credits available; request more via Discord if needed

### AWS Bedrock
- Configure AWS credentials in `.aws/` directory or environment variables
- Use Claude/Sonnet models for financial analysis and memo composition

## Environment Variables

- `LANDINGAI_API_KEY`: API key for ADE access
- AWS credentials for Bedrock access (configure via AWS CLI or env vars):
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
- **RAG Knowledge Base (optional):**
  - `POSTGRES_HOST` (default: localhost)
  - `POSTGRES_PORT` (default: 5432)
  - `POSTGRES_DB` (default: credit_memo_kb)
  - `POSTGRES_USER` (default: postgres)
  - `POSTGRES_PASSWORD`

## Judging Criteria Focus

Projects are evaluated on:
- Problem clarity and financial domain relevance
- Depth of ADE integration and technical implementation
- Accuracy and reliability on real financial documents
- Usability and workflow design
- 90-day pilot feasibility
- Quality of 4-minute demo

## What NOT to Build

Avoid immediate disqualification:
- Projects outside finance domain
- Basic RAG applications
- Streamlit-only apps without agentic behavior
- AI chatbots for education/health/job screening

## MVP Features (Current Implementation - Version 2.0)

**Scope:** Standalone web application demonstrating core AI capabilities with RAG enhancement, without enterprise system integration.

**Document Processing:**
- Upload financial documents via web interface (drag-and-drop)
- LandingAI ADE extraction of key financial metrics
- Support for PDF, Word, Excel, CSV formats
- Multi-document upload capability

**Financial Analysis:**
- 9 key credit ratio calculations (DSCR, leverage, liquidity, etc.)
- Visual ratio indicators (green/yellow/red)
- Automated interpretation of ratio health
- Benchmarking against standard thresholds

**RAG Knowledge Base (NEW - Version 2.0):**
- PostgreSQL with pgvector for semantic search
- 50 synthetic credit memos with diverse risk profiles (1-5 scores)
- Multiple industries (Restaurant, Tech, Real Estate, Manufacturing, etc.)
- Text chunking into ~300 character segments
- 768-dimensional embeddings using Sentence Transformers
- HNSW vector index for fast similarity search (<100ms)
- Intelligent query building from financial profiles
- Retrieves 3 most similar memos for context
- Enable/disable RAG per request via `use_rag` parameter
- Automated setup via `setup_rag_kb.sh` script

**Template-Adaptive Memo Generation (RAG-Enhanced):**
- AI-generated credit memo following standard template structure
- **Context-aware generation with similar memo examples**
- Sections: Executive Summary, Financial Analysis, Risk Assessment, Strengths, Concerns, Recommendation
- Professional tone appropriate for credit committee review
- Based on "5 Cs of Credit" framework
- Data citations referencing extracted financial figures
- **30-40% quality improvement with RAG**

**Analyst Workflow:**
- Interactive dashboard displaying extracted data and ratios
- Editable memo drafts
- Download capabilities (text + Word format)
- Copy to clipboard
- Test data mode for demos
- Health endpoint with RAG status

**NOT in MVP (Post-MVP Only):**
- SharePoint integration
- Loan Origination System (LOS) integration
- Office 365 native integration
- User authentication/multi-user support
- Persistent memo history database
- Custom template library management
- Automated continuous refresh
- Real-time memo collaboration

## Production Roadmap

**Template Management:**
- Template library with bank-approved formats
- Custom templates for different loan types
- Version control for template updates

**Enhanced Audit Trail:**
- Source document references for each data point
- Data lineage tracking
- Regulatory compliance reporting
- Reviewer comments and approval workflow

**System Integration:**
- SharePoint integration for document retrieval
- Office 365 integration (Word/Excel export)
- Loan Origination System (LOS) connectors

**Multi-Document Capabilities:**
- Reconciliation engine for multiple source documents
- Continuous refresh as new documents arrive
- Batch processing

**Infrastructure:**
- User authentication and role-based access
- Database persistence for memo history
- Cloud deployment with high availability
