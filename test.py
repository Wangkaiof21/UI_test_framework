from commonlib.baselib.excel import Excel
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_DEBUG, LOG_WARN, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
import os

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
# msg = MsgCenter(MODULE_NAME)
msg = MsgCenter(MODULE_NAME, level=LOG_DEBUG)

import json
from operator import itemgetter
from itertools import groupby


def list_add(test_list: list):
    node_ = []
    for ele in test_list:
        node_ += ele
    return node_


def list_to_str(d_list):
    ret_str = ""
    for line in d_list:
        for k, v in line.items():
            ret_str += v + ","
    return ret_str


def read_json_to_files(files_path, action_dict: dict):
    """
    从条目合成页数

    item_list对应的value是个list
    list有多个值 一个type对应多个content
    type和content 是同级别的

    'type': 15002 是动作 ，'content': {}是对应动作可以选择的值
    首先 先要合并dialog_no 相等的list 获取一页之内可以操作的动作 和动作的值，以后空点也要设置一个type 那这样以后就可以方便操作
    :param files_path:
    :param action_dict:
    :return:
    """
    book_ = list()
    for file_path, dir_list, files in os.walk(files_path):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_ = os.path.join(file_path, file_name)
                chapter_data = dict()
                with open(file_, "r", encoding="utf-8") as r:
                    json_file = str(r.read())
                    json_object = json.loads(json_file)
                    # 其他数据可能不重要 直接取 action_list
                    action_list = json_object["action_list"]
                    new_action_list = list()
                    # 把条目分组
                    for date, items in groupby(action_list, key=itemgetter('dialog_no')):
                        new_action_list.append(list(items))

                    full_action_list = list()
                    for index in range(len(new_action_list)):
                        index_ = list()
                        new_ = ""
                        for line in new_action_list[index]:
                            content_types = list()
                            for content in line["item_list"]:
                                content_type = dict()
                                for key, value in content.items():
                                    # 获取与配置'content': {}是对应动作可以选择的值 ,'type': 15002 是动作的值
                                    if key == "type":
                                        # 'type': 15002 动作的值直接转化成action_dict 里的字符串 也是就行动的名称 COSTUME_LIST:14002
                                        value = matching_dictionary_to_language(str(value), action_dict)
                                        content_type[key] = value
                                content_types.append(content_type)
                            index_.append(content_types)
                            new_ = list_add(index_)
                            new_ = list_to_str(new_)
                        new_action_list[index][0]["item_list"] = new_
                        # 新增是否测试 测试点开关ture or false 方便处理树状分支剧情
                        new_action_list[index][0]["test_or_not"] = ""
                        # 暂时屏蔽前置条件 这个做法有问题 后期看看怎么改
                        new_action_list[index][0]["show_pre"] = ""
                        full_action_list.append(new_action_list[index])
                    # 去除多一层列表
                    full_action_lists = list()
                    for line in full_action_list:
                        full_action_lists.append(line[0])
                    # 获得一个章节的内容 {章节名 : 章节内容}
                    chapter_name = os.path.basename(file_).split('.')[0]
                    chapter_data[chapter_name] = full_action_lists
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


def read_txt_to_dict(fp):
    """
    把txt里面的内容读出来 且转换成字典 用type的key去调用转换成 方法名？
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
            LogMessage(level=LOG_ERROR, msg=f"Change dict error {e}", module=MODULE_NAME)
            return {}
    return action_name_dict


def write_action_boot_data(book_action_data, excel_fp: str) -> None:
    """
    写入数据
    :param book_action_data:
    :param excel_fp:
    :return:
    """
    excel = Excel(excel_fp)
    for index in range(len(book_action_data)):
        # ch_name = str(book_action_data[index].keys())
        # print(action_data[index]["dialog_10190001"])
        for ch, value in book_action_data[index].items():
            excel.records_write(ch, records=value, start_row=None)


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.getcwd(), "parse_data_files"))
    # path =  os.path.abspath(os.path.join(os.getcwd(), "../../parse_data_files"))

    # txt_path = os.path.abspath(os.path.join(os.getcwd(), "../../action_dict.txt"))
    txt_path = os.path.abspath(os.path.join(os.getcwd(), "action_book.txt"))
    excel_path = os.path.abspath(os.path.join(os.getcwd(), "action_.xlsx"))
    result_dict = read_txt_to_dict(txt_path)
    results = read_json_to_files(path, action_dict=result_dict)
    write_action_boot_data(book_action_data=results, excel_fp=excel_path)
