# -*- coding: utf-8 -*-
# 数据库操作，mysql数据库
import os, sys, string  
from decimal import *
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb

class DBSaver:
    def __init__(self, host = "localhost", port = 3306, user='root',passwd='123456'
        ,db='web_data',charset='UTF8'):
        self.user_id = 0
        
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

        # 性能信息
        self.perf_attr = ['navigationStart','unloadEventStart', 'unloadEventEnd',\
        'redirectStart', 'redirectEnd', 'fetchStart', 'domainLookupStart', \
        'domainLookupEnd', 'connectStart', 'secureConnectionStart', 'connectEnd', 'requestStart',\
        'responseStart', 'responseEnd', 'domLoading', 'domInteractive', \
        'domContentLoadedEventStart', 'domContentLoadedEventEnd', \
        'domComplete', 'loadEventStart', 'loadEventEnd']
        # 资源信息
        self.res_attr = [
            'test_id', 'resource_id', 'name', 'entryType', 'startTime',\
            'duration', 'initiatorType', 'redirectStart', 'redirectEnd',\
            'fetchStart', 'domainLookupStart', 'domainLookupEnd',\
            'connectStart', 'connectEnd', 'secureConnectionStart',\
            'requestStart', 'responseStart', 'responseEnd', 'transferSize',\
            'nextHopProtocol', 'workerStart', 'encodedBodySize',\
            'decodedBodySize']

    def save_user(self, gender, age, education, occupation, netage, pos_info):
        # 保存用户信息
        conn = None
        try:  
            conn = MySQLdb.connect(host=self.host, port = self.port, user = self.user,
                passwd = self.passwd, db = self.db, charset='UTF8')

        except Exception, e:  
            return False, e
        # 获取cursor对象来进行操作  
        cursor = conn.cursor()

        country = pos_info['country'] or "NULL"
        area = pos_info['area'] or "NULL"
        ip = pos_info['ip'] or "NULL"
        isp = pos_info['isp'] or "NULL"
        region = pos_info['region'] or "NULL"
        city = pos_info['city'] or "NULL"
        # sql语句
        sql = "insert into user(gender, age, education, occupation, netage,\
                ip, isp, country, area, region, city) values(%d, %d, %d, %d, %d,\
                '%s', '%s', '%s', '%s', '%s', '%s')" %(gender, age, education, 
                occupation, netage, ip, isp, country, area, region, city)
        # 执行sql
        try:
            cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e

        # 获取用户id
        sql = "select LAST_INSERT_ID();"
        try:
          cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e
        alldata = cursor.fetchall()
        self.user_id = alldata[0][0]
        
        # 提交保存，关闭链接
        cursor.close()  
        conn.commit()
        conn.close()
        return True, self.user_id

    def save(self, user_id, url, perf, res, browser_id, score):
        # 保存测试结果
        conn = None
        try:  
            conn = MySQLdb.connect(host=self.host, port = self.port, user = self.user,
                passwd = self.passwd, db = self.db, charset='UTF8')

        except Exception, e:  
            return False, e

        # 获取cursor对象来进行操作  
        cursor = conn.cursor()

        # sql语句
        sql = "insert into performance(user_id, url, navigation, score, flag, "
        for item in self.perf_attr:
            sql += item + ','
        sql = sql[:-1] + ')'
        sql += " values("+str(user_id) + "," +"'" + url + "'," + str(browser_id) + "," + str(score) + "," + str(1) + ","

        
        if 'secureConnectionStart' not in perf:
            perf['secureConnectionStart'] = -1

        try:
            for item in self.perf_attr:
                sql += str(perf[item]) + ","
        except Exception, e:
            # 属性值缺失
            print "***error:"
            print perf
            self.rollback(cursor, conn)
            return True, e

        sql = sql[:-1] + ")"

        # 执行sql
        # print(sql)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e

        # 获得保存索引
        sql = "select LAST_INSERT_ID();"
        try:
          cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e
        alldata = cursor.fetchall()
        index = alldata[0][0]

        res_count = len(res)
        

        # 资源数据保存
        for i in xrange(res_count):

            sql = "insert into resource("
            for item in self.res_attr:
                sql += item + ","
            sql = sql[:-1] + ")"

            sql += " values("

            res_attr_dic = {}
            for item in self.res_attr:
                res_attr_dic[item] = None

            res_attr_dic['test_id'] = str(index)
            res_attr_dic['resource_id'] = str(i + 1)

            #try:
            # 可能存在属性值缺失的情况，诡异的资源类型
            # 这类资源也保存，数据处理的时候注意
            if 'name' in res[i]:
                res_attr_dic['name'] = "'" + res[i]['name'] + "'"
            if 'entryType' in res[i]:
                res_attr_dic['entryType'] = "'" + res[i]['entryType'] + "'"
            if 'startTime' in res[i]:
                res_attr_dic['startTime'] = "%.10f" %res[i]['startTime']
            if 'duration' in res[i]:
                res_attr_dic['duration'] = "%.10f" %res[i]['duration']
            if 'initiatorType' in res[i]:
                res_attr_dic['initiatorType'] = "'" + res[i]['initiatorType'] + "'"
            if 'redirectStart' in res[i]:
                res_attr_dic['redirectStart'] = "%.10f" %res[i]['redirectStart']
            if 'redirectEnd' in res[i]:
                res_attr_dic['redirectEnd'] = "%.10f" %res[i]['redirectEnd']
            if 'fetchStart' in res[i]:
                res_attr_dic['fetchStart'] = "%.10f" %res[i]['fetchStart']
            if 'domainLookupStart' in res[i]:
                res_attr_dic['domainLookupStart'] = "%.10f" %res[i]['domainLookupStart']
            if 'domainLookupEnd' in res[i]:
                res_attr_dic['domainLookupEnd'] = "%.10f" %res[i]['domainLookupEnd']
            if 'connectStart' in res[i]:
                res_attr_dic['connectStart'] = "%.10f" %res[i]['connectStart']
            if 'connectEnd' in res[i]:
                res_attr_dic['connectEnd'] = "%.10f" %res[i]['connectEnd']
            if 'secureConnectionStart' in res[i]:
                res_attr_dic['secureConnectionStart'] = "%.10f" %res[i]['secureConnectionStart']
            if 'requestStart' in res[i]:
                res_attr_dic['requestStart'] = "%.10f" %res[i]['requestStart']
            if 'responseStart' in res[i]:
                res_attr_dic['responseStart'] = "%.10f" %res[i]['responseStart']
            if 'responseEnd' in res[i]:
                res_attr_dic['responseEnd'] = "%.10f" %res[i]['responseEnd']

            # 不一定存在的属性
            if 'transferSize' in res[i]:
                res_attr_dic['transferSize'] = "%d" %res[i]['transferSize']
            if 'nextHopProtocol' in res[i]:
                res_attr_dic['nextHopProtocol'] = "'" + res[i]['nextHopProtocol'] + "'"
            
            if 'workerStart' in res[i]:
                res_attr_dic['workerStart'] = "%.10f" %res[i]['workerStart']
            if 'encodedBodySize' in res[i]:
                res_attr_dic['encodedBodySize'] = "%d" %res[i]['encodedBodySize']
            if 'decodedBodySize' in res[i]:
                res_attr_dic['decodedBodySize'] = "%d" %res[i]['decodedBodySize']

            for item in self.res_attr:
                if res_attr_dic[item] != None:
                    sql += res_attr_dic[item] + ","
                else:
                    sql += "NULL" + ","

            sql = sql[:-1] + ")"
            #print sql
            try:
                cursor.execute(sql)
            except Exception, e:
                self.rollback(cursor, conn)
                return True, e

        # 提交保存，关闭链接
        cursor.close()  
        conn.commit()
        conn.close()

        return True, None

    def save_timeout(self, user_id, url, browser_id, score):
        # 保存测试结果
        conn = None
        try:  
            conn = MySQLdb.connect(host=self.host, port = self.port, user = self.user,
                passwd = self.passwd, db = self.db, charset='UTF8')

        except Exception, e:  
            return False, e

        # 获取cursor对象来进行操作  
        cursor = conn.cursor()

        # sql语句
        sql = "insert into performance(user_id, url, navigation, score, flag,"
        for item in self.perf_attr:
            sql += item + ','
        sql = sql[:-1] + ')'
        sql += " values("+str(user_id) + "," +"'" + url + "'," + str(browser_id) + "," + str(score) + "," + str(0) + ","
         #+ "%d,"*19 + "%d)" + 
        
  
        for item in self.perf_attr:
            sql += str(-1) + ","
        
        sql = sql[:-1] + ")"

        # 执行sql
        # print(sql)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.rollback(cursor, conn)
            return False, e

         # 提交保存，关闭链接
        cursor.close()  
        conn.commit()
        conn.close()

        return True, None


    def rollback(self, cursor, conn):
        # 出错数据库回滚
        try:
            cursor.close()
            conn.rollback()
            conn.close()
        except:
            pass

def test():
    t = DBSaver()
    pref = {"unloadEventStart": 0, "domLoading": 1495106462767, 
        "fetchStart": 1495106461081, "responseStart": 1495106462690, 
        "loadEventEnd": 1495106463517, "connectStart": 1495106461081, 
        "domainLookupStart": 1495106461081, "redirectStart": 0, 
        "domContentLoadedEventEnd": 1495106463221, "requestStart": 1495106462201, 
        "secureConnectionStart": 0, "connectEnd": 1495106461081, 
        "navigationStart": 1495106460845, "loadEventStart": 1495106463512, 
        "domInteractive": 1495106463214, "domContentLoadedEventStart": 1495106463214,
        "redirectEnd": 0, "domainLookupEnd": 1495106461081, "unloadEventEnd": 0, 
        "responseEnd": 1495106462769, "domComplete": 1495106463512}

    res = [
        {"startTime": 0, "initiatorType": "navigation", "unloadEventStart": 0, 
        "fetchStart": 235.11, "duration": 2671.135, "responseStart": 1844.66, 
        "loadEventEnd": 2671.135, "transferSize": 29135, "connectStart": 235.11, 
        "domainLookupStart": 235.11, "redirectStart": 0, 
        "domContentLoadedEventEnd": 2375.385, "requestStart": 1355.7050000000002, 
        "type": "navigate", "secureConnectionStart": 0, "connectEnd": 235.11, 
        "redirectCount": 0, "workerStart": 0, "decodedBodySize": 102058, 
        "loadEventStart": 2666.9300000000003, "encodedBodySize": 28096, 
        "entryType": "navigation", "domInteractive": 2368.675, 
        "domContentLoadedEventStart": 2368.82, "redirectEnd": 0, 
        "name": "http://www.baidu.com/", "domainLookupEnd": 235.11, 
        "unloadEventEnd": 0, "responseEnd": 1923.1950000000002, 
        "domComplete": 2666.83, "toJSON": {}}
        ,
        {"secureConnectionStart": 0, "redirectStart": 0, "transferSize": 8190, 
        "redirectEnd": 0, "name": "http://www.baidu.com/img/bd_logo1.png", 
        "responseStart": 2090.28, "startTime": 1950.43, 
        "domainLookupEnd": 1950.43, "connectEnd": 1950.43, "requestStart": 1957.9, 
        "initiatorType": "img", "responseEnd": 2094.91, "workerStart": 0, 
        "decodedBodySize": 7877, "fetchStart": 1950.43, 
        "duration": 144.4799999999998, "encodedBodySize": 7877, "toJSON": {}, 
        "entryType": "resource", "connectStart": 1950.43, 
        "domainLookupStart": 1950.43}
        ]
    res, e = t.save(1, "aaa", pref, res, 1, 5)
    if res == False:
        print e

def test_user():
    t = DBSaver()
    pos_info = {
        "country": "中国",
        "area": "华东",
        "ip": "10.10.92.30",
        "isp": "",
        "region": "山东省",
        "city": "潍坊市"
    }
    res, e = t.save_user(0, 0, 0, 0, 0, pos_info)
    print res, e
if __name__ == '__main__':
    test()
    test_user()





