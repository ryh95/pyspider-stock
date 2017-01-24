# coding:utf8
import smtplib
from email import encoders, MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import datetime

import pandas as pd


def send(date,section_list):
    _user = "1971990184@qq.com"
    _pwd = "rxdaltsmieszgfje"
    # _to = ['henry.duye@gmail.com','qliu.net@gmail.com','380312089@qq.com']

    # test
    _to = ['ryuanhang@gmail.com']

    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # grab_time = yes_time.strftime('%m-%d')

    msg = MIMEMultipart.MIMEMultipart()
    # mail's title
    msg["Subject"] = date+"Result"
    msg["From"] = _user
    msg["To"] = ",".join(_to)

    # add content for the mail
    msg_content = ''
    for section_name in section_list:
        msg_content += excel2str(date, section_name=section_name)
        msg_content += '\n'

    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))

    #with open(date+'attachment.xls', 'rb') as f:
       # # 设置附件的MIME和文件名，这里是png类型:
       # mime = MIMEBase('file', 'xls', filename=date+'attachment.xls')
       # # 加上必要的头信息:
       # mime.add_header('Content-Disposition', 'attachment', filename=date+'attachment.xls')
       # mime.add_header('Content-ID', '<0>')
       # mime.add_header('X-Attachment-Id', '0')
       # # 把附件的内容读进来:
       # mime.set_payload(f.read())
       # # 用Base64编码:
       # encoders.encode_base64(mime)
       # # 添加到MIMEMultipart:
       # msg.attach(mime)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print "Succeed in sending mail!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e

def excel2str(date,section_name=''):
    df = pd.read_excel("data/" + date+section_name + "result.xls",
        converters={'positive': str, 'negative': str, 'hottest': str},header=None)
    string = ''
    for list in df.values:
        for item in list:
            string += str(item)+'    '
        string += "\n"
    return string
