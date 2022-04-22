import os
from commonlib.baselib.excel import Excel
from commonlib.baselib.msg_center import MsgCenter
from commonlib.baselib.log_message import LOG_DEBUG

MsgCenter("ll", level=LOG_DEBUG)


def write_action_boot_data(action_data, excel_fp: str):
    """
    写入数据
    :param action_data:
    :param excel_fp:
    :return:
    """
    excel = Excel(excel_fp)
    for ch_ in action_data:
        excel.records_write('dialog_10190001', records=ch_['dialog_10190001'], start_row=2)


if __name__ == '__main__':
    excel_path = os.path.abspath(os.path.join(os.getcwd(), "acc.xlsx"))
    data = [{
        'dialog_10190001': [
            {'id': 10001, 'dialog_id': 10001, 'instance_id': 20001, 'dialog_no': '1', 'action_id': 0,
             'item_list': 'add_scene,play_sound,play_sound,cosplay_cossuit,play_dialog,object_scene_move,'},
            {'id': 10002, 'dialog_id': 10002, 'instance_id': 20001, 'dialog_no': '2', 'action_id': 0,
             'item_list': 'add_scene,play_sound,play_sound,cosplay_cossuit,play_dialog,object_scene_move,'},
            {'id': 10003, 'dialog_id': 10003, 'instance_id': 20001, 'dialog_no': '3', 'action_id': 0,
             'item_list': 'add_scene,play_sound,play_sound,'},
            {'id': 10004, 'dialog_id': 10004, 'instance_id': 20001, 'dialog_no': '4', 'action_id': 0,
             'item_list': 'add_scene,play_sound,play_sound,cosplay_cossuit,play_dialog,object_scene_move,'}
        ]
    }]
    write_action_boot_data(action_data=data, excel_fp=excel_path)

