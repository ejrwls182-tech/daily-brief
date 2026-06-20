# 스케줄 태스크 프롬프트 (daily-dashboard-content)

- **taskId**: `daily-dashboard-content`
- **cron**: `0 7 * * *` (매일 오전 7시, 로컬 시간)
- **description**: Generate daily headlines + deep analysis (with vocab footnotes and Korean translations), then commit & push to deploy on Vercel

아래 내용을 스케줄 태스크 프롬프트로 그대로 사용:

---

Generate fresh daily content for the DailyBrief news dashboard and deploy it. Work fully autonomously, no user interaction.

STEP 1 — Generate content.
Use WebSearch to find current news, then write valid JSON to /Users/jin/news-dashboard/content.json with this EXACT structure:

{
  "updated": "YYYY-MM-DD",
  "headlines": [
    {
      "title": "...",
      "title_ko": "...",
      "summary": "...",
      "source": "...",
      "tag": "Politics" | "Economy",
      "vocab": [ { "word": "...", "korean": "..." } ]
    }
  ],
  "analysis": [
    {
      "title": "...",
      "title_ko": "...",
      "sections": [
        { "question": "Q1. ...", "question_ko": "Q1. ...", "answer": "...", "answer_ko": "..." }
      ],
      "sources": [ { "name": "Publisher — article title", "url": "https://..." } ]
    }
  ]
}

Content requirements:
- headlines: exactly 3 stories, POLITICS and ECONOMY/BUSINESS only (no sports). International/world priority. title = English headline. title_ko = a natural Korean translation of that headline. Summary = 4-6 sentences in English covering what happened, who's involved, why it matters, implications. Under 600 chars.
- vocab: for EACH headline, pick 3-5 advanced/difficult English words or phrases that actually appear in that headline's summary, each with a concise Korean definition. Format: { "word": "exact word/phrase", "korean": "한국어 뜻" }.
- analysis: 2 intellectually interesting topics (geopolitics, economics, science, tech, current events). Each with title (English) + title_ko (Korean translation) + 2-3 Q&A sections + a "sources" array. Each section needs: question (English, prefixed "Q1." etc.), question_ko (Korean translation of the question), answer (English, 3-5 substantial paragraphs with history/mechanisms/data/competing views — explainer-article depth), answer_ko (a faithful, natural Korean translation of the English answer). Plain text only — no markdown symbols. Separate paragraphs with \n\n inside answer/answer_ko strings.
- sources: for EACH analysis item, include 2-4 real source URLs that informed or support the analysis — these MUST be actual URLs that appeared in your WebSearch results for that topic (do not invent URLs). Each entry: { "name": "Publisher — short title", "url": "https://..." }. These are shown to the reader as 'Sources / 출처' links, so they must be genuine and relevant.
- updated: today's date, YYYY-MM-DD.

STEP 2 — Validate.
Run: python3 -c "import json; json.load(open('/Users/jin/news-dashboard/content.json')); print('valid')"
If invalid, fix the JSON and re-validate before continuing.

STEP 3 — Deploy via git push (this is what updates the live site).
Run these commands:
  cd /Users/jin/news-dashboard
  git add content.json
  git commit -m "Daily content update: $(date +%Y-%m-%d)"
  git push origin main

The repo's origin is git@github.com:ejrwls182-tech/daily-brief.git over SSH (key already configured). Vercel is connected to this GitHub repo with auto-deploy, so pushing automatically triggers a redeploy of the static site at https://daily-brief-virid.vercel.app. The site is purely static (index.html + content.json), so a git push is all that's needed — no server, no build step.

STEP 4 — Confirm.
Report the git push result and the commit hash. The Vercel redeploy goes live within a minute or two (no cold start).
