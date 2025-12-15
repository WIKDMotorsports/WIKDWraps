from playwright.sync_api import sync_playwright
import os

def check_page(page, url, name):
    print(f"Checking {name}...")
    page.goto(url)
    # Scroll to the bottom to find the CTA
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # Wait for the gradient element to be visible
    # Ideally find the section with the gradient.
    # The gradient is pseudo-element, so we check if the wrapper is there.
    wrapper = page.locator(".car-composite-wrapper")
    wrapper.scroll_into_view_if_needed()

    # Take screenshot of the wrapper area
    # We might want a bit more context
    page.screenshot(path=f"verification/{name}.png")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # We can use file:// protocol for local HTML files
        cwd = os.getcwd()

        check_page(page, f"file://{cwd}/Ceramic Coatings.html", "ceramic_coatings")
        check_page(page, f"file://{cwd}/index.html", "index")
        check_page(page, f"file://{cwd}/Maintenance Plans.html", "maintenance")
        check_page(page, f"file://{cwd}/Our Services.html", "our_services")
        check_page(page, f"file://{cwd}/Tint.html", "tint")

        browser.close()

if __name__ == "__main__":
    main()
