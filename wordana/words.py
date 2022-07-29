import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
import string
import pandas as pd

## todo: 去除人名，常见单词

# 创建一个新列表，包含我们想要清理的标点符号
punctuations = list(string.punctuation)
punctuations.extend(['‘', '’', '—', '“', '”'])

# 初始化stopwords变量
stop_words = stopwords.words('english')
data = pd.read_excel('D:/file share with phone/20000_words调序整洁版.xlsx', index_col=None, header=None)
df = data.loc[:1000, [1]]
extra_words=df[1].tolist()
stop_words.extend(extra_words)


def extract_text_word_frequcncy(file_name):
  file=open(file_name, 'r', encoding='utf-8')
  source=file.read()
  # 函数word_tokenize() 会将文本句子解析为词汇
  tokens = word_tokenize(source)
  tokens = [word for word in tokens if not word.lower() in stop_words and word not in punctuations ]
  tokens = [word for word in tokens if re.search('[A-Z]{1,1}\.{1,1}', word) is None and re.search('[0-9]+', word) is None and re.search('[a-zA-Z]+-$', word) is None and not len(word)<2]
  origin_word = [WordNetLemmatizer().lemmatize(word) for word in tokens ]
  print(len(origin_word))
  freq=FreqDist(w.lower().strip(string.punctuation).strip('—') for w in origin_word)
  # 写入excel
  df1 = pd.DataFrame(columns=['单词', '频率'])
  i=0
  for key,value in freq.items():
    df1.loc[i] = [key, value]
    i+=1

  excel_writer = pd.ExcelWriter('D:/Testcode/zc/Resource/atheoryofjustice.xlsx')  # 定义writer，选择文件（文件可以不存在）
  df1.to_excel(excel_writer, sheet_name='ch1', index=False)  # 写入指定表单
  excel_writer.save()  # 储存文件
  excel_writer.close()

if __name__ == '__main__':
  # extract_text_word_frequcncy('D:/file share with phone/A-Theory-of-Justice.txt')
  extract_text_word_frequcncy('D:/Testcode/zc/Resource/a-theory-of-justice-ch1.txt')
  print('end')
