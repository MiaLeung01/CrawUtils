from PIL import Image, ImageDraw, ImageFont
from matplotlib.pyplot import title


FONT_CH = "D:\\Testcode\\zc\\Resource\\font\\nzgrKangxi.ttf"
FONT_EN = ".D:\\Testcode\\zc\\Resource\\font\\Roboto\\roboto-medium.ttf"
FONT_CH_EN = "D:\\Testcode\\zc\\Resource\\font\\MiSans\\misans_normal.ttf"
RESOLUTION_1080 = (1920, 1080)
RESOLUTION_720 = (1280, 720)

class CreateTextImg:

  font = ImageFont.truetype(FONT_CH_EN, 50)

  def __init__(self, file_name, title="默认标题", content="默认段落1\n默认段落2", backgroud_color="#000000", size=RESOLUTION_720):
    self.file_name = file_name
    # 预设宽度 可以修改成你需要的图片宽度
    self.width = 1100
    self.size = size
    self.title = title
    self.content = content
    self.backgroud_color = backgroud_color
    # 段落 , 行数, 行高
    self.sections, self.note_height, self.line_height = self.get_sections()

  def split_text(self, text):
    # txt = Image.new('RGBA',self.size, (255, 255, 255, 0))
    # draw = ImageDraw.Draw(txt)
    # 所有文字的段落
    sections = ""
    # 宽度总和
    sum_width = 0
    # 几行
    line_count = 1
    # 行高
    line_height = 0
    # for char in text:
    #   width, height = draw.textsize(char, CreateTextImg.font)
    #   sum_width += width
    #   if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
    #     line_count += 1
    #     sum_width = 0
    #     sections += '\n'
    #   sections += char
    #   line_height = max(height, line_height)
    # if not sections.endswith('\n'):
    #   sections += '\n'
    # print(text)
    # print(sections)
    return text, line_height, line_count

  def get_sections(self):
    # 按规定宽度分组
    max_line_height, total_lines = 0, 0
    allText = []
    for text in self.content.split('\n'):
      sections, line_height, line_count = self.split_text(self.content)
      max_line_height = max(line_height, max_line_height)
      total_lines += line_count
      allText.append((sections, line_count))
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
    return str


  def draw_text(self):
    """
    绘图以及文字
    :return:
    """
    # im = Image.new("RGBA", self.size, self.backgroud_color).convert("RGBA")
    im = Image.new("RGB", self.size, self.backgroud_color)
    draw = ImageDraw.Draw(im)

    header_font = ImageFont.truetype(FONT_CH_EN, 110)
    header_x = 100
    header_y = 100
    draw.text((header_x, header_y), u'%s' % self.title, fill=(255, 255, 255), font=header_font)
    print(self.title)
    # 左上角开始
    x, y = 100, 300
    for section, line_count in self.sections:
      draw.text((x, y), section, fill=(255, 255, 255), font=self.font)
      y += self.line_height * line_count
    # 预览
    # im.show()
    im.save(self.file_name)


    