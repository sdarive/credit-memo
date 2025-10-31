# Automated Credit Memo Generation MVP  
## Using LandingAI’s ADE API + AWS Bedrock

---

## 1. Overview

**Goal:**  
Develop an automated platform to generate credit memos for bank loan underwriting using AI for document extraction (LandingAI’s ADE) and LLMs (AWS Bedrock).

**Features:**  
- Upload borrower financial docs (statements, tax returns, annual reports)
- ADE-powered document parsing for key financial values and coverage
- Calculation of lending risk ratios (DSCR, leverage, liquidity etc.)
- Auto-generate memo narrative using LLMs (Claude, Sonnet, etc., via Bedrock)
- Downloadable/editable memo

---

## 2. Core Technologies

- **LandingAI ADE API:** [API Playground](https://va.landing.ai/my/playground/ade)  
  *For document “ADE” extraction: parsing, field capture, table/rich layout understanding*  
  *Register or sign in to access API keys and orchestration interface.*

- **AWS Bedrock:**  
  *For prompt-based LLM (Claude, Sonnet, etc.) integration and orchestration.*  
  [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)

- **Public Datasets:**  
  *Training/test data/prototyping from HuggingFace—no proprietary data required.*

    - [AdaptLLM/finance-tasks](https://huggingface.co/datasets/AdaptLLM/finance-tasks)
    - [gbharti/finance-alpaca](https://huggingface.co/datasets/gbharti/finance-alpaca)
    - [PatronusAI/financebench](https://huggingface.co/datasets/PatronusAI/financebench)
    - [JanosAudran/financial-reports-sec](https://huggingface.co/datasets/JanosAudran/financial-reports-sec)

---

## 3. MVP Workflow

### A. Document Intake & ADE Extraction

1. **User uploads a PDF/Word/CSV of a financial statement.**
2. **Backend calls LandingAI’s ADE API:**  
   - POST document to `/ade` endpoint with API key  
   - Receive structured JSON of fields, tables, and extractions (revenues, net income, debts, etc.)

