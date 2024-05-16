import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://m.weibo.cn/")
    page.get_by_placeholder("大家都在搜：歌手踢馆").fill("长江电力")
    page.locator("li").filter(has_text="实时").locator("span").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
