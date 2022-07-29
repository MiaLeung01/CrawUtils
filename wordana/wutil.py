import os
from time import sleep
import requests

HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


def request_page(url):
  sleep(4)
  try:
    response = requests.get(url, headers=HEADERS)
    return response.content
  except Exception as e:
    print("请求 " + url + " page 错误", e)
    return ''

def download_stream_file(file_path, url):
  """ Use to download online stream file such as mp3, mp4 file if file does not exists in loacl. """
  try:
    print(os.path.exists(file_path))
    if not os.path.exists(file_path):
      sleep(4)
      print('正在下载：', file_path)
      response = requests.get(url, stream=True, headers=HEADERS)
      with open(file_path, 'wb') as f:
        for chunk in response.iter_content():
          f.write(chunk)
  except Exception as e:
    print('下载错误', e)


def get_local_page_content(file_path):
  """ Get local file content. If file dose not exist, then return empty string. """
  if os.path.exists(file_path):
    print('读取本地文件: '+file_path)
    file = open(file_path, 'r', encoding='utf-8')
    file_content = file.read()
    return file_content
  else:
    print(file_path, ' :文件不存在')
    return ''

def ls_directory(directory_path, store_path):
  """获取该目录下所有文件，存入列表中"""
  file_list=os.listdir(directory_path)

  content = ''
  for item in file_list:
    content += 'file '+ item + '\n'
 
  with open(store_path, 'w', encoding='utf-8') as f:
    f.write(content)
    f.close()

def rename_file():
  base = 'D:/Testcode/zc/CrawUtils/ParseUnits/audio/'
  #获取该目录下所有文件，存入列表中
  file_list=os.listdir(base)

  for item in file_list:
    new_name = item.replace(' ', '_')
    print(item, new_name)
    os.rename(base+item,base+new_name)


def save_excel(file_path='', columns=['列A', '列B'], ex_list=[['行1A','行1B']], sheet_name='sheet1'):
  """ 写入excel """
  import pandas as pd

  df1 = pd.DataFrame(columns=columns)
  for i, item in enumerate(ex_list):
    df1.loc[i] = item
  excel_writer = pd.ExcelWriter(file_path)  # 定义writer，选择文件（文件可以不存在）
  df1.to_excel(excel_writer, sheet_name=sheet_name, index=False)  # 写入指定表单
  excel_writer.save()  # 储存文件
  excel_writer.close()


# file 'happy1.jpg'
# duration 2

# file = open('D:/Testcode/zc/CrawUtils/ParseUnits/wordcard/aaa.txt', 'r', encoding='utf-8')
# file_content = file.readlines()
# sum=0
# for el in file_content:
#   a = re.search('[1-9]+\.?[0-9]*', el)
#   if (not a is None):
#     print(a.group())
#     sum+=float(a.group())
# print(sum)

