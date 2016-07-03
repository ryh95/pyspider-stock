# coding:utf8
import smtplib
from email import encoders, MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import datetime


def send(date):
    _user = "1971990184@qq.com"
    _pwd = "#"
    _to = "henry.duye@gmail.com"

    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # grab_time = yes_time.strftime('%m-%d')

    msg = MIMEMultipart.MIMEMultipart()
    # mail's title
    msg["Subject"] = date+"Result"
    msg["From"] = _user
    msg["To"] = _to
    msg.attach(MIMEText("yesterday's result", 'plain', 'utf-8'))

    with open('/home/ryh/gitProject/pyspider-stock/data/'+date+'result.xls', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('file', 'xls', filename=date+'result.xls')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=date+'result.xls')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print "Succeed in sending mail!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e
