import os
import re
import praw
import markdown_to_text
import time
from videoscript import VideoScript
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
CLIENT_ID = config["Reddit"]["CLIENT_ID"]
CLIENT_SECRET = config["Reddit"]["CLIENT_SECRET"]
USER_AGENT = config["Reddit"]["USER_AGENT"]
SUBREDDIT = config["Reddit"]["SUBREDDIT"]
VOICEID = config["Voiceover"]["VOICEID"]

def getContent(outputDir, postOptionCount) -> VideoScript:
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)

    now = int(time.time())
    autoSelect = postOptionCount == 0
    posts = []
    
    postOptionCount = postOptionCount if postOptionCount != 0 else 1
    print(f"postOptionCount: {postOptionCount}")
    for submission in reddit.subreddit(SUBREDDIT).top(time_filter="day", limit=postOptionCount*3):
        if (f"{submission.id}.mp4" in existingPostIds or submission.over_18):
            print(f"skipping post {submission}")
            continue
        hoursAgoPosted = (now - submission.created_utc) / 3600
        print(f"[{len(posts)}] {submission.title}     {submission.score}    {'{:.1f}'.format(hoursAgoPosted)} hours ago")
        posts.append(submission)
        if autoSelect != 0 and (autoSelect or len(posts) >= postOptionCount):
            break

    if autoSelect:
        return __getContentFromPost(posts[0])
    else:
        postSelection = int(input("Input: "))
        selectedPost = posts[postSelection]
        return __getContentFromPost(selectedPost)

def getContentFromId(outputDir, submissionId) -> VideoScript:
    print(f"Getting content from id: {submissionId}")
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)

    if (submissionId in existingPostIds):
        print("Video already exists!")
        exit()
    try:
        submission = reddit.submission(submissionId)
    except Exception:
        print(f"Submission with id '{submissionId}' not found!")
        exit()
    return __getContentFromPost(submission)

def __getReddit():
    print("Getting reddit instance...")
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )


def __getContentFromPost(submission) -> VideoScript:
    content = VideoScript(submission.url, submission.title, submission.id, VOICEID)
    print(f"Creating video for post: {submission.title}")
    print(f"Url: {submission.url}")

    failedAttempts = 0
    for comment in submission.comments:
        if(content.addCommentScene(markdown_to_text.markdown_to_text(comment.body), comment.id, VOICEID)):
            failedAttempts += 1
        if (content.canQuickFinish() or (failedAttempts > 2 and content.canBeFinished())):
            break
    return content

def __getExistingPostIds(outputDir):
    print("Getting existing post ids...")
    files = os.listdir(outputDir)
    # I'm sure anyone knowledgeable on python hates this. I had some weird 
    # issues and frankly didn't care to troubleshoot. It works though...
    files = [f for f in files if os.path.isfile(f'{outputDir}/{f}')]
    return [re.sub(r'.*?-', '', file) for file in files]
