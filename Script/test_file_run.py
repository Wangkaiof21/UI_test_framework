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

from commonlib.baselib.PocoDrivers import poco_try_find_click, poco_try_offspring_click, poco_find, \
    poco_play_dialog_rename, \
    poco_play_dialog, poco_select_skin, poco_cosplay_cossuit, poco_play_dialog_monologue, poco_play_dialog_voiceover, \
    poco_play_dialog_dialog_noshow, \
    poco_play_dialog, poco_play_dialog_think, poco_play_dialog_dialog

from commonlib.baselib.ConnectAdb import AdbConnect
from poco.drivers.unity3d import UnityPoco
from airtest.core.api import G, sleep, text, touch
import os

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
EXCEL_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "../excel_package"))
LOG_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "../logs"))
TEST_OR_NOT = 'test_or_not'
TYPE = "type"
DIALOG_TYPE = "dialog_type"
EXECUTABLE_LIST = ["select_skin", "play_dialog", "cosplay_cossuit"]

MsgCenter(MODULE_NAME)


# MsgCenter(MODULE_NAME, level=LOG_DEBUG)

class DeviceRun:
    """
    这里写的很烂
    """

    def __init__(self, adb=AdbConnect(), app_name="com.stardust.spotlight", ip="127.0.0.1:5037",
                 local_host="local_host", port=5001, log_fp=LOG_FILES_PATH, test_mode=False):
        self.test_mode = test_mode

        if not self.test_mode:
            try:
                # adb模块实例化
                self.adb = adb
                # 获取 device 设备号
                self.device = adb.get_dev_name()
                self.log = log_fp
                self.app_name = app_name
                # 链接adb
                self.adb.connect_device(ip=ip, devices_names=self.device, log_path=self.log)
                # 唤醒机器和打开app
                phone_wake(G.DEVICE)
                stop_game(G.DEVICE, self.app_name)
                start_game(G.DEVICE, self.app_name)
                sleep(14)
                # 实例化poco 给下面的函数调
                self.poco = UnityPoco((local_host, port))
                self.excel_path = EXCEL_FILES_PATH
            except Exception as e:
                LogMessage(module=MODULE_NAME, level=LOG_ERROR, msg=f"Init phone error => {e}")
        else:
            try:
                self.excel_path = EXCEL_FILES_PATH
            except Exception as e:
                LogMessage(module=MODULE_NAME, level=LOG_ERROR, msg=f"Init phone error => {e}")

    def initial_data(self) -> dict:
        """
        获取书名，和书本章节
        这里应该为未来多本书籍做准备 测试阶段只支持一本书籍

        :return: 返回{书籍名:[章节名1，章节名2，章节名3.......],书籍名:[章节名1，章节名2，章节名3.......]}
        """
        book_abs_path = ""
        for file_path, dir_list, files in os.walk(self.excel_path):
            for file_name in files:
                if file_name.endswith(".xlsx"):
                    # name_ = file_name.split(".")[0]
                    book_abs_path = os.path.join(file_path, file_name)
        book = dict()
        excel = Excel(book_abs_path)
        sheet_names = excel.sheet_list
        book[book_abs_path] = sheet_names
        return book

    def search_book(self, book_name="") -> bool:
        """
        使用搜索框输入书本名字找到对应书籍 初始化进入页面
        :param book_name:书籍名字
        :return:
        """

        try:
            diamond_num = self.poco("top").offspring("Diamond").child("num").attr("TMP_Text")
            power_num = self.poco("top").offspring("Power").child("num").attr("TMP_Text")
            LogMessage(level=LOG_INFO, module=MODULE_NAME,
                       msg=f"init the game has Diamond:{diamond_num} Power:{power_num}")
            poco_try_find_click(self.poco, target_name="Search", module_type="Node")
            poco_try_offspring_click(self.poco, target_name="ViewCanvasUpper", module_type="Node",
                                     offspring_name="InputField")
            text(book_name, enter=False)
            if poco_find(self.poco, target_name="SearchBook(Clone)", module_type="Node"):
                # 这里需要空点一下 以退出输入框
                touch([0.5, 0.5])
                poco_try_find_click(self.poco, target_name="SearchBook(Clone)", module_type="Node")
                # 重置书籍
                poco_try_find_click(self.poco, target_name="Reset", module_type="Node")
                poco_try_find_click(self.poco, target_name="ComfirmBtn", module_type="Button")
                return True
            else:
                # 如果没有搜索到书本则直接关掉游戏 或者等其他处理
                stop_game(G.DEVICE, self.app_name)
                g = DeviceRun()
                g.search_book(book_name)
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Init book error -> {e}")
            return False

    def wash_the_books_action(self, records: dict) -> dict:
        """
        清洗excel读出来的数据
        使用初始化方法 进入游戏

        :param records:
        :return:
        """
        books_ = dict()
        (book_abs, sheets_list), = records.items()
        book_name = os.path.basename(book_abs).split(".")[0]

        if not self.test_mode:
            self.search_book(book_name)

        excel = Excel(book_abs)
        # 清洗数据 把test_or_not标记为yes的留下 重新组装字典
        clean_dict = dict()
        for sheet_ in sheets_list:
            clean_list = list()
            ch_result = excel.records_get(sheet_)
            # 筛选出带yes标记的信息
            for line in ch_result:
                if line[TEST_OR_NOT] != "yes":
                    continue
                clean_list.append(line)
            clean_dict[sheet_] = clean_list
        books_[book_name] = clean_dict

        for book_name, datas in books_.items():
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Test book -> {book_name}")
            for ch_num, ch_page_data in datas.items():
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Chapter_No.{ch_num} -> Test page -> {ch_page_data}")

        return books_

    def select_chapters_first_entry(self, book_datas):
        """
        这里假设是从第一章节读起 后续要做成只读某几章节
        :param book_datas:
        :return:
        """
        (book_name, chapters_value), = book_datas.items()
        sleep(1)
        for key, value in chapters_value.items():
            if not value:
                continue
            # 章节名的最后一个数字 做选章节的操作 这个其实不够保险
            ch_index = int(key[-1]) - 1
            print("ch_____________________", ch_index)
            if ch_index == 0:
                poco_try_find_click(self.poco, target_name="Search", module_type="Node", list_num=ch_index)
                poco_try_find_click(self.poco, target_name="Play", module_type="Node")
                sleep(7)
            else:
                poco_try_find_click(self.poco, target_name="Play", module_type="Node")
                sleep(7)
            # 章节的条目数据 就是每一步的行动数据 对这个精细操作
            entry_data = value
            self.read_chapters(entry_data)
            break

    def read_chapters(self, entry_data):
        """
        不需要处理状况 根据条目的内容 实例化方法
        :param entry_data:
        :return:
        """
        try:
            index = 1
            for line in entry_data:
                self.confirm_executable_method(line[TYPE], line[DIALOG_TYPE], index)
                # 先解析两个type里面有什么东西
                # 这里直接转换成方法试试？
                index += 1
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Read entry error -> {e}! ")

    def confirm_executable_method(self, type_str: str, dialog_type_str: str, index_):
        """
        切割字符串 获取list
        :param type_str:
        :param dialog_type_str:
        :param index_:条目数量
        :return:
        """
        try:
            dialog_type_str = self.gen_str(dialog_type_str)
            # 可执行动作的list 多个行动对多个行动不好处理
            func_names = type_str.split(",")[:-1]
            for func_name in func_names:
                if EXECUTABLE_LIST.count(func_name) > 0 and dialog_type_str:
                    LogMessage(level=LOG_INFO, module=MODULE_NAME,
                               msg=f"{index_} Func start -> poco_{func_name}_{dialog_type_str}")
                    globals()[f"poco_{func_name}_{dialog_type_str}"](self.poco)
                elif EXECUTABLE_LIST.count(func_name) > 0 and not dialog_type_str:
                    LogMessage(level=LOG_INFO, module=MODULE_NAME,
                               msg=f"{index_} Func start -> poco_{func_name}")
                    globals()[f"poco_{func_name}"](self.poco)
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Func error -> {e}")

    def gen_str(self, d_type_str):
        if not d_type_str:
            return ""
        else:
            return d_type_str.split(",")[0]


if __name__ == '__main__':
    test = DeviceRun()
    # test = DeviceRun(test_mode=True)
    res = test.initial_data()
    res_dict = test.wash_the_books_action(res)
    test.select_chapters_first_entry(res_dict)
