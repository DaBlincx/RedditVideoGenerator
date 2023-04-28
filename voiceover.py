import pyttsx3

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text, voiceid):
    print(f"Creating voiceover for {fileName}...")
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    engine = pyttsx3.init()
    engine.setProperty('voice', voiceid)
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath