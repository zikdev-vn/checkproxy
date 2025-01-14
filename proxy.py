import requests
import time
import os

# URL của file chứa danh sách proxy
proxy_url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"

# Tải file proxy về
def download_proxy_file(url, output_file="data.txt"):
    if os.path.exists(output_file):
        os.remove(output_file)  
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        with open(output_file, "w") as file:
            file.write(response.text)
        print(f"Tải file proxy thành công: {output_file}")
    except Exception as e:
        print(f"Lỗi khi tải file proxy: {e}")

# Đọc danh sách proxy từ file
def read_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Kiểm tra proxy và lưu trực tiếp vào file nếu hoạt động
def check_and_save_proxy(proxy, output_file):
    test_url = "http://httpbin.org/ip"  
    proxies = {"http": proxy, "https": proxy}
    try:
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=5)
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            print(f"Proxy {proxy} hoạt động - Tốc độ: {elapsed_time:.2f} giây")
            # Ghi proxy hoạt động vào file
            with open(output_file, "a") as file:
                file.write(proxy + "\n")
    except Exception as e:
        print(f"Proxy {proxy} không hoạt động - Lỗi: {e}")

if __name__ == "__main__":
    proxy_file = "data.txt"
    output_file = "working_proxies.txt"

    
    if os.path.exists(output_file):
        os.remove(output_file)

    download_proxy_file(proxy_url, proxy_file)

    proxies_list = read_proxies(proxy_file)

    for proxy in proxies_list:
        check_and_save_proxy(proxy, output_file)

    print(f"\nKiểm tra hoàn tất. Proxy hoạt động được lưu trong file: {output_file}")

