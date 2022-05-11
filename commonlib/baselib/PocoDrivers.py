from time import sleep
import os
from poco.exceptions import PocoNoSuchNodeException
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
from airtest.core.api import text, touch

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
# MsgCenter(MODULE_NAME)
SLEEP_TIME = 1


def poco_find(poco, target_name: str, module_type: str, wait_time=1, list_num=None) -> bool:
    """
    :param poco: poco对象
    :param target_name:控件的name属性
    :param wait_time:等待时间
    :param module_type:控件的type属性
    :param list_num:拥有多个同级的元素 得拿下标取值的
    :return:
    """
    try:
        if list_num:
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Try find {target_name}[{list_num}]....")
            if poco(target_name, type=module_type)[list_num].wait(wait_time).exists():
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Find {target_name} !")
                return True
        else:
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Try find {target_name}....")
            if poco(target_name, type=module_type).wait(wait_time).exists():
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Find {target_name} !")
                return True
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} not find! error -> {e}")
        return False


def poco_try_find_click(poco, target_name: str, module_type: str, list_num=None) -> bool:
    """
    尝试寻找和点击 后面要加个功能 => 尝试等待返回结果
    :param poco: poco对象
    :param target_name:控件的name属性
    :param module_type:控件的type属性
    :param list_num:拥有多个同级的元素 得拿下标取值的
    :return:
    """
    if list_num:
        try:
            if poco_find(poco=poco, target_name=target_name, module_type=module_type, list_num=list_num):
                poco(target_name, type=module_type)[list_num].click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} success!")
                sleep(SLEEP_TIME)
                return True
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Click {target_name} fail! {e}")
            return False
    else:
        try:
            if poco_find(poco=poco, target_name=target_name, module_type=module_type):
                poco(target_name, type=module_type).click()
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} success!")
                sleep(SLEEP_TIME)
                return True
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Click {target_name} fail! {e}")
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
    time = 2
    while time > 0:
        time -= 1
        try:
            if poco_find(poco=poco, target_name=input_field, module_type=module_type):
                poco(input_field, type=module_type).set_text(str(text_))
                return True
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Send text {text_} fail! -> {e}")
            return False


def poco_try_find_offspring(poco, target_name: str, module_type: str, offspring_name: str, wait_time=1, ):
    """
    父级关联查找
    :param poco: poco对象
    :param target_name: 控件的name属性
    :param module_type: 控件的type属性
    :param offspring_name: 父级控件的关联字段
    :param wait_time: 等待时间
    :return:
    """
    try:
        LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Try find {target_name}....")
        poco(target_name=target_name, type=module_type).offspring(offspring_name).wait(wait_time).exists()
        LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Find {target_name} !")
        sleep(SLEEP_TIME)
        return True
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} not find! error -> {e}")
        return False


def poco_try_offspring_click(poco, target_name: str, module_type: str, offspring_name: str, wait_time=1) -> bool:
    """
    尝试寻找和点击 后面要加个功能 => 尝试等待返回结果
    :param poco: poco对象
    :param target_name:控件的name属性
    :param module_type:控件的type属性
    :param offspring_name: 父级控件的关联字段
    :param wait_time:
    :return:
    """
    if poco_try_find_offspring(poco=poco, target_name=target_name, module_type=module_type,
                               offspring_name=offspring_name):

        poco(target_name, type=module_type).offspring(offspring_name).wait(wait_time).click()
        LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} success!")
        return True
    else:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Click {target_name} fail!")
        return False


# 行动封装
def poco_play_dialog_rename(poco, wait_time=0.5):
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


def poco_select_skin(poco, wait_time=0.5) -> bool:
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


def poco_play_dialog_monologue(poco, wait_time=0.5):
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


def poco_cosplay_cossuit(poco, wait_time=4):
    """
    行动 -> 换装
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    poco_result = poco_try_find_click(poco, target_name="confirm", module_type="Image")
    sleep(wait_time)
    return poco_result


def poco_play_dialog_voiceover(poco, wait_time=1):
    """
    行动 -> 画外音
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    poco_child_find(poco, target_name="ViewCanvas", target_child="View", module_type="Node")
    sleep(wait_time)


def poco_play_dialog_dialog_noshow(poco, wait_time=1):
    """
    行动 -> 换装
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    sleep(wait_time + 0.5)
    # poco_try_find_click(poco, target_name="OnPass", module_type="Node")
    pass


def poco_play_dialog_think(poco, wait_time=0.5):
    """
    行动 -> 思考
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    poco_try_find_click(poco, target_name="Dialog_Left", module_type="Node")
    sleep(wait_time)


def poco_play_dialog_dialog(poco, wait_time=0.5):
    """
    行动 -> 一般对话
    :param poco:
    :param wait_time: 超时时间
    :return:
    """
    # poco("Story_Option(Clone)",type="Node")[0].click()
    poco_child_find(poco, target_name="ViewCanvas", target_child="View", module_type="Node")
    sleep(wait_time)


def poco_option_list(poco, index_: int, wait_time=0.5):
    """
    行动 -> 选项框
    :param poco:
    :param index_: 超时时间
    :param wait_time: 超时时间
    :return:
    """
    # poco("dialog",type="Node").child("Story_Option(Clone)")[0].click()
    poco_child_find(poco, target_name="dialog", target_child="Story_Option(Clone)", module_type="Node",
                    list_num=index_ - 1)
    sleep(wait_time)
    pass


def poco_child_find(poco, target_name: str, target_child: str, module_type: str, wait_time=1, list_num=None) -> bool:
    """
    :param poco: poco对象
    :param target_name:控件的name属性
    :param wait_time:等待时间
    :param module_type:控件的type属性
    :param list_num:拥有多个同级的元素 得拿下标取值的
    :param target_child:子级别元素
    :return:
    """
    try:
        if list_num:
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Try find {target_name}[{list_num}]....")
            if poco(target_name, type=module_type).child(target_child)[list_num].wait(wait_time).exists():
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} !")
                poco(target_name, type=module_type).child(target_child)[list_num].click()
                return True
        else:
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Try find {target_name}....")
            if poco(target_name, type=module_type).child(target_child).wait(wait_time).exists():
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} !")
                poco(target_name, type=module_type).child(target_child).click()
                return True

        LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Click {target_name} Success!")
    except Exception as e:
        LogMessage(level=LOG_ERROR, module=MODULE_NAME,
                   msg=f"Wait time out ,element {target_name} not find! error -> {e}")
        return False

#
#
# def findClick_childobject(poco, description="", waitTime=1, tryTime=1, sleeptime=0,
#                           clickPos=None):
#     """用于关联父级才能点击到的元素"""
#     #
#     if poco.wait(waitTime).exists():
#         mylog.debug("发现{0}".format(description))
#         # mylog.deviceInfo("查找点击元素-【{}】--成功".format(description))
#         if clickPos is None:
#             poco.click()
#         else:
#             poco.click(clickPos)
#         sleep(sleeptime)
#         return True
#     else:
#         log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败", snapshot=True)
#     log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败", snapshot=True)
#     raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))
#
#
# def notchfit_childobject(poco, description="", waitTime=0.5, tryTime=1, sleeptime=0, log=True):
#     """用于关联父级才能点击到的元素"""
#     if poco.wait(waitTime).exists():
#         mylog.info("发现{0}".format(description))
#         # mylog.deviceInfo("查找点击元素-【{}】--成功".format(description))
#         poco.click()
#         sleep(sleeptime)
#         # mylog.deviceInfo("点击元素-【{}】--成功".format(description))
#         # poco.use_render_resolution(False, GData.mobileconf_dir["screen"][ADBdevice])
#         return True
#     else:
#         pass
#         # mylog.error("查找-【{}】-元素失败".format(description))
#     log(PocoNoSuchNodeException("点击-【{}】-元素失败".format(description)), desc="点击元素失败", snapshot=True)
#     raise PocoNoSuchNodeException("点击-【{}】-元素失败".format(description))
