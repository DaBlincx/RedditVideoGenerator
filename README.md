# Reddit Video Generator

## modified version with cookies to support auto darkmode and language defaults

*This project is further explained in [this video](https://youtu.be/ZmSb3LZDdf0)*

*This code is meant only for educational reference and will not be maintained. Because of this, the repo is archived and is in a read-only state*

---
This program generates a .mp4 video automatically by querying the top post on the
r/askreddit subreddit, and grabbing several comments. The workflow of this program is:
- Install dependencies
- Make a copy of config.example.ini and rename to config.ini
- Register with Reddit to create an application [here](https://www.reddit.com/prefs/apps/) and copy the credentials
- Use the credentials from the previous step to update config.ini (lines 22 -> 24)
- create a file called `cookies.json`
- open `reddit.com/r/*somesubreddit*` in your browser and copy all cookies into cookies.json (using something like editthiscookie browser extension or defautl dev tools)

Now, you can run `python main.py` to be prompted for which post to choose. Alternatively,
you can run `python main.py <reddit-post-id>` to create a video for a specific post.
