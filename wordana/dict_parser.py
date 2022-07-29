import re
from bs4 import BeautifulSoup

HTML_TEMPLATE = """
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

class Bing:
  def store_bing_page(content, word, base_path):
    """ Extract useful infomation from Bing Dictionary HTML content and store in local. """
    try:
      soup = BeautifulSoup(content, 'html.parser')
      # 真正的单词
      real_word = soup.select_one('#headword').get_text()
      if (real_word == word):
        file_name = base_path+real_word+'.html'
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
          html = HTML_TEMPLATE.format(content=html)
          html = html.encode("utf-8")
          with open(file_name, 'wb') as f:
            f.write(html)
            f.close()
          print('新的！保存！')
    except Exception as e:
      print("保存错误", e)


  def parse_bing_page(origin_content):
    """ Extract useful infomation from Bing Dictionary HTML content. 
    You will need it when you want to store information in Excel. """
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