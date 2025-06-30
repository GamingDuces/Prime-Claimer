from playwright.sync_api import sync_playwright

URL = "https://gaming.amazon.com/home"


def fetch_covers():
    """Return cover image URLs for claimable games only."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        try:
            page.goto(URL)
            page.wait_for_load_state("networkidle")
            images = page.eval_on_selector_all(
                "div:has-text('Claim')",
                "els => els.map(el => {\n"
                "  if (el.innerText.toLowerCase().includes('luna')) return null;\n"
                "  const img = el.querySelector('img');\n"
                "  return img && img.src ? img.src : null;\n"
                "}).filter(Boolean)"
            )
        except Exception:
            images = []
        finally:
            browser.close()
    return images


if __name__ == "__main__":
    for src in fetch_covers():
        print(src)
