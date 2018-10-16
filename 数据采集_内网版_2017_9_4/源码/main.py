# -*- coding: utf-8 -*- 
# main主程序入口，界面实现
from Tkinter import *
from ttk import *
import config
import browser
import url
import save
import subprocess
import threading
import Queue
import dns
import path
import db
import position
import time
#import my_pickle


class Main():
    def __init__(self):
        # 当前目录加入环境变量中
        path.add_path()

        # 界面控制变量
        self.root = None
        self.text_frame = None
        self.list_frame = None
        self.next_botton = None
        self.scrollbar = None
        self.score_entry = None
        self.listbox = None
        self.label = None
        self.save_button = None
        self.prefix = "   "

        # 配置
        self.configer = config.Config()

        # url获取
        self.url = url.URL(self.configer.url_dir, self.configer.url_dir_cn, 
            self.configer.class_num, self.configer.url_num, self.configer.url_num_cn)

        # 当前测试url序列号
        self.index = 0
        # 当前剩余url数
        self.all_url_num = 0
        # 当前测试url
        self.cur_url = None

        # 保存测试结果
        self.saver = save.Save(self.configer.result_file)
        self.db_saver = db.DBSaver(self.configer.host, self.configer.port, self.configer.user, self.configer.passwd, self.configer.db)
        
        # 线程通信队列
        self.queue = Queue.Queue()

        # 运行停止标识
        self.running = False
        self.stop_flag = False

        # 文件主窗口
        self.question_win = None
        # 用户标识
        self.user_id = 0

    def questionnaire(self):
        # 问卷调查主窗口
        self.question_win = Tk()
        self.question_win.withdraw()
        self.question_win.protocol("WM_DELETE_WINDOW", self.question_win_kill)
        self.question_win.title("问卷调查")
        self.question_win.iconbitmap('logo.ico')
        w = 700
        h = 560
        sw = self.question_win.winfo_screenwidth()
        sh = self.question_win.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.question_win.geometry('%dx%d+%d+%d' %(w, h, x, y))

        font = ("courier new", 12, "")
        # 问卷调查
        q = Label(self.question_win, text = "问卷调查", font = font)
        q.place(in_ = self.question_win, x = 300, y = 20)

        # 帮助感谢
        h = Label(self.question_win, text = "请帮助我们了解您的基本信息。谢谢！", font = font)
        h.place(in_ = self.question_win, x = 10, y = 50)

        init_sel = -1
        #user_data = my_pickle.load()
        # 性别
        gender_label = Label(self.question_win, text = "1.请问您的性别:", font = font)
        gender_label.place(in_ = self.question_win, x = 10, y = 90)
        
        self.gender_v = IntVar()
        self.gender_v.set(init_sel) #user_data["gender"])
        Radiobutton(self.question_win,variable = self.gender_v
            ,text = 'A.男', value = 0).place(in_ = self.question_win, x = 200, y = 90)
        Radiobutton(self.question_win,variable = self.gender_v
            ,text = 'B.女', value = 1).place(in_ = self.question_win, x = 270, y = 90)

        # 年龄
        age_label = Label(self.question_win, text = "2.请问您的年龄是:", font = font)
        age_label.place(in_ = self.question_win, x = 10, y = 130)

        self.age_v = IntVar()
        self.age_v.set(init_sel)    #user_data["age"])
        Radiobutton(self.question_win,variable = self.age_v
            ,text = 'A.20以下', value = 0).place(in_ = self.question_win, x = 30, y = 160)
        Radiobutton(self.question_win,variable = self.age_v
            ,text = 'B.20-30岁', value = 1).place(in_ = self.question_win, x = 130, y = 160)
        Radiobutton(self.question_win,variable = self.age_v
            ,text = 'C.30-40', value = 2).place(in_ = self.question_win, x = 230, y = 160)
        Radiobutton(self.question_win,variable = self.age_v
            ,text = 'D.40-50', value = 3).place(in_ = self.question_win, x = 330, y = 160)
        Radiobutton(self.question_win,variable = self.age_v
            ,text = 'E.50以上', value = 4).place(in_ = self.question_win, x = 430, y = 160)

        # 教育
        education_label = Label(self.question_win, text = "3.请问您的教育经历是:", font = font)
        education_label.place(in_ = self.question_win, x = 10, y = 200)

        self.education_v = IntVar()
        self.education_v.set(init_sel)  #user_data["education"])
        Radiobutton(self.question_win,variable = self.education_v
            ,text = 'A.初中及以下', value = 0).place(in_ = self.question_win, x = 30, y = 230)
        Radiobutton(self.question_win,variable = self.education_v
            ,text = 'B.高中', value = 1).place(in_ = self.question_win, x = 130, y = 230)
        Radiobutton(self.question_win,variable = self.education_v
            ,text = 'C.专科', value = 2).place(in_ = self.question_win, x = 230, y = 230)
        Radiobutton(self.question_win,variable = self.education_v
            ,text = 'D.本科', value = 3).place(in_ = self.question_win, x = 330, y = 230)
        Radiobutton(self.question_win,variable = self.education_v
            ,text = 'E.硕士', value = 4).place(in_ = self.question_win, x = 430, y = 230)
        Radiobutton(self.question_win,variable = self.education_v
            ,text = 'F.博士', value = 5).place(in_ = self.question_win, x = 530, y = 230)

        # 职业
        occupation_label = Label(self.question_win, text = "4.请问您的职业是:", font = font)
        occupation_label.place(in_ = self.question_win, x = 10, y = 270)

        self.occupation_v = IntVar()
        self.occupation_v.set(init_sel) #user_data["occupation"])
        Radiobutton(self.question_win,variable = self.occupation_v
            ,text = 'A.IT工作者', value = 0).place(in_ = self.question_win, x = 30, y = 300)
        Radiobutton(self.question_win,variable = self.occupation_v
            ,text = 'B.教育', value = 1).place(in_ = self.question_win, x = 130, y = 300)
        Radiobutton(self.question_win,variable = self.occupation_v
            ,text = 'C.科研', value = 2).place(in_ = self.question_win, x = 230, y = 300)
        Radiobutton(self.question_win,variable = self.occupation_v
            ,text = 'D.其他工作者', value = 3).place(in_ = self.question_win, x = 330, y = 300)
        #Radiobutton(self.question_win,variable = self.occupation_v
        #    ,text = 'E.硕士', value = 4).place(in_ = self.question_win, x = 430, y = 300)
        #Radiobutton(self.question_win,variable = self.occupation_v
        #    ,text = 'F.博士', value = 5).place(in_ = self.question_win, x = 530, y = 300)

        netage_label = Label(self.question_win, text = "5.请问您的网龄:", font = font)
        netage_label.place(in_ = self.question_win, x = 10, y = 340)

        self.netage_v = IntVar()
        self.netage_v.set(init_sel)   #user_data["netage"])
        Radiobutton(self.question_win,variable = self.netage_v
            ,text = 'A.0-1年', value = 0).place(in_ = self.question_win, x = 30, y = 370)
        Radiobutton(self.question_win,variable = self.netage_v
            ,text = 'B.1-5年', value = 1).place(in_ = self.question_win, x = 130, y = 370)
        Radiobutton(self.question_win,variable = self.netage_v
            ,text = 'C.5年以上', value = 2).place(in_ = self.question_win, x = 230, y = 370)
        #Radiobutton(self.question_win,variable = self.netage_v
        #    ,text = 'D.其他工作者', value = 3).place(in_ = self.question_win, x = 330, y = 370)
        """
        # 省
        area_label = Label(self.question_win, text = "6.请问您所在的省市是:", font = font)
        area_label.place(in_ = self.question_win, x = 10, y = 410)

        self.area_v = StringVar()
        self.area_v.set(user_data["province"])
        Entry(self.question_win ,textvariable = self.area_v).place(in_ = self.question_win,
            x = 250, y = 410, width = "100")
        #Label(self.question_win, text = "*格式:").place(in_ = self.question_win,
        #    x = 400, y = 410)

        # 市
        self.area_city_v = StringVar()
        self.area_city_v.set(user_data["city"])
        Entry(self.question_win ,textvariable = self.area_city_v).place(in_ = self.question_win,
            x = 400, y = 410, width = "100")
        #Label(self.question_win, text = "*格式:").place(in_ = self.question_win,
        #    x = 700, y = 410)
        txt = "省市格式:直辖市(北京市,北京市)  其他(山东省,济南市)"
        Label(self.question_win, text = txt, foreground = "#0000ff").place(in_ = self.question_win,
            x = 200, y = 450)
        """
        tip = "提示:点击确定后会使用api查询ip归属地，短时间频繁查询会导致查询时间较长(大约20秒)，请耐心等待"
        self.tip = Label(self.question_win, text = tip, foreground = "#0000ff")
        self.tip.place(in_ =self.question_win, x = 30, y = 500)

        self.err_info = Label(self.question_win, text = "", foreground = "#ff0000")
        self.err_info.place(in_ = self.question_win, x = 10, y = 530)
        #self.tip.place(in_ =self.question_win, x = 30, y = 450)
        #self.tip.place_forget()
        #self.tip.place(in_ =self.question_win, x = 30, y = 450)

        # 确定
        ok_button = Button(self.question_win, text = "确定", command = self.ok)
        ok_button.place(in_ = self.question_win, x = 400, y = 450)
        
        self.question_win.update()
        self.question_win.deiconify()
        self.question_win.mainloop()

    def question_win_kill(self):
        self.stop_flag = True
        self.question_win.destroy()

    def ok(self):
        # 问卷ok按钮回调函数，获取用户信息，保存到数据库中
        # 得到用户id，用于后续测试
        gender = self.gender_v.get()
        age = self.age_v.get()
        education = self.education_v.get()
        occupation = self.occupation_v.get()
        netage = self.netage_v.get()

        # 用户选择检查
        if gender == -1:
            self.err_info.config(text = "error:请选择您的性别(问题1)")
            return
        if age == -1:
            self.err_info.config(text = "error:请选择您的年龄(问题2)")
            return
        if education == -1:
            self.err_info.config(text = "error:请选择您的教育背景(问题3)")
            return
        if occupation == -1:
            self.err_info.config(text = "error:请选择您的职业(问题4)")
            return
        if netage == -1:
            self.err_info.config(text = "error:请选择您的网龄(问题5)")
            return
        self.err_info.config(text = "")
        #print type(city)
        #city = city.encode("gb2312")
        # print city
        #print city
        #city = city.encode("utf-8")
        #print type(city)

        # 通过ip获取用户归属地信息
        pos_info = None
        
        pos = position.position()

        #pos[0] = False
        if pos[0] == False:
            # 失败
            self.err_info.config(text = "error:获取归属地信息失败" + str(pos[1]))
            pos_info = pos[2]
            #time.sleep(10)
        else:
            pos_info = pos[1]
            
        
        #city = city.encode("utf-8")
        #province = province.encode("utf-8")
        res, e = self.db_saver.save_user(gender, age, education,
         occupation, netage, pos_info)
        
        if res == False:
            self.err_info.config(text = "error:" + str(e))
        else:
            #my_pickle.save(gender, age, education, occupation, netage, city, province)
            #self.tip.place_forget()
            self.user_id = e
            self.question_win.destroy()

    def main(self):
        # 问卷窗口
        self.questionnaire()
        # 用户点击关闭问卷窗口
        if self.stop_flag:
            return

        # root窗口，主测试窗口
        self.root = Tk()
        self.root.withdraw()
        self.root.title("网站评价")
        self.root.iconbitmap('logo.ico')
        self.root.resizable(True, False)
        w = 750
        h = 550
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry('%dx%d+%d+%d' %(w, h, x, y))

        # frame框架
        self.text_frame = Frame(self.root, height = 250)
        self.list_frame = Frame(self.root, height = 300)
        self.list_frame.pack(side = TOP, fill = X)
        self.text_frame.pack(side = BOTTOM, fill = X)
        self.list_frame.propagate(0)
        self.text_frame.propagate(0)

        # 字体
        font = ("宋体", 12, "")
        # 运行信息列表
        self.scrollbar = Scrollbar(self.list_frame, orient = VERTICAL)
        self.listbox = Listbox(self.list_frame, yscrollcommand = self.scrollbar.set
            , height = 15, font = font)
        self.scrollbar.configure(command = self.listbox.yview)
        self.listbox.pack(side = LEFT, fill = BOTH, expand = 1)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        # 提示label
        self.label = Label(self.text_frame, text = "", font = font)
        self.label.place(in_ = self.text_frame, x = 10, y = 20)

        font2 = ("宋体", 11, "")

        self.tip_txt_test = ">部分网站获取数据较慢,可能会达到超时时间(5分钟),请耐心等待！\r\n"
        self.tip_txt_test += ">测试过程中，不要关闭测试浏览器和测试控制台!"

        self.tip_txt_score = ">网站访问出现任何故障,例如DNS解析失败;链接RESET;404;502等用户评价选[A.不满意]！\r\n"
        self.tip_txt_score += ">网站出现超时，用户评价请选择[A.不满意]！\r\n"

        self.tip = Label(self.text_frame, foreground = "#0000cc", text = self.tip_txt_test,
                        font = font2)
        self.tip.place(in_ = self.text_frame, x = 20, y = 150)
        # 选项按钮
        self.score_v = IntVar()
        self.score_v.set(-1)

        # radiobutton
        self.sel_item1 = Radiobutton(self.text_frame,variable = self.score_v
                                    ,text = 'A.不满意', value = 0)
        self.sel_item2 = Radiobutton(self.text_frame,variable = self.score_v
                                    ,text = 'B.较差', value = 1)
        self.sel_item3 = Radiobutton(self.text_frame,variable = self.score_v
                                    ,text = 'C.正常', value = 2)
        self.sel_item4 = Radiobutton(self.text_frame,variable = self.score_v
                                    ,text = 'D.较好', value = 3)
        self.sel_item5 = Radiobutton(self.text_frame,variable = self.score_v
                                    ,text = 'E.满意', value = 4)
        
        # 驱动按钮
        self.next_button = Button(self.text_frame, text="运行", command = self.run_test)
        self.save_button = Button(self.text_frame, text="保存", command = self.save_score)
        self.next_button.place(in_ = self.text_frame, x = 100, y = 100)
        self.save_button.place(in_ = self.text_frame, x = 300, y = 100)
        self.save_button.config(state = "disabled")

        # 取第一个url
        self.index += 1
        url_flag, url = self.url.get_next()

        if url_flag == False:
            # 没有url
            self.list_insert_error("##没有url,测试完成!##")
            self.next_button.config(state = "disabled")
            self.root.update()
            self.root.deiconify()
            self.root.mainloop()
        else:
            # 提示信息
            self.list_insert("##一共需要测试 [" + str(self.configer.url_num) + "] 个url##")
            self.all_url_num = self.configer.url_num 
            #self.list_insert_error("**注意,当访问的网站出现故障时，用户的评价应为不满意！")
            self.list_insert(str(self.index) + ".当前测试:" + url[1] + '(' + url[0] + ')')
            self.list_insert(self.prefix + "点击 [运行] 按钮,测试网站性能!")
            self.cur_url = url
            self.label.config(text = str(self.index) + ".当前测试网站(" + "网址:" 
                + self.cur_url[1] + " 类别:" + self.cur_url[0] + " 序号:" + str(self.index) 
                + " 剩余:" + str(self.all_url_num - self.index) + ")")

            self.root.update()
            self.root.deiconify()
            self.root.mainloop()

    def show_entry(self):
        self.tip.config(text = self.tip_txt_score)
        self.label.config(text = str(self.index) + ".您对网站(" + "网址:" + 
            self.cur_url[1] + " 类别:" + self.cur_url[0] + ")的评价:")
        self.sel_item1.place(in_ = self.text_frame, x = 30, y = 60)
        self.sel_item2.place(in_ = self.text_frame, x = 130, y = 60)
        self.sel_item3.place(in_ = self.text_frame, x = 230, y = 60)
        self.sel_item4.place(in_ = self.text_frame, x = 330, y = 60)
        self.sel_item5.place(in_ = self.text_frame, x = 430, y = 60)
    
    def hide_entry(self):
        self.tip.config(text = self.tip_txt_test)
        self.label.config(text = "")
        self.sel_item1.place_forget()
        self.sel_item2.place_forget()
        self.sel_item3.place_forget()
        self.sel_item4.place_forget()
        self.sel_item5.place_forget()

    def save_score(self):
        # 保存用户评分和测试结果数据
        # 评价
        score = self.score_v.get()
        # 如果用户未选择满意度
        if score == -1:
            self.list_insert_error(self.prefix + "##请选择您的满意度##")
            return

        self.save_button.config(state = "disabled")

        # 保存到数据库
        #save_flag = self.saver.save(self.cur_url[1], self.res, score)
        db_flag = None
        e = None
        if len(self.res) == 1:
            db_flag, e = self.db_saver.save_timeout(self.user_id, self.cur_url[1], self.res[0], 
                score)
        else:
            db_flag, e = self.db_saver.save(self.user_id, self.cur_url[1],
                self.res[0], self.res[1], self.res[2], score)

        if db_flag:
            if e == None:
                self.list_insert(self.prefix + "保存到数据库成功!")
            else:
                self.list_insert_error(self.prefix + "##保存到数据库失败,属性值缺失("+ str(e) 
                    + "),继续测试!##")
        else:
            self.list_insert_error(self.prefix + "##保存到数据库失败,点击[保存]重试!##")
            self.list_insert_error(self.prefix + "##error:" + str(e) + "##")
            self.save_button.config(state = "normal")
            return

        #if save_flag:
        #    self.list_insert(self.prefix + "保存到文件成功!")
        #else:
        #    self.list_insert(self.prefix + "保存到文件失败!")

        # 当前测试结果保存成功，取下一个url测试
        """
        self.index += 1
        url_flag, url = self.url.get_next()
        if url_flag == False:
            self.list_insert("**没有下一个url,测试完成!**")
            return
        self.list_insert(str(self.index) + ".当前测试:" + url[1] + '(' + 
            url[0] + ')')
        self.cur_url = url
        self.label.config(text = str(self.index) + ".您对网站(" + "网址:" + self.cur_url[1] + " 类别:" + 
            self.cur_url[0] + ")的评价:")
        self.list_insert(self.prefix + "点击run按钮,运行下一个网站的测试!")

        self.next_button.config(state = "normal")
        """
        self.score_v.set(-1)
        self.list_insert("")
        self.hide_entry()
        self.get_next_url()

    def get_next_url(self):
        self.index += 1
        url_flag, url = self.url.get_next()
        if url_flag == False:
            self.list_insert_error("##没有下一个url,测试完成!##")
            browser.close_browser()
            return
        self.list_insert(str(self.index) + ".当前测试:" + url[1] + '(' + url[0] + ')')
        self.cur_url = url
        self.label.config(text = str(self.index) + ".当前测试网站(" + "网址:" + self.cur_url[1]
            + " 类别:" + self.cur_url[0] + " 序号:" + str(self.index) 
            + " 剩余:" + str(self.all_url_num - self.index) + ")")
        self.list_insert(self.prefix + "点击 [运行] 按钮,运行下一个网站的测试!")

        self.next_button.config(state = "normal")

    def run_test(self):
        # 测试
        # 关闭浏览器
        browser.close_browser()
        if self.cur_url[1] == None:
            self.next_botton.config(state = "disabled")
            return
        
        self.list_insert(self.prefix + "清理dns缓存...")
        res = dns.clear_dns()
        if res:
            self.list_insert(self.prefix + "缓存清理成功!")
        else:
            self.list_insert_error(self.prefix + "##缓存清理失败,点击 [运行] 重新运行##")
            self.next_botton.config(state = "normal")
            return
        # 用于从通信队列中取消息，同步窗口界面和测试线程
        self.period_call()

        self.next_button.config(state = "disabled")
        
        # 启动测试线程
        handle = threading.Thread(target = Main.run_thread, args=(self,))
        handle.setDaemon(True)
        handle.start()
    
    def period_call(self):
        # 从消息队列中取消息，用于同步窗口线程和测试线程
        msg = None
        end_flag = False
        while self.queue.qsize():
            try:
                # 队列中获取消息
                msg = self.queue.get(0)
                # 根据消息不同执行不同的动作
                if msg == "end":
                    # 测试线程结束，周期调用函数终止
                    end_flag = True
                else:
                    # 继续识别消息
                    com = msg.split("=")
                    if com[0] == "list":
                        # list插入消息
                        self.list_insert(com[1])
                    elif com[0] == "list_error":
                        # list插入错误消息
                        self.list_insert_error(com[1])
                    elif com[0] == "button":
                        # 按钮消息
                        if com[1] == "test":
                            # 继续运行
                            self.list_insert("")
                            self.get_next_url()
                        else:
                            # 正确执行，显示
                            self.show_entry()
                            self.save_button.config(state = "normal")
                    else:
                        # 显示主窗口的消息
                        self.root.deiconify()
                        #self.root.lift()
                        #self.root.wm_attributes('-topmost',1)
            except Queue.Empty:
                pass

        if end_flag == False:
            # 测试线程还在运行，周期回调函数继续调用
            self.root.after(200, self.period_call)

    def run_thread(self):
        # 测试url
        test_flag, self.res = browser.test(self.cur_url[1], self.listbox)
        if test_flag == False:
            # 测试失败
            self.queue.put("list_error=" + self.prefix + "##测试 [" + self.cur_url[1] + "] 失败!##")
            self.queue.put("list_error=" + self.prefix + str(self.res))
            self.queue.put("list_error=" + self.prefix + "##测试异常,点击 [运行] 继续测试##")
            self.queue.put("button=test")
            self.queue.put("root")
            self.queue.put("end")
            return
        elif len(self.res) == 1:
            self.queue.put("list=" + self.prefix + "测试 [" + self.cur_url[1] + "] 超时!")
        else:
            self.queue.put("list=" + self.prefix + "测试 [" + self.cur_url[1] + "] 成功!")
        txt = "根据网站的表现选择您对网站的满意度,然后点击 [保存] 按钮!"
        self.queue.put("list=" + self.prefix + txt)
        self.queue.put("button=save")
        self.queue.put("root")
        self.queue.put("end")

    def list_insert(self, txt):
        self.listbox.insert(END, txt)
        self.listbox.see(END)

    def list_insert_error(self, txt):
        self.listbox.insert(END, txt)
        size = self.listbox.size()
        self.listbox.itemconfig(size - 1, foreground = "#ff0000")
        self.listbox.see(END)
      
if __name__ == '__main__':
    m = Main()
    m.main()