# RedditMLBot
Monitors a subreddit's top posts and if they are images, classifies the images utilizing Google Vision API and posts the classifications.

# Usage
1. Must have `google cloud services` and `praw` installed for python.

2. Place praw.ini file in the same folder as the `bot.py` file. Edit `praw.ini` file with your own bot's `secret/token` and `ID/Password`.

3. In the `bot.py` file, enter which `subreddit` you want to run the bot on as well as change how many top posts to search.

4. Run the bot and it will reply to the top posts on the subreddit with its image classifications.
