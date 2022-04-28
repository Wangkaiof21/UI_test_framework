import os

import json
from commonlib.baselib.log_message import LogMessage, LOG_INFO, LOG_ERROR

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
TYPE = "type"
DIALOG_TYPE = "dialog_type"
CONTENT = "content"
ITEM_LIST = 'item_list'

TEST_OR_NOT = 'test_or_not'


def wash_action_datas(file_path_, txt_, lua_):
    try:
        book_ = list()
        for file_path, dir_list, files in os.walk(file_path_):
            for file_name in files:
                if file_name.endswith(".txt"):
                    file_abs_ = os.path.join(file_path, file_name)
                    chapter_data = dict()
                    with open(file_abs_, "r", encoding="utf-8") as r:
                        json_file = str(r.read())
                        json_object = json.loads(json_file)
                        # 其他数据可能不重要 直接取 action_list
                        action_list = json_object["action_list"]
                        new_action_list = list()
                        for line in action_list:
                            items_data = get_key_datas(line.get(ITEM_LIST), txt_, lua_)
                            reline = init_new_line(line_dict=line, item_data=items_data)
                            new_action_list.append(reline)
                        # 把条目分组
                        # for date, items in groupby(action_list, key=itemgetter('dialog_no')):
                        #     new_action_list.append(list(items))
                        # print(new_action_list)
                        chapter_name = os.path.basename(file_abs_).split('.')[0]
                        chapter_data[chapter_name] = new_action_list
                        LogMessage(module="read_json_to_files", level=LOG_INFO,
                                   msg=f"Add the book chapter => {chapter_name}")
                    book_.append(chapter_data)
                    """写一个写表的模块 读表的模块
                        封装方法eval()
                         set{'select_list': [{'select_id': 1019000212701,
                    """
        for index in range(len(book_)):
            for ch, value in book_[index].items():
                LogMessage(level=LOG_INFO, msg=f"The book has chapter {ch}", module=MODULE_NAME)
        return book_
    except Exception as e:
        LogMessage(level=LOG_ERROR, msg=f"chapter file error {e}", module=MODULE_NAME)


def init_new_line(line_dict: dict, item_data: dict) -> dict:
    """根据传入值新建新的字典"""
    result = dict()
    result['id'] = line_dict.get('id')
    result['dialog_id'] = line_dict.get('dialog_id')
    result['instance_id'] = line_dict.get('instance_id')
    result['dialog_no'] = line_dict.get('dialog_no')
    result['type'] = item_data.get(TYPE)
    result['dialog_type'] = item_data.get(DIALOG_TYPE)
    result['test_or_not'] = ""
    return result


def get_key_datas(lines, txt_file_data, lua_file_data) -> dict:
    """
    整个ITEM_LIST 进行转换 重新包装
    :param lines: ITEM_LIST
    :param txt_file_data: 行动字典
    :param lua_file_data: lua字典 行动字典的下级 目前只有一个特殊判断就是rename
    :return:
    """
    result_list = list()
    for line in lines:
        # 以后有更多需要的"content"里面的值，在这里加，例如文字对话: text_ = line.get("content").get("text_content", "")
        result_dict = dict()
        # 这里要做双重转换 step 1 根据lua文件转换
        result_dict[DIALOG_TYPE] = matching_dictionary_to_language(str(line.get("content").get("dialog_type", "")),
                                                                   lua_file_data)
        # 这里要做双重转换 step 2 根据action_list.txt文件转换
        result_dict[TYPE] = matching_dictionary_to_language(str(line.get(TYPE)), txt_file_data)
        result_list.append(result_dict)
    # 这里需要做一个数据转换成文字 且拼接 多个字典
    # [{'dialog_type': 'voiceover', 'type': 'play_dialog'}, {'dialog_type': '', 'type': 'object_scene_move'}...]转换成
    # [{'dialog_type': 'voiceover', 'type': 'play_dialog,object_scene_move'}]
    result_list = dict_datas_to_string(result_list)
    return result_list


def read_txt_to_dict(fp):
    """
    把txt里面的内容读出来 且转换成字典 用type的key去调用转换成 ddd:方法名,方法名,方法名,方法名
    :param fp:
    :return:
    """
    action_name_dict = dict()
    with open(fp, 'rb') as f:
        try:
            data = f.read().decode("utf-8")
            data = data.split("\r")[5:-1]
            for line in data:
                new_ = line.replace("\n    ", "").replace("\n", '').replace(",", "").replace("//", "").replace(" ", "")
                if "=" in new_:
                    key, value = new_.split("=")
                    action_name_dict[value] = key
        except Exception as e:
            print(f"Change dict error {e}")
            return {}
    return action_name_dict


def dict_datas_to_string(action_line: list) -> dict:
    """

    :param action_line:
    :return:
    """
    ty = ""
    dty = ""
    new_action_line = dict()
    for line in action_line:
        if not line.get(TYPE):
            continue
        ty += line.get(TYPE) + ","
        if not line.get(DIALOG_TYPE):
            continue
        dty += line.get(DIALOG_TYPE) + ","
    new_action_line[TYPE] = ty
    new_action_line[DIALOG_TYPE] = dty
    return new_action_line


def matching_dictionary_to_language(value: str, action_dict: dict):
    """
    匹配字典的
    :param value:
    :param action_dict:
    :return:
    """
    if value not in action_dict.keys():
        result = value
    else:
        result = action_dict.get(value).lower()
    return result


def read_lua_to_dict(fp):
    """
    把lua里面的内容读出来 且转换成字典 用type的key去调用转换成 ddd:方法名,方法名,方法名,方法名
    :param fp:
    :return:
    """
    action_name_dict = dict()
    with open(fp, 'rb') as f:
        try:
            data = f.read().decode("utf-8")
            data = data.split("\r")[7:-1]
            for line in data:
                new_ = line.replace("\n    ", "").replace("\n", '').replace(",", "").replace("//", "").replace(" ", "")
                if "=" in new_:
                    key, value = new_.split("=")
                    action_name_dict[value] = key
        except Exception as e:
            print(f"Change dict error {e}")
            return {}
    return action_name_dict


if __name__ == '__main__':
    file_ = "C:\\Users\\王凯\Desktop\\test_file\\UI_test_framework\\parse_data_files\\"
    txt_path = os.path.abspath(os.path.join(os.getcwd(), "action_book.txt"))
    lua_path = os.path.abspath(os.path.join(os.getcwd(), "StoryDialogType.lua"))
    txt_result_dict = read_txt_to_dict(txt_path)

    lua_result_dict = read_lua_to_dict(lua_path)

    wash_action_datas(file_, txt_result_dict, lua_result_dict)
