# import matplotlib.pyplot as plt  # 数学绘图库
# import jieba  # 分词库
# from wordcloud import WordCloud  # 词云库
#
# # 1、读入txt文本数据
# text = open('./q_subject.txt', "r",encoding='utf8').read()
#
#
# # 2、结巴分词，默认精确模式。可以添加自定义词典userdict.txt,然后jieba.load_userdict(file_name) ,file_name为文件类对象或自定义词典的路径
# # 自定义词典格式和默认词库dict.txt一样，一个词占一行：每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒
#
# cut_text = jieba.cut(text)
# result = "/".join(cut_text)  # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
# # print(result)
#
# # 3、生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
# # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
# wc = WordCloud(font_path=r"C:\Windows\Fonts\simhei.ttf", background_color='white', width=800,
#                height=600, max_font_size=50,
#                max_words=1000)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
# wc.generate(result)
# wc.to_file(r"./wordcloud.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
#
# # 4、显示图片
# plt.figure("词云图")  # 指定所绘图名称
# plt.imshow(wc)  # 以图片的形式显示词云
# plt.axis("off")  # 关闭图像坐标系
# plt.show()
#=====================================================================================
import matplotlib.pyplot as plt  # 数学绘图库
from PIL import Image
import numpy as np  # 科学数值计算包，可用来存储和处理大型矩阵
import jieba  # 分词库
from wordcloud import WordCloud, ImageColorGenerator  # 词云库

# 1、读入txt文本数据
text = open(r'./q_subject.txt', "r",encoding='utf8').read()

# 2、结巴分词:cut_all参数可选, True为全模式，False为精确模式,默认精确模式
cut_text = jieba.cut(text, cut_all=False)
result = "/".join(cut_text)  # 必须给个符号分隔开分词结果,否则不能绘制词云

# 3、初始化自定义背景图片
image = Image.open(r'C:\Users\Administrator\Desktop\timg.png')
graph = np.array(image)

# 4、产生词云图
# 有自定义背景图：生成词云图由自定义背景图像素大小决定
wc = WordCloud(font_path=r"C:\Windows\Fonts\simhei.ttf", background_color='white', max_font_size=50,
               mask=graph)
wc.generate(result)

# 5、绘制文字的颜色以背景图颜色为参考
image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
wc.recolor(color_func=image_color)
wc.to_file(r"./wordcloud.png")  # 按照背景图大小保存绘制好的词云图，比下面程序显示更清晰

# 6、显示图片
plt.figure("词云图")  # 指定所绘图名称
plt.imshow(wc)  # 以图片的形式显示词云
plt.axis("off")  # 关闭图像坐标系
plt.show()