def confirm_executable_method(type_str: str):
    """
    切割字符串 获取list
    :param type_str:
    :return:
    """
    # 可执行动作的list
    executable_list = ["select_skin", "play_dialog", "cosplay_cossuit"]
    method_list = []
    print(type_str.split(",")[:-1])


def subordinate_data_confirm_executable_method(type_str: str):
    """
    切割字符串 获取list
    :param type_str:
    :return:
    """
    print(type_str)


if __name__ == '__main__':
    v = {"11": "play_dialog,animation_role,phone,", "ss": "monologue,"}
    v = v['11']
    confirm_executable_method(v)
