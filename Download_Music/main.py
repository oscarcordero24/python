import argparse
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

PAGE_URL = "https://the-site.com"

HERE = Path(__file__).parent


def read_inputs(path):
    lines = (line.strip() for line in Path(path).read_text().splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def unique_path(folder, name):
    path = Path(folder) / name
    n = 2
    while path.exists():
        path = Path(folder) / f"{path.stem.rsplit(' (', 1)[0]} ({n}){Path(name).suffix}"
        n += 1
    return path


def convert_and_download(browser, url, text, input_selector, button_selector, success_selector, download_dir, timeout_ms):
    """Returns the saved file's path, or None if the conversion or the download did not happen."""
    page = browser.new_page()
    try:
        page.goto(url)
        page.fill(input_selector, text)
        page.click(button_selector)
        page.wait_for_selector(success_selector, state="visible", timeout=timeout_ms)

        with page.expect_download(timeout=timeout_ms) as download_info:
            page.click(success_selector)
        download = download_info.value

        saved = unique_path(download_dir, download.suggested_filename)
        saved.parent.mkdir(parents=True, exist_ok=True)
        download.save_as(saved)
        return saved
    except PlaywrightTimeoutError:
        return None
    finally:
        page.close()


def main():
    parser = argparse.ArgumentParser(description="Type each line of a text file into a page's input box, click its button, and download the result.")
    parser.add_argument("--url", default=PAGE_URL, help="Page to open (default: PAGE_URL at the top of this file)")
    parser.add_argument("--inputs", default=str(HERE / "inputs.txt"), help="Text file with one entry per line")
    parser.add_argument("--input", default="#link", help="CSS selector of the input box")
    parser.add_argument("--button", default=".form__actions button[type=submit]", help="CSS selector of the button")
    parser.add_argument("--headless", action="store_true", help="Run without showing the browser window")
    parser.add_argument("--success", default="button.download", help="CSS selector of the Download button that appears when the job is done")
    parser.add_argument("--timeout", type=int, default=60000, help="Milliseconds to wait for the Download button and for the file")
    parser.add_argument("--out", default=str(HERE / "downloads"), help="Folder to save the downloaded files in")
    args = parser.parse_args()

    entries = read_inputs(args.inputs)
    if not entries:
        raise SystemExit(f"No entries found in {args.inputs}")

    failed = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=args.headless,
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled"],
        )
        for i, text in enumerate(entries, start=1):
            print(f"[{i}/{len(entries)}] {text} ... ", end="", flush=True)
            saved = convert_and_download(
                browser, args.url, text, args.input, args.button, args.success, args.out, args.timeout
            )
            if saved:
                print(f"saved {saved}")
            else:
                print("FAILED")
                failed.append(text)
        browser.close()

    print(f"\nDone: {len(entries) - len(failed)} of {len(entries)} downloaded.")
    if failed:
        print("Failed: " + ", ".join(failed))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
