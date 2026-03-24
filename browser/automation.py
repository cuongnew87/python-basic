import asyncio
from playwright.async_api import async_playwright

async def run_automation():
    async with async_playwright() as p:
        # Mở trình duyệt Chromium (headed=True để bạn nhìn thấy nó chạy)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Đi đến trang web
        print("--- Đang truy cập trang web ---")
        await page.goto("https://www.google.com")

        # 2. Tương tác: Nhập từ khóa tìm kiếm
        # 'textarea[name="q"]' là selector của ô tìm kiếm Google
        await page.fill('textarea[name="q"]', "Lập trình Python Automation")
        await page.press('textarea[name="q"]', "Enter")

        # 3. Đợi trang kết quả tải xong
        await page.wait_for_load_state("networkidle")

        # 4. Chụp ảnh màn hình kết quả
        await page.screenshot(path="google_search.png")
        print("--- Đã chụp ảnh màn hình thành công! ---")

        # Đóng trình duyệt
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())