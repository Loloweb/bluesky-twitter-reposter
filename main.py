from client import *
import asyncio
from typing import NoReturn
from twikit import Client, Tweet
from atproto import Client as BlueskyClient

twitter_client = Client()
bluesky_client = BlueskyClient("https://bsky.social")

USER_ID = '97672707' # @STARendirect
CHECK_INTERVAL = 60 * 5 # 5 minutes. Rate limit for fetching user tweets is 50 requests per 15 minutes.

def callback(tweet: Tweet) -> None:
    print(f"New tweet from {tweet.user.screen_name}: {tweet.text}")
    bluesky_client.post_tweet(tweet.text)

async def get_latest_tweet():
    return (await twitter_client.get_user_tweets(USER_ID, 'Tweets', count=1))[0]

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
        if (
            before_tweet.id != latest_tweet.id and
            before_tweet.created_at_datetime < latest_tweet.created_at_datetime
        ):
            callback(latest_tweet)
            before_tweet = latest_tweet
        #else:
        #    print(f"Latest tweet from {latest_tweet.user.screen_name}: {latest_tweet.text}") # Debug

asyncio.run(main())