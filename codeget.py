import urllib.request
import urllib.parse
import re
import json
import jsonpath
import time
from bs4 import BeautifulSoup
import lxml
import pymysql
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_one_page(url2):
    response = urllib.request.Request(url2)
    r = urllib.request.urlopen(response)
    return r.read().decode('utf-8')



def main():
    # 某栋id 11 13 12 14栋 合景

    # bcode=('181504','190964','195234','1955341')
    # 保利天悦 5 6栋'623800', '623810' 4栋 623090
    # bcode = ('623090')
    #
    # for we in bcode:


        url2 = 'http://fsfc.fszj.foshan.gov.cn/hpms_project/room.jhtml?id=195534'
        html = get_one_page(url2)
        # parse_one_page(html)
        # for item in parse_one_page(html):
        #     print(item)
        sdd=json.loads(html)
        ss=jsonpath.jsonpath(sdd,"$..fwcode")
        for oo in ss:
            if oo is not None:
                db = pymysql.connect(host='localhost', user='root', password='lzg123lzg', port=3306,
                                             db='mysql', charset='utf8')
                cursor = db.cursor()
                cursor.execute('select version()')
                sql = 'INSERT INTO buildcode(buildno,roomno) values (%s,%s)'
                try:
                     cursor.execute(sql,('195534',oo))
                     print('Successful')
                     db.commit()
                except:
                     print('Failed')
                     db.rollback()
                     db.close()
            else:
                print("没有数据")


main()