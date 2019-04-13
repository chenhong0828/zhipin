import json
import xlwt
from xlutils.copy import copy

pages = int(input('请输入需要转换的文件数：[1-6]:'))

wb = xlwt.Workbook()
for page in range(1, pages + 1):
    f = open('F:\\LearnPython\\zhipin\\guangzhou_pyhton_job_{}.json'.format(page), encoding='utf-8')
    info = json.load(f)

    sh = wb.add_sheet('Sheet {}'.format(page),page)

    attributes = []

    for x in info:
        for attr in x.keys():
            if attr not in attributes:
                attributes.append(attr)
                sh.write(0, attributes.index(attr), attr)
            sh.write(info.index(x) + 1, attributes.index(attr), x[attr])

wb.save('cpda.xlsx')