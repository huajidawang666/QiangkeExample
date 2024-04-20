from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time
import ddddocr

username = "..."
password = "..."
url = "..." 

# XPath(s)

login = "/html/body/div[1]/div[2]/div[1]/form/div[2]/div[5]/a" # 登录按钮

checkbox = "//*[@id=\"userAgreement\"]/i" # 用户协议复选框
slide = "/html/body/div[4]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]" # 抠出来的图片
crop = "/html/body/div[4]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]" # 验证码背景
slide_button = "/html/body/div[4]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]" # 滑块
sec_button = "/html/body/div[2]/div/div[1]/section[2]/div/div/ul/li[1]/p/span" # 二级目录

# 识别验证码
def Identify_verifi_code(driver):
    time.sleep(2)
    driver.save_screenshot(".\qiangke.png")
    screenshot = Image.open(".\qiangke.png")
    crop_png = driver.find_element(By.XPATH, crop)
    loc = crop_png.location
    region = screenshot.crop((loc['x']+80, loc['y'], loc['x']+crop_png.size['width'], loc['y']+crop_png.size['height']))  #//对获取的截图进行裁剪
    region.save('.\qiangke_crop.png')  # 保存裁剪后的图片

    slide_png = driver.find_element(By.XPATH, slide)
    slide_loc = slide_png.location
    region2 = screenshot.crop((slide_loc['x'], slide_loc['y'], slide_loc['x']+slide_png.size['width'], slide_loc['y']+slide_png.size['height']))
    region2.save('.\qiangke_slide.png')

    ocr = ddddocr.DdddOcr(det=True)  # 导入验证码识别
    with open(".\qiangke_crop.png", "rb") as f:
        background_bytes = f.read()
    with open(".\qiangke_slide.png", "rb") as f:
        slide_bytes = f.read()
    res = ocr.slide_match(slide_bytes, background_bytes, simple_target=True)  #//将识别出来的验证码赋给res
    # print(res)
    return res
    
# 模拟登陆打卡
def do_login(driver):
    driver.maximize_window() #将窗口最大化

    # 找到登录框 输入账号密码
    driver.find_element(By.ID, 'username').send_keys(username)# 输入用户名
    driver.find_element(By.ID, 'password').send_keys(password)# 输入密码

    driver.find_element(By.XPATH, checkbox).click() # 点击同意用户协议
    driver.find_element(By.XPATH, login).click() # 点击登录

    result = Identify_verifi_code(driver) # 识别验证码

    move = ActionChains(driver)
    move.click_and_hold(driver.find_element(By.XPATH, slide_button)).move_by_offset(result['target'][0]+80, 0).release().perform() # 移动滑块

    wait = WebDriverWait(driver, 20) #20秒内每隔500毫秒扫描1次页面变化，当出现指定的元素后结束。
    wait.until(lambda driver: driver.find_element(By.XPATH, sec_button))
    driver.find_element(By.XPATH, sec_button).click()#点击培养管理

    time.sleep(10)
    
    count = 0
    
    while True:
        count = count + 1
        print(count, end = " ")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div[3]/table/tbody/tr[5]/td[10]/div/button/span")
        time.sleep(0.5)

if __name__ == '__main__':
    # 模拟浏览器打开网站
    # 添加参数
    options = Options()
    # 关闭沙盒启动
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options = options)
    driver.get(url)

    # 登录并查询
    try:
        do_login(driver)
    except:
        driver.quit()
        driver = webdriver.Chrome(options = options)
        driver.get(url)
        do_login(driver)    
