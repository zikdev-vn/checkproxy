import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor

# URL của các file chứa danh sách proxy
proxy_url1 = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"
proxy_url2 = "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/All_proxies.txt"

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

# Kiểm tra proxy nâng cao và ghi vào file nếu hợp lệ
def check_proxy_advanced(proxy, output_file):
    test_url = "https://httpbin.org/ip"  
    real_url = "https://google.com"     
    proxies = {"http": proxy, "https": proxy}
    
    try:
        # Kiểm tra proxy có hoạt động không
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code != 200:
            return False

        # Kiểm tra proxy có thể truy cập web thực tế không
        response = requests.get(real_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} hoạt động tốt!")

            # Ghi ngay proxy hoạt động vào file
            with open(output_file, "a") as file:
                file.write(proxy + "\n")
            return True
    except Exception as e:
        print(f"Proxy {proxy} không hợp lệ: {e}")
    return False

if __name__ == "__main__":
    proxy_file1 = "data1.txt"
    proxy_file2 = "data2.txt"
    output_file = "proxies.txt"

    # Xóa file cũ nếu tồn tại
    for file in [proxy_file1, proxy_file2, output_file]:
        if os.path.exists(file):
            os.remove(file)
    time.sleep(3)
    # Tải danh sách proxy từ cả hai URL
    download_proxy_file(proxy_url1, proxy_file1)
    download_proxy_file(proxy_url2, proxy_file2)
    time.sleep(5)
    # Đọc danh sách proxy từ cả hai file đã tải
    proxies_list1 = read_proxies(proxy_file1)
    proxies_list2 = read_proxies(proxy_file2)
    time.sleep(3)
    
    all_proxies = proxies_list1 + proxies_list2

    # Kiểm tra proxy 
    max_threads = 50
    with ThreadPoolExecutor(max_threads) as executor:
        executor.map(lambda proxy: check_proxy_advanced(proxy, output_file), all_proxies)

    print(f"\nKiểm tra hoàn tất. Proxy hoạt động được lưu trong file: {output_file}")
