import os
import json

WAIT_TIME = "time_scale"
TYPE = "type"
DIALOG_TYPE = "dialog_type"
action_line = [{'dialog_type': '', 'type': 'add_scene', 'time_scale': ''},
               {'dialog_type': '', 'type': 'object_scene_move', 'time_scale': ''},
               {'dialog_type': '', 'type': 'play_sound', 'time_scale': ''},
               {'dialog_type': 'ccccccccccccccc', 'type': 'role_set_position', 'time_scale': 1000},
               {'dialog_type': '', 'type': 'lens_move', 'time_scale': ''},
               {'dialog_type': '', 'type': 'animation_role', 'time_scale': 1000},
               {'dialog_type': '', 'type': 'role_set_position', 'time_scale': 1500},
               {'dialog_type': '+++++++', 'type': 'animation_role', 'time_scale': 1000},
               {'dialog_type': '', 'type': 'play_sound', 'time_scale': 87568}]
wtm = 0
ty = ""
dty = ""
new_action_line = dict()
# for line in action_line:
# ty += "" if not line.get("type") else ty += line.get("type") + ","
# ty = ty + '' if not line.get("type") else ty + ","

# if not line.get("type"):
#     ty += ""
# else:
#     ty += line.get("type") + ","
#
# if not line.get("time_scale"):
#     wtm += 0
# else:
#     wtm += line.get("time_scale")
# if not line.get("dialog_type"):
#     dty += ""
# else:
#     dty += line.get("dialog_type") + ","


a = [i["dialog_type"] for i in action_line if i["dialog_type"]]
new_action_line["dialog_type"] = ','.join(a)

a = [i["type"] for i in action_line if i["type"]]
new_action_line["type"] = ','.join(a)

a = [i["time_scale"] for i in action_line if i["time_scale"]]
new_action_line["time_scale"] = sum(a)

#
# def confirm_executable_method(self, type_str: str, dialog_type_str: str, branch_tree: str, wait_time_: str,
#                               dia_log_id: str):
#     """
#     切割字符串 获取list 取action的交集
#     import numpy
#     array1 = ["play_dialog","play_sound","animation_role","phone","animation_role",]
#     array2 = ["select_skin", "play_dialog", "cosplay_cossuit", "option_list"]
#     c = numpy.intersect1d(array1, array2, assume_unique=False, return_indices=False)
#     print(c)
#     :param type_str:行动类型
#     :param dialog_type_str:行动细分类型
#     :param branch_tree:条目数量
#     :param wait_time_:镜头运动时间 画外音可能要取消
#     :param dia_log_id: 页数ID
#     :return:
#     """
#     try:
#         dialog_type_str = self.gen_str(dialog_type_str)
#         # 可执行动作的list 多个行动对多个行动不好处理
#         func_names = type_str.split(",")[:-1]
#         result_index = self.union_data(func_names, ConfigView.EXECUTABLE_LIST)
#         # result_index = numpy.intersect1d(func_names, ConfigView.EXECUTABLE_LIST, assume_unique=False,
#         #                                  return_indices=False)
#         run_time = 0
#         while run_time < 3:
#             # 加个for循环
#             if len(result_index) > 0 and dialog_type_str:
#                 LogMessage(level=LOG_INFO, module=MODULE_NAME,
#                            msg=f"Func start ID: {dia_log_id} poco_{result_index[0]}_{dialog_type_str} time_out -> {wait_time_} second")
#                 if globals()[f"poco_{result_index[0]}_{dialog_type_str}"](self.poco, wait_time_):
#                     LogMessage(level=LOG_INFO, module=MODULE_NAME,
#                                msg=f"poco_{result_index[0]}_{dialog_type_str} run success")
#                     break
#
#             elif len(result_index) > 0 and not dialog_type_str and not branch_tree:
#                 LogMessage(level=LOG_INFO, module=MODULE_NAME,
#                            msg=f"Func start ID: {dia_log_id} poco_{result_index[0]} time_out -> {wait_time_} second")
#                 if globals()[f"poco_{result_index[0]}"](self.poco, wait_time_):
#                     LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"poco_{result_index[0]} run success")
#                     break
#
#             elif len(result_index) > 0 and not dialog_type_str and branch_tree:
#                 LogMessage(level=LOG_INFO, module=MODULE_NAME,
#                            msg=f"Func start ID: {dia_log_id} poco_{result_index[0]} -> branch {int(branch_tree)} time_out -> {wait_time_} second")
#                 if globals()[f"poco_{result_index[0]}"](self.poco, int(branch_tree), wait_time_):
#                     LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"poco_{result_index[0]} run success")
#                     break
#             # break
#             run_time += 1
#
#     except Exception as e:
#         LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Func error -> {e}")
vv = ['play_dialog', 'lens_move']
if len(vv) > 1 and vv.count('lens_move'):
    print(111)
