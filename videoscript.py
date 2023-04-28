from datetime import datetime
from moviepy.editor import AudioFileClip
import voiceover

MAX_WORDS_PER_COMMENT = 100
MIN_COMMENTS_FOR_FINISH = 4
MIN_DURATION = 40
MAX_DURATION = 60

class VideoScript:
    title = ""
    fileName = ""
    titleSCFile = ""
    url = ""
    totalDuration = 0
    frames = []

    def __init__(self, url, title, fileId, voiceid) -> None:
        self.fileName = f"{datetime.today().strftime('%Y-%m-%d')}-{fileId}"
        self.url = url
        self.title = title
        self.titleAudioClip = self.__createVoiceOver("title", title, voiceid)

    def canBeFinished(self) -> bool:
        return (len(self.frames) > 0) and (self.totalDuration > MIN_DURATION)

    def canQuickFinish(self) -> bool:
        return (len(self.frames) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION)

    def addCommentScene(self, text, commentId, voiceid) -> None:
        print(f"Adding comment scene for comment: {commentId}")
        wordCount = len(text.split())
        if (wordCount > MAX_WORDS_PER_COMMENT):
            return True
        frame = ScreenshotScene(text, commentId)
        frame.audioClip = self.__createVoiceOver(commentId, text, voiceid)
        if (frame.audioClip == None):
            return True
        self.frames.append(frame)

    def getDuration(self):
        print(f"Total duration: {self.totalDuration}")
        return self.totalDuration

    def getFileName(self):
        print(f"File name: {self.fileName}")
        return self.fileName

    def __createVoiceOver(self, name, text, voiceid):
        print(f"Creating voiceover for {name}...")
        file_path = voiceover.create_voice_over(f"{self.fileName}-{name}", text, voiceid)
        audioClip = AudioFileClip(file_path)
        if (self.totalDuration + audioClip.duration > MAX_DURATION):
            return None
        self.totalDuration += audioClip.duration
        return audioClip


class ScreenshotScene:
    text = ""
    screenShotFile = ""
    commentId = ""

    def __init__(self, text, commentId) -> None:
        self.text = text
        self.commentId = commentId