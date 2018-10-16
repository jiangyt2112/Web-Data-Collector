# -*- coding: utf-8 -*- 
# 浏览器操作
from selenium import webdriver
import selenium
from Tkinter import END
import config

g_driver = None

def open_browser(browser):
    # 打开浏览器
    driver = None

    if browser == "Chrome":
        try:
            driver = webdriver.Chrome()
        except Exception, e:
            print e
            return False, None, -1
        else:
            return True, driver, 0
    elif browser == "Firefox":
        try:
            driver = webdriver.Firefox()
        except Exception, e:
            print e
            return False, None, -1
        else:
            return True, driver, 1
    #elif browser == "Ie":
    #    try:
    #        driver = webdriver.Ie()
    #    except Exception, e:
    #        print e
    #        return False, None, -1
    #    else:
    #        return True, driver, 2
    else:
        return False, None, -1
      
    #return res, driver, browser_id
    

def test(url, listbox):
    # 测试url
    browser = config.Config().browser#["Chrome"] #, "Firefox"]
    res = False
    driver = None
    browser_id = -1
    perf_time = None
    entry_time = None
    global g_driver

    try:
        for i in browser:
            res, driver, browser_id = open_browser(i)
            if res:
                break
        if res == False:
            return False, None
        # 超时时间
        #driver.set_page_load_timeout(10)
        #driver.set_script_timeout(10)
        
        g_driver = driver
        driver.get(url)
        #
        #if browser_id == 2:
        #    perf_time = driver.execute_script("return window.performance.timing.toJSON()")
        #    entry_time = {}

        #else:
        perf_time = driver.execute_script("return window.performance.timing")
        entry_time = driver.execute_script("return window.performance.getEntriesByType('resource')")
    # 超时
    except selenium.common.exceptions.TimeoutException, e:
        listbox.insert(END, "   ##error:" + str(e) + "##")
        size = listbox.size()
        listbox.itemconfig(size - 1, foreground = "#ff0000")
        listbox.see(END)
        return True, [browser_id]
    # 其他异常
    except Exception, e:
        listbox.insert(END, "   ##error:" + str(e) + "##")
        size = listbox.size()
        listbox.itemconfig(size - 1, foreground = "#ff0000")
        listbox.see(END)
        # 可能产生超时异常，如何处理
        return False, e
        
    g_driver = driver
    #driver.close()
    #driver.quit()
    return True, (perf_time, entry_time, browser_id)


def close_browser():
    # 关闭浏览器
    global g_driver
    if g_driver == None:
        pass
    else:
        try:
            g_driver.close()
            g_driver.quit()
            g_driver = None
        except Exception, reason:
            print reason
            g_driver = None


    
