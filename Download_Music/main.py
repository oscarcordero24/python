import argparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def submit_text(url, input_selector, text, button_selector, success_selector, headless=False, timeout_ms=60000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)

        page.fill(input_selector, text)
        page.click(button_selector)

        try:
            page.wait_for_selector(success_selector, state="visible", timeout=timeout_ms)
            is_success = True
        except PlaywrightTimeoutError:
            is_success = False

        page.screenshot(path="result.png")
        browser.close()
        return is_success


def main():
    parser = argparse.ArgumentParser(description="Type text into a page's input box and click its button.")
    parser.add_argument("url", help="Page to open")
    parser.add_argument("text", help="Text to type into the input box")
    parser.add_argument("--input", default="#link", help="CSS selector of the input box")
    parser.add_argument("--button", default=".form__actions button[type=submit]", help="CSS selector of the button")
    parser.add_argument("--headless", action="store_true", help="Run without showing the browser window")
    parser.add_argument("--success", default="button.download", help="CSS selector that appears when the job is done")
    parser.add_argument("--timeout", type=int, default=60000, help="Milliseconds to wait for the success element")
    args = parser.parse_args()

    is_success = submit_text(args.url, args.input, args.text, args.button, args.success, args.headless, args.timeout)
    print("Success: the Download button appeared." if is_success else "Failed: the Download button never appeared.")
    raise SystemExit(0 if is_success else 1)


if __name__ == "__main__":
    main()
