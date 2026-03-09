# tests/test_ui.py
import osmkdir -p certs
from pages.wallester_page import WallesterPage

def test_navigate_to_api_docs_via_footer(page):
    """
    Test Case: Verify navigation to API Documentation from the footer.
    Goal: Ensure the 'API documentation' link opens the correct external site.
    """
    wallester = WallesterPage(page)
    
    # 1. Open Home Page
    wallester.open()
    
    # 2. Handle Cookies
    wallester.accept_cookies()
    
    # 3. Click the footer link and capture the new tab
    # The method now uses JS click for maximum stability
    new_tab = wallester.click_footer_api_docs()
    
    # 4. Wait for the new page to stabilize
    new_tab.wait_for_load_state("networkidle")
    
    # 5. Advanced URL Validation
    actual_url = new_tab.url
    expected_base_url = "https://api-doc.wallester.com/"
    
    print(f"\n[VERIFICATION] Target tab URL: {actual_url}")
    
    # We check that the URL starts with the correct domain
    assert actual_url.startswith(expected_base_url), f"Expected URL to start with {expected_base_url}, but got {actual_url}"
    
    # Check if the page title contains "Wallester" to be 100% sure it's the right site
    page_title = new_tab.title()
    print(f"[VERIFICATION] Page Title: {page_title}")
    assert "Wallester" in page_title
    # 5. Screenshot
    # Create folder for screenshots
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        
    screenshot_path = "screenshots/api_docs_success.png"
    new_tab.screenshot(path=screenshot_path, full_page=True)
    
    print(f"[SUCCESS] Скриншот сохранен: {screenshot_path}")