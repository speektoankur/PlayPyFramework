from playwright.sync_api import Page, expect


class BrowsingHistory:
    def __init__(self, page: Page):
        self.page = page
        # Define locators for each element
        self.search_input = self.page.get_by_placeholder("Looking for something?")
        self.search_button = self.page.get_by_role("button", name="Search", exact=True)
        self.search_by_keyword = self.page.get_by_label("Search by keyword")
        self.clear_search = self.page.get_by_label("Clear search")

    def perform_search(self, query: str):
        # Click, fill, and submit search
        self.search_input.click()
        self.search_input.fill(query)
        self.search_button.click()

    def verify_search_results_visible(self, query: str):
        # Verify the search results heading is visible
        expected_value = f'Search results for "{query}"'
        expect(self.page.get_by_role("heading", name=expected_value)).to_be_visible()

    def clear_search_field(self):
        # Click the clear search and search by keyword
        self.search_by_keyword.click()
        self.clear_search.click()
        self.search_by_keyword.click()
