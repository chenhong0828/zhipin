import requests
import json

from queue import Queue
from threading import Thread

from lxml import etree
import re

import time

base_url = "https://www.zhipin.com"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

# 存储招聘信息的列表
jobs_queue = Queue()

# 创建存储url地址的队列
url_queue = Queue()

# 正则表达式：去掉标签中的<br/>和<em></em>标签，便于使用xpath解析提取文本
regx_obj = re.compile(r'<br/>|<(em).*?>.*?</\1>')


def send_request(url_path, headers, param=None):
    """
    :brief 发送请求，获取html响应(这里是get请求)
    :param url_path: url地址
    :param headers: 请求头参数
    :param param: 查询参数, 如：param = {'query': 'python', 'page': 1}

    :return: 返回响应内容
    """
    response = requests.get(url=url_path, params=param, headers=headers)

    response = regx_obj.sub('', response.text)

    return response


def value_of_path(html_obj, path):
    paths = html_obj.xpath(path)
    if paths:
        return paths[0].replace("\n","").strip()
    return ""


def parse_data():
    """
    :brief 从html文本中提取制定信息
    ：return：None
    """
    # 解析为html文档
    try:
        while True:
            # 等待25s,超时则抛出异常
            detail_url = url_queue.get(timeout=25)

            html = send_request(detail_url, headers, param=None)
            html_obj = etree.HTML(html)
            item = {}

            #岗位状态
            item['jobStatus'] = value_of_path(html_obj, '//div[@class="job-status"]//text()')
            #岗位名称
            item['position'] = value_of_path(html_obj,'//div[@class="info-primary"]//h1/text()')
            #薪水
            item['salary'] = value_of_path(html_obj,'//span[@class="salary"]/text()')
            #职责
            item['responsibility'] = value_of_path(html_obj,'//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()')
            #公司名称
            item['companyName'] = value_of_path(html_obj,'//div[@class="job-sec"]//div[@class="name"]/text()')
            #职位标签
            item['jobTags'] = value_of_path(html_obj,'//div[@class="job-sec"]//div[@class="job-tags"]/span/text()')
            #公司简介
            item['companyInfo'] = value_of_path(html_obj,'//div[@class="job-sec company-info"]/div[@class="text"]/text()')
            #公司地址
            item['address'] = value_of_path(html_obj,'//div[@class="location-address"]/text()')
            #公司段位
            item['companyStage'] = value_of_path(html_obj,'//*[@id="main"]/div[3]/div/div[1]/div[2]/p[2]/text()')
            #公司规模
            item['companyScale'] = value_of_path(html_obj,'//*[@id="main"]/div[3]/div/div[1]/div[2]/p[3]/text()')
            #链接
            item['URL'] = detail_url
            # print(item)
            jobs_queue.put(item)
            time.sleep(15)
    except Exception as e:
        print(e)


def detail_url(param):
    """
    :brief 获取详情页的url地址
    :param param:  get请求的查询参数
    :return: None
    """
    guangzhou_url = '/'.join([base_url, "c101280100/h_101280100/"])

    html = send_request(guangzhou_url, headers, param=param)
    #列表也页面
    html_obj = etree.HTML(html)
    #提取详情页url地址
    nodes = html_obj.xpath('.//div[@class="info-primary"]//a/@href')
    for node in nodes:
        detail_url = '/'.join([base_url, node])
        print(detail_url)
        url_queue.put(detail_url)


def write_data(page):
    """
    :brief 将数据保存为json文件
    :param page: 页面数
    :return: None
    """
    with open('F:\\LearnPython\\zhipin\\guangzhou_pyhton_job_{}.json'.format(page), 'w', encoding='utf-8') as f:
        f.write('[')
        try:
            while True:
                job_dict = jobs_queue.get(timeout=25)
                job_json = json.dumps(job_dict, indent=4, ensure_ascii=False)
                f.write(job_json + ',')
        except:
            pass
        
        f.seek(0,2)
        position = f.tell()
        f.seek(position - 1, 0)
        f.write(']')


def start_work(page):
    """
    :biref 调度器
    :param page: 页面编号
    :return: None
    """
    #生产者：获取详情页的页面链接
    for page in range(page, page + 1):
        param = {'query': '数据分析', 'page': page}
        producter = Thread(target=detail_url, args=[param])
        producter.start()

    #消费者：提取详情页的数据
    for i in range(1):
        consumer = Thread(target=parse_data)
        consumer.start()

    #将数据保存为json文件
    print('存储第{}页数据中...'.format(page))
    write_data(page)
    print('\t存储第{}页数据完毕!!!'.format(page))


if __name__ =="__main__":
    pages = int(input('请输入需要爬取的页面数：[1-10]:'))
    for page in range(1, pages + 1):
        start_work(page)
        time.sleep(15)