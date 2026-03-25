#!/usr/bin/env python3
import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.parse
import urllib.request

API_URL = "https://api.x.com/1.1/statuses/home_timeline.json"


def pct(value: str) -> str:
    return urllib.parse.quote(str(value), safe='~-._')


def collect_oauth_params():
    return {
        'oauth_consumer_key': os.environ['X_CONSUMER_KEY'],
        'oauth_nonce': secrets.token_hex(16),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_token': os.environ['X_ACCESS_TOKEN'],
        'oauth_version': '1.0',
    }


def build_signature(method: str, url: str, oauth_params: dict, query_params: dict) -> str:
    merged = []
    for src in (oauth_params, query_params):
        for k, v in src.items():
            merged.append((pct(k), pct(v)))
    merged.sort()
    param_string = '&'.join(f'{k}={v}' for k, v in merged)
    base_string = '&'.join([method.upper(), pct(url), pct(param_string)])
    signing_key = f"{pct(os.environ['X_CONSUMER_SECRET'])}&{pct(os.environ['X_ACCESS_TOKEN_SECRET'])}"
    digest = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
    return base64.b64encode(digest).decode()


def build_auth_header(oauth_params: dict) -> str:
    items = ', '.join(f'{pct(k)}="{pct(v)}"' for k, v in sorted(oauth_params.items()))
    return 'OAuth ' + items


def normalize_item(item: dict) -> dict:
    user = item.get('user') or {}
    full_text = item.get('full_text') or item.get('text') or ''
    entities = item.get('entities') or {}
    urls = [u.get('expanded_url') or u.get('url') for u in entities.get('urls', []) if u.get('expanded_url') or u.get('url')]
    return {
        'id': item.get('id_str') or str(item.get('id')),
        'created_at': item.get('created_at'),
        'user_name': user.get('name'),
        'screen_name': user.get('screen_name'),
        'text': full_text,
        'favorite_count': item.get('favorite_count'),
        'retweet_count': item.get('retweet_count'),
        'reply_count': item.get('reply_count'),
        'quote_count': item.get('quote_count'),
        'lang': item.get('lang'),
        'urls': urls,
        'is_retweet': 'retweeted_status' in item,
    }


def main():
    parser = argparse.ArgumentParser(description='Read X home timeline via OAuth 1.0a user context.')
    parser.add_argument('--count', type=int, default=20)
    parser.add_argument('--pretty', action='store_true')
    parser.add_argument('--normalized', action='store_true')
    args = parser.parse_args()

    for key in ['X_CONSUMER_KEY', 'X_CONSUMER_SECRET', 'X_ACCESS_TOKEN', 'X_ACCESS_TOKEN_SECRET']:
        if not os.environ.get(key):
            raise SystemExit(f'Missing required env var: {key}')

    query_params = {
        'count': str(max(1, min(args.count, 200))),
        'tweet_mode': 'extended',
    }
    oauth_params = collect_oauth_params()
    oauth_params['oauth_signature'] = build_signature('GET', API_URL, oauth_params, query_params)
    auth_header = build_auth_header(oauth_params)
    url = API_URL + '?' + urllib.parse.urlencode(query_params)
    req = urllib.request.Request(url, headers={
        'Authorization': auth_header,
        'Accept': 'application/json',
        'User-Agent': 'OpenClaw x-twitter skill',
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        raise SystemExit(json.dumps({'status': e.code, 'error': err}))

    data = json.loads(body)
    if args.normalized:
        data = [normalize_item(item) for item in data]

    if args.pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    main()
