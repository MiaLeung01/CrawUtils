import os
import re
import pandas as pd
import wutil
from dict_parser import Bing
import pic_generator

word_list_path="D:/Testcode/zc/Resource/atheoryofjustice.xlsx"
base_bing_url = 'https://www.bing.com/dict/search?q='
base_bing_html_store="D:/Testcode/zc/Resource/dictionary/bing/"
base_bing_words_excel="D:/Testcode/zc/Resource/"
base_bing_br_mp3="D:/Testcode/zc/Resource/audio/bing/br/"
base_bing_pic="D:/Testcode/zc/Resource/wordcard/bing/"


EXCEL_FILE=base_bing_words_excel+'novel.xlsx'

# 1. 从词频统计excel获取单词列表，只取正常单词
def get_word_list():
  data = pd.read_excel(word_list_path)
  df = data.loc[:, ['单词']]
  word_list=[]
  for index, row in df.iterrows():
    word=row['单词']
    # 只对正常单词处理!!
    if(not re.search("^[a-zA-Z]+$", word) is None):
      word_list.append(word)
  return word_list

# 2.取到单词的释义那些，存到excel
def get_pages():
  word_list=get_word_list()
  entries = []
  for index, word in enumerate(word_list):
    content=get_bing_page(word)
    if(content):
      entry=Bing.parse_bing_page(content)
      if(entry != -1):
        entries.append(entry)
  
  df1 = pd.DataFrame(columns=['单词', '释义', '英音', '美音','英音mp3', '美音mp3'])
  for i, item in enumerate(entries):
    df1.loc[i] = item
  excel_writer = pd.ExcelWriter(EXCEL_FILE)  # 定义writer，选择文件（文件可以不存在）
  df1.to_excel(excel_writer, sheet_name='atoj', index=False)  # 写入指定表单
  excel_writer.save()  # 储存文件
  excel_writer.close()

# 获取 bing 该 word 的 html 文件，有本地的从本地取
def get_bing_page (word):
  file_name = base_bing_html_store+word+'.html'
  url = base_bing_url + word
  content = ''
  if os.path.exists(file_name):
    content =wutil.get_local_page_content(file_name)
  else:
    content = wutil.request_page(url)
    if (content != ''):
      Bing.store_bing_page(content, word, base_bing_html_store)
    else:
      content = -1
  return content


# 3. 下载 excel 里的所有mp3
def save_all_mp3():
  data = pd.read_excel(EXCEL_FILE)
  df = data.loc[:, ['单词','英音mp3']]

  for index, row in df.iterrows():
    mp3_path = base_bing_br_mp3+row['单词']+'.mp3'
    mp3_url = row['英音mp3']
    if(not pd.isnull(mp3_url)):
      print(mp3_url, type(mp3_url))
      wutil.download_stream_file(mp3_path, mp3_url)

# 4. 生成单词卡片
def gen_cards_pic():
  data = pd.read_excel(EXCEL_FILE)
  df = data.loc[:, ['单词','释义','英音mp3']]

  for index, row in df.iterrows():
    mp3_path = base_bing_br_mp3+row['单词']+'.mp3'
    flag=os.path.exists(mp3_path)
    print(mp3_path, flag)
    if(flag):
      title = row['单词']
      content = row['释义']
      file_name = (base_bing_pic+title+'.jpg') 
      pic_generator.CreateTextImg(file_name, title, content).draw_text() 

# 5.组合单词卡和音频
def a_w_list():
  data = pd.read_excel(EXCEL_FILE)
  df = data.loc[:, ['单词','释义','英音mp3']]
  content=[]
  for index, row in df.iterrows():
    # The above single quotes and without quotes only safe if it only contains "letters, digits, period(except prefix), underscore and hyphen".
    mp3_path=base_bing_br_mp3+row['单词']+'.mp3'
    pic_path=base_bing_pic+row['单词']+'.jpg'
    if(os.path.exists(mp3_path) and os.path.exists(pic_path)):
      content.append("file \'"+row['单词']+".mp3\'")
  
  with open(base_bing_words_excel+'cwords.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content))
    f.close()

def gen_cmds():
  data = pd.read_excel(EXCEL_FILE)
  df = data.loc[:, ['单词','释义','英音mp3']]
  content=[]
  for index, row in df.iterrows():
    # The above single quotes and without quotes only safe if it only contains "letters, digits, period(except prefix), underscore and hyphen".
    word=row['单词']
    mp3_path=base_bing_br_mp3+word+'.mp3'
    pic_path=base_bing_pic+word+'.jpg'
    if(os.path.exists(mp3_path) and os.path.exists(pic_path)):
      cm="ffmpeg -framerate 1 -i "+"'./wordcard/bing/" +word+".jpg' -i './audio/bing/br/"+word+".mp3' -shortest -c:v libx264 -r 30 -pix_fmt yuv420p './video/"+word+".mp4'"
      content.append(cm)
  
  with open(base_bing_words_excel+'cmds.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content))
    f.close()
  # 命令行合并图片+mp3 => mp4
  #  ffmpeg -framerate 1 -i './wordcard/'$jp -i './video/'$name'.mp3' -shortest -c:v libx264 -r 30 -pix_fmt yuv420p './video/'$name'.mp4'
  # 命令行合并mp3
  # ffmpeg -f concat -i cwords.txt -c copy combinelist.mp3
  #  ffmpeg -f concat -i ccc.txt -c copy aaa.mp4

if __name__ == "__main__":
  get_pages()
  save_all_mp3()
  gen_cards_pic()
  a_w_list()


 








