# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automated Credit Memo Generator for the LandingAI Financial AI Hackathon Championship 2025. The system combines LandingAI's Agentic Document Extraction (ADE) API with AWS Bedrock LLMs to automatically generate credit memos for bank loan underwriting from uploaded financial documents.

**Submission Deadline:** Nov 10, 11:59 PM ET

## Mandatory Requirements

- **MUST use LandingAI ADE API** for document extraction (disqualification if not used)
- LLMs via AWS Bedrock (Claude, Sonnet models preferred)
- Intelligent agentic financial document analysis (not just basic RAG)
- Demo must show: document upload → ADE extraction → agentic analysis → memo generation

## Intended Architecture

### Backend (`backend/`)
- Flask or FastAPI application (`app.py`)
- LandingAI ADE integration module (`ade_api.py`)
- AWS Bedrock integration for LLM-based memo generation
- Financial ratio calculations (DSCR, leverage, liquidity)

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

1. User uploads financial document (PDF/Word/CSV)
2. Backend calls LandingAI ADE API to extract structured data (revenues, net income, debts, tables)
3. Calculate lending risk ratios from extracted data
4. Pass extracted data + ratios to AWS Bedrock LLM for memo narrative generation
5. Return editable, downloadable credit memo to user

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
- AWS credentials for Bedrock access (configure via AWS CLI or env vars)

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
