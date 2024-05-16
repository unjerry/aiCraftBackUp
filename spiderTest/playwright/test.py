import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time


async def ro(page):
    for _ in range(1000):
        # time.sleep(1.0)
        await page.mouse.wheel(0, 1000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://m.weibo.cn/")
    page.locator(
        "//html//body//div//div[1]//div[1]//div[1]//a//aside//label//div"
    ).click()
    page.locator(
        "//html//body//div//div[1]//div[1]//div[1]//div//div//div[2]//form//input"
    ).fill("易烊千玺")
    page.locator(
        "//html//body//div//div[1]//div[1]//div[1]//div//div//div[2]//form//input"
    ).press("Enter")
    page.locator("li").filter(has_text="实时").locator("span").click()
    page.mouse.wheel(0, 1000)
    for _ in range(1000):
        # time.sleep(1.0)
        page.mouse.wheel(0, 1000)
    # # ---------------------
    time.sleep(500)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
