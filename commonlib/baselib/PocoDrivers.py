import time
from time import sleep
import os
from poco.exceptions import PocoNoSuchNodeException
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
from airtest.core.api import text, touch

# from airtest.core.api import G, sleep, text, touch

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]

MsgCenter(MODULE_NAME)
SLEEP_TIME = 0.3


# 这里要重新写 把所有等待干掉 因为冻结poco树 只需要在行动前等待足够多的时间，直接点击就完事了

def poco_find(poco, target_name: str, module_type: str, list_num=None) -> bool:
    """
    直接尝试查找
    :param poco: poco对象
    :param target_name:控件的name属性
    :param module_type:控件的type属性
    :param list_num:拥有多个同级的元素 得拿下标取值的
    :return:
    """
    sleep(SLEEP_TIME)
    try:
        if not list_num:
            if poco(target_name, type=module_type).exists():
                return True
        else:
            if poco(target_name, type=module_type)[list_num].exists():
                return True
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} not find! error -> {e}")
        return False


def poco_try_find_click(poco, target_name: str, module_type: str, list_num=None) -> bool:
    """
    直接尝试查找和点击 后面要加个功能 => 尝试等待返回结果
    :param poco: poco对象
    :param target_name:控件的name属性
    :param module_type:控件的type属性
    :param list_num:拥有多个同级的元素 得拿下标取值的
    :return:
    """
    sleep(SLEEP_TIME)
    try:
        if not list_num:
            if poco(target_name, type=module_type).exists():
                poco(target_name, type=module_type).click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} {module_type} success!")
                return True
            else:
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Can't not find {target_name} {module_type}!")
                return False
        elif list_num:
            if poco(target_name, type=module_type)[list_num].exists():
                poco(target_name, type=module_type)[list_num].click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Click {target_name} {module_type}  Number:{list_num} success!")
                return True
            else:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Can't not find {target_name} {module_type}  Number:{list_num}!")
                return False
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Click {target_name} {module_type}  Number:{list_num} fail! {e}")
        return False


def poco_send_text(poco, input_field: str, module_type: str, text_: str) -> bool:
    """
    尝试输入文字 这个方法是最好的，
    这里的实现是迫不得已用原生
    :param poco:poco对象
    :param input_field:控件的name属性
    :param text_:输入字符串
    :param module_type:控件的type属性
    :return:
    """
    sleep(SLEEP_TIME)
    time_ = 2
    try:
        while time_ > 0:
            time_ -= 1
            if poco_find(poco=poco, target_name=input_field, module_type=module_type):
                poco(input_field, type=module_type).set_text(str(text_))
                return True
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Send text {text_} fail! -> {e}")
        return False


def poco_try_find_offspring(poco, target_name: str, module_type: str, offspring_name: str, num_=None) -> bool:
    """
    后代关联查找
    :param poco: poco对象
    :param target_name: 控件的name属性
    :param module_type: 控件的type属性
    :param offspring_name: 后代控件的关联字段
    :param num_: 拥有多个同级的元素 得拿下标取值的
    :return:
    """
    sleep(SLEEP_TIME)
    try:
        if not num_:
            poco(target_name=target_name, type=module_type).offspring(offspring_name).exists()
            return True
        elif num_:
            poco(target_name=target_name, type=module_type).offspring(offspring_name)[num_].exists()
            return True
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} {module_type} {offspring_name} Number:{num_} "
                       f"not find! error -> {e}")
        return False


def poco_try_offspring_click(poco, target_name: str, module_type: str, offspring_name: str, num_=None) -> bool:
    """
    尝试寻找后代节点和点击 后面要加个功能 => 尝试等待返回结果
    :param poco: poco对象
    :param target_name:控件的name属性
    :param module_type:控件的type属性
    :param offspring_name: 后代控件的关联字段
    :param num_: 父级控件的关联字段
    :return:
    """
    sleep(SLEEP_TIME)
    try:
        if not num_:
            if poco(target_name=target_name, type=module_type).offspring(offspring_name).exists():
                poco(target_name, type=module_type).offspring(offspring_name).click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Click {target_name} {module_type} {offspring_name} success!")
                return True
            else:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Can't not find  {target_name} {module_type} {offspring_name}!")
                return False
        elif num_:
            if poco(target_name=target_name, type=module_type).offspring(offspring_name)[num_].exists():
                poco(target_name, type=module_type).offspring(offspring_name)[num_].click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Click {target_name} {module_type} {offspring_name} {num_}success!")
                return True
            else:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Can't not find {target_name} {module_type} {offspring_name} {num_}!")
                return False
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} {module_type} {offspring_name} Number:{num_} "
                       f"not find! error -> {e}")
        return False


def poco_child_find(poco, target_name: str, target_child: str, module_type: str, list_num=None) -> bool:
    """
    尝试寻找子对象 且点击
    :param poco: poco对象
    :param target_name:控件的name属性
    :param module_type:控件的type属性
    :param list_num:拥有多个同级的元素 得拿下标取值的
    :param target_child:子级别元素
    :return:
    """
    sleep(SLEEP_TIME)
    try:
        if not list_num:
            if poco(target_name, type=module_type).child(target_child).exists():
                poco(target_name, type=module_type).child(target_child).click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Click {target_name} {module_type} {target_child} Success!")
                return True
            else:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Can't not find {target_name} {module_type} {target_child}!")
                return False
        elif list_num:
            if poco(target_name, type=module_type).child(target_child)[list_num].exists():
                poco(target_name, type=module_type).child(target_child)[list_num].click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Click {target_name} {module_type} {target_child} Number:{list_num} Success!")
                return True
            else:
                LogMessage(level=LOG_INFO, module=MODULE_NAME,
                           msg=f"Can't not find {target_name} {module_type} {target_child} Number:{list_num}!")
                return False
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} {module_type} {target_child} Number:{list_num} "
                       f"not find! error -> {e}")
        return False


# 行动封装
def poco_play_dialog_rename(poco, wait_time=0.1) -> bool:
    """
    行动 -> 重命名
    :param poco:
    :param wait_time:
    :return:
    """
    poco_result = poco_try_find_click(poco, target_name="Confirm", module_type="Image")
    sleep(wait_time)
    return poco_result


def poco_play_dialog(poco):
    # poco("Confirm", type="Image").click()
    touch([0.5, 0.5])
    sleep(1)


def poco_select_skin(poco, wait_time=2) -> bool:
    """
    行动 -> 捏脸 这边有两种情况 一是刚进来的时候 选择一次然后确认捏不捏脸，第二种情况是直接跳转捏脸界面
    :param poco:
    :param wait_time:
    :return:
    """
    check_index_ = poco_find(poco, target_name="OnPass", module_type="Node")
    if check_index_:
        poco_result = poco_try_find_click(poco, target_name="OnPass", module_type="Node")
        sleep(wait_time)
        return poco_result
    elif not check_index_:
        # poco("Confirm", type="Button").click()
        poco_result = poco_try_find_click(poco, target_name="Confirm", module_type="Button")
        sleep(wait_time)
        return poco_result


def poco_play_dialog_monologue(poco, wait_time=0.1) -> bool:
    """
    行动 -> 内心独白
    :param poco:
    :param wait_time:超时时间
    :return:
    """
    # 内心独白
    # poco_try_find_offspring(poco, target_name="ViewCanvas", module_type="Node", offspring_name="Dialog_Monologue_")
    poco_result = poco_try_find_click(poco, target_name="Dialog_Monologue", module_type="Node")
    # poco_try_find_click(poco, target_name="Dialog_Monologue_", module_type="Image")
    sleep(wait_time)
    return poco_result


def poco_cosplay_cossuit(poco, wait_time=4) -> bool:
    """
    行动 -> 换装
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    sleep(wait_time)
    poco_result = poco_try_find_click(poco, target_name="confirm", module_type="Image")
    return poco_result


def poco_play_dialog_voiceover(poco, wait_time=0.1) -> bool:
    """
    行动 -> 画外音
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    poco_result = poco_child_find(poco, target_name="ViewCanvas", target_child="View", module_type="Node")
    sleep(wait_time)
    return poco_result


def poco_play_dialog_dialog_noshow(poco, wait_time=0.1) -> bool:
    """
    行动 -> 换装
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    # sleep(wait_time + 1.5)
    sleep(wait_time)
    # poco_try_find_click(poco, target_name="OnPass", module_type="Node")
    return True


def poco_play_dialog_think(poco, wait_time=0.1) -> bool:
    """
    行动 -> 思考
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    poco_result = poco_try_find_click(poco, target_name="Dialog_Left", module_type="Node")
    sleep(wait_time)
    return poco_result


def poco_play_dialog_dialog(poco, wait_time=0.1) -> bool:
    """
    行动 -> 一般对话
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    # poco("Story_Option(Clone)",type="Node")[0].click()
    poco_result = poco_child_find(poco, target_name="ViewCanvas", target_child="View", module_type="Node")
    sleep(wait_time)
    return poco_result


def poco_option_list(poco, index_: int, wait_time=0.5) -> bool:
    """
    行动 -> 选项框
    :param poco:
    :param index_: 超时时间
    :param wait_time: 超时时间
    :return:
    """
    # poco("dialog",type="Node").child("Story_Option(Clone)")[0].click()
    poco_result = poco_child_find(poco, target_name="dialog", target_child="Story_Option(Clone)", module_type="Node",
                                  list_num=index_ - 1)
    sleep(wait_time)
    return poco_result


def poco_lens_move(poco, wait_time=0.1) -> bool:
    """
    行动 -> 角色移动
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    sleep(wait_time)
    return True


def poco_lens_move_voiceover(poco, wait_time=0.5) -> bool:
    """
    行动 -> 角色移动 +画外音类型
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    sleep(wait_time)
    return True
