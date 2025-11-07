# Demo Video Recording Guide
## 4-Minute YouTube Demo for Hackathon Submission

**Goal:** Record a compelling 4-minute demo showing Ernie in action
**Tools:** QuickTime (Mac built-in) or OBS Studio (free)
**Deadline:** November 10, 11:59 PM ET

---

## PRE-RECORDING CHECKLIST (10 minutes)

### 1. Clean Your Desktop
```bash
# Hide desktop icons temporarily
defaults write com.apple.finder CreateDesktop false
killall Finder

# To restore later:
# defaults write com.apple.finder CreateDesktop true
# killall Finder
```

### 2. Close Unnecessary Apps
- Close Slack, email, messaging apps
- Close all browser tabs except demo
- Turn off notifications:
  - System Settings → Notifications → Do Not Disturb → ON

### 3. Start Backend & Frontend
```bash
# Terminal 1: Backend
kill_5001  # Kill any existing process
start_ernie_backend

# Terminal 2: Frontend (or just use browser at localhost:3000)
# If not running: cd /Users/sivad/projects/credit-memo/frontend && npm start
```

### 4. Open Browser in Clean State
- Chrome Incognito or new Safari window
- Go to: http://localhost:3000
- Test "Use Test Data" button works (should take ~40 seconds)
- Refresh page to reset for recording

### 5. Prepare Your Script
- Open: DEMO_SCRIPT_FINAL.md or DEMO_SLIDES_COMPELLING.md
- Read through once for timing
- Optional: Have script on second screen or printed

---

## RECORDING SETUP (5 minutes)

### Option A: QuickTime (Easiest)
1. Open QuickTime Player
2. File → New Screen Recording
3. Click Options dropdown:
   - Microphone: Built-in Microphone (or external mic)
   - Show Mouse Clicks: ON
4. Click "Record Entire Screen" or drag to select area
5. Click Record button

### Option B: OBS Studio (More Professional)
1. Download: https://obsproject.com/
2. Add Source: "Display Capture" or "Window Capture"
3. Add Audio: Built-in microphone
4. Settings → Video: 1920x1080, 30fps
5. Click "Start Recording"

---

## DEMO SCRIPT (3:45 target)

### Introduction (30 seconds)
**Show yourself on camera or just voice:**

"Hi, I'm [Name] and this is Ernie - an AI Credit Assistant that saves banks $4 billion annually. Credit analysts spend 4-6 hours per loan on manual copy-paste work. Ernie does it in 40 seconds using three AI engines: LandingAI's document extraction, AWS Bedrock for memo generation, and a RAG knowledge base for institutional learning."

**Switch to screen recording of Ernie interface**

### Demo Part 1: The Problem (30 seconds)
**Show Ernie homepage:**

"Here's Ernie's interface. In traditional workflows, analysts manually extract data from 10+ documents - balance sheets, tax returns, bank statements - then spend hours writing credit memos. Let me show you how Ernie transforms this."

### Demo Part 2: Upload & Processing (45 seconds)
**Click "Use Test Data" button:**

"I'm clicking 'Use Test Data' to simulate uploading three financial documents. Watch as LandingAI's ADE API extracts structured data in real-time."

**While processing, narrate:**
- "It's reading balance sheets, income statements, tax returns..."
- "Multi-document reconciliation happening automatically..."
- "Building a complete financial profile..."

**Wait for processing to complete (~40 seconds)**

### Demo Part 3: Results Dashboard (60 seconds)
**Scroll through results:**

"Here's what Ernie extracted: $2.1 million in revenue, $385K net income, $890K in debt."

**Point to ratios:**
"Ernie calculated 9 key lending ratios automatically:
- DSCR of 2.15 - GREEN - strong debt coverage
- Leverage ratio 32% - GREEN - conservative debt levels
- Current ratio 2.8 - GREEN - excellent liquidity"

**Highlight audit trail:**
"Every number has source citations - which document, which page, which field. Full audit compliance."

### Demo Part 4: Credit Memo (60 seconds)
**Scroll through generated memo:**

"Now the magic: AWS Bedrock generated a complete credit memo in 40 seconds."

**Point to key sections:**
- "Bank header - template-adaptive, matches bank branding"
- "Executive Summary - professional tone for credit committees"
- "Financial Analysis - cites source documents for compliance"
- "Risk Assessment - RAG retrieved insights from similar loans in our knowledge base"
- "Recommendation - clear guidance for loan decision"

**Show edit & download:**
"Analysts can edit the memo, then download as Word with full formatting."

### Closing (30 seconds)
**Return to you or final screen:**

"That's Ernie: 40 seconds to process, 30 minutes for analyst review, compared to 4-6 hours of manual work. That's 92% time reduction with better quality thanks to RAG-enhanced generation.

The tech stack:
- LandingAI ADE for document extraction
- AWS Bedrock Claude 4.5 for memo generation
- PostgreSQL with pgvector for semantic search
- All production-ready, all open source on GitHub.

This is Ernie - where AI meets institutional intelligence. Thank you."

**Show final slide with:**
- GitHub: github.com/sdarive/credit-memo
- Your email/contact

---

## RECORDING TIPS

### Audio Quality
- Record in quiet room
- Close windows (block outside noise)
- Use headphone mic if available (better quality than built-in)
- Speak clearly, not too fast
- Project enthusiasm without shouting

### Screen Recording
- Full screen browser (hide bookmarks bar)
- Cursor movements should be deliberate
- Don't rush clicking - let viewers see what you're clicking
- Zoom browser if needed: Cmd + (but test first)

### Timing
- Practice once before recording
- If you go over 4 minutes, that's OK up to 4:15
- Better to be clear than rushed

### Mistakes
- If you mess up, just pause and restart that section
- Edit out pauses later (QuickTime: Edit → Trim)
- Or just re-record - it's only 4 minutes!

---

## POST-RECORDING (15 minutes)

### 1. Review the Video
- Watch it once
- Check: Can you hear clearly?
- Check: Is screen readable?
- Check: Under 4 minutes?

### 2. Edit if Needed (Optional)
**QuickTime:**
- Edit → Trim → Drag yellow handles to cut beginning/end
- File → Save

**iMovie (for more editing):**
- File → Import → Select video
- Drag to timeline
- Cut out mistakes
- File → Share → File

### 3. Export Final Video
- Format: MP4 or MOV
- Resolution: 1080p
- Quality: High
- File size: <500MB for YouTube

---

## UPLOADING TO YOUTUBE (10 minutes)

### 1. Go to YouTube
- Visit: https://studio.youtube.com
- Sign in with Google account

### 2. Upload Video
- Click "Create" button (camera icon with +)
- Select "Upload Videos"
- Drag your video file or click to browse

### 3. Video Details
**Title:**
```
Ernie - AI Credit Assistant | LandingAI Financial Hackathon 2025
```

**Description:**
```
Ernie is an AI-powered credit memo generator that reduces credit analyst workload by 92%.

Built with:
- LandingAI ADE for intelligent document extraction
- AWS Bedrock Claude 4.5 for memo generation
- PostgreSQL with pgvector for RAG-enhanced context

Demo shows:
- Multi-document financial data extraction
- Automated credit ratio calculations with visual indicators
- Template-adaptive credit memo generation with full audit trail
- RAG knowledge base for institutional learning

Transforms 4-6 hours of manual work into 40 seconds of AI processing + 30 minutes of analyst review.

GitHub: https://github.com/sdarive/credit-memo
Built for: LandingAI Financial AI Hackathon Championship 2025

Team: [Your name/team]
Contact: [Your email]
```

**Visibility:**
- Choose: "Unlisted" (only people with link can view)
- Or "Public" (searchable on YouTube)
- Do NOT choose "Private" (form submission won't work)

**Tags:**
```
AI, Financial Technology, Credit Analysis, LandingAI, AWS Bedrock, RAG, Document Extraction, Hackathon
```

### 4. Save & Get Link
- Click "Next" through remaining screens
- Click "Publish"
- Copy the video URL (looks like: https://youtu.be/XXXXXXXXXXX)

---

## SUBMISSION CHECKLIST

After video is uploaded, you need:

✓ **Team Name**
✓ **Team Members** (names, emails, organizations, titles)
✓ **GitHub Link:** https://github.com/sdarive/credit-memo
✓ **YouTube Link:** [Your video URL]
✓ **Attendance:** Can you attend NYC in person?

**Next Steps:**
1. Register: https://www.luma.com/jme15h1t
2. Submit form: https://forms.gle/q682wg7ZWLnNUqQL6

---

## TROUBLESHOOTING

**Problem: Backend takes too long to start**
```bash
kill_5001
cd /Users/sivad/projects/credit-memo/backend
python3 app.py
```

**Problem: "Use Test Data" button doesn't work**
- Check backend terminal for errors
- Refresh frontend page
- Try real browser (not incognito) if issues persist

**Problem: Video file too large**
- Use HandBrake (free) to compress: https://handbrake.fr/
- Target: 1080p, H.264, ~5-10 Mbps bitrate

**Problem: Audio sounds bad**
- Re-record in quieter space
- Move closer to microphone
- Use external mic if available

**Problem: Went over 4 minutes**
- Edit out pauses/mistakes
- Or speed up slightly in iMovie (1.1x speed)
- Or trim less critical sections

---

## QUICK START: ONE COMMAND RECORDING

If you want to do everything in one take:

1. Start backend: `start_ernie_backend`
2. Open browser: http://localhost:3000
3. Open QuickTime → New Screen Recording
4. Press Record
5. Follow script naturally (don't rush)
6. Click "Use Test Data" when ready
7. Narrate while it processes
8. Show results, scroll through memo
9. Stop recording
10. Upload to YouTube

**That's it! You got this.** 🎬
