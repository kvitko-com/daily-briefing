#!/usr/bin/env python3
import argparse
import json
import os
import urllib.parse
import urllib.request

BASE = 'https://api.x.com/2'


def bearer_token() -> str:
    token = os.environ.get('X_BEARER_TOKEN') or os.environ.get('TWITTER_BEARER_TOKEN') or os.environ.get('BEARER_TOKEN')
    if not token:
        raise SystemExit('Missing bearer token: expected X_BEARER_TOKEN, TWITTER_BEARER_TOKEN, or BEARER_TOKEN')
    return token


def get_json(url: str):
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {bearer_token()}',
        'Accept': 'application/json',
        'User-Agent': 'OpenClaw x-twitter skill',
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        raise SystemExit(json.dumps({'status': e.code, 'error': body}))


def cmd_user(args):
    params = {
        'user.fields': 'created_at,description,public_metrics,verified,profile_image_url,url,location'
    }
    url = f"{BASE}/users/by/username/{urllib.parse.quote(args.username)}?{urllib.parse.urlencode(params)}"
    return get_json(url)


def cmd_search(args):
    params = {
        'query': args.query,
        'max_results': str(max(10, min(args.max_results, 100))),
        'tweet.fields': 'created_at,author_id,public_metrics,lang,conversation_id',
        'expansions': 'author_id',
        'user.fields': 'username,name,profile_image_url,verified',
    }
    url = f"{BASE}/tweets/search/recent?{urllib.parse.urlencode(params)}"
    return get_json(url)


def cmd_user_tweets(args):
    user = cmd_user(argparse.Namespace(username=args.username))
    data = user.get('data') or {}
    user_id = data.get('id')
    if not user_id:
        raise SystemExit(json.dumps({'error': f'Could not resolve user: {args.username}'}))
    params = {
        'max_results': str(max(5, min(args.max_results, 100))),
        'tweet.fields': 'created_at,public_metrics,lang,conversation_id',
        'exclude': 'replies' if args.exclude_replies else '',
    }
    params = {k: v for k, v in params.items() if v}
    url = f"{BASE}/users/{user_id}/tweets?{urllib.parse.urlencode(params)}"
    return get_json(url)


def main():
    p = argparse.ArgumentParser(description='Read X API v2 endpoints with bearer token auth.')
    sub = p.add_subparsers(dest='cmd', required=True)

    p_user = sub.add_parser('user', help='Look up a user by username')
    p_user.add_argument('username')

    p_search = sub.add_parser('search', help='Search recent tweets')
    p_search.add_argument('query')
    p_search.add_argument('--max-results', type=int, default=10)

    p_ut = sub.add_parser('user-tweets', help='Get a user\'s recent tweets')
    p_ut.add_argument('username')
    p_ut.add_argument('--max-results', type=int, default=10)
    p_ut.add_argument('--exclude-replies', action='store_true')

    p.add_argument('--pretty', action='store_true')
    args = p.parse_args()

    if args.cmd == 'user':
        out = cmd_user(args)
    elif args.cmd == 'search':
        out = cmd_search(args)
    elif args.cmd == 'user-tweets':
        out = cmd_user_tweets(args)
    else:
        raise SystemExit('Unknown command')

    if args.pretty:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    main()
