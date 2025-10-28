from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the root URL using the explicit hash format
        page.goto("http://localhost:5173/#/")

        # 1. Verify the main heading on the login page is visible
        heading = page.get_by_role("heading", name="Отслеживание производства EVE Online")
        expect(heading).to_be_visible()

        # 2. Verify the "Login with EVE" button is visible and has the correct link
        login_link = page.get_by_role("link", name="Войти через EVE")
        expect(login_link).to_be_visible()
        expect(login_link).to_have_attribute("href", "http://localhost:5000/sso/login")

        # 3. Take a screenshot for visual confirmation of the login page
        page.screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()