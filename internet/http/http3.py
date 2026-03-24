import httpx
import asyncio

async def fetch_http3():
    # Sử dụng AsyncClient mặc định (hỗ trợ HTTP/1.1 và HTTP/2)
    # Nó sẽ tự nâng cấp lên HTTP/3 nếu Server yêu cầu
    async with httpx.AsyncClient() as client:
        try:
            # Truy vấn Cloudflare - một trong những bên hỗ trợ h3 tốt nhất
            url = "https://www.cloudflare.com"
            response = await client.get(url)
            
            print(f"--- Kết quả ---")
            print(f"URL: {response.url}")
            print(f"Status: {response.status_code}")
            
            # Kiểm tra xem Server có hỗ trợ HTTP/3 không qua Header Alt-Svc
            alt_svc = response.headers.get("alt-svc")
            if alt_svc:
                print(f"Server hỗ trợ HTTP/3: {alt_svc}")
                # Thường thì trình duyệt sẽ dùng h3 ở lần request thứ 2
            else:
                print("Server này chưa hỗ trợ hoặc chưa bật HTTP/3.")

            # Kiểm tra phiên bản hiện tại đang dùng (thường là HTTP/2 ở lần đầu)
            print(f"Phiên bản đang dùng: {response.http_version}")

        except Exception as e:
            print(f"Lỗi: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_http3())