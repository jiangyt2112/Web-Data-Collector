# -*- coding: utf-8 -*- 
# 配置
from ConfigParser import ConfigParser

class Config():
    def __init__(self):
        self.config_file = "config.ini" # 配置文件名
        self.result_file = None         # 结果文件名
        self.url_dir = None             # url目录
        self.url_dir_cn = None          # url目录(中文)
        self.class_num = 0              # url要测试类别数
        self.url_num = 0                # 总共需要测试url数
        self.host = None                # 数据库主机ip
        self.port = None
        self.user = None                # 数据库用户名
        self.passwd = None              # 数据库密码
        self.db = None                  # 数据库名
        self.browser = None             # 浏览器
        self.parse()                    # 从文件中获取配置信息

    def parse(self):
        # 解析配置文件，获取配置信息
        cf = ConfigParser()
        cf.read("config.ini")
        self.result_file = cf.get("result", "file")
        self.url_dir = cf.get("url", "dir")
        self.url_dir_cn = cf.get("url", "cn_dir")
        self.class_num = int(cf.get("url", "class"))
        self.url_num = int(cf.get("url", "num"))
        self.url_num_cn = int(cf.get("url", "num_cn"))
        
        self.host = cf.get("database", 'host')
        self.port = int(cf.get("database", 'port'))
        self.user = cf.get("database", 'user')
        self.passwd = cf.get("database", 'passwd')
        self.db = cf.get("database", 'db')

        self.browser = eval(cf.get("browser", "browser"))
        #print self.browser

def test():
    config = Config()

if __name__ == '__main__':
    test()
