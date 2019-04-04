# -*- coding: utf-8 -*-
import json
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from lxml import etree
import poplib
import re
import pymysql

poplib._MAXLINE = 20480

email = '1206604668@qq.com'  # 邮箱地址
password = 'ckerfiaudlhmhgdi'  # pop3密码
pop3_server = "pop.qq.com"


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg, indent=0):
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return print_info(part)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset,'ignore')
                clear = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
                content = clear.sub("",content)
                clear = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
                content = clear.sub("",content)
                selector=etree.HTML(content)
                if selector is not None:
                    content=selector.xpath('string(.)')
                    a = ''.join(content.split())
                    a = str(a).strip().replace(',','').replace("'",'').replace("""""""",'').replace('(',' ').replace(')',' ').replace('%', ' ').replace('<', ' ').replace('>', ' ')
                    return a
        else:
            print(content_type)


def print_subject(msg, indent=0):
    if indent == 0:
        for header in ['Subject']:
            value = msg.get(header, '')
            if value:
                value = decode_str(value)
            value = str(value).strip().replace(',','').replace("'",'').replace("""""""",'').replace('(',' ').replace(')',' ').replace('%', ' ').replace('<', ' ').replace('>', ' ')

            return value


server = poplib.POP3_SSL(pop3_server, 995)
server.user(email)
server.pass_(password)
resp, mails, octets = server.list()
index = len(mails)

# connent = pymysql.connect(host='localhost', user='root', passwd='qwert.....', db='ccc_data', charset='utf8')
# cursor = connent.cursor()
for i in range(index, 0, -1):
    resp, lines, octets = server.retr(i)
    msg_content = b'\r\n'.join(lines).decode('unicode_escape', 'ignore')
    msg_subject = b'\r\n'.join(lines).decode('utf-8', 'ignore')

    msg = Parser().parsestr(msg_content)
    msg_s = Parser().parsestr(msg_subject)
    content = print_info(msg)
    subject = print_subject(msg_s)
    print(str(subject))
    print(str(content))
    try:
        with open('q_subject.txt','a+',encoding='utf8')as f:
            f.write(subject)
            f.write('\r\n')
    except:
        pass
    try:
        with open('q_content.txt','a+',encoding='utf8')as f:
            f.write(content)
            f.write('\r\n')
    except:
        pass

    # CREATE TABLE `tt` (`a` char(100) , `b` text ) ENGINE=MyISAM DEFAULT CHARSET=utf8;  # 建表语句
#     cursor.execute("INSERT INTO tt(a, b) VALUES (\'%s\', \'%s\')" % (str(subject), str(content)))
#     connent.commit()
#     print('--------------')
#
# cursor.close()
# connent.close()
server.quit()
