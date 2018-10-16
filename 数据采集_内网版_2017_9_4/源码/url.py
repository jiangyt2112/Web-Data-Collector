# -*- coding: utf-8 -*- 
# 获取测试url
import os
import random

class URL():
    def __init__(self, url_dir, url_dir_cn, class_num, url_num, url_num_cn):
        # 初始化
        self.class_num = class_num  # 类别数
        self.url_num = url_num      # url总数  
        self.url_num_cn = url_num_cn# url中文数

        # 路径
        cur_dir = os.getcwd()
        self.url_dir = os.path.join(cur_dir, url_dir)       # url路径
        self.url_dir_cn = os.path.join(cur_dir, url_dir_cn) # url中文路径
        #print self.url_dir
        #print self.url_dir_cn

        # 随机抽取类别
        self.url_files = random.sample(os.listdir(self.url_dir), class_num)
        avg_num = self.url_num / self.class_num # 每个类别url数
        avg_last = avg_num - self.url_num_cn    # 每个类别非中文url数
        avg_num_cn = self.url_num_cn            # 每个类别中文url数

        #print self.url_files
        # 随机url列表
        self.urls = []
        #print avg_num
        
        for i in xrange(self.class_num):
            c = self.url_files[i].split('.')[0]
            
            # url文件与对应的中文url文件
            file = os.path.join(self.url_dir, self.url_files[i])
            file_cn = os.path.join(self.url_dir_cn, self.url_files[i])
            # 打开文件
            fp = open(file, "r")
            fp_cn = open(file_cn, "r")

            # 读取国内url
            urls = fp_cn.read().strip().split('\n')
            urls = map(lambda x: [c, x], urls)
            self.urls += random.sample(urls, avg_num_cn)

            # 读取url
            urls = fp.read().strip().split('\n')
            urls = map(lambda x: [c, x], urls)
            self.urls += random.sample(urls, avg_last)
            

            for i in self.urls:
                if i[1].find("Https") == 0:
                    pass
                #elif i[1].find("www") == 0:
                #    i[1] = "http://" + i[1]
                #else:
                #    i[1] = "http://www." + i[1]
                else:
                    i[1] = "http://" + i[1]

            #print self.urls
            fp.close()
            fp_cn.close()
        
        #print self.urls
        self.current_index = 0

    def get_next(self):
        # true, url/none
        if self.current_index < self.url_num:
            self.current_index += 1
            return True, self.urls[self.current_index - 1]
        else:
            return False, None


def test():
    url = URL("urls\\categorys", "urls\\cn_categorys", 1, 20, 5)
    for i in range(5):
        print url.get_next()
        print url.get_next()
        print url.get_next()

if __name__ == '__main__':
    test()

