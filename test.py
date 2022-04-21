import os

# from datetime import date
#
# user = 'eric_idle'
# member_since = date(1975, 7, 31)
#
# delta = date.today() - member_since
#
# print(f'{user=!s}  {delta.days=:,d}')
#
# x = 3
# print(f"{x+1=}")

import os
import sys

# print("sys.path[0] = ", sys.path[0])
# print("sys.argv[0] = ", sys.argv[0])
# print("__file__ = ", __file__)
# print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
# print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
# print("os.path.dirname(os.path.realpath(__file__)) = ",
#        os.path.dirname(os.path.realpath(__file__)))
# print("os.path.split(os.path.realpath(__file__)) = ",
#        os.path.split(os.path.realpath(__file__)))
# print("os.path.split(os.path.realpath(__file__))[0] = ",
#        os.path.split(os.path.realpath(__file__))[0])
# print("os.getcwd() = ", os.getcwd())
import zipfile

s = {'id': 10003, 'dialog_id': 10001, 'instance_id': 20001, 'dialog_no': '1', 'action_id': 0,
     'item_list':
         [{'content': {'id': 11904, 'sound_id': 11904, 'play_type': 11001, 'type': 1, 'playEffect': 0, 'play_count': 1},
           'type': 15002,
           'delay': 0,
           'belong_split': 0,
           'editorActionId': 8
           }]
     }
"""
从条目合成页数

item_list对应的value是个list 
list有多个值 一个type对应多个content
type和content 是同级别的 

'type': 15002 是动作 ，'content': {}是对应动作可以选择的值
首先 先要合并dialog_no 相等的list 获取一页之内可以操作的动作 和动作的值，以后空点也要设置一个type 那这样以后就可以方便操作
"""

import json
from operator import itemgetter
from itertools import groupby


def list_add(test_list: list):
    node_ = []
    for ele in test_list:
        node_ += ele
    return node_


def read_json_to_files(files_path, action_dict: dict):
    """

    :param files_path:
    :param action_dict:
    :return:
    """
    for fp in files_path:
        with open(fp, "r", encoding="utf-8") as r:
            json_file = str(r.read())
            json_object = json.loads(json_file)
            # 其他数据可能不重要 直接取 action_list
            action_list = json_object["action_list"]
            new_action_list = list()
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
                            if key == "type":
                                value = matching_dictionary_to_language(str(value), action_dict)
                                content_type[key] = value
                        content_types.append(content_type)
                    index_.append(content_types)
                    new_ = list_add(index_)
                new_action_list[index][0]["item_list"] = new_
                full_action_list.append(new_action_list[index])
            full_action_lists = list()
            for line in full_action_list:
                full_action_lists.append(line[0])
            for line in full_action_lists:
                print(line)
        print("\n")
        """写一个写表的模块 读表的模块 
            封装方法eval()
        """


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
            print(f"Change dict error {e}")
            return {}
    return action_name_dict


if __name__ == '__main__':
    path1 = "C:\\Users\\王凯\\Desktop\\test_file\\UI_test_framework\\parse_data_files\\dialog_10190001.txt"
    path2 = "C:\\Users\\王凯\\Desktop\\test_file\\UI_test_framework\\parse_data_files\\dialog_10190002.txt"
    path = [path1, path2]
    # txt_path = os.path.abspath(os.path.join(os.getcwd(), "../../action_dict.txt"))
    txt_path = os.path.abspath(os.path.join(os.getcwd(), "action_book.txt"))
    result_dict = read_txt_to_dict(txt_path)
    read_json_to_files(path, action_dict=result_dict)
