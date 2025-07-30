from client import *
import asyncio
import re
from typing import NoReturn, List, Dict
from twikit import Client, Tweet
from atproto import Client as BlueskyClient
import httpcore

twitter_client = Client()
bluesky_client = BlueskyClient("https://bsky.social")

CHECK_INTERVAL = 60 * 5 # 5 minutes. Rate limit for fetching user tweets is 50 requests per 15 minutes.

def callback(tweet: Tweet) -> None:
    print(f"New tweet from {tweet.user.screen_name} at {tweet.created_at}: {tweet.text}")
    hashtags_links = parse_facets(tweet.text)
    bluesky_client.post(tweet.text, facets=hashtags_links, langs=["fr"]) # For English posts, change from fr to en

def parse_urls(text: str) -> List[Dict]:
    spans = []
    # From https://docs.bsky.app/docs/advanced-guides/posts#mentions-and-links
    # partial/naive URL regex based on: https://stackoverflow.com/a/3809435
    # tweaked to disallow some training punctuation
    url_regex = rb"[$|\W](https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*[-a-zA-Z0-9@%_\+~#//=])?)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(url_regex, text_bytes):
        spans.append({
            "start": m.start(1),
            "end": m.end(1),
            "url": m.group(1).decode("UTF-8"),
        })
    return spans

def parse_hashtags(text: str) -> List[Dict]:
    spans = []
    # The docs don't have an example for hashtags, so this is based on the URL regex
    hashtag_regex = rb"(^|\s)(#[a-zA-Z0-9_]+)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(hashtag_regex, text_bytes):
        spans.append({
            "start": m.start(2),
            "end": m.end(2),
            "tag": m.group(2).decode("UTF-8"),
        })
    return spans

def parse_facets(text: str) -> List[Dict]:
    facets = []
    for m in parse_hashtags(text):
        facets.append({
            "index": {
                "byteStart": m["start"],
                "byteEnd": m["end"],
            },
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": m["tag"][1:]}],  # Remove the '#' from the tag
        })
    for u in parse_urls(text):
        facets.append({
            "index": {
                "byteStart": u["start"],
                "byteEnd": u["end"],
            },
            "features": [
                {
                    "$type": "app.bsky.richtext.facet#link",
                    # NOTE: URI ("I") not URL ("L")
                    "uri": u["url"],
                }
            ],
        })
    return facets

async def get_latest_tweet():
    try:
        return (await twitter_client.get_user_tweets(USER_ID, 'Tweets', count=1))[0]
    except httpcore.ConnectTimeout:
        print("Connection timeout while fetching latest tweet. Will retry on next interval.")
        return None
    except Exception as e:
        print(f"Error fetching latest tweet: {e}")
        return None

async def main() -> NoReturn:

    await twitter_client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json',
    )
    print(f"Logged in on Twitter as {USERNAME}")

    bluesky_client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
    print(f"Logged in on Bluesky as {BLUESKY_USERNAME}")

    before_tweet = await get_latest_tweet()
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        latest_tweet = await get_latest_tweet()
        if latest_tweet is None:
            print("Skipping this check due to connection error...")
            continue # Don't replace before_tweet if we couldn't fetch the latest tweet
        if (
            before_tweet.id != latest_tweet.id and
            before_tweet.created_at_datetime < latest_tweet.created_at_datetime
        ):
            callback(latest_tweet)
            before_tweet = latest_tweet
        #else:
        #    print(f"Latest tweet from {latest_tweet.user.screen_name}: {latest_tweet.text}") # Debug

asyncio.run(main())
