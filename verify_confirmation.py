from playwright.sync_api import sync_playwright
import os

def capture_screenshot():
    file_path = f"file://{os.path.abspath('Confirmation.html')}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_path)
        page.wait_for_timeout(2000)
        page.screenshot(path="confirmation_screenshot.png", full_page=True)
        browser.close()

if __name__ == "__main__":
    capture_screenshot()
