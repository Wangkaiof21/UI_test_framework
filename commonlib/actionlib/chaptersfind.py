#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/27 14:54
# @Author  : WangKai
# @Site    : 
# @File    : chaptersfind.py
# @Software: PyCharm
import time


class ChaptersFind:
    def __init__(self, CheckObject, bookid, chapter_id,bookchapter):
        self.bookid = bookid
        self.index = chapter_id
        self.bookchapter=bookchapter
        self.uuid = CheckObject.checkData["conf"]["uuid"]
        self.poco = CheckObject["poco"]
        # self.rpc = DeviceObject["rpc"]
        self.pos = PosTurn([0.5, 0.3],  CheckObject["adb"])
        self.mpackage=CheckObject.M_package
        self.sequel_from = None
        self.ticket = None
        self.diamond = None
        print("用户id",self.uuid)

    def escape_AD(self):
        """广告处理"""
        re = api_getAdConfigApi(self.uuid)
        if re["is_pay_user"] == 0:
            if poco_tryfind(self.poco, "TxtFree", "非付费用户章节头广告",waitTime=5):
                touch(self.pos)
                keyevent("HOME")
                start_app(self.mpackage)
                sleep(2)
                keyevent("HOME")
                start_app(self.mpackage)
                sleep(2)
            try:
                if self.poco("SceneBG").exists():
                    return
                else:
                    keyevent("HOME")
                    start_app(self.mpackage)
                    sleep(2)
            except:
                pass
        else:
            po_tryClick(self.poco, "UIABBonusFrame", "BtnSkip", description="付费用户章节头奖励")

    def action_choiceRead(self):
        """选择书籍和章节动作已经点击"""
        self.ini_bookData()  # 阅读数据初始化
        re_choice_bookid,desc = self.choice_bookid()  # 选择书籍
        if not re_choice_bookid:
            return False,desc
        sleep(2)
        re_choice_chapters,desc = self.choice_chapters()  # 选择章节
        if not re_choice_chapters:
            return False,desc
        re_play = Bookfind.click_Play(self.poco, self.sequel_from)
        if not re_play:
            return False, "点击play按钮失败"
        re = self.bookLoad()  # 书籍加载
        if not re:
            poco_click(self.poco, "HomeBtn", "HomeBtn", description="加载书籍超时,返回大厅")
            Bookfind.click_Play(self.poco, self.sequel_from)
        sleep(3)
        self.escape_AD() #广告处理
        return True,'OK'

    # def chapter_check(self):
    #     chapterProgress= get_ReadProgress(self.rpc)["Item2"]  # 更新本地当前阅读对话进度
    #     if self.bookchapter!=chapterProgress:
    #


    def choice_bookid(self):
        """新版本查找"""
        # self.poco("InputField").wait(3).set_text(self.bookid)
        po_trySetText(self.poco, "InputField", self.bookid)
        poco_clicked(self.poco, "SearchBtn", description="bookid搜索按钮", waitTime=3, sleeptime=2)
        if poco_tryfind(self.poco, "UIVisualDetailView", "书籍详情页", waitTime=2):
            return True,'OK'
        elif poco_tryfind(self.poco, "UIBookErrorEmail", "书籍详情页"):
            log(Exception("书籍不存在"), snapshot=True)
            return False,'书籍不存在'
        else:
            log(Exception("查找书籍异常原因未知"), snapshot=True)
            return False,'查找书籍异常,原因未知'

    def choice_chapters(self):
        '''选择章节'''
        time = 3
        while time > 0:
            time -= 1
            try:
                po_trySetText(self.poco, "TestInput", set_text=self.index)
                poco_clicked(self.poco,"TestInput", description="搜索框", sleeptime=1)
                poco_clicked(self.poco,"UIVisualDetailView", description="详情页")
                chapterInfo = self.poco("UIVisualDetailView").offspring("Detail").get_TMPtext()
                listInfo = chapterInfo.split(" ")
                if int(listInfo[1]) == int(self.index):
                    return True,'OK'
            except Exception as e:
                print(e)
        return False,'选择章节异常'
        # raise Exception("选择章节异常")

    def click_Play(poco, sequel_from):
        """新版本的play"""
        if po_tryClick(poco, "Play", "Play", description="Play按钮", waitTime=5):
            pass
        else:
            po_tryClick(poco, "DaypassPlay", "DaypassPlay", description="Daypass按钮", waitTime=1)
        if sequel_from:
            po_tryClick(poco, "UpBtn", "UpBtn", description="Yes,I do")
        return True

    def ini_bookData(self):
        """阅读条件检查"""
        self.getUsercurrency()
        data = booklistInfoApi(self.uuid, bookId=self.bookid)  # 拉取书籍详情
        if "sequel_from" not in data.keys():
            self.sequel_from = False
        else:
            self.sequel_from = data["sequel_from"]

        try:
            self.sequel_from = data["sequel_from"]

        except:
            self.sequel_from = False
            print("不存在sequel_from")

    def bookLoad(self):
        """书籍加载DefaultBg"""
        self.download_bookresource(self.bookid)
        self.download_bookresource(self.bookchapter)
        startime = time.time()
        sleep(2)
        loadtime=0
        while loadtime<2000:
            loadtime = time.time() - startime
            if loadtime > 2000:
                poco_click(self.poco, "HomeBtn", "HomeBtn", description="加载书籍超时,返回大厅")
                log(Exception("加载书籍异常"), snapshot=True)
                raise Exception("加载书籍超时")
            if poco_tryfind(self.poco, "SimpleHome", description="书籍场景") or poco_tryfind(self.poco, "UIBeginAdShow", description="AD广告") or poco_tryfind(self.poco, "UIABBonusFrame", description="AB广告"):
                log("完成书籍加载".format(loadtime), timestamp=time.time(), desc="完成书籍加载", snapshot=True)
                return True



        log(Exception("加载书籍异常"), snapshot=True)
        return False

    def download_bookresource(self,bookid):
        """拉取书籍资源"""

        file = os.path.join(path_resource,bookid)
        mybool = os.path.exists(file)
        if mybool:
            return True
        re = api_avgcontentApi(bookid)
        if re:
            print("下载书籍配置成功")
            return True
        else:
            return False

    def click_close(self):
        """详情页关闭按钮"""
        po_tryClick(self.poco, "UIVisualDetailView", "Close", description="关闭详情页按钮", waitTime=8)

    def getUsercurrency(self):
        """	虚拟币类型currency"""

        self.diamond = api_syncValue(self.uuid, value_type="diamond")["value"]
        self.ticket = api_syncValue(self.uuid, value_type="ticket")["value"]
        try:
            if int(self.diamond) < 3000:
                self.updateUsercurrency("diamond", "3000")
            if int(self.ticket) < 99:
                self.updateUsercurrency("ticket", "99")
        except:
            print("调用虚拟币接口异常")

        # credit = self.memberInfoApi(self.UserData_dir["uuid"])["data"]["credit"]
        # self.UserData_dir["credit"] = credit

    def updateUsercurrency(self, value_type, number):
        """	修改虚拟币类型currency"""
        api_syncValue(self.uuid, value_type=value_type, valuechange=number)

