#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/5 11:26
# @Author  : WangKai
# @Site    : 
# @File    : Config.py
# @Software: PyCharm
# 请求头json数据 和一些配置
import os


class ConfigView:
    LOGIN_HEADER = {
        'timestamp': '',
        'sign': '',
        'noise': '',
        'did': '',
        'version': '3.151.1',
        'channel': 'AVG10003',
        'package-name': 'com.stardust.spotlight',
        'Accept-Language': 'en',
        'dievel': '_medium'
    }
    EXECUTABLE_LIST = ["select_skin", "play_dialog", "cosplay_cossuit", "option_list", "lens_move"]
    EXCEL_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../excel_package"))
    LOG_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../logs"))
