import argparse
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def submit_text(url, input_selector, text, button_selector, success_selector, download_dir, headless=False, timeout_ms=60000):
    """Returns the saved file's path, or None if the conversion or the download did not happen."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = browser.new_page()
        page.goto(url)

        page.fill(input_selector, text)
        page.click(button_selector)

        try:
            page.wait_for_selector(success_selector, state="visible", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            browser.close()
            return None

        try:
            with page.expect_download(timeout=timeout_ms) as download_info:
                page.click(success_selector)
            download = download_info.value
            saved = Path(download_dir) / download.suggested_filename
            saved.parent.mkdir(parents=True, exist_ok=True)
            download.save_as(saved)
        except PlaywrightTimeoutError:
            saved = None

        browser.close()
        return saved


def main():
    parser = argparse.ArgumentParser(description="Type text into a page's input box, click its button, and download the result.")
    parser.add_argument("url", help="Page to open")
    parser.add_argument("text", help="Text to type into the input box")
    parser.add_argument("--input", default="#link", help="CSS selector of the input box")
    parser.add_argument("--button", default=".form__actions button[type=submit]", help="CSS selector of the button")
    parser.add_argument("--headless", action="store_true", help="Run without showing the browser window")
    parser.add_argument("--success", default="button.download", help="CSS selector of the Download button that appears when the job is done")
    parser.add_argument("--timeout", type=int, default=60000, help="Milliseconds to wait for the Download button and for the file")
    parser.add_argument("--out", default=str(Path(__file__).parent / "downloads"), help="Folder to save the downloaded file in")
    args = parser.parse_args()

    saved = submit_text(args.url, args.input, args.text, args.button, args.success, args.out, args.headless, args.timeout)
    if saved:
        print(f"Success: saved {saved}")
    else:
        print("Failed: no file was downloaded.")
    raise SystemExit(0 if saved else 1)


if __name__ == "__main__":
    main()
