# _*_ coding: utf-8 _*_
# 获取用户的ip地址所在地与运营商
import urllib2
import requests
import json
from bs4 import BeautifulSoup

# 获取外网IP
def get_out_ip(url):
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    return ip

# 获取链接地址
def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt,"html.parser").iframe
    return soup["src"]

# 通过外网地址，查询地址与运营商信息
def checkip(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip="+ ip
    json_data = json.loads(urllib2.urlopen(url).read())
    #print json_data

    # 解析失败
    if json_data[u'code'] == 1:
        json_data[u'data'] = {u'region': u'',u'city': u'',u'isp': u'',
                            u'country': u'', u'area': u'', u'ip': ip}
    result = {
            "country": json_data[u'data'][u'country'].encode("utf-8"),
            "area": json_data[u'data'][u'area'].encode("utf-8"),
            "region": json_data[u'data'][u'region'].encode("utf-8"),
            "city": json_data[u'data'][u'city'].encode("utf-8"),
            "isp": json_data[u'data'][u'isp'].encode("utf-8"),
            "ip": json_data[u'data'][u'ip'].encode("utf-8")
    }
    return result

def position():
    ip = None
    result = {
            "country": "",
            "area": "",
            "region": "",
            "city": "",
            "isp": "",
            "ip": ""
    }
    try:
        ip = get_out_ip(get_real_url())
    except Exception, e:
        print e
        return False, e, result

    try:
        #ip = get_out_ip(get_real_url())
        res = checkip(ip)
    except Exception, e:
        print e
        result['ip'] = ip.encode("utf-8")
        return False, e, result
    return True, res

if __name__ == '__main__':
    #print get_out_ip(get_real_url())
    print position()