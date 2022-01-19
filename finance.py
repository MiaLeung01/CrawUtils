# -*- coding: utf-8 -*-

from selenium.webdriver.support.wait import WebDriverWait
import time
import captchacrack
import selefunc

driver = selefunc.initDriver()

# 1、中国执行公开
def zxgk(arr):
  driver.get('http://zxgk.court.gov.cn/zhzxgk/')
  for i, k in enumerate(arr):
    try:
      input = driver.find_element_by_id('pName')
      input.send_keys(k)
      element = driver.find_element_by_id('captchaImg')  # 定位验证码图片
      element.click()
      time.sleep(2)

      captcha = captchacrack.normal_captcha_crack(element)
      codeInput = driver.find_element_by_name('pCode')
      codeInput.send_keys(captcha)
      time.sleep(1)

      btn = driver.find_element_by_xpath('//*[@id="yzm-group"]/div[6]/button')
      btn.click()
      time.sleep(2)
      selefunc.screenshot_file_save('1、中国执行公开', i, k)
      driver.refresh()
      time.sleep(2)
    except Exception as e:
      print('错误', e)

# 2、国家税务局
def tax(arr):
  for i, k in enumerate(arr):
    url = 'http://www.chinatax.gov.cn/s?siteCode=bm29000002&qt=' + k
    driver.get(url)
    try:
      input = driver.find_element_by_id('qt')
      input.clear()
      input.send_keys(k)
      btn = driver.find_element_by_id('searchBtn')
      btn.click()
      time.sleep(2)
      selefunc.screenshot_file_save('2、国家税务局', i, k)
      time.sleep(2)
    except Exception as e:
      print('tax错误', e)

# 3-1 应急管理部
def yjglb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'https://www.mem.gov.cn/was5/web/sousuo/index.html'
      driver.get(url)
      input = driver.find_element_by_id('key')
      input.clear()
      input.send_keys(k)
      btn = driver.find_element_by_id('query_btn')
      btn.click()
      time.sleep(2)
      selefunc.screenshot_file_save('3-1 应急管理部', i, k)
      time.sleep(2)
    except Exception as e:
      print('tax错误', e)

# 3-2 国家企业信用信息公示
# todo 打印pdf
def gjqyxygs(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.gsxt.gov.cn/'
      driver.get(url)
      input = driver.find_element_by_id('keyword')
      input.clear()
      input.send_keys(k)
      btn = driver.find_element_by_id('btn_query')
      btn.click()
      time.sleep(2)
      selefunc.screenshot_file_save('3-2 国家企业信用信息公示', i, k)
      time.sleep(2)
    except Exception as e:
      print('tax错误', e)

# 3-3 信用中国
# todo 这个点击打开新页
# 还有反爬 = =
def xyzg(arr):
  for i, k in enumerate(arr):
    # url = 'https://www.creditchina.gov.cn/xinyongxinxi/index.html?index=0&scenes=defaultScenario&tableName=credit_xyzx_tyshxydm&searchState=2&entityType=1,2,4,5,6,7,8&keyword=' + k
    url = 'https://www.creditchina.gov.cn/'
    # 反爬
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.implicitly_wait(10)
    driver.get(url)
    try:
      input = driver.find_element_by_id('search_input')
      input.clear()
      input.send_keys(k)
      btn = driver.find_element_by_class_name('search_btn')
      btn.click()
      time.sleep(2)
      handles = driver.window_handles          #获取当前浏览器的所有窗口句柄
      driver.switch_to.window(handles[-1])     #切换到最新打开的窗口
      # li = driver.find_elements_by_xpath('//*[@id="companylists"]/li')
      # print(li)
      # if (li):
      #   li.click()
      #   time.sleep(2)
      #   handles = driver.window_handles          #获取当前浏览器的所有窗口句柄
      #   driver.switch_to.window(handles[-1])     #切换到最新打开的窗口
      #   # driver.switch_to.window(handles[-2])     #切换到倒数第二个打开的窗口
      #   # driver.switch_to.window(handles[0])      #切换到最开始打开的窗口
      #   btn = driver.find_element_by_class_name('download')
      #   btn.click()
      #   time.sleep(5)
    except Exception as e:
      print('tax错误', e)
  

# 4-1 生态环境部
def sthjb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'https://www.mee.gov.cn/searchnew/?searchword=' + k
      driver.get(url)
      selefunc.screenshot_file_save('4-1 生态环境部', i, k)
      time.sleep(2)
    except Exception as e:
      print('sthjb错误', e)

# 5-1 中国工业和信息化部
def gyb(arr):
  url = 'https://www.miit.gov.cn/search/index.html?websiteid=110000000000000'
  driver.get(url)
  for i, k in enumerate(arr):
    try:
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('q')).clear()
      input = driver.find_element_by_id('q')
      input.send_keys(k)
      btn = driver.find_element_by_id('ipt_btn')
      btn.click()
      time.sleep(4)
      selefunc.screenshot_file_save('5-1 中国工业和信息化部', i, k)
      time.sleep(1)
    except Exception as e:
      print('gyb错误', e)

# 6-1 国家外汇管理局
def whj(arr):
  for i, k in enumerate(arr):
    try:
      url = 'https://www.safe.gov.cn/'
      driver.get(url)
      # WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_xpath('//*[@id="title"]')).clear()
      input = driver.find_element_by_xpath('//*[@id="title"]')
      input.send_keys(k)
      btn = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/form/input[4]')
      btn.click()
      time.sleep(4)
      selefunc.screenshot_file_save('6-1 国家外汇管理局', i, k)
      time.sleep(1)
    except Exception as e:
      print('whj错误', e)

# 6-2 中国人民银行
def rmyh(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://wzdig.pbc.gov.cn:8080/search/pcRender?pageId=fa445f64514c40c68b1c8ffe859c649e'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('q')).clear()
      input = driver.find_element_by_id('q')
      input.send_keys(k)
      btn = driver.find_element_by_xpath('//*[@id="mySearchFormAction"]/div/input[2]')
      btn.click()
      time.sleep(4)
      selefunc.screenshot_file_save('6-2 中国人民银行', i, k)
      time.sleep(1)
    except Exception as e:
      print('rmyh 错误', e)

# 6-3 中国银行保险监督管理委员会
def ybj(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.cbirc.gov.cn/cn/view/pages/index/index.html'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('search')).clear()
      input = driver.find_element_by_id('search')
      input.send_keys(k)
      btn = driver.find_element_by_id('goJiansuo')
      btn.click()
      time.sleep(4)
      selefunc.screenshot_file_save('6-3 中国银行保险监督管理委员会', i, k)
      time.sleep(1)
    except Exception as e:
      print('rmyh 错误', e)

# 6-4 中国证监会
def zjh(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.csrc.gov.cn/pub/newsite/'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('schword')).clear()
      input = driver.find_element_by_id('schword')
      input.send_keys(k)
      btn = driver.find_element_by_class_name('so_btn')
      btn.click()
      time.sleep(3)
      selefunc.screenshot_file_save('6-4 中国证监会', i, k)
      time.sleep(1)
    except Exception as e:
      print('zjh 错误', e)
  

# 6-5 中国证监会证券期货市场失信信息公开查询平台
def qh(arr):
  driver.implicitly_wait(10)
  driver.get('https://neris.csrc.gov.cn/shixinchaxun/')
  for i, k in enumerate(arr):
    try:
      input = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/form/div[1]/div/div/input')
      input.send_keys(k)
      element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/form/div[3]/div/div[2]/img')  # 定位验证码图片
      element.click()
      time.sleep(2)

      captcha = captchacrack.normal_captcha_crack(element)
      codeInput = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/form/div[3]/div/div[1]/input')
      codeInput.send_keys(captcha)
      time.sleep(1)

      btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/form/div[3]/div/div[3]/div/span')
      btn.click()
      time.sleep(2)
      selefunc.screenshot_file_save('6-5 中国证监会证券期货市场失信信息公开查询平台', i, k)
      time.sleep(2)
    except Exception as e:
      print('错误', e)

# 6-6 中国国家发展和改革委员会
def fgw(arr):
  for i, k in enumerate(arr):
    try:
      url = 'https://so.ndrc.gov.cn/s?siteCode=bm04000007&ssl=1&token=&qt='
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('qt')).clear()
      input = driver.find_element_by_id('qt')
      input.send_keys(k)
      btn = driver.find_element_by_id('searchBtn')
      btn.click()
      time.sleep(3)
      selefunc.screenshot_file_save('6-6 中国国家发展和改革委员会', i, k)
      time.sleep(1)
    except Exception as e:
      print('fgw 错误', e)
  

# 7-1 市场监督管理总局
def sjj(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.samr.gov.cn/search4/s?searchWord=' + k +'&x=0&y=0&column=%E5%85%A8%E9%83%A8&siteCode=bm30000012'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('fl'))
      selefunc.screenshot_file_save('7-1 市场监督管理总局', i, k)
      time.sleep(2)
    except Exception as e:
      print('sjj 错误', e)
  

# 8-1 盐行业信用管理与公众服务平台
def yhy(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://yan.bcpcn.com/website/xyjl.jsp?keyword=' + k +'&searchtype=1&page=1'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('page_tit'))
      selefunc.screenshot_file_save('8-1 盐行业信用管理与公众服务平台', i, k)
      time.sleep(2)
    except Exception as e:
      print('yhy 错误', e)
  

# 10-1 国家统计局
def gjtjj(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.stats.gov.cn/was5/web/search?channelid=288041&andsen=' + k
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('center_list_contlist'))
      selefunc.screenshot_file_save('10-1 国家统计局', i, k)
      time.sleep(2)
    except Exception as e:
      print('gjtjj 错误', e)
  
# 12-1 商务部
def swb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://search.mofcom.gov.cn/swb/swb_search/searchList_main.jsp'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('searchValue')).clear()
      input = driver.find_element_by_id('searchValue')
      input.send_keys(k)
      btn = driver.find_element_by_xpath('/html/body/section/section/div[1]/div/div[1]/div[1]/div[2]/span')
      btn.click()
      time.sleep(3)
      selefunc.screenshot_file_save('12-1 商务部', i, k)
      time.sleep(1)
    except Exception as e:
      print('swb 错误', e)
  

# 13-1 国家能源局
def energy(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://so.news.cn/was5/web/search?channelid=229767&searchword=' + k
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('sousuoTit'))
      time.sleep(3)
      selefunc.screenshot_file_save('13-1 国家能源局', i, k)
      time.sleep(1)
    except Exception as e:
      print('energy 错误', e)
  

# 13-2 中国海洋信息网
def ocean(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.nmdis.org.cn/front/search/result?SiteID=15&&AllSite=1&Query=' + k
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('list'))
      time.sleep(3)
      # 为了页面有公司名，输进去，但是不搜索
      # input = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/input')
      # input.clear()
      # input.send_keys(k)
      selefunc.screenshot_file_save('13-2 中国海洋信息网', i, k)
      time.sleep(1)
    except Exception as e:
      print('ocean 错误', e)
  


# 15-1 中国财政部
# 第二页反爬
def czb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.mof.gov.cn/index.htm?from=www.gogeeks.cn'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_name('andsen')).clear()
      input = driver.find_element_by_name('andsen')
      input.send_keys(k)
      btn = driver.find_element_by_xpath('//*[@id="searchform"]/div/a')
      btn.click()
      time.sleep(3)
      handles = driver.window_handles          #获取当前浏览器的所有窗口句柄
      driver.switch_to.window(handles[-1])     #切换到最新打开的窗口
      selefunc.screenshot_file_save('15-1 中国财政部', i, k)
      time.sleep(1)
    except Exception as e:
      print('czb 错误', e)
  

# 15-2 中国政府采购网
def zgcgw(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&start_time=&end_time=&timeType=2&searchparam=&searchchannel=0&dbselect=bidx&kw=' +k+'&bidSort=0&pinMu=0&bidType=0&buyerName=&projectId=&displayZone=&zoneId=&agentName='
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('vT_z'))
      time.sleep(3)
      selefunc.screenshot_file_save('15-2 中国政府采购网', i, k)
      time.sleep(1)
    except Exception as e:
      print('zgcgw 错误', e)
  


# 16-1 中国农业农村部
def zgncb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.moa.gov.cn/was5/web/search?searchword=' +k+'&channelid=233424&prepage=10&orderby=-DOCRELTIME'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('cx_list'))
      time.sleep(3)
      selefunc.screenshot_file_save('16-1 中国农业农村部', i, k)
      time.sleep(1)
    except Exception as e:
      print('zgncb 错误', e)
  

# 17-1 中国海关企业进出口信用信息公示平台
# 动态二维码 
# 重试机制
def hgjck(arr):
  driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
    """
  })
  driver.implicitly_wait(10)
  driver.get('http://credit.customs.gov.cn/')
  # 单个输入操作
  def __input_values(i, k, trytimes = 0):
    # 输入公司名
    input = driver.find_element_by_id('ID_codeName')
    input.clear()
    input.send_keys(k) 
    # 定位验证码图片
    element = driver.find_element_by_id('verifyCode')
    element.click()
    time.sleep(2)
    cpcode = captchacrack.git_captcha_crack(element, 4, 10)
    codeInput = driver.find_element_by_id('checkCode')
    codeInput.send_keys(cpcode)
    time.sleep(1)
    # 搜索
    btn = driver.find_element_by_class_name('serch_ico1')
    btn.click()
    time.sleep(2)
    
    # 如果验证码错了，换张图再来
    errorBox = selefunc.isElementPresent(driver, 'xpath', '//*[@id="layui-layer1"]/div[2]')
    if (errorBox and errorBox.text == '请输入正确的验证码'):
      if (trytimes > 2):
        print('重试次数达到上限，自己手动截吧 = =')
        raise
      else:
        __input_values(i, k, trytimes+1)
    return
  
  for i, k in enumerate(arr):
    try:
      __input_values(i, k, 0)
      # 截屏
      selefunc.screenshot_file_save('17-1 中国海关企业进出口信用信息公示平台', i, k)
      driver.refresh()
      time.sleep(2)
    except Exception as e:
      print('hgjck 错误', e)

# 18-1 中国住房和城乡建设部
def jsb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://search.mohurd.gov.cn/?tn=mohurd&lastq=%24wstquerystring%24&sort=last-modified+desc&rn=10&auth_info=&table_id=%24wsttableid%24&pn=0&query=' + k + '&ty=a&ukl=&uka=&ukf=&ukt=&sl=&ts=&te=&upg=0'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('content'))
      time.sleep(3)
      selefunc.screenshot_file_save('18-1 中国住房和城乡建设部', i, k)
      time.sleep(1)
    except Exception as e:
      print('jsb 错误', e)
  

# 18-2中国自然资源部
def zrzyb(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://s.lrn.cn/jsearchfront/search.do?websiteid=110000000000000&pg=1&p=1&searchid=1&tpl=13&cateid=1&q=' + k +'&filter=001&x=6&y=17'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('content'))
      time.sleep(3)
      selefunc.screenshot_file_save('18-2中国自然资源部', i, k)
      time.sleep(1)
    except Exception as e:
      print('zrzyb 错误', e)
  

# 百度
def baidu(arr):
  for i, k in enumerate(arr):
    try:
      url = 'https://www.baidu.com/'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('kw')).clear()
      input = driver.find_element_by_id('kw')
      input.send_keys(k)
      btn = driver.find_element_by_id('su')
      btn.click()
      time.sleep(3)
      selefunc.screenshot_file_save('百度', i, k)
      time.sleep(1)
    except Exception as e:
      print('baidu 错误', e)
  


# 海关总署
# 反爬 WebDriver (New) present (failed)
def hgzc(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.customs.gov.cn/'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('ess_ctr151088_ListC_Info_ctl00_KEYWORDS')).clear()
      input = driver.find_element_by_id('ess_ctr151088_ListC_Info_ctl00_KEYWORDS')
      input.send_keys(k)
      btn = driver.find_element_by_xpath('//*[@id="customs-search"]/span')
      btn.click()
      time.sleep(3)
      handles = driver.window_handles          #获取当前浏览器的所有窗口句柄
      driver.switch_to.window(handles[-1])     #切换到最新打开的窗口
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('default-result-list')) 
      selefunc.screenshot_file_save('海关总署', i, k)
      time.sleep(1)
    except Exception as e:
      print('hgzc 错误', e)
  

# 上交所
def sjs(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.sse.com.cn/home/search/?webswd=' + k
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_xpath('//*[@id="resultTable"]/div[4]/div[2]'))
      time.sleep(3)
      selefunc.screenshot_file_save('上交所', i, k)
      time.sleep(1)
    except Exception as e:
      print('sjs 错误', e)
  


# 深交所
def szjs(arr):
  for i, k in enumerate(arr):
    # try:
      url = 'http://www.szse.cn/application/search/index.html?keyword=' + k + '&r=1634119663611'
      driver.get(url)
      # WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_class_name('right-content'))
      time.sleep(3)
      selefunc.screenshot_file_save('深交所', i, k)
      time.sleep(1)
    # except Exception as e:
    #   print('szjs 错误', e)
  

# 盐业协会
def yyxh(arr):
  for i, k in enumerate(arr):
    try:
      url = 'http://www.cnsalt.cn/owsc/search.htm?searchCondition=' + k
      driver.get(url)
      time.sleep(3)
      selefunc.screenshot_file_save('盐业协会', i, k)
      time.sleep(1)
    except Exception as e:
      print('yyxh 错误', e)
  

# 中国债券信息网
def zgzqxxw(arr):
  for i, k in enumerate(arr):
    try:
      url = 'https://www.chinabond.com.cn/jsp/include/CB_CN/solrSearch/searchpage.jsp'
      driver.get(url)
      WebDriverWait(driver, 5).until(lambda driver:driver.find_element_by_id('name')).clear
      input = driver.find_element_by_id('name')
      input.send_keys(k)
      btn = driver.find_element_by_id('searchbtn')
      btn.click()
      time.sleep(3)
      selefunc.screenshot_file_save('中国债券信息网', i, k)
      time.sleep(1)
    except Exception as e:
      print('zgzqxxw 错误', e)
  
 
arr = [
  '东吴证券股份有限公司',
]
map = {
  '1': '失信被执行人',
  '2': '国家税务局',
  '3-1': '应急管理部',
  '3-3': '信用中国',
}

zxgk(arr)
tax(arr)
yjglb(arr)
sthjb(arr)
gyb(arr)
whj(arr)
ybj(arr)
fgw(arr)
sjj(arr)
yhy(arr)
gjtjj(arr)
swb(arr)
energy(arr)
ocean(arr)
czb(arr)
zgcgw(arr)
zgncb(arr)
jsb(arr)
zrzyb(arr)
baidu(arr)
sjs(arr)
szjs(arr)
yyxh(arr)
zgzqxxw(arr)


## 打开的很慢的
rmyh(arr)
qh(arr)
hgjck(arr)
hgzc(arr)

# 不行的
# gjqyxygs(arr)
# xyzg(arr)
