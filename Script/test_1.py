#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 16:11
# @Author  : WangKai
# @Site    : 
# @File    : test_1.py
# @Software: PyCharm
"""
读取excel内容 获取到 {新增excel 读取信息模块}
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
import os


def test_1(fp):
    fp = "C:\\Users\\王凯\Desktop\\test_file\\UI_test_framework\\excel_package\\Behind Closed Doors.xlsx"
    excel = Excel(fp)
    # s = excel.records_get("dialog_10190001")
    s = excel.get_sheet_names("sss")


if __name__ == '__main__':
    excel_base_path = ""
    fp = os.path.abspath(os.path.join(os.getcwd(), "../../excel_package/Behind Closed Doors.xlsx"))
    test_1(fp)
