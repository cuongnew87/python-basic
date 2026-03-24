import httpx
import asyncio

async def fetch_http2():
    # Khởi tạo client hỗ trợ HTTP/2
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    
    async with httpx.AsyncClient(http2=True, limits=limits) as client:
        # Kiểm tra phiên bản HTTP đang sử dụng
        response = await client.get("https://www.google.com")
        print(f"Phiên bản HTTP: {response.http_version}") # Sẽ in ra HTTP/2
        
        # Mô phỏng Multiplexing: Gửi nhiều request cùng lúc trên 1 kết nối
        tasks = [
            client.get("https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"),
            client.get("https://www.google.com/services/"),
            client.get("https://www.google.com/intl/en/about/")
        ]
        
        results = await asyncio.gather(*tasks)
        for res in results:
            print(f"Đã tải {res.url} - Status: {res.status_code}")

if __name__ == "__main__":
    asyncio.run(fetch_http2())