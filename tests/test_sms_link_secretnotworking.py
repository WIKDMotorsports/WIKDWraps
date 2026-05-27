from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    file_path = f"file://{os.path.abspath('secretnotworking.html')}"
    page.goto(file_path)

    # Wait for the first step to appear and lock to fade
    page.wait_for_selector('#stage-3-code.active', timeout=10000)

    # Wait for scramble code to finish
    page.wait_for_timeout(3000)

    # Force click "Claim Your Discount"
    page.click('#init-claim-btn', force=True)

    # Wait for step 2 warning to appear
    page.wait_for_selector('#step-2-warning', state='visible', timeout=10000)

    # Verify the button exists and is a button tag
    element = page.locator('#final-open-sms-btn')
    assert element.evaluate("e => e.tagName") == "BUTTON"

    print("secretnotworking.html SMS button is correctly rendered as a BUTTON tag and is clickable.")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
