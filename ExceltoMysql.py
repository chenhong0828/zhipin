import xlrd
import pymysql

try:
    conn = pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = '123456',
        db = 'zhipin',
        port = 3306,
        charset = 'utf8'
    )
except:
    print("could not connect to mysql server")
cur = conn.cursor()
cur.execute('show tables;')
for i in cur.fetchall():
    if i[0] == 'zhipinjob':
        break
    else:
        sql_create_TB = """create table zhipinjob(
            id int not null auto_increment,
            jobStatus varchar(10),
            position varchar(50),
            salary varchar(10),
            salary_low tinyint,
            salary_high tinyint,
            responsibility text(500),
            requirement text(500),
            companyName varchar(50),
            jobTags varchar(100),
            companyInfo text(800),
            address varchar(80),
            companyStage varchar(20),
            companyScale varchar(20),
            URL char(100) primary key
            );"""

cur.execute(sql_create_TB)

book = xlrd.open_workbook('cpda.xlsx')
sheets = book.sheets()

for sheet in sheets:
    sheet = book.sheet_by_name(sheet.name)
    for r in range(1,sheet.nrows):
        jobStatus = sheet.cell(r,0).value
        position = sheet.cell(r,1).value
        salary = sheet.cell(r,2).value
        salary_low = sheet.cell(r,3).value
        salary_high = sheet.cell(r,4).value
        responsibility = sheet.cell(r,5).value
        requirement = sheet.cell(r,6).value
        companyName = sheet.cell(r,7).value
        jobTags = sheet.cell(r,8).value
        companyInfo = sheet.cell(r,9).value
        address = sheet.cell(r,10).value
        companyStage = sheet.cell(r,11).value
        companyScale = sheet.cell(r,12).value
        URL = sheet.cell(r,13).value

        value = (jobStatus, position, salary, salary_low, salary_high, responsibility, requirement, \
            companyName, jobTags, companyInfo, address, companyStage, companyScale, URL)
        sql_insert = """insert into zhipinjob(jobStatus, position, salary, salary_low, salary_high, responsibility, requirement,
            companyName, jobTags, companyInfo, address, companyStage, companyScale, URL)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        
        cur.execute(sql_insert, value)
        
cur.close()
conn.commit()
conn.close()   