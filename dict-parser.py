# 词典数据解析

from pickle import FALSE, TRUE
from time import sleep
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

import requests
import os
import re
import pdfkit
from bs4 import BeautifulSoup
from sqlalchemy import true

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
    
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://dictionary.cambridge.org/common.css?version=5.0.193" rel="stylesheet" type="text/css" />
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""


htmls = []

# 保存 bing 词条网页
def store_bing_page(content, word):
  try:
    soup = BeautifulSoup(content, 'html.parser')
    # 真正的单词
    real_word = soup.select_one('#headword').get_text()
    if (real_word == word):
      file_name = 'D:/Testcode/zc/CrawUtils/ParseUnits/bing/'+real_word+'.html'
      # 正文
      dibody = soup.find_all(class_="qdef")
      # 删除不需要的
      for cls in [".img_area", ".df_div", ".se_div"]:
        tp = soup.select_one(cls)
        if (tp):
          tp.extract()
          
      if (len(dibody)):
        body = dibody[0]
        html = str(body)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        with open(file_name, 'wb') as f:
          f.write(html)
          f.close()
        print('新的！保存！')
  except Exception as e:
    print("保存错误", e)

def get_local_page_content(file_name):
  if os.path.exists(file_name):
    print('读取本地文件 '+word+'.html')
    file = open(file_name, 'r', encoding='utf-8')
    file_content = file.read()
    return file_content
  else:
    print(file_name, '文件不存在')
    return ''

def request_bing_page(word):
  sleep(4)
  base_url = 'https://www.bing.com/dict/search?q='
  url = base_url + word
  try:
    response = requests.get(url, headers=headers)
    return response.content
  except Exception as e:
    print("请求 bing" + word + " page 错误", e)
    return ''

# 获取 bing 该 word 的 html 文件，有本地的从本地取
def get_bing_page (word):
  file_name = 'D:/Testcode/zc/CrawUtils/ParseUnits/bing/'+word+'.html'
  content = ''
  if os.path.exists(file_name):
    content = get_local_page_content(file_name)
  else:
    content = request_bing_page(word)
    if (content != ''):
      store_bing_page(content, word)
  return content
   

def parse_bing_page(origin_content):
  try:
    soup = BeautifulSoup(origin_content, 'html.parser')
    real_word = soup.select_one('#headword').get_text()
    
    # 音标
    pr_us = soup.select_one(".hd_prUS")
    pr_us_audio = pr_us and pr_us.find_next_sibling("div", "hd_tf")
    pr_us_audio_url = pr_us_audio and re.search("https?:\/\/(.+\/)+.+(\.(swf|avi|flv|mpg|rm|mov|wav|asf|3gp|mkv|rmvb|mp4|mp3))",pr_us_audio.a['onclick'])


    pr_eg = soup.select_one(".hd_pr")
    pr_eg_audio = pr_eg and pr_eg.find_next_sibling("div", "hd_tf")
    pr_eg_audio_url = pr_eg_audio and re.search("https?:\/\/(.+\/)+.+(\.(swf|avi|flv|mpg|rm|mov|wav|asf|3gp|mkv|rmvb|mp4|mp3))",pr_eg_audio.a['onclick'])

    print(pr_us and pr_us.get_text(), pr_eg and pr_eg.get_text())
    print(pr_eg_audio_url)

    def_list = []
    defination = soup.select('.qdef > ul > li')
    for el in defination:
      def_list.append(el.get_text())
    # 批量换行符
    # 方法1：替换功能——查找“CHAR(10)”，替换为“ctrl+j”（适用于笔记本）
    # 方法2: 替换功能——查找“CHAR(10)”，替换为“长按alt+先按小键盘1松开后按0”（笔记本没实验成功，可能台式机可以）
    return [real_word, '\n'.join(def_list), pr_eg and pr_eg.get_text(), pr_us and pr_us.get_text(), pr_eg_audio_url and pr_eg_audio_url.group(0), pr_us_audio_url and pr_us_audio_url.group(0)]

  except Exception as e:
    print("解析错误", e)
    return -1


def get_related_word_list(range_word):
  whtml_file = 'D:/Testcode/zc/CrawUtils/ParseUnits/bing/list_'+range_word+'.txt'

  if os.path.exists(whtml_file):
    print('已存在, 直接返回')
    file = open(whtml_file, 'r', encoding='utf-8')
    file_content = file.readlines()
    return file_content
  else:
    url = 'https://relatedwords.io/' + range_word
    try:
      response = requests.get(url, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')
      terms_list = soup.find_all(class_='term')
      content = ''
      for term in terms_list:
        content += term.get_text('\n', strip=True) + '\n'
      
      with open(whtml_file, 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()
      print('新的词表：'+whtml_file+'保存！')
      return content
    except Exception as e:
      print("词表获取错误", e)


def download_stream_file(subname, url):
  try:
    file_name= 'D:/Testcode/zc/CrawUtils/ParseUnits/audio/'+subname
    print(os.path.exists(file_name))
    if not os.path.exists(file_name):
      sleep(4)
      print('正在下载：', file_name)
      response = requests.get(url, stream=true, headers=headers)
      with open(file_name, 'wb') as f:
        for chunk in response.iter_content():
          f.write(chunk)
  except Exception as e:
    print('下载错误', e)

def rename_file():
  base = 'D:/Testcode/zc/CrawUtils/ParseUnits/audio/'
  #获取该目录下所有文件，存入列表中
  file_list=os.listdir(base)

  for item in file_list:
    new_name = item.replace(' ', '_')
    print(item, new_name)
    os.rename(base+item,base+new_name)


from PIL import Image, ImageDraw, ImageFont

class ImgText:
  font = ImageFont.truetype("C:\\Users\\liang\\AppData\\Local\\Microsoft\\Windows\\Fonts\\nzgrKangxi.ttf", 70)

  def __init__(self, title, content, size, backColor):
    # 预设宽度 可以修改成你需要的图片宽度
    self.width = 900
    self.size = size
    self.title = title
    self.content = content
    self.backColor = backColor
    # 文本
    # self.text = text
    # 段落 , 行数, 行高
    self.duanluo, self.note_height, self.line_height = self.split_text()

  def get_duanluo(self, text):
    txt = Image.new('RGBA',self.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    # 所有文字的段落
    duanluo = ""
    # 宽度总和
    sum_width = 0
    # 几行
    line_count = 1
    # 行高
    line_height = 0
    for char in text:
      width, height = draw.textsize(char, ImgText.font)
      sum_width += width
      if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
        line_count += 1
        sum_width = 0
        duanluo += '\n'
      duanluo += char
      line_height = max(height, line_height)
    if not duanluo.endswith('\n'):
      duanluo += '\n'
    return duanluo, line_height, line_count

  def split_text(self):
    # 按规定宽度分组
    max_line_height, total_lines = 0, 0
    allText = []
    for text in self.content.split('\n'):
      duanluo, line_height, line_count = self.get_duanluo(self.content)
      max_line_height = max(line_height, max_line_height)
      total_lines += line_count
      allText.append((duanluo, line_count))
    line_height = max_line_height
    total_height = total_lines * line_height
    return allText, total_height, line_height

  def RGB_to_Hex(self, tmp):
    rgb = tmp.split(',')  # 将RGB格式划分开来
    strs = '#'
    for i in rgb:
      num = int(i)  # 将str转int
      # 将R、G、B分别转化为16进制拼接转换并大写
      strs += str(hex(num))[-2:].replace('x', '0').upper()
      # print(strs)
      # color = RGB_to_Hex('249,204,190')
    img = Image.new("RGBA", self.size, strs)
    img.save("back.png")

  def draw_text(self):
    self.RGB_to_Hex(self.backColor)
    """
    绘图以及文字
    :return:
    """
    note_img = Image.open("back.png").convert("RGBA")
    draw = ImageDraw.Draw(note_img)

    # header = 'this is a title'
    # font_type = 'ABACE-PFB-2.ttf'
    font_type = 'D:\\Testcode\\zc\\font\\Roboto\\roboto-medium.ttf'


    color = "#FFFFFF"
    header_font = ImageFont.truetype(font_type, 110)

    header_x = 100
    header_y = 100
    print(self.title)
    draw.text((header_x, header_y), u'%s' % self.title, fill=(255, 255, 255), font=header_font)

    # 左上角开始
    x, y = 100, 300
    for duanluo, line_count in self.duanluo:
      draw.text((x, y), duanluo, fill=(255, 255, 255), font=self.font)
      y += self.line_height * line_count
    note_img.show()
    note_img.save("backResult.png")

    

if __name__ == "__main__":
  ## 1. 获取词表
  # word_list = get_related_word_list('flower')

  ## 2. 下载词表词条内容并解析，写入 excel
  # ex_list = []
  # for word in word_list:
  #   strip_word = word.strip()
  #   origin_content = get_local_page_content('D:/Testcode/zc/CrawUtils/ParseUnits/bing/'+strip_word+'.html')
  #   if (origin_content):
  #     ex_item = parse_bing_page(origin_content)
  #     if(ex_item != -1):
  #       ex_list.append(ex_item)

  # print(ex_list)
  # import pandas as pd

  # df1 = pd.DataFrame(columns=['单词', '释义', '英音', '美音','英音mp3', '美音mp3'])
  # for i, item in enumerate(ex_list):
  #   df1.loc[i] = item
  # excel_writer = pd.ExcelWriter('文件.xlsx')  # 定义writer，选择文件（文件可以不存在）
  # df1.to_excel(excel_writer, sheet_name='flower', index=False)  # 写入指定表单
  # excel_writer.save()  # 储存文件
  # excel_writer.close()

  # # 3. 下载mp3
  # import pandas as pd
  # data = pd.read_excel('文件.xlsx')
  # df = data.loc[:, ['单词','英音mp3']]
  # content = []

  # for index, row in df.iterrows():
  #   # The above single quotes and without quotes only safe if it only contains "letters, digits, period(except prefix), underscore and hyphen".
  #   mp3_path = row['单词'].strip().replace(' ', '_').replace('\'', '')+'_eg.mp3'
  #   mp3_url = row['英音mp3']
  #   if(not pd.isnull(mp3_url)):
  #     print(mp3_url, type(mp3_url))
  #     download_stream_file(mp3_path, mp3_url)
  #     content.append("file \'"+mp3_path+"\'" )
  
  # with open('D:/Testcode/zc/CrawUtils/ParseUnits/audio/combinelist.txt', 'w', encoding='utf-8') as f:
  #   f.write('\n'.join(content))
  #   f.close()

  ## 4. 命令行合并mp3
  # ffmpeg -f concat -i combinelist.txt -c copy combinelist.mp3



  word_list = get_related_word_list('flower')
  ex_list = []
  for word in word_list:
    strip_word = word.strip()
    origin_content = get_local_page_content('D:/Testcode/zc/CrawUtils/ParseUnits/bing/'+strip_word+'.html')
    file_name= 'D:/Testcode/zc/CrawUtils/ParseUnits/audio/'+strip_word.strip().replace(' ', '_').replace('\'', '')+'_eg.mp3'
    if (origin_content and os.path.exists(file_name)):
      ex_item = parse_bing_page(origin_content)
      if(ex_item != -1):
        ex_list.append(ex_item)

  print(ex_list)
  import pandas as pd

  df1 = pd.DataFrame(columns=['单词', '释义', '英音', '美音','英音mp3', '美音mp3'])
  for i, item in enumerate(ex_list):
    df1.loc[i] = item
  excel_writer = pd.ExcelWriter('文件.xlsx')  # 定义writer，选择文件（文件可以不存在）
  df1.to_excel(excel_writer, sheet_name='flower', index=False)  # 写入指定表单
  excel_writer.save()  # 储存文件
  excel_writer.close()
  data = pd.read_excel('文件.xlsx')
  df = data.loc[:, ['单词','释义']]
  
  for index, row in df.iterrows():
    # The above single quotes and without quotes only safe if it only contains "letters, digits, period(except prefix), underscore and hyphen".
    c = row['释义']
    #5. 生成图片
    size_6 = (2688, 1242)
    size_720 = (1280, 720)
    title = row['单词'].strip()
    content = row['释义']
    color = ('0,0,0')
    n = ImgText(title,content,size_720,color)
    n.draw_text()









# =============== 备忘录 =================
# cuda: ffmpeg -codecs | findstr cuvid

# transcode: ffmpeg -threads 3 -i *.flv -c copy *.mp4
# merge: ffmpeg -threads 3 -f concat -i list.txt -c copy *.mp4
# split: ffmpeg -threads 3 -ss 00:00:00 -t 00:00:00 -i *.mp4 -vcodec copy -acodec copy *.mp4

# encode: ffmpeg -i *.mp4 -r 60 -vcodec hevc_nvenc -preset slow -ab 192k -ar 44100 -b:v 6000k -maxrate 24400k -minrate 5800k *.mp4
# encode:(additional) -c:v h264_nvenc

# music: ffmpeg -i *.mp4 -vn -acodec copy *.aac
# subtitle:ffmpeg -c:v h264_cuvid -i *.mp4 -vf subtitles=*.ass -c:v h264_nvenc -b:v 6000k -c:a copy *.mp4
