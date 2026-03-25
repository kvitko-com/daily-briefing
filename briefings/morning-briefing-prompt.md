# Morning Briefing Prompt

Run a daily morning briefing for Daneek.

Goals:
- Keep it concise enough to read in about 2 minutes.
- Focus on: AI, cybersecurity events, tech stocks, Harrisonburg VA local news, and the top national news story.
- Store the final structured briefing locally.
- Send the final summary to Discord channel `channel:1482939264194052206`.

## Inputs to gather

### 1) X / Twitter
Use the X skill and available bearer-token v2 endpoints.

Important limitation:
- If home timeline / followed-feed is not available because the X API tier blocks it, say so internally and fall back to the best available X sources.
- Preferred source is the authenticated home timeline of roughly the latest 100 posts from followed accounts.
- If that is unavailable, use a combination of relevant searches and direct account/news-source reads to approximate a useful morning brief.

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
- major local X posts if useful

### 3) National / tech context
Use the web search tool sparingly to find:
- one top national story
- one to three meaningful tech/AI/cyber stories if they are genuinely relevant

## Output format

Use exactly these sections, in this order:

**Top Stories**
- 3 to 5 bullets max

**Interesting Threads**
- 1 to 3 bullets max

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

## Local storage

Write the final briefing to:
`briefings/daily/YYYY-MM-DD.md`

Also write a machine-readable JSON summary to:
`briefings/daily/YYYY-MM-DD.json`

The markdown file should include:
- generated timestamp in UTC
- the four required sections
- optional Action Items section

The JSON file should include:
- date
- generatedAt
- topStories[]
- interestingThreads[]
- techNews[]
- localNews[]
- actionItems[]
- notes.aboutTimelineAccess

## Delivery

After writing the files locally, send the markdown summary text to Discord channel:
`channel:1482939264194052206`

If a tool or API source fails:
- continue with the remaining sources
- note the limitation briefly in the local JSON under `notes`
- do not make the Discord message noisy with technical failure details unless the briefing quality is materially affected
