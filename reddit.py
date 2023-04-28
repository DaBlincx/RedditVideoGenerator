import os, re, praw, markdown_to_text, time
from videoscript import VideoScript

redditUrl = "https://www.reddit.com/"

def getContent(outputDir, postOptionCount) -> VideoScript:
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)

    now = int( time.time() )
    autoSelect = postOptionCount == 0
    posts = []
    print("evaluating posts...")
    postOptionCount = postOptionCount if postOptionCount != 0 else 1
    print(f"postOptionCount: {postOptionCount}")
    for submission in reddit.subreddit("askreddit").top(time_filter="day", limit=postOptionCount*10):
        if (fr"{submission}.mp4" in existingPostIds or submission.over_18):
            print(f"skipping post {submission}")
            continue
        hoursAgoPosted = (now - submission.created_utc) / 3600
        print(f"[{len(posts)}] {submission.title}     {submission.score}    {'{:.1f}'.format(hoursAgoPosted)} hours ago")
        posts.append(submission)
        if autoSelect != 0:
            if (autoSelect or len(posts) >= postOptionCount):
                break

    if autoSelect:
        return __getContentFromPost(posts[0])
    else:
        postSelection = int(input())
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
    except:
        print(f"Submission with id '{submissionId}' not found!")
        exit()
    return __getContentFromPost(submission)

def __getReddit():
    print("Getting reddit instance...")
    return praw.Reddit(
        client_id="FvW76Iy4RLZw7rdzGC3SIg",
        client_secret="md_FqnmN9J31cVer3ETCAlUO5wkchQ",
        # user_agent sounds scary, but it's just a string to identify what your using it for
        # It's common courtesy to use something like <platform>:<name>:<version> by <your name>
        # ex. "Window11:TestApp:v0.1 by u/Shifty-The-Dev"
        user_agent="Windows10:cool-app:v0.1 by u/BlincxYT"
    )


def __getContentFromPost(submission) -> VideoScript:
    content = VideoScript(submission.url, submission.title, submission.id)
    print(f"Creating video for post: {submission.title}")
    print(f"Url: {submission.url}")

    failedAttempts = 0
    for comment in submission.comments:
        if(content.addCommentScene(markdown_to_text.markdown_to_text(comment.body), comment.id)):
            failedAttempts += 1
        if (content.canQuickFinish() or (failedAttempts > 2 and content.canBeFinished())):
            break
    return content

def __getExistingPostIds(outputDir):
    print("Getting existing post ids...")
    files = os.listdir(outputDir)
    # I'm sure anyone knowledgable on python hates this. I had some weird 
    # issues and frankly didn't care to troubleshoot. It works though...
    files = [f for f in files if os.path.isfile(outputDir+'/'+f)]
    return [re.sub(r'.*?-', '', file) for file in files]