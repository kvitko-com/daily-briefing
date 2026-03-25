# Morning Briefing Prompt

Run a daily morning briefing for Daneek.

Goals:
- Keep it concise enough to read in about 2 minutes.
- Focus on: AI, cybersecurity events, tech stocks, local Harrisonburg VA news, and the top national story.
- Store the final structured briefing locally.
- Send the final summary to Discord channel `channel:1482939264194052206`.
- Prefer high-signal source diversity over many shallow items.

## Required references

Before gathering sources, read:
- `/home/node/.openclaw/workspace/skills/morning-briefing/references/source-priority.md`
- `/home/node/.openclaw/workspace/skills/morning-briefing/references/formatting-rules.md`
- `/home/node/.openclaw/workspace/skills/morning-briefing/references/x-source-handles.md`

## Inputs to gather

### 1) X / Twitter
Use the X skill and available bearer-token v2 endpoints.

Important limitation:
- If home timeline / followed-feed is not available because the X API tier blocks it, do not fail the briefing.
- Preferred source is the authenticated home timeline of roughly the latest 100 posts from followed accounts.
- If that is unavailable, use the compact fallback account buckets from `source-priority.md` plus targeted searches.
- Do not let one source dominate the briefing unless the story is overwhelmingly central.

Topics to prioritize:
- AI
- cybersecurity events / incidents / major advisories
- tech stocks / major company moves
- local Harrisonburg / Shenandoah Valley news
- top national story

### 2) Local web news
Search the web for recent Harrisonburg, Virginia news.
Prioritize:
- WHSV
- WSVA
- Daily News-Record / DNROnline
- Rocktown Now
- official city/JMU sources when useful

### 3) National / tech context
Use web search sparingly to find:
- one top national story
- one to three meaningful tech/AI/cyber stories if they are genuinely relevant

## Research budget

Keep the run lean:
- avoid broad web-search loops
- avoid fetching many near-duplicate stories
- stop once the sections can be filled with high-confidence items

## Output format

Use exactly these sections, in this order:

**Top Stories**
- 3 to 5 bullets max

**Interesting Threads**
- 0 to 3 bullets max; omit the section entirely if there is nothing genuinely interesting

**Tech News**
- 2 to 4 bullets max

**Local News**
- 2 to 4 bullets max

**Action Items**
- only include if there is something actionable
- otherwise omit this section

## Style
- concise
- useful
- no fluff
- no long intro
- prefer bullets over paragraphs
- mention why an item matters in a few words
- avoid duplicating the same story across sections unless necessary

## Local storage

Write the final briefing to:
`briefings/daily/YYYY-MM-DD.md`

Also write a machine-readable JSON summary to:
`briefings/daily/YYYY-MM-DD.json`

The markdown file should include:
- generated timestamp in UTC
- sections actually used
- a one-line timeline access note

The JSON file should include:
- date
- generatedAt
- topStories[]
- interestingThreads[]
- techNews[]
- localNews[]
- actionItems[]
- notes.aboutTimelineAccess
- notes.sources

## Delivery

After writing the files locally, send the markdown summary text to Discord channel:
`channel:1482939264194052206`

If a tool or API source fails:
- continue with the remaining sources
- note the limitation briefly in the local JSON under `notes`
- do not make the Discord message noisy with technical failure details unless the briefing quality is materially affected
