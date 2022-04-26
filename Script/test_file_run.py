#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/25 15:13
# @Author  : WangKai
# @Site    : 
# @File    : test_file_run.py
# @Software: PyCharm

"""
读取excel内容 获取到 {新增excel 读取信息模块}
1。需要获取书名 章节名 初始化进入章节检测到内容 则为成功

获取book的每一章信息
封装基础poco点击寻找模块
封装上级找书模块 消除广告模块 消除弹窗模块
找到目标书本{需要一个可靠的搜索方法，先建一个以书本为名字的excel 读取书本名字在搜索和点击进入章节}

匹配book章节key 精准找到目标书本的章节{需要一个可靠的搜索方法，}
生成阅读每一页的 行动列表->list
循环每一页的行动列表 实例化相对应的方法 从而实现自动化
"""

from commonlib.baselib.excel import Excel
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_DEBUG, LOG_WARN, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
from commonlib.baselib.ControlAdb import phone_wake, start_game, stop_game
from commonlib.baselib.PocoDrivers import poco_try_find_click, poco_try_offspring_click, poco_find

from commonlib.baselib.ConnectAdb import AdbConnect
from poco.drivers.unity3d import UnityPoco
from airtest.core.api import G, sleep, text, touch
import os

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
EXCEL_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "../excel_package"))
LOG_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "../logs"))


# MsgCenter(MODULE_NAME)
# MsgCenter(MODULE_NAME, level=LOG_DEBUG)

class DeviceRun:
    """
    这里写的很烂
    """

    def __init__(self, adb=AdbConnect(), app_name="com.stardust.spotlight", ip="127.0.0.1:5037",
                 local_host="local_host", port=5001, log_fp=LOG_FILES_PATH):
        try:
            # # adb模块实例化
            # self.adb = adb
            # # 获取 device 设备号
            # self.device = adb.get_dev_name()
            # self.log = log_fp
            # self.app_name = app_name
            # # 链接adb
            # self.adb.connect_device(ip=ip, devices_names=self.device, log_path=self.log)
            # # 唤醒机器和打开app
            # phone_wake(G.DEVICE)
            # stop_game(G.DEVICE, self.app_name)
            # start_game(G.DEVICE, self.app_name)
            # sleep(10)
            # # 实例化poco 给下面的函数调
            # self.poco = UnityPoco((local_host, port))
            self.excel_path = EXCEL_FILES_PATH
        except Exception as e:
            LogMessage(module=MODULE_NAME, level=LOG_ERROR, msg=f"Init phone error => {e}")

    def initial_data(self) -> dict:
        """
        获取书名，和书本行动数据
        :return:
        """
        book_list = list()
        name_list = list()
        for file_path, dir_list, files in os.walk(self.excel_path):
            for file_name in files:
                if file_name.endswith(".xlsx"):
                    name_list.append(file_name.split(".")[0])
                    book_list.append(os.path.join(file_path, file_name))

        books_ = dict()
        for index in range(len(name_list)):
            excel = Excel(book_list[index])
            result = excel.get_sheet_names("")
            books_[name_list[index]] = result

        return books_

    def search_book(self, book_name="") -> bool:
        """
        使用搜索框输入书本名字找到对应书籍 初始化进入页面
        :param book_name:书籍名字
        :return:
        """

        try:
            diamond = self.poco("top").offspring("Diamond").child("num").attr("TMP_Text")
            power = self.poco("top").offspring("Power").child("num").attr("TMP_Text")
            poco_try_find_click(self.poco, target_name="Search", module_type="Node")
            poco_try_offspring_click(self.poco, target_name="ViewCanvasUpper", module_type="Node",
                                     offspring_name="InputField")
            text(book_name, enter=False)
            if poco_find(self.poco, target_name="SearchBook(Clone)", module_type="Node"):
                # 这里需要空点一下 以退出输入框
                touch([0.5, 0.5])
                poco_try_find_click(self.poco, target_name="SearchBook(Clone)", module_type="Node")
                return True
            else:
                # 如果没有搜索到书本则直接关掉游戏 或者等其他处理
                stop_game(G.DEVICE, self.app_name)
                g = DeviceRun()
                g.search_book()
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Init book error -> {e}")
            return False

    def read_books(self, records: dict, ):
        """
        开始阅读书籍 使用初始化方法
        :param records:
        :return:
        """
        name = ""
        value = ""
        for k, v in records.items():
            name = k
            value = v
            print(v)
        print(9981, name)
        print(9981, value)


if __name__ == '__main__':
    test = DeviceRun()
    res = test.initial_data()
    test.read_books(res)
