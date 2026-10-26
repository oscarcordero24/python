import argparse

from playwright.sync_api import sync_playwright


def submit_text(url, input_selector, text, button_selector, headless=False, wait_ms=5000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)

        page.fill(input_selector, text)
        page.click(button_selector)

        page.wait_for_timeout(wait_ms)
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Type text into a page's input box and click its button.")
    parser.add_argument("url", help="Page to open")
    parser.add_argument("text", help="Text to type into the input box")
    parser.add_argument("--input", default="input[type=text]", help="CSS selector of the input box")
    parser.add_argument("--button", default="button:has-text('Go')", help="CSS selector of the button")
    parser.add_argument("--headless", action="store_true", help="Run without showing the browser window")
    parser.add_argument("--wait", type=int, default=5000, help="Milliseconds to wait after clicking")
    args = parser.parse_args()

    submit_text(args.url, args.input, args.text, args.button, args.headless, args.wait)


if __name__ == "__main__":
    main()
