# -*- coding:utf-8 -*-
import urllib.request
import requests
import time
import os
import shutil
from lxml import html
def getPage():
    '''
    Get the link of beauty picture in the home page.
    '''
    fres=open('res.txt','w')
    htm=urllib.request.urlopen('http://www.mzitu.com/')
    out=htm.read()
    out=html.fromstring(out)
    urls=[]
    for res in out.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(res)
    for r in urls:
        fres.write(r)
        fres.write('\n\r')
    fres.close()
    return urls
def getPiclink(url):
    '''
    Get the each beauty picture title,link of pictures and Referer link.
    '''
    i_headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    sel=requests.get(url).text
    sel=html.fromstring(sel)
    total=sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    title=sel.xpath('//h2[@class="main-title"]/text()')[0]
    jpglist=[]
    for i in range(int(total)):
        link='{}/{}'.format(url, i+1)
        s=html.fromstring(requests.get(link).text)
        jpg=s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        jpglist.append(jpg)
    #print(jpglist)
    return title,jpglist
def downloadJpg(title,piclist,link):
    '''
    Download pictures
    '''
    k=1
    count=len(piclist)
    if title.find(':'):
        title=title.replace(':', '-')
    dirname=u"[%sP]%s" %(str(count), title)
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.mkdir(dirname)
    #Create title dir
    i_header={}
    i_header['Referer']=link
    #Add Referer field to the http header,which can solve anti-stealing-link 
    for i in piclist:
        filename='%s/%s/%s.jpg' %(os.path.abspath('.'),dirname, k)
        with open(filename,'wb') as jpg:
            jpg.write(requests.get(i, headers=i_header).content)
            time.sleep(0.5)
        k+=1
if __name__=='__main__':
    tpdict = {}
    li = []
    k=0
    for link in getPage():
        title, pic = getPiclink(link)
        downloadJpg(title, pic, link)
    print('OK!')
