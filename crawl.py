from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # 引入 By 類

import time

def crawl_info(website,postdata):    
    driver = webdriver.Chrome()
    '''
    service = Service(executable_path="C:\\Users\\yo030\\Desktop\\web_project\\chromedriver-win32\\chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    '''

    # 前往頁面
    driver.get(website)

    for key in postdata:
    # 輸入帳號和密碼並按下登入按鈕
        input = driver.find_element(By.ID, key)  # 使用 By.ID 定位元素
        #password_input = driver.find_element(By.ID, "password")  # 使用 By.ID 定位元素

        input.send_keys(postdata[key])
        #password_input.send_keys(password)
    input.send_keys(Keys.RETURN)
    '''
    # 前往你想要爬取的目標頁面
    target_page_url = "https://ais3.org/Account/Info"  # 換成你想要爬取的目標頁面的代號，例如: https://www.facebook.com/groups/your_group_id/
    driver.get(target_page_url)
    '''
    # 取得目標頁面的 HTML
    #time.sleep(5)
    html = driver.page_source
    return(html)
    # 將HTML內容寫入HTML檔案
    '''
    output_file = "./templates/fake_info.html"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML內容已儲存至 {output_file}")
    '''