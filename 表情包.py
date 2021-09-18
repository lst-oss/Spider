import requests
import time
from lxml import html
import re


etree = html.etree
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}


def change_names(title):
    '''
    去除非法字段
    '''
    pattern = re.compile(r'[\\\/\:\*\?\"\<\>\|]')     # 将字符串对象转换成正则表达式对象
    new_names = re.sub(pattern, '', title)
    return new_names


def biaoqing(url):

    res = requests.get(url=url, headers=headers).text
    data_html = etree.HTML(res)
    pic_name = data_html.xpath('//div[@class="tagbqppdiv"]/a/@title')
    pic_urls = data_html.xpath('//div[@class="tagbqppdiv"]/a/img/@data-original')
    j = 0
    for pic_url in pic_urls:
        response = requests.get(url=pic_url, headers=headers).content
        pic_name_ = change_names(pic_name[j])
        print(pic_name_)
        with open('{:s}.gif'.format(pic_name_), mode='wb') as f:
            f.write(response)
        print('下载成功: ', pic_name[j])
        j += 1


if __name__ == '__main__':
    for i in range(1, 11):
        print('------------------------正在下载第{:d}页------------------------'.format(i))
        url = 'https://fabiaoqing.com/biaoqing/lists/page/{:s}.html'.format(str(i))
        try:
            biaoqing(url)
            time.sleep(5)
        except FileNotFoundError as e:
            print(e)
