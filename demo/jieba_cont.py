
import jieba
from collections import Counter

def get_words_cont(txt):
	list = jieba.cut(txt)
	c = Counter()
	for x in list:
		if len(x) > 1 and x != '\r\n' and x != 'nbsp' and x != 'gt' and x != 'lt':
			c[x] += 1

	fh = open('./jieba_cont.txt', 'a',encoding='utf8')
	fh.write('邮箱内容常用词')
	fh.write('\n')
	fh.close()
	for (k, v) in c.most_common(100):
		fh = open('./jieba_cont.txt', 'a',encoding='utf8')
		fh.write('%s  %d' % (k, v))
		fh.write('\n')
		fh.close()


with open('./q_content.txt', 'r',encoding='utf8') as f:
	txt = f.read()
	txtlength = len(txt)
	fh = open('./jieba_cont.txt', 'a',encoding='utf8')
	fh.write('邮箱内容总字数：' + str(txtlength))
	fh.write('\n')
	fh.close()

get_words_cont(txt)




