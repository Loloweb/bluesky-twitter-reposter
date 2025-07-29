Simple Python 3.11 program that uses [twikit](https://github.com/d60/twikit) to read a Twitter account evey 5 mins, then reposts any new tweet as a Bluesky post.

## Requirements
- Python >=3.10 with these libraries (you might want to set up a [venv](https://docs.python.org/3/library/venv.html) for them):
```bash
pip install twikit # Twitter scraper
pip install atproto # AT protocol (Bluesky) SDK
```
- A Twitter account in somewhat good standing.
    - This doesn't have to be the Twitter account being scraped, but if the account you want to scrape is protected (🔒), ensure the account used for scraping can read the tweets of the protected account.
    - Ever since the enshittification years ago, Twitter now requires either an account or a small monthly payment of $200 just to *read* tweets (needless to say, this program uses the former). The Twitter account will be used to read tweets and will never post by itself. However, because this is against Twitter's TOS, <ins>the risk of being flagged/banned by Twitter is always present.</ins> While this program doesn't do anything overly suspicious, ensure any modification you do follows the [twikit recommendations](https://github.com/d60/twikit/blob/main/ToProtectYourAccount.md) and respects the [rate limits](https://github.com/d60/twikit/blob/main/ratelimits.md). I am not responsible for any account banned due to the use of this program.
    - **You will need to put the account's password in plain text** unless you set it to read it from your environment variables (todo: tutorial on that). Make sure your password is not being used elsewhere (they should never be!!!!!). Keep in mind changing the password of a Twitter account temporarily restricts it from some actions, though this shouldn't affect the ability to read tweets.
- A Bluesky account
    - Unlike Twitter, Bluesky is based and allows you to set [app passwords](https://bsky.app/settings/app-passwords) in order to avoid putting your password in plain text.
    - I don't recommend using your personal Bluesky account for this unless you know what you're doing. Creating a new account is fast and not restricted by invites anymore.

## Setup
1. Clone this repo
2. Fill in client.py
    - To get the ID of the Twitter user you want to scrape, either:
        - In the user's banner URL, the first set of numbers is the user's ID (example for [@unicouniuni3](https://pbs.twimg.com/profile_banners/1271278270718242819/1705494722/1500x500), the ID would be 1271278270718242819)
        - If the user does not have a banner, enter the user's username [here](https://ilo.so/twitter-id/). If the website has too many requests, try again in 15 minutes.
    - A Twitter user ID can be longer or shorter depending on when the account was made.
    - For the Bluesky account's password, it is highly recommended to set an [app password](https://bsky.app/settings/app-passwords) instead of the account's actual password.
3. Adjust main.py to your liking such as:
    - The language of your Bluesky posts. This affects who can see the posts in their feed. **(defaults to French)**
    - The frequency in which you check for new tweets (in seconds, default is 5 minutes, careful not to surpass the [rate limit](https://github.com/d60/twikit/blob/main/ratelimits.md)!)
    - And more...?
4. Run it
```bash
python main.py
path/to/venv/bin/python main.py # if you have a venv set up
```
5. Profit?