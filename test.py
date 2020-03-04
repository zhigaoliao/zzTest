import urllib.request
import urllib.parse
import re
import json
import time
from bs4 import BeautifulSoup
import lxml
import pymysql
import jsonpath
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_one_page(url):
    response = urllib.request.Request(url)
    r = urllib.request.urlopen(response)
    return r.read().decode('utf-8')

def main():
    bcode=('195234','195534')

    for we in bcode:

        db = pymysql.connect(host='localhost', user='root', password='lzg123lzg', port=3306,
                             db='mysql', charset='utf8')
        cursor = db.cursor()
        cursor.execute('select version()')
        sql3 = 'select roomno from buildcode where buildno=%s'
        cursor.execute(sql3,we)
        wqq=cursor.fetchall()
        for ds in wqq:
            qs=ds[0]
            url = 'https://fsfc.fszj.foshan.gov.cn/hpms_project/roomview.jhtml?id='+qs+'&xmmc='
            html = get_one_page(url)
            soup = BeautifulSoup(html, 'lxml')
            # 房间地址
            roomdr = soup.find(text = re.compile('栋'))
            rdrr = ""
            rdrr = rdrr.join(roomdr)
            print(rdrr)

            # 面积
            area = soup.find(text = re.compile('[0-9][0-9]{1,3}\.\d+'))
            sdw1 = ""
            sdw1 = sdw1.join(area)
            areaq = float(sdw1)

            # 获取状态
            rstatus1 = soup.find(text = re.compile('预订'))
            rstatus2 = soup.find(text = re.compile('可售'))
            if (rstatus1 is not None):
                rst = "限制房产"
            elif (rstatus2 is not None):
                rst = "可售"
            else:
                rst = 0

            # 预订和可售状态才获取价格
            if (rst != 0):
                roomprice = soup.table.find_all(text = re.compile('[0-9]\d{6}(?!\d)'))[0]
                sdw = ""
                sdw = sdw.join(roomprice)
                ww = int(sdw)
                npr = int(ww / int(areaq))

            # 获取当前时间
            timew = time.strftime("%Y-%m-%d", time.localtime())

            # 数据写入mysql
            if (rst != 0 ):
                db = pymysql.connect(host = 'localhost', user = 'root', password = 'lzg123lzg', port = 3306,
                                     db = 'mysql', charset = 'utf8')
                cursor = db.cursor()
                cursor.execute('select version()')
                sql1 = 'select price from pricelist where name=(%s)'
                if cursor.execute(sql1, (rdrr)):
                        print("已经有数据了")
                        eq1=cursor.fetchone()[0]
                        if ww != int(eq1):
                            print("要更新价格")
                            sql2 = 'update pricelist set status=%s,price=%s,nprice=%s,time=%s where pricelist.name=%s'
                            cursor.execute(sql2, (rst, ww, npr, timew,rdrr))
                            db.commit()
                        else:
                            db.close()
                            print("不用更新价格")
                else:
                    sql = 'INSERT INTO pricelist (name,area,price,time,status,nprice,roomcode) values (%s,%s,%s,%s,%s,%s,%s)'
                    try:
                        cursor.execute(sql, (rdrr, areaq, ww, timew, rst, npr, qs))
                        print("插入成功")
                        db.commit()
                    except:
                        print('Failed')
                        db.rollback()
                        db.close()
            else:
                print("have nothing")


main()
