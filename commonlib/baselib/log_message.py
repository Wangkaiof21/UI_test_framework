#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/21 14:28
# @Author  : WangKai
# @Site    : 
# @File    : log_message.py
# @Software: PyCharm
import os
import sys
import logging
import time
from functools import wraps
from colorama import Fore, Style

TIMER_FLAG = False
# 定义log打印等级
LOG_DEBUG = logging.DEBUG
LOG_INFO = logging.INFO
LOG_WARN = logging.WARN
LOG_ERROR = logging.ERROR
# 自定义log打印等级 增加sys
LOG_SYS = 90
logging.addLevelName(LOG_SYS, "SYS")

# 日志打印等级
_LEVEL_COLOR = {
    LOG_DEBUG: Fore.BLUE,
    LOG_INFO: Fore.WHITE,
    LOG_WARN: Fore.YELLOW,
    LOG_ERROR: Fore.RED,
    LOG_SYS: Fore.GREEN,
}


def LogMessage(level=LOG_INFO, module="NA", msg="NA", logger_name="iAutos"):
    """
    日志输出模块
    :param level:打印等级
    :param module: 模块名
    :param msg: 打印信息
    :param logger_name:
    :return:
    """
    logger = logging.getLogger(logger_name)
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = ""  # LogMessage调用者
    if level == LOG_ERROR or level == LOG_WARN:
        # 获取调用者的函数名
        f_back = sys._getframe().f_back
        co_name = f_back.f_code.co_name
        # 获取调用者的文件名
        file_name = os.path.basename(f_back.f_code.co_filename)
        # 获取当前文件的行号
        line_no = f_back.f_lineno
        caller = f'\t[{file_name}:{line_no}={co_name}]'
    level_name = logging.getLevelName(level)
    color = _LEVEL_COLOR.get(level)
    log_msg = '\n'.join(
        [f'{color}{t}\t{level_name}\t[{module}]\t{row}{caller}{Style.RESET_ALL}' for row in str(msg).split("\n")])
    logger.log(level, log_msg)


if __name__ == '__main__':
    LogMessage(level=LOG_DEBUG)
