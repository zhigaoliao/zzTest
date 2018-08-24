import urllib.request
import urllib.parse
import re
import json
import time
import pymysql

def get_one_page(url):
    response = urllib.request.Request(url)
    r = urllib.request.urlopen(response)
    return r.read().decode('utf-8')

def parse_one_page(html):
    pattern =re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield ({
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time':  item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()})

# def write_to_json(content):
#     with open('result.txt', 'ab') as f:
#         # print(type(json.dumps(content)))
#         f.write(json.dumps(content, ensure_ascii=False,).encode('utf-8'))
#         # f.write('\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # aa = parse_one_page(html)
    # print(aa)
    for item in parse_one_page(html):
         print(item)
         db = pymysql.connect(host='10.9.25.100', user='ihr_1plus', password='!@IHR4rfvbhu8', port=3307,
                             db='ihr_sit_1plus', charset='utf8')
         cursor = db.cursor()
         cursor.execute('select version()')
         # data = cursor.fetchone()
         # print('version:',data)
         table = 'pytest'
         keys = ', '.join(item.keys())
         print(keys)
         values = ', '.join(['%s'] * len(item))
         print(item.values())
         sql = 'INSERT INTO {table} VALUES ({values})'.format(table=table, keys=keys, values=values)
         try:
             if cursor.execute(sql, tuple(item.values())):
                 print('Successful')
                 db.commit()
         except:
             print('Failed')
             db.rollback()
         db.close()
        # write_to_json(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(2)
