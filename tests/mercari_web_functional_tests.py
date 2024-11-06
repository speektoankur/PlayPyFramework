import pytest

from pages.browsing_history_generator import BrowsingHistory
from playwright.sync_api import Page, expect


@pytest.fixture
def browsing_history_page(page):
    return BrowsingHistory(page)


def test_validate_product_search(page):
    page.goto("https://jp.mercari.com")

    page.get_by_placeholder("なにをお探しですか？").click()
    page.get_by_text("カテゴリーからさがす").click()
    page.locator(
        "//div/a[contains(text(),'本・雑誌・漫画')]/ancestor::div[@data-testid='merListItem-container']").click()
    page.wait_for_load_state('load')
    page.wait_for_url("https://jp.mercari.com/categories?category_id=5")
    page.locator("//div/a[contains(text(),'本')]/ancestor::div[@data-testid='merListItem-container']").click()
    page.wait_for_url("https://jp.mercari.com/categories?category_id=72")
    page.locator("//div/a[contains(text(),'コンピュータ・IT')]/parent::div").click()
    page.wait_for_timeout(4000)
    # Selected Products Assertions
    expect(page.get_by_test_id("chip-label")).to_have_text("本 コンピュータ・IT")
    expect(page.locator("//span[contains(text(),'コンピュータ・IT')]/ancestor::label/input")).to_be_checked()


def test_validate_search_history(page, browsing_history_page):
    page.goto("https://jp.mercari.com/")
    button = page.get_by_role("navigation").get_by_role("button", name="日本語")
    expect(button).to_be_visible()
    page.get_by_role("navigation").get_by_role("button", name="日本語").click()
    page.get_by_test_id("preferences-selector-option-en").check()
    page.get_by_role("button", name="言語と通貨を更新する").click()
    page.wait_for_timeout(1000)
    # FIRST search
    browsing_history_page.perform_search("Computers & Technology")
    browsing_history_page.verify_search_results_visible("Computers & Technology")
    browsing_history_page.clear_search_field()
    page.wait_for_timeout(1000)
    # SECOND search
    browsing_history_page.perform_search("javascript")
    browsing_history_page.verify_search_results_visible("javascript")
    browsing_history_page.clear_search_field()
    expect(page.get_by_test_id("search-history").get_by_role("link", name="Computers & Technology")).to_be_visible()
    expect(page.get_by_test_id("search-history").get_by_role("link", name="javascript")).to_be_visible()
    expect(page.get_by_test_id("search-history").get_by_role("link")).to_have_count(2)
