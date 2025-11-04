# Quick Submission Checklist

**Print this and check off as you go!**

---

## ☐ TASK 1: Commit & Push (5 min)

```bash
cd /Users/sivad/projects/credit-memo
git add -A
git commit -m "Add professional Ernie branding with bank letterhead and technology logos"
git push origin main
```

---

## ☐ TASK 2: Test Everything (30-45 min)

### Terminal 1 - Backend:
```bash
cd backend
python3 app.py
```

### Terminal 2 - Health Check:
```bash
curl http://localhost:5001/health
```

### Terminal 3 - Frontend:
```bash
cd frontend
npm start
```

### Browser Testing:
- ☐ Click "Use Test Data" button
- ☐ Wait for memo generation (~40 seconds)
- ☐ Verify bank letterhead appears
- ☐ Check LandingAI & AWS Bedrock logos in title
- ☐ Test Edit Memo
- ☐ Test Download (Text)
- ☐ Test Download (Word)
- ☐ Open Word file - verify branding

**Any issues?** Write them down: _______________

---

## ☐ TASK 3: Demo Script (60-90 min)

- ☐ Open: `/Users/sivad/projects/credit-memo/DEMO_SCRIPT.md`
- ☐ Read through entire script
- ☐ Customize with your talking points
- ☐ Plan 3:30-3:45 timing

---

## ☐ TASK 4: Rehearse (60 min)

- ☐ Rehearsal 1: Go through without timing
- ☐ Rehearsal 2: Timed (4 minutes max)
- ☐ Rehearsal 3: Record yourself

**Final time:** _____ minutes

---

## ☐ TASK 5: Record Demo Video (60 min)

### Recording:
- ☐ Start QuickTime or OBS
- ☐ Close unnecessary windows
- ☐ Record full demo with narration
- ☐ Watch & review
- ☐ Re-record if needed
- ☐ Save as: `ERNIE-DEMO-FINAL.mp4`

### Upload:
- ☐ Upload to Google Drive/YouTube/Dropbox
- ☐ Make shareable/public
- ☐ Copy URL: _______________________________

---

## ☐ TASK 6: Pre-Submission Check (30 min)

```bash
# Check git status
git status  # Should show "nothing to commit"

# Get GitHub URL
git remote -v
```

**GitHub URL:** _______________________________

### Final Test:
- ☐ Restart both servers
- ☐ Test "Use Test Data" one more time
- ☐ Verify everything works

### Documentation:
- ☐ README.md up to date
- ☐ CLAUDE.md accurate
- ☐ Demo video plays

---

## ☐ TASK 7: SUBMIT! (15 min)

**Form:** https://forms.gle/q682wg7ZWLnNUqQL6

**Deadline:** November 10, 11:59 PM ET

### Have Ready:
- ☐ Your name & email
- ☐ Project name: **Ernie - AI Credit Assistant**
- ☐ GitHub URL: _______________________________
- ☐ Demo video URL: _______________________________
- ☐ Project description (see FINAL_SUBMISSION_TASKS.md)

### After Submit:
- ☐ Save confirmation
- ☐ Screenshot submission
- ☐ Post to Discord (optional)

---

## 🎉 DONE!

**Submission completed at:** _______________

---

## Emergency Numbers

**If something breaks:**

1. Backend won't start:
   ```bash
   # Check what's running on port 5001
   lsof -i :5001
   # Kill if needed: kill -9 [PID]
   ```

2. Frontend won't start:
   ```bash
   # Check what's running on port 3000
   lsof -i :3000
   # Kill if needed: kill -9 [PID]
   ```

3. Demo fails during recording:
   - Use screenshot slides as backup
   - Narrate what would happen
   - Show previous successful test

4. Can't access GitHub:
   - Make sure you have internet
   - Try: `git push -u origin main`

---

**Total Estimated Time: 4-5 hours**

**Good luck! 🚀**
