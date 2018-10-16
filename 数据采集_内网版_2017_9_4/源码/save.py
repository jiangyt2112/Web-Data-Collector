# -*- coding: utf-8 -*- 
# 保存测试结果到文件中
import json

class Save():
    def __init__(self, result_file):
        self.result_file = result_file

    def save(self, url, result, score):
        try:
            with open(self.result_file, "a") as fp:
                fp.write(url + "\n")
                fp.write(json.dumps(result[0]) + "\n")
                fp.write(json.dumps(result[1]) + "\n")
                #fp.write(str(result[2]) + "\n")
                fp.write(str(score) + "\n")
                fp.write("\n")
        except Exception, reason:
            return False
        return True

def test():
    s = Save("result.txt")
    s.save("aaaa", [123, 234], 23)

if __name__ == '__main__':
    test()
    
        