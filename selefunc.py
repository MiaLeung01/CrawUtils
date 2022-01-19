import os
import time
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import random


def initDriver():
  # #chromedriver的路径
  chromedriver = r"D:\chromedriver.exe"
  os.environ["webdriver.chrome.driver"] = chromedriver
  #设置chrome开启的模式，headless就是无界面模式
  #一定要使用这个模式，不然截不了全页面，只能截到你电脑的高度
  chrome_options = Options()
  # chrome_options.add_argument('--window-size=1920,1080')
  # chrome_options.add_argument('headless')
  # 反爬 Chrome 正受到自动测试软件的控制。
  chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
  # 反爬 WebDriver (New) present (failed)
  chrome_options.add_argument('--disable-blink-features=AutomationControlled')
  #下载路径
  downloadConfig = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': os.path.join(os.getcwd(), 'result', 'file')
  }
  driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
  driver.maximize_window()
  
  # 反爬 webdriver = true
  driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => false
      })
    """
  })
  # with open('./stealth.min.js') as f:
  #   js = f.read()

  # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  #     "source": js
  # })
  return driver

# res = isElementPresent("id", "query")
def isElementPresent(driver, by, value):
  # 从selenium.common.exceptions模块导入NoSuchElementException异常类
  from selenium.common.exceptions import NoSuchElementException
  try:
    element = driver.find_element(by=by, value=value)
  except NoSuchElementException as e:
    # 打印异常信息
    print(e)
    # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
    return False
  else:
    # 没有发生异常，表示在页面中找到了该元素，返回元素
    return element

# selenium 裁剪图片
def crop_image(driver, element):
# 获取验证码图片在网页中的位置
  left = int(element.location['x'])  # 获取图片左上角坐标x
  top = int(element.location['y'])  # 获取图片左上角y
  right = int(left + element.size['width'])  # 获取图片右下角x
  bottom = int(top + element.size['height'])  # 获取图片右下角y
  print(left, top)
  # 通过Image处理图像
  filename = os.getcwd() + '\\' + str(random.random()) + '.png'  # 生成随机文件名
  print (filename)
  driver.save_screenshot(filename)  # 截取当前窗口并保存图片
  im = Image.open(filename)  # 打开图片
  im = im.crop((left, top, right, bottom))  # 截图验证码
  im.save(filename)  # 保存验证码图片


from PIL import ImageGrab

def img_path(folder, index, name):
  save_path = os.path.join(os.getcwd(), 'jiangsu', folder)
  if not os.path.exists(save_path):
    os.makedirs(save_path)
  save_name = str(index + 1) + '.' + name + '.png'
  return save_path + '\\' + save_name

# 截电脑屏幕
def screenshot_file_save(folder, index, name):
  path = img_path(folder, index, name)
  im = ImageGrab.grab()
  im.save(path, 'png')


# 截网页全屏
def screenshot_full_page(driver, path):
  time.sleep(1)
  #接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
  width = driver.execute_script("return document.documentElement.scrollWidth")
  height = driver.execute_script("return document.documentElement.scrollHeight")
  print(width,height)
  #将浏览器的宽高设置成刚刚获取的宽高
  driver.set_window_size(width, height)
  time.sleep(1)
  #截图并关掉浏览器
  driver.save_screenshot(path)

# 获取元素内容
# element.text