from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

def get_final_url(short_url):
    response = requests.head(short_url,allow_redirects=True)
    return response.url

def get_link_list(key_lists):
    # 创建无头浏览器对象
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Windows系统需要这个选项
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()

    link_lists = []
    try:
        # 打开Baidu网站
        driver.get("https://www.baidu.com/")
        time.sleep(1)
        print(driver.title,"open baidu successfully")
        for key in key_lists:
            search_box = driver.find_element(By.ID, "kw")
            search_box.clear()  # 清空搜索框
            search_box.send_keys(key)
            driver.find_element(By.ID, "su").click()
            time.sleep(1)
            print("search for key: ",key)
            results = driver.find_elements(By.CSS_SELECTOR, "h3.t>a")
            for result in results:
                link = get_final_url(result.get_attribute('href'))
                # 过滤掉以 'https://www.baidu.com/sf/vsearch?' 开头的链接
                if not link.startswith("https://www.baidu.com/sf/vsearch?") and not link.startswith("https://image.baidu.com/") and not link.startswith("https://image.baidu.com/search/index?") and "qqtn" not in link and "wappass" not in link:
                    link_lists.append(link)
                    print(link)
    except Exception as e:
        print(f"An error occured:{e}")
    finally:
        # 关闭浏览器
        driver.quit()
    print(link_lists)
    return link_lists

if __name__ == "__main__":
    print(get_link_list(["星露谷 阿比盖尔","星露谷 钓鱼"]))