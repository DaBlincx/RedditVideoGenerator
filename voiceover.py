import pyttsx3

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    print(f"Creating voiceover for {fileName}...")
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    engine = pyttsx3.init()
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0")
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath