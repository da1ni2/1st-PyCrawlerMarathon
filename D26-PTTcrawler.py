# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re


class PttcrawlerSpider(scrapy.Spider):
    name = 'PTTcrawler'
    allowed_domains = ['https://www.ptt.cc/bbs/Gossiping/M.1577709238.A.8E7.html']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/M.1577709238.A.8E7.html']
    cookies = {'over18':'1'}
    
    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url ,callback = self.parse , cookies= self.cookies )
    
    def parse(self, response):
        if response.status != 200:
            print('Error : {} is not available to acess'.format(response.url))
            return
        
        soup =BeautifulSoup(response.text , 'html5lib')
        main_content = soup.find(id = 'main-content')
        metas = main_content.select('div.article-metaline')
        
        if metas:
            if metas[0].select('span.article-meta-value')[0]:
                author = metas[0].select('span.article-meta-value')[0].text
            if metas[1].select('span.article-meta-value')[0]:
                title = metas[1].select('span.article-meta-value')[0].text
            if metas[2].select('span.article-meta-value')[0]:
                title = metas[2].select('span.article-meta-value')[0].text
            for m in metas:
                m.extract()
            for m in main_content.select('div.article-metaline-right'):
                m.extract()
                
        pushes = main_content.finad_all('div',class_ = 'push')
        for p in pushes:
            p.extract()
        
        try:
            ip = main_content.find(text = re.compile(u'※ 發信站'))
            ip = re.search('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*',ip).group()
        except:
            ip=''
        
        filters = []
        for i in main_content.stripped_strings:
            if i[0] not in [u'※', u'◆'] and i[:2] not in [u'--']:
                filters.append(i)
        expr = re.compile(u'[^一-龥。；，：“”（）、？《》\s\w:/-_.?~%()]')
        for i in range(len(filters)):
            filters[i] = re.sub(expr,'',filters[i])
        filters = [i for i in filters if i]
            
        content_text = ''.join(filters)    
        
        p,b,n = 0,0,0
        message = []
        
        for push in pushes:
            if not push.find('span' , 'push-tag'):
                continue
        # 過濾額外空白與換行符號
        # push_tag 判斷是推文, 箭頭還是噓文
        # push_userid 判斷留言的人是誰
        # push_content 判斷留言內容
        # push_ipdatetime 判斷留言日期時間
        
            push_tag = push.find('span' , 'push-tag').text
            push_userid = push.find('span','push-userid').text
            push_content = push.find('span','push-content').text
            push_content = ''.join(push_content[1:]).strip('\t\n\r')
            push_ipdatetime = push.find('span','push-ipdatetime').text.strip('\t\n\r')
            
            message.append({'push_tag':push_tag,'push_userid':push_userid,
                            'push_content':push_content,'push_ipdatetime':push_ipdatetime
                })
            
            if push_tag == u'推 ':
                p+=1
            elif push_tag == u'噓 ':
                b+=1
            else:
                n+=1
        message_count = {'all': p+b+n, 'count': p-b, 'push': p, 'boo': b, 'neutral': n}
        
        data = {
            'url': response.url,
            'article_author': author,
            'article_title': title,
            'article_date': date,
            'article_content': content,
            'ip': ip,
            'message_count': message_count,
            'messages': messages
        }
        yield data
    
        
        print(r)
        pass
