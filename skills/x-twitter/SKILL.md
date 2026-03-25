---
name: x-twitter
description: Read and search X/Twitter data using either bearer-token v2 endpoints or OAuth 1.0a user-context credentials. Use when the user asks to look up an X account, search recent tweets, inspect recent posts from a username, or—when the app tier allows it—read their home timeline/followed-feed.
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["python3"],"env":["X_BEARER_TOKEN"]}}}
---

# X / Twitter feed reader

Use this skill to read the user's X home timeline with OAuth 1.0a **user context**. Prefer read-only behavior unless the user explicitly asks to post, like, follow, or take another write action.

Important: this relies on the legacy `statuses/home_timeline` endpoint. Some X developer tiers return error `453` for this route even with valid OAuth credentials. If that happens, report the access-tier limitation clearly instead of implying the credentials are malformed.

## What this skill is for

Use this skill when the user wants to:

- read their X feed
- see posts from accounts they follow
- summarize their timeline
- find notable or interesting recent posts
- check whether specific followed accounts posted recently

This skill supports two auth modes:

- Bearer token for X API v2 reads/searches:
  - `X_BEARER_TOKEN`
- OAuth 1.0a user context for legacy home timeline access:
  - `X_CONSUMER_KEY`
  - `X_CONSUMER_SECRET`
  - `X_ACCESS_TOKEN`
  - `X_ACCESS_TOKEN_SECRET`

Prefer bearer-token v2 endpoints for user lookup, recent tweet search, and recent posts by username. Use OAuth 1.0a home timeline only if the endpoint is actually allowed for the app tier.

Do not print these secrets. Do not ask the user to paste them into chat if they are already configured.

## Workflow

1. For user lookup, search, or recent posts from a known username, use `{baseDir}/scripts/read_v2.py`.
2. For the authenticated home timeline/followed-feed, use `{baseDir}/scripts/read_home_timeline.py`.
3. Start with a modest count such as `10`, `20`, or `40`.
4. If the user asked for a summary, summarize the posts clearly and link important items to authors.
5. If the user asked for raw data, return only the relevant fields instead of dumping huge JSON blobs unless they explicitly want full output.
6. If home timeline access fails with code `453`, fall back to v2 searches or recent posts for the named account and explain the limitation.

## Commands

Look up a user:

```bash
python3 {baseDir}/scripts/read_v2.py --pretty user daneek
```

Search recent tweets from `@daneek`:

```bash
python3 {baseDir}/scripts/read_v2.py --pretty search 'from:daneek' --max-results 10
```

Get recent tweets from `@daneek` directly:

```bash
python3 {baseDir}/scripts/read_v2.py --pretty user-tweets daneek --max-results 10 --exclude-replies
```

Fetch the authenticated home timeline when the app tier allows it:

```bash
python3 {baseDir}/scripts/read_home_timeline.py --count 20 --normalized --pretty
```

## Response guidance

When summarizing, include:

- who posted
- the main point of each notable post
- whether the feed trends toward news, personal updates, technical posts, memes, etc.

When the user asks for "my feed" or "people I'm following," interpret that as the authenticated home timeline.

## Safety and privacy

- Never expose OAuth secrets.
- Never echo authorization headers.
- Treat timeline content as private user data.
- Avoid write actions unless the user explicitly requests them.
- If X returns code `453`, explain that the app's X API access tier does not include this endpoint.
