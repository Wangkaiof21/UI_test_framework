import json
import os


def get_json_file_path(json_path):
    """
    从路径获取所有json
    :param json_path:
    :return:
    """
    path_list = list()
    full_path = os.walk(json_path)
    for file_path, dir_list, files in full_path:
        for file_name in files:
            if file_name.endswith(".txt"):
                path_list.append(os.path.join(file_path, file_name))
    return path_list


def read_json_to_dict(fp):
    json_path_list = get_json_file_path(fp)


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.getcwd(), "../../json_package"))

    read_json_to_dict(path)
