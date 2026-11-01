import logging
import time
from datetime import date
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

# Full path to a Firefox profile that is already logged in to TikTok.
PROFILE_PATH = r"..."

# Username of your friend exactly as shown in the chat list.
FRIEND_NAME = "..."

# Message to send.
MESSAGE = "..."

# Run Firefox without a visible window. Set to False if it does not work.
HEADLESS = True

# Maximum seconds to wait for each page element.
WAIT_TIMEOUT = 30

# How many times to retry if a run fails.
MAX_RETRIES = 3

# Files used by the script (created next to this script).
BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "last_sent.txt"
LOG_FILE = BASE_DIR / "streak.log"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("streak")


# ---------------------------------------------------------------------------
# State: do not send twice on the same day
# ---------------------------------------------------------------------------

def already_sent_today():
    if not STATE_FILE.exists():
        return False
    return STATE_FILE.read_text(encoding="utf-8").strip() == date.today().isoformat()


def mark_sent():
    STATE_FILE.write_text(date.today().isoformat(), encoding="utf-8")


# ---------------------------------------------------------------------------
# Browser
# ---------------------------------------------------------------------------

def create_driver():
    options = webdriver.FirefoxOptions()
    options.profile = PROFILE_PATH
    if HEADLESS:
        options.add_argument("-headless")
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


def safe_click(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def send_once():
    driver = create_driver()
    try:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        log.info("Opening TikTok messages...")
        driver.get("https://www.tiktok.com/messages")

        log.info("Looking for chat with '%s'...", FRIEND_NAME)
        chat_xpath = f"//*[normalize-space(text())='{FRIEND_NAME}']"
        chat = wait.until(EC.element_to_be_clickable((By.XPATH, chat_xpath)))
        safe_click(driver, chat)
        log.info("Chat opened.")

        wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "[contenteditable='true']")) > 0
        )
        boxes = driver.find_elements(By.CSS_SELECTOR, "[contenteditable='true']")
        chat_input = boxes[-1]
        safe_click(driver, chat_input)
        chat_input.send_keys(MESSAGE)
        chat_input.send_keys(Keys.ENTER)

        # Short pause so the message is actually sent before closing the browser.
        time.sleep(2)
        log.info("Message sent.")
    except Exception:
        screenshot = BASE_DIR / "error.png"
        try:
            driver.save_screenshot(str(screenshot))
            log.error("Screenshot saved to %s", screenshot)
        except Exception:
            pass
        raise
    finally:
        driver.quit()


def main():
    if already_sent_today():
        log.info("Already sent today. Nothing to do.")
        return

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info("Attempt %d of %d", attempt, MAX_RETRIES)
            send_once()
            mark_sent()
            return
        except TimeoutException:
            log.error("Timed out waiting for a page element (chat name or input box).")
        except Exception as exc:
            log.error("Error: %s", exc)
        if attempt < MAX_RETRIES:
            time.sleep(10)

    log.error("All attempts failed.")


if __name__ == "__main__":
    main()