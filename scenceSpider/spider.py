# -*- coding: utf-8 -*-
import urllib2
import urllib
from bs4 import BeautifulSoup
import MySQLdb

# baseUrl = 'http://s.visitbeijing.com.cn/index.php'
user_agent = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
headers = {'User-Agent': user_agent}
values = {
    'm': 'content',
    'c': 'search',
    'catid': 7,
    'theme': 0,
    'area': 0,
    'crowd': 0,
    'level': 0,
    'ticselect': 0,
    'page': 1
}
def getContent(page):
    '''获取网页信息'''
    values = {
    'm': 'content',
    'c': 'search',
    'catid': 7,
    'theme': 0,
    'area': 0,
    'crowd': 0,
    'level': 0,
    'ticselect': 0,
    'page': page
}


    data = urllib.urlencode(values)
    # baseUrl.replace('@PAGE', '1')
    # print baseUrl
    # print data

    # url= 'http://s.visitbeijing.com.cn/index.php?m=content&c=search&catid=7&theme=0&area=0&crowd=0&level=0&ticselect=0&page='
    # url = url + str(page)

    try:
        f=urllib.urlopen("http://s.visitbeijing.com.cn/index.php?%s" % data)
        # response = urllib2.urlopen(url)
        # req = urllib2.Request(url, headers)
        # response = urllib2.urlopen(req)
        # the_page = response.read()
        the_page = f.read()
        # print the_page
        return the_page
    except urllib2.HTTPError,e:
        print e.code
        print e.reason
        # print e.read()
    # save2file(the_page, 'page.txt')
    #


def parseContent(content):
    '''解析网页'''
    soup = BeautifulSoup(content, "lxml")
    scenceList = soup.select('div.list')
    # save2file(scenceList)
    # print scenceList
    for i in scenceList:
        href = i.select('a')
        # print href
        url = href[0]['href'] #景点链接

        conn = conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        if cur.execute("select url from scenes_list where url='"+url+"'") > 0:
            print "here"
            continue


        print url
        node = i.select('div.fr > p')
        # print node
        name = ""
        grade = ""
        price = ""
        guide = ""
        address = ""
        nodelen = len(node)
        for index, p in enumerate(node):
            if index == 0:
                # text = p.get_text()
                name = p.select('a')[0].get_text()
                grade = p.select('span')[0].get_text()
            if index == 1:
                tmptx = p.get_text()
                if u'价格' in tmptx:
                    price = tmptx.strip()
                else:
                    price = u"无"
            if index == nodelen - 2:
                tmptx = p.get_text()
                if u'导语' in tmptx:
                    guide = tmptx.strip()
                else:
                    guide = u"无"
                # guide = p.get_text()
            if index == nodelen - 1:
                tmptx = p.get_text()
                if u'地址' in tmptx:
                    address = tmptx.strip()
                else:
                    address = u"无"
                # address = p.get_text()
        print name + '--' +grade + '--' + price + '--' +guide + '--' + address

        special = i.select('div.fr > ul')
        if special:
            for m in special:
                spe = ""
                spicialli = m.select('li')
                for ind, k in enumerate(spicialli):
                    # spe = []
                    if ind % 2 != 0:
                        # print "~~~~~~~~~~~"
                        # print k.get_text()
                        # spe.append(str(k.get_text()))
                        spe = spe + "|" + k.get_text().strip('\n') # 特色
        else:
            spe = ""
        print spe
            # special = ''.join(spe)
        # print special

        print '--'*15
        save2db(name, url, grade, price, guide, address, spe)


def spider():
    '''循环爬取'''
    for i in range(107):
        if i == 0:
            continue
        content = getContent(i)
        if content:
            parseContent(content)



def save2db(name, url, grade, price, guide, address, spe):
    '''保存到数据库'''
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    # cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat + 1, tmplng + 1, float(distance)))
    cur.execute("insert into sns.scenes_list(name, url, grade, price, guide, address, special) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(name, url, grade, price, guide, address, spe))
    conn.commit()
    cur.close()
    conn.close()


def save2file(filename, content):
    '''没什么用'''
    f = open(filename, 'wb+')
    f.write(content)
    f.close()


if __name__ == '__main__':
    '''主函数'''
    # content = getContent(3)
    # parseContent(content)
    spider()
