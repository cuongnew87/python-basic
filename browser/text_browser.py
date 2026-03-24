import requests
from bs4 import BeautifulSoup

def simple_text_browser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) TextBrowser/1.0'
    }
    
    try:
        # 1. Tải nội dung trang web
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 2. Parse HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Loại bỏ các thành phần không phải nội dung (script, style)
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # 3. Lấy tiêu đề và nội dung văn bản
        title = soup.title.string if soup.title else "No Title"
        text = soup.get_text(separator='\n')
        
        # Làm sạch khoảng trắng
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)

        print(f"=== TIÊU ĐỀ: {title} ===")
        print("-" * 30)
        print(clean_text[:2000]) # In ra 2000 ký tự đầu tiên
        print("-" * 30)
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    url = input("Nhập URL (ví dụ https://vietnamnet.vn): ")
    if not url.startswith('http'):
        url = 'https://' + url
    simple_text_browser(url)