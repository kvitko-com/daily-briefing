#!/usr/bin/env bash
set -euo pipefail

cd /home/node/.openclaw/workspace

cat <<'MSG'
Use the morning-briefing skill and x-twitter skill to generate Daneek's morning briefing now.

Requirements:
- Read /home/node/.openclaw/workspace/briefings/morning-briefing-prompt.md
- Save markdown to /home/node/.openclaw/workspace/briefings/daily/YYYY-MM-DD.md
- Save JSON to /home/node/.openclaw/workspace/briefings/daily/YYYY-MM-DD.json
- Send the final concise summary to Discord channel:1482939264194052206
- Keep it readable in about 2 minutes
MSG
