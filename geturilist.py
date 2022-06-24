import requests
import xlwt


##projectId=549 项目ID，自行替换需要抓取的项目ID
##branch=master 分支，自行替换需要抓取的项目分支
projectId = '282'
branch= 'master'
tagee_url = 'https://tagee.duowan.com/api/projectInterface/groupList?projectId=' + projectId + '&branch=' + branch

urlinfo = []
requs = requests.get(url=tagee_url).json()
grouplist = requs['data']
for group in grouplist:
    gp = group['projectInterfaceList']
    for uris in gp:
        ud = []
        ##获取tagee组名称，URI名称和路径
        ud.append(group['name'])
        ud.append(uris['name'])
        ud.append(uris['uri'])
        urlinfo.append(ud)
print(urlinfo)

workbook = xlwt.Workbook(encoding="UTF-8")
sheet = workbook.add_sheet("sheet1")

for col,colum in enumerate(["组名称","接口名称","接口路径"]):
    sheet.write(0,col,colum)
for row , data in enumerate(urlinfo):
    for col ,col_data in enumerate(data):
        sheet.write(row+1,col,col_data)

workbook.save("geturlinfo.xls")