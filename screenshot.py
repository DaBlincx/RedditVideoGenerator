from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json

# Config
screenshotDir = "Screenshots"
screenWidth = 500
screenHeight = 1000

def clickClose(driver):
    print("tryna click icon_close")

    time.sleep(3)
    driver.execute_script("document.getElementsByClassName('icon-close')[0].parentElement.click()")

    print("clicked")
    time.sleep(1)

def getPostScreenshots(filePrefix, script):
    print("Starting Webdriver...")
    driver, wait = __setupDriver(script.url)
    
    try:
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except:
        with open("cookies.json", "w") as f:
            f.write()
        print("No cookies.json found")
        print("Check README.md for instructions on how to get cookies.json")
        input("Press enter to exit...")
        exit()

    time.sleep(1)
    driver.refresh()
    time.sleep(1)

    clickClose(driver)

    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait)
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")

    with open("cookies.json", "w") as f:
        json.dump(driver.get_cookies(), f)

    driver.quit()

    print("Webdriver closed")

def __takeScreenshot(filePrefix, driver, wait, handle="Post"):
    print(f"Taking screenshot of {handle}")
    method = By.CLASS_NAME if (handle == "Post") else By.ID
    search = wait.until(EC.presence_of_element_located((method, handle)))
    driver.execute_script("window.focus();")

    print(filePrefix.replace(filePrefix[:-7],""))
    print(handle)

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    with open(fileName, "wb") as fp:
        fp.write(search.screenshot_as_png)
    return fileName

def __setupDriver(url: str):
    print("Setting up webdriver...")
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False
    driver = webdriver.Firefox(options=options)
    
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)

    return driver, wait