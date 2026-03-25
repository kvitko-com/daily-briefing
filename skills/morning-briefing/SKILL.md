---
name: morning-briefing
description: Generate a concise daily morning briefing from X/Twitter, web search, and local news sources, then save it locally and deliver it to the target chat. Use when the user asks for a recurring daily brief, an on-demand test-run briefing, or a short structured summary covering AI, cybersecurity, tech stocks, local Harrisonburg news, and the top national story.
metadata: {"openclaw":{"emoji":"☕","requires":{"bins":["python3"],"config":["tools.web.search.enabled"]}}}
---

# Morning Briefing

Use this skill for Daneek's daily coffee briefing.

## Output contract

Produce a briefing that can be read in about 2 minutes.

Use these sections, in this exact order:

- **Top Stories**
- **Interesting Threads**
- **Tech News**
- **Local News**
- **Action Items** (only when there is something actionable)

Keep it concise. Prefer bullets. Avoid filler.

## Source priorities

### X / Twitter

Primary goal: inspect roughly the latest 100 posts from followed accounts.

If the authenticated home timeline endpoint is blocked by X API tier limits, do not fail the whole briefing. Fall back to:

- direct reads of important accounts or source accounts
- targeted searches
- recent tweets from relevant usernames

Prioritize items relevant to:

- AI
- cybersecurity incidents, advisories, or major breaches
- tech stocks / large company moves
- Harrisonburg / Shenandoah Valley local news
- one major national story

### Local news

Prioritize:

- WHSV
- WSVA
- Daily News-Record / DNROnline
- relevant X posts when helpful

### National / tech context

Use web search sparingly. Pick only genuinely relevant items.

## Required references

Read these before generating the briefing:

- `{baseDir}/references/source-priority.md`
- `{baseDir}/references/formatting-rules.md`
- `{baseDir}/references/x-source-handles.md`

Use them to rank story relevance, keep source diversity, improve X fallback behavior, and avoid wasted research.

## Local persistence

Before finishing, write:

- markdown to `briefings/daily/YYYY-MM-DD.md`
- JSON to `briefings/daily/YYYY-MM-DD.json`

Include a UTC timestamp and a brief note about whether full home timeline access worked or whether fallback sources were used.

## Delivery

After writing local files, send the concise markdown summary to the configured Discord destination.

## Failure handling

If one source fails:

- continue with the remaining sources
- note the limitation in the local JSON
- keep the chat output clean unless the quality is materially degraded
