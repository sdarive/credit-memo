# Ernie Demo Script - 4 Minutes

**Project:** Ernie - AI Credit Assistant for Midwest Regional Bank
**Target Time:** 3:30-3:45 (leaves buffer)
**Delivery Style:** Confident, clear, problem-focused

---

## 🎯 Opening (30 seconds)

**[Show Ernie homepage with branding]**

"Hi, I'm [YOUR NAME], and I built **Ernie** - an AI Credit Assistant for commercial bank loan underwriting.

**The problem:** Credit analysts spend 4-6 hours per loan manually extracting data from PDFs, calculating ratios in Excel, and writing credit memos from scratch. This creates bottlenecks and delays loan decisions.

**Ernie's solution:** Automate the heavy lifting while empowering analysts to focus on what they do best - credit analysis and decision-making."

---

## 💡 How It Works (30 seconds)

**[Point to interface elements]**

"Ernie uses three key technologies:

1. **LandingAI's Agentic Document Extraction** - reads financial documents and extracts structured data
2. **Multi-agent financial analysis** - calculates 9 key credit ratios with automated risk assessment
3. **AWS Bedrock with RAG** - generates bank-approved credit memos following the '5 Cs of Credit' framework

Let me show you a live demo."

---

## 🚀 Live Demo - Upload & Process (45 seconds)

**[Screen: Upload interface]**

"I'll use our Test Data feature to demonstrate the full workflow."

**Actions:**
1. Click **"Use Test Data"** button
2. **[While progress bar runs - narrate]:**

"Watch the multi-stage process:
- LandingAI ADE extracts 15+ financial metrics from documents
- System calculates debt service coverage, liquidity ratios, leverage
- AWS Bedrock generates the narrative analysis
- Total time: about 40 seconds"

**[Wait for completion - can narrate more if needed]:**
- "This normally takes an analyst 4-6 hours of manual work"
- "Ernie handles the data entry, we handle the judgment"

---

## 📊 Results Dashboard (45 seconds)

**[Screen: Results page]**

"Here's what Ernie produced:

**1. Financial Metrics** [scroll to metrics]
- Revenue, net income, assets, liabilities
- All extracted automatically with source references

**2. Risk Ratios** [point to ratio cards]
- Debt Service Coverage: 1.71x - **Green** (healthy)
- Current Ratio: 3.00x - **Green** (strong liquidity)
- Debt to EBITDA: 1.67x - **Green** (low leverage)

Color-coded for instant risk assessment - analysts see the full picture at a glance.

**3. Risk Summary** [point to summary section]
- Overall rating, key strengths and concerns identified automatically"

---

## 📝 Credit Memo with Bank Letterhead (45 seconds)

**[Scroll to memo section]**

"And here's the AI-generated credit memo:

**[Point to letterhead at top]**
- Professional bank branding - Midwest Regional Bank with FDIC tagline
- Ready for credit committee review

**[Scroll through sections]**
- **Executive Summary** with recommendation
- **Financial Analysis** - every number cited with source references
- **5 Cs of Credit** - Character, Capacity, Capital, Collateral, Conditions
- **Risk Assessment** with specific strengths and concerns
- **Final Recommendation** with loan conditions

Every assertion is grounded in the extracted data for full audit trail and regulatory compliance."

---

## ✏️ Analyst Workflow (30 seconds)

**[Click Edit Memo]**

"Ernie doesn't replace analysts - it empowers them.

The workflow:
1. **Ernie generates the draft** - handles data entry and structure
2. **Analyst reviews and refines** - adds institutional knowledge, adjusts tone
3. **Download for approval** - Word format with full bank branding

**[Click Download as Word]**

Analysts go from 4-6 hours of grunt work to 30 minutes of high-value analysis."

---

## 🏗️ Why This Isn't Just Another RAG App (30 seconds)

**[Can show diagram or just explain]**

"This is a **multi-agent agentic workflow**, not a basic RAG chatbot:

**Agent 1:** Document Intelligence - LandingAI ADE parses financial statements
**Agent 2:** Financial Analysis - calculates and interprets 9 credit ratios
**Agent 3:** Knowledge Retrieval - RAG finds similar approved memos for context
**Agent 4:** Narrative Generation - AWS Bedrock writes bank-compliant analysis

All orchestrated with:
- Template-adaptive structure (not generic)
- Banking domain expertise built-in
- Full audit trail for compliance
- Source citations for every data point"

---

## 📈 Impact & Next Steps (20 seconds)

"**Impact:**
- 80% reduction in data entry time
- Consistent quality across all analysts
- Faster loan decisions for customers
- Full regulatory compliance

**90-Day Pilot:**
- Deploy with 3 credit analysts
- Process 50 loans
- Measure time savings and quality improvements
- Plan integration with loan origination system"

---

## 🎤 Closing (10 seconds)

"That's Ernie - transforming credit memo generation from hours to minutes while maintaining the quality and compliance banks require.

Questions?"

---

## 🎬 DEMO SETUP CHECKLIST

**Before You Start:**
- [ ] Backend running: `cd backend && python3 app.py`
- [ ] Frontend running: `cd frontend && npm start`
- [ ] Browser at: http://localhost:3000
- [ ] Test "Use Test Data" button works (40 sec processing time)
- [ ] Close extra browser tabs/windows
- [ ] Set timer for 4 minutes
- [ ] Have backup slides ready (just in case)

**During Demo:**
- Speak clearly and confidently
- Point to specific UI elements
- Keep energy up during 40-second processing wait
- Watch the clock - aim to finish by 3:45

---

## 🔑 KEY TALKING POINTS TO EMPHASIZE

**Must Include (Judging Criteria):**
1. ✅ **LandingAI ADE integration** (mandatory requirement)
2. ✅ **Agentic workflow** (multi-agent, not basic RAG)
3. ✅ **Financial domain expertise** (9 ratios, 5 Cs framework)
4. ✅ **Production-ready features** (audit trail, bank branding, compliance)
5. ✅ **Analyst empowerment** (not replacement)

**Avoid:**
- Don't spend too long on any one section
- Don't get bogged down in technical details
- Don't apologize if something loads slowly
- Don't say "this is just a demo" - it's a working MVP!

---

## ❓ ANTICIPATED QUESTIONS & ANSWERS

**Q: "How accurate is the extraction?"**
A: "LandingAI ADE uses foundation models trained on financial documents. We validate with ratio reconciliation - if numbers don't add up, we flag it for analyst review."

**Q: "What if the AI hallucinates?"**
A: "Every statement is grounded in extracted data with source citations. The RAG system provides similar memo examples for context. And most importantly - analysts review and approve everything before it goes to credit committee."

**Q: "How does this integrate with existing systems?"**
A: "The MVP is standalone to prove the concept. Our 90-day pilot roadmap includes integration with loan origination systems, SharePoint document libraries, and Office 365 workflows."

**Q: "Isn't this just a RAG chatbot?"**
A: "No - it's a multi-agent financial workflow. We have specialized agents for document extraction, financial analysis, knowledge retrieval, and narrative generation. RAG is one enhancement, not the core product. We're automating a complete analyst workflow, not just answering questions."

**Q: "What about regulatory compliance?"**
A: "Full audit trail built-in. Every extracted data point includes source references. All assertions cite specific documents. Generated memos include data lineage for regulatory review. Analysts maintain final approval authority."

**Q: "How long did this take to build?"**
A: "About [X weeks/months] of development. The core challenge was understanding banking workflows and compliance requirements, then building agentic orchestration rather than simple prompting."

---

## ⏱️ TIMING BREAKDOWN

| Section | Time | Running Total |
|---------|------|---------------|
| Opening | 0:30 | 0:30 |
| How It Works | 0:30 | 1:00 |
| Live Demo (Upload) | 0:45 | 1:45 |
| Results Dashboard | 0:45 | 2:30 |
| Credit Memo | 0:45 | 3:15 |
| Analyst Workflow | 0:30 | 3:45 |
| Why Not Basic RAG | 0:30 | 4:15 (SKIP IF RUNNING LONG) |
| Impact & Next Steps | 0:20 | 4:35 (SKIP IF RUNNING LONG) |
| Closing | 0:10 | 4:45 |

**Strategy:**
- Sections 1-6 are MUST HAVE (3:45)
- Section 7 (Why Not RAG) - skip if running long
- Section 8 (Impact) - shorten if needed

---

## 🎥 BACKUP PLAN (If Live Demo Fails)

**Option 1: Use Screenshots**
- Have slides ready showing each screen
- Narrate what would happen
- "In a working demo, this would show..."

**Option 2: Play Pre-recorded Video**
- Have video file ready to play
- "Let me show you a recording of the workflow..."

**Option 3: Explain with Diagrams**
- Show architecture diagram
- Walk through workflow conceptually
- Focus on value proposition

**Remember:** Judges care more about the idea, approach, and value than perfect execution!

---

## 📸 SLIDES TO PREPARE (Backup)

If you want safety slides:

1. **Title Slide:** Ernie - AI Credit Assistant
2. **Problem Slide:** Current analyst workflow (4-6 hours)
3. **Solution Slide:** Ernie workflow (30 minutes)
4. **Architecture Slide:** Multi-agent diagram
5. **Screenshot Slide:** Upload interface
6. **Screenshot Slide:** Results dashboard
7. **Screenshot Slide:** Credit memo with letterhead
8. **Impact Slide:** Metrics and next steps

---

## ✅ FINAL PRE-DEMO CHECKLIST

**Test Your Setup:**
- [ ] Run through demo once completely
- [ ] Time yourself (should be 3:30-3:45)
- [ ] Verify "Use Test Data" works (40 seconds)
- [ ] Check audio (speak clearly)
- [ ] Check video (screen readable)
- [ ] Have water nearby (for dry mouth!)

**Mental Preparation:**
- [ ] You've built something impressive - be confident!
- [ ] It's OK to be nervous - judges expect it
- [ ] Focus on the problem you're solving
- [ ] Remember: They want you to succeed!

---

**YOU'VE GOT THIS! 🚀**

Good luck with your demo!
