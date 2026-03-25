# Daily Briefing Setup

This repo contains the workspace-side pieces for the daily morning briefing.

## Included

- `skills/morning-briefing/` — briefing workflow skill
- `skills/x-twitter/` — X/Twitter reading helpers
- `briefings/morning-briefing-prompt.md` — briefing instructions
- `config/openclaw.setup.example.json` — sanitized OpenClaw config example
- `config/openclaw.cron.jobs.example.json` — sanitized cron job example

## Secrets not stored here

Do not commit live secrets. Keep these in `~/.openclaw/.env` or your own secret store:

- `X_BEARER_TOKEN`
- `X_CONSUMER_KEY`
- `X_CONSUMER_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`
- Brave API key
- Discord token

## Recommended local config

Enable:
- web search via Brave
- skill `x-twitter`
- cron scheduler

## Create the scheduled job

Recommended command:

```bash
openclaw cron add \
  --name "Daily Morning Briefing" \
  --cron "0 8 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Read /home/node/.openclaw/workspace/briefings/morning-briefing-prompt.md and execute it exactly. Use the morning-briefing skill and x-twitter skill plus web search/fetch as needed. Write the results to /home/node/.openclaw/workspace/briefings/daily/YYYY-MM-DD.md and .json, then send the final concise summary to Discord channel:1482939264194052206." \
  --announce \
  --channel discord \
  --to "channel:1482939264194052206"
```

## Trigger a manual test run

```bash
openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id> --limit 20
```

## Notes

- Full home timeline access on X may depend on API tier.
- If timeline access is blocked, the workflow should fall back to v2 searches and direct account/news-source reads.
