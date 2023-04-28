import os

def removeTempFiles():
    for file in os.listdir("./Voiceovers"):
        os.remove(f"./Voiceovers/{file}")
        print(f"Removed {file}")
    for file in os.listdir("./Screenshots"):
        os.remove(f"./Screenshots/{file}")
        print(f"Removed {file}")

if __name__ == "__main__":
    removeTempFiles()