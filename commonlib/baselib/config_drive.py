#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 10:41
# @Author  : WangKai
# @Site    : 
# @File    : config_drive.py
# @Software: PyCharm
"""
需求：
读取excel内容 获取到 {新增excel 读取信息模块}
1。需要获取书名 章节名 初始化进入章节检测到内容 则为成功

获取book的每一章信息
封装基础poco点击寻找模块
封装上级找书模块 消除广告模块 消除弹窗模块
找到目标书本{需要一个可靠的搜索方法，先建一个以书本为名字的excel 读取书本名字在搜索和点击进入章节}

匹配book章节key 精准找到目标书本的章节{需要一个可靠的搜索方法，}
生成阅读每一页的 行动列表->list
循环每一页的行动列表 实例化相对应的方法 从而实现自动化
5.1348
"""

from commonlib.baselib.excel import Excel
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_DEBUG, LOG_WARN, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
from commonlib.baselib.ControlAdb import phone_wake, start_game, stop_game
from commonlib.baselib.Config import ConfigView
from commonlib.baselib.PocoDrivers import poco_try_find_click, poco_send_text, poco_try_offspring_click, poco_find, \
    poco_play_dialog_rename, \
    poco_play_dialog, poco_select_skin, poco_cosplay_cossuit, poco_play_dialog_monologue, poco_play_dialog_voiceover, \
    poco_play_dialog_dialog_noshow, \
    poco_play_dialog_think, poco_play_dialog_dialog, poco_option_list, poco_lens_move, \
    poco_lens_move_voiceover, poco_get_element_attr

from commonlib.baselib.ConnectAdb import AdbConnect
from poco.drivers.unity3d import UnityPoco
from airtest.core.api import G, sleep, text, touch
import os
import numpy as np

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
TEST_OR_NOT = 'test_or_not'
TYPE = "type"
DIALOG_TYPE = "dialog_type"
BRANCH_TREE = 'branch_tree'
WAIT_TIME = "time_scale"
DIALOG_NO = "dialog_no"

MsgCenter(MODULE_NAME)


# MsgCenter(MODULE_NAME, level=LOG_DEBUG)

class DeviceRun:
    """
    这里写的不好
    test_mode模式是测试用 只读取excel数据不进行手机的初始化
    test_mode模式为True则 初始化机器 唤醒 和打开app 把app的sdk poco实例化给self.poco
    """

    def __init__(self, app_name="com.stardust.spotlight", ip="127.0.0.1:5037",
                 local_host="local_host", port=5001, log_fp=None, test_mode=False, excel_path=None):
        self.test_mode = test_mode

        if not self.test_mode:
            try:
                # adb模块实例化
                self.adb = AdbConnect()
                # 获取 device 设备号
                self.device = self.adb.get_dev_name()
                self.log = log_fp
                self.app_name = app_name
                # 链接adb
                self.adb.connect_device(ip=ip, devices_names=self.device, log_path=self.log)
                # 唤醒机器和打开app
                phone_wake(G.DEVICE)
                stop_game(G.DEVICE, self.app_name)
                start_game(G.DEVICE, self.app_name)
                sleep(7.5)
                # 实例化poco 给下面的函数调
                self.poco = UnityPoco((local_host, port))
                self.excel_path = excel_path

            except Exception as e:
                LogMessage(module=MODULE_NAME, level=LOG_ERROR, msg=f"Init phone error => {e}")
        else:
            try:
                self.excel_path = ConfigView.EXCEL_FILES_PATH
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
                    book_abs_path = os.path.join(file_path, file_name)
        book = dict()
        excel = Excel(book_abs_path)
        sheet_names = excel.sheet_list
        book[book_abs_path] = sheet_names
        return book

    def cancel_all_popups(self):
        """
        取消所有弹窗
        :return:
        """
        pass

    def search_book(self, book_name="") -> bool:
        """
        使用搜索框输入书本名字找到对应书籍 初始化进入页面
        :param book_name:书籍名字
        :return:
        """
        # 冻结元素前等待时间
        ele_time = 0.2
        try:
            # 母亲节弹窗临时处理 以后全部弹窗做处理
            # poco_try_find_click(self.poco.freeze(), target_name="close", module_type="Image")
            diamond_num = poco_get_element_attr(self.poco, wait_time=ele_time, name="top", type_="Node",
                                                offspring_="Diamond", child_="num", ele_name="TMP_Text")
            power_num = poco_get_element_attr(self.poco, wait_time=ele_time, name="top", type_="Node",
                                              offspring_="Power", child_="num", ele_name="TMP_Text")
            LogMessage(level=LOG_INFO, module=MODULE_NAME,
                       msg=f"Init the game has Diamond:{diamond_num} Power:{power_num}")

            poco_try_find_click(self.poco, target_name="Search", module_type="Node")
            poco_try_offspring_click(self.poco, target_name="ViewCanvasUpper", module_type="Node",
                                     offspring_name="Text Area", wait_time=ele_time)
            poco_send_text(self.poco, text_=book_name)
            touch([0.5, 0.5])
            # 这里需要空点一下 以退出输入框
            poco_try_find_click(self.poco, target_name="SearchBook(Clone)", module_type="Node")
            poco_try_offspring_click(self.poco, target_name="ViewCanvasUpper", module_type="Node",
                                     offspring_name="Reset", wait_time=ele_time)
            poco_try_offspring_click(self.poco, target_name="ViewCanvasHighest", module_type="Node",
                                     offspring_name="ComfirmBtn", wait_time=ele_time)
            # else:
            #     # 如果没有搜索到书本则直接关掉游戏 或者等其他处理
            #     stop_game(G.DEVICE, self.app_name)
            #     g = DeviceRun()
            #     g.search_book(book_name)
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Init book error -> {e}")
            return False

    def wash_the_books_action(self, records: dict):
        """
        清洗excel读出来的数据
        使用初始化方法 进入游戏

        :param records:
        :return:
        """
        books_ = dict()
        (book_abs, sheets_list), = records.items()
        book_name = os.path.basename(book_abs).split(".")[0]
        excel = Excel(book_abs)
        # 清洗数据 把test_or_not标记为yes的留下 重新组装字典
        chapter_dict = dict()
        for sheet_ in sheets_list:
            clean_list = list()
            ch_result = excel.records_get(sheet_)
            # 筛选出带yes标记的信息
            for line in ch_result:
                if line[TEST_OR_NOT] != "yes":
                    continue
                clean_list.append(line)
            chapter_dict[sheet_] = clean_list
        books_[book_name] = chapter_dict

        for book_name, datas in books_.items():
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Test book -> {book_name}")
            for ch_num, ch_page_data in datas.items():
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Chapter_No.{ch_num} -> Test page -> {ch_page_data}")

        return books_, book_name

    def select_chapters_first_entry(self, book_datas):
        """
        解包书本excel数据 选择章节
        :param book_datas:
        :return:
        """
        (book_name, chapters_value), = book_datas.items()
        sleep(1)
        for key, values in chapters_value.items():
            if not values:
                continue
            # 章节名的最后一个数字 做选章节的操作 这个其实不够保险
            self.click_chapter(ch_index=key)
            # 章节的条目数据 就是每一步的行动数据 对这个精细操作
            try:
                for entry in values:
                    # 解析 条目数据
                    self.confirm_executable_method(entry.get(TYPE), entry.get(DIALOG_TYPE), entry.get(BRANCH_TREE),
                                                   entry.get(WAIT_TIME), entry.get(DIALOG_NO))

            except Exception as e:
                LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Read entry error -> {e}! ")
            break

    def click_chapter(self, ch_index, ch_read_model=None) -> None:
        """
        这里假设是从第一章节读起 后续要做成只读某几章节
        :param ch_index:
        :param ch_read_model: 区间章节阅读标记
        :return:
        """
        try:
            ch_index = int(ch_index[-1]) - 1
            if ch_index == 0:
                # poco_try_find_click(self.poco.freeze(), target_name="Search", module_type="Node", list_num=ch_index)
                poco_try_find_click(self.poco.freeze(), target_name="Play", module_type="Node")
                sleep(7)
            else:
                poco_try_find_click(self.poco.freeze(), target_name="Play", module_type="Node")
                sleep(7)
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Chapter.{ch_index} Not find Play button -> {e}")

    def gen_str(self, d_type_str):
        if not d_type_str:
            return ""
        else:
            return d_type_str.split(",")[0]

    def confirm_executable_method(self, type_str: str, dialog_type_str: str, branch_tree: str, wait_time_: str,
                                  dia_log_id: str):
        """
        切割字符串 获取list 取action的交集
        import numpy
        array1 = ["play_dialog","play_sound","animation_role","phone","animation_role",]
        array2 = ["select_skin", "play_dialog", "cosplay_cossuit", "option_list"]
        c = numpy.intersect1d(array1, array2, assume_unique=False, return_indices=False)
        :param type_str:行动类型
        :param dialog_type_str:行动细分类型
        :param branch_tree:条目数量
        :param wait_time_:镜头运动时间 画外音可能要取消
        :param dia_log_id: 页数ID
        :return:
        """
        try:
            dialog_type_str = self.gen_str(dialog_type_str)
            # 可执行动作的list 多个行动对多个行动不好处理
            func_names = type_str.split(",")[:-1]
            result_index = self.union_data(func_names, ConfigView.EXECUTABLE_LIST)
            # result_index = numpy.intersect1d(func_names, ConfigView.EXECUTABLE_LIST, assume_unique=False,
            #                                  return_indices=False)
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"{result_index, dialog_type_str}")
            if len(result_index) > 1 and result_index.count('lens_move'):
                for action in result_index:
                    if action == 'lens_move':
                        self.execute_read_action(action_name=action, action_type=dialog_type_str,
                                                 branch_index=branch_tree, wait_time=0,
                                                 action_id=dia_log_id)
                    else:
                        self.execute_read_action(action_name=action, action_type=dialog_type_str,
                                                 branch_index=branch_tree, wait_time=wait_time_,
                                                 action_id=dia_log_id)
            else:
                for action in result_index:
                    self.execute_read_action(action_name=action, action_type=dialog_type_str, branch_index=branch_tree,
                                             wait_time=wait_time_,
                                             action_id=dia_log_id)
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Func error -> {e}")
        print("\n")

    def union_data(self, array_1, array_2):
        """

        :param array_1:
        :param array_2:
        :return:
        """
        if len(set(array_1) & set(array_2)) == 0:
            return []
        elif len(set(array_1) & set(array_2)) >= 1:
            return list(set(array_1) & set(array_2))

    def execute_read_action(self, action_name, action_type, branch_index, wait_time, action_id):
        """
        上层可以控制这里的输入 ['lens_move', 'play_dialog'] 不能等待两次
        这里是执行字符串转方法实例化的地方 会返回布尔值 来确定条目过不过
        # 这里要实现先等待 再冻结 再点击的功能 没有则直接返回False 报没这个元素
        :param action_name: 行动名
        :param action_type: 行动详细
        :param branch_index: 分枝树
        :param wait_time: 等待时间
        :param action_id: 条目id 用来展示用
        :return:
        """
        index = poco_get_element_attr(self.poco, wait_time=0.2, name="top", type_="Node",
                                      offspring_="index", child_="index_", ele_name="TMP_Text")
        run_time = 0
        while run_time < 2:
            if action_name and action_type:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Func start ID: {action_id} poco_{action_name}_{action_type}"
                               f" wait_time -> {wait_time} second")
                if globals()[f"poco_{action_name}_{action_type}"](self.poco, wait_time) and index == "start":
                    LogMessage(level=LOG_INFO, module=MODULE_NAME,
                               msg=f"poco_{action_name}_{action_type} run success")
                    # 确认多一次index是否为结束
                    break

            elif action_name and not action_type and not branch_index:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Func start ID: {action_id} poco_{action_name} wait_time -> {wait_time} second")
                if globals()[f"poco_{action_name}"](self.poco, wait_time) and index:
                    LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"poco_{action_name} run success")
                    break

            elif action_name and not action_type and branch_index:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Func start ID: {action_id} poco_{action_name} -> branch {int(branch_index)} "
                               f"wait_time -> {wait_time} second")
                if globals()[f"poco_{action_name}"](self.poco, int(branch_index), wait_time) and index:
                    LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"poco_{action_name} run success")
                    break
            # break
            run_time += 1


if __name__ == '__main__':
    TEST_RANK = True
    if TEST_RANK:
        test = DeviceRun(excel_path=ConfigView.EXCEL_FILES_PATH, log_fp=ConfigView.LOG_FILES_PATH)
        res = test.initial_data()
        res_dict, book_name_ = test.wash_the_books_action(res)
        test.search_book(book_name=book_name_)
        # test.select_chapters_first_entry(res_dict)
    else:
        test = DeviceRun(test_mode=True, excel_path=ConfigView.EXCEL_FILES_PATH, log_fp=ConfigView.LOG_FILES_PATH)
        res = test.initial_data()
        res_dict, book_name_ = test.wash_the_books_action(res)
        # test.search_book(book_name=book_name_)
        test.select_chapters_first_entry(res_dict)
