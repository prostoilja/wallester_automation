from pages.base_page import BasePage

class WallesterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://wallester.com/"
        
        # Locators
        self.accept_all_btn = page.get_by_role("button", name="Accept all")
        # Standard Playwright recommended locator
        self.api_docs_footer_link = page.get_by_role("link", name="API documentation")

    def open(self):
        """Navigate to the home page"""
        self.navigate(self.url)

    def accept_cookies(self):
        """Handle the cookie consent banner if it appears"""
        if self.accept_all_btn.is_visible():
            print("[UI] Accepting cookie consent...")
            self.accept_all_btn.click()

    def click_footer_api_docs(self):
        """
        Forcefully click the API documentation link using JavaScript 
        to bypass viewport issues.
        """
        print("[UI] Ensuring footer link is present...")
        # Wait until the link is actually in the DOM
        self.api_docs_footer_link.wait_for(state="attached")
        
        print("[UI] Clicking API Documentation link via JS...")
        
        # We still need to catch the new tab
        with self.page.context.expect_page() as new_page_info:
            # Using dispatch_event("click") is more reliable than a mouse click 
            # when elements are 'outside the viewport'
            self.api_docs_footer_link.dispatch_event("click")
        
        return new_page_info.value