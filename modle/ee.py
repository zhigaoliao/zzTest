import pymysql
import json

data = {
    'id': "1",
    'image': "http://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c",
    'title': "霸王别姬",
    'actor': "张国荣,张丰毅,巩俐",
    'time': "1993-01-01(中国香港)",
    'score': "9.6"
}


db = pymysql.connect(host='10.9.25.100',user='ihr_1plus',password='!@IHR4rfvbhu8',port=3307,db='ihr_sit_1plus', charset='utf8')
cursor =db.cursor()
cursor.execute('select version()')
# data = cursor.fetchone()
# print('version:',data)
# sql = 'create table if not exists pytest (id int not null,image varchar(25), title varchar(25),actor varchar(25),time varchar(25), score varchar(25),primary key(id))'
# cursor.execute(sql)
# db.close()

# sql = 'insert into pytest values ("11","teg","9","测测侧是是是","233","3")'
# cursor.execute(sql)
# db.commit()

table = 'pytest'
keys = ', '.join(data.keys())
print(keys)
values = ', '.join(['%s'] * len(data))
print(data.values())
sql = 'INSERT INTO {table} VALUES ({values})'.format(table=table, keys=keys, values=values)
print(sql)
cursor.execute(sql, tuple(data.values()))
db.commit()
# try:
#    if cursor.execute(sql, tuple(data.values())):
#        print('Successful')
#        db.commit()
# except:
#     print('Failed')
#     db.rollback()
db.close()
