import os
import json
from datetime import datetime
from pathlib import Path

import pyotp
from playwright.sync_api import sync_playwright
from apprise import Apprise

URL_HOME = "https://gaming.amazon.com/home"
LOG_FILE = Path(os.getenv("AMZ_LOGFILE", "data/prime-gaming.json"))


def login(page, email, password, otp_key=None):
    page.goto(URL_HOME)
    page.wait_for_load_state("networkidle")
    # Accept cookies if banner present
    try:
        page.click('[aria-label="Cookies usage disclaimer banner"] button:has-text("Accept")', timeout=5000)
    except Exception:
        pass
    if page.locator('button:has-text("Sign in")').count():
        page.click('button:has-text("Sign in")')
        page.fill('[name=email]', email)
        page.click('input[type="submit"]')
        page.fill('[name=password]', password)
        page.click('input[type="submit"]')
        if otp_key:
            try:
                page.wait_for_selector('input[name=otpCode]', timeout=10000)
                otp = pyotp.TOTP(otp_key).now()
                page.fill('input[name=otpCode]', otp)
                page.click('input[type="submit"]')
            except Exception:
                pass
        page.wait_for_url('**/home?signedIn=true', timeout=60000)


def claim_games(page):
    claimed = []
    page.click('button[data-type="Game"]').catch(lambda _: None)
    cards = page.locator('div[data-a-target="offer-list-FGWP_FULL"] div:has-text("Claim")')
    count = cards.count()
    for i in range(count):
        card = cards.nth(i)
        title = card.locator('.item-card-details__body__primary').inner_text()
        card.click()
        page.wait_for_load_state('networkidle')
        try:
            page.click('[data-a-target="buy-box"] .tw-button:has-text("Get game")', timeout=5000)
        except Exception:
            try:
                page.click('[data-a-target="buy-box"] .tw-button:has-text("Claim")', timeout=5000)
            except Exception:
                pass
        claimed.append(title)
        page.goto(URL_HOME)
        page.wait_for_load_state('networkidle')
        page.click('button[data-type="Game"]').catch(lambda _: None)
    return claimed


def log_claims(user, titles):
    if not titles:
        return
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LOG_FILE.exists():
        try:
            data = json.loads(LOG_FILE.read_text())
        except Exception:
            data = {}
    else:
        data = {}
    user_data = data.setdefault(user, {})
    now = datetime.utcnow().isoformat()
    for title in titles:
        user_data[title] = {"title": title, "time": now}
    LOG_FILE.write_text(json.dumps(data, indent=2))


def notify_claims(titles):
    notify_url = os.getenv("AMZ_NOTIFY")
    if not notify_url or not titles:
        return
    apobj = Apprise()
    apobj.add(notify_url)
    msg = "Claimed:\n" + "\n".join(f"- {t}" for t in titles)
    apobj.notify(body=msg, title="Prime Gaming")


def main():
    email = os.getenv("AMZ_EMAIL")
    password = os.getenv("AMZ_PASSWORD")
    otp_key = os.getenv("AMZ_OTPKEY")
    headless = os.getenv("HEADLESS", "1") != "0"
    if not email or not password:
        print("Missing AMZ_EMAIL/AMZ_PASSWORD env variables")
        return
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        login(page, email, password, otp_key)
        claimed = claim_games(page)
        if claimed:
            print("Claimed:")
            for t in claimed:
                print("-", t)
            log_claims(email, claimed)
            notify_claims(claimed)
        else:
            print("No claimable games found")
        browser.close()


if __name__ == "__main__":
    main()
