import json
import os

import requests
import time
import hmac
import random
import zipfile
import json
from operator import itemgetter
from itertools import groupby

BOOK_ID = "666010190"
SLEEP_TIME = 1


def list_add(test_list: list):
    node_ = []
    for ele in test_list:
        node_ += ele
    return node_


def get_json_file_path(json_path):
    """
    从路径获取所有json
    :param json_path:
    :return:
    """
    index = 0
    path_list = list()
    full_path = os.walk(json_path)
    for file_path, dir_list, files in full_path:
        for file_name in files:
            if file_name.endswith(".txt"):
                path_list.append(os.path.join(file_path, file_name))
                print(f"章节文件 --> {os.path.join(file_path, file_name)}")
                index += 1
    print(f"一共{index}个章节")
    return path_list


def read_json_to_dict(fp):
    """

    :param fp:
    :return:
    """
    json_path_list = get_json_file_path(fp)
    for name in json_path_list:
        with open(name, "r", encoding="utf-8") as r:
            new_dict = json.loads(r.read())
        # 配置数据太麻烦 通过端口拉运行数据


# 加密
def get_sign(data, secret):
    h = hmac.new(secret.encode(), data.encode(), digestmod='sha256')
    return h.hexdigest()


def concatenate_strings(data1, data2):
    data = []
    # 将两个字典合并
    data3 = dict(data1, **data2)
    # 将合并的字典key和value用=连接存入列表
    for i in sorted(data3.items()):
        data.append("=".join(i))
    # 将列表用&连接返回字符串
    data_ = '&'.join(data)
    return data_


def get_app_login_token(debug=True, secret="56a354ec", did="zpf0001"):
    """

    :param debug: 选择服务器
    :param secret: 密钥？
    :param did: user_id
    :return:
    """
    url = get_test_url(debug)
    login_header = {
        'timestamp': '',
        'sign': '',
        'noise': '',
        'did': '',
        'version': '3.151.1',
        'channel': 'AVG10003',
        'package-name': 'com.stardust.spotlight',
        'Accept-Language': 'en',
        'dievel': '_medium'
    }

    common_data = {
        "did": f"{did}",
        "timestamp": f"{str(int(time.time()))}"
    }
    payload = {'identity_type': '1',
               'identifier': f'{did}'
               }
    # 将参数加密
    data = concatenate_strings(common_data, payload)
    # headers赋值
    login_header["sign"] = get_sign(data, secret)
    login_header['timestamp'] = str(int(time.time()))
    login_header['noise'] = str(random.randrange(100, 999))
    login_header["did"] = did
    try:
        # user_agent =
        response = requests.post(url + "/login", headers=login_header, data=payload)
    except Exception as e:
        raise e
    token = response.json()["data"]["access_token"]

    return token


def ini_common_header() -> dict:
    """
    自動化生成新的dict
    :return:
    """
    result = dict()
    result['timestamp'] = ''
    result['sign'] = ''
    result['noise'] = ''
    result['did'] = ''
    result['version'] = '3.170.1'
    result['channel'] = 'AVG10003'
    result['package-name'] = 'com.stardust.spotlight'
    result['Accept-Language'] = 'en'
    result['dlevel'] = '_medium'
    result['authorization'] = ''
    return result


def get_test_url(debug=True):
    """

    :param debug:
    :return:
    """
    if debug:
        # 测试服HOST
        url = "http://project_x_api.stardustworld.cn/api/v1"
        return url
    else:
        # 审核服HOST
        url = "http://dev_spt_aws_game_api.stardustgod.com/api/v1"
        return url


def get_book_chapter_id_result(token, story_chapter_ids: list, debug=True, secret="56a354ec", did="zpf0001",
                               story_id_change=False, change_id="6660"):
    """
    666010190001 实际上是6660 1019+0001 书籍的id + ？
    所以我们要先通过接口获取书籍信息 书籍id 有多少章节 拼接字段

    从章节id获取资源数据 取资源数据的path 拼接 行动数据的zip
    后面需要封装request库，
    :param token:
    :param debug:debug模式 打开则是测试服 不打开审核服
    :param secret:加密字段
    :param did:唯一标识
    :param story_chapter_ids章节id
    :param story_id_change:打开则是要重新编辑id 现在是暂时在id前面加字段
    :param change_id:需要添加的字段
    :return:
    """
    zip_path_list = list()
    for ch_id in story_chapter_ids:
        if story_id_change:
            full_id = str(f"{change_id}{ch_id}")
        else:
            full_id = str(ch_id)
        url = get_test_url(debug)
        uri = "/story/chapter/actions/"
        # 'version': '3.151.1',
        common_header = ini_common_header()
        common_data = {
            "did": f"{did}",
            "timestamp": f"{str(int(time.time()))}"
        }
        payload = {"story_chapter_id": full_id}
        # 将参数拼接
        data = concatenate_strings(common_data, payload)
        # 将参数加密
        sign = get_sign(data, secret)
        common_header["sign"] = sign
        common_header['timestamp'] = str(int(time.time()))
        common_header['noise'] = str(random.randrange(100, 999))
        common_header['did'] = did
        common_header["authorization"] = "Bearer" + " " + token
        try:
            response = requests.request("GET", url + uri, headers=common_header, params=payload)
            action_file_path = response.json().get("data").get("action_file").get("path")
            zip_path_list.append(action_file_path)
        except Exception as e:
            raise e
        time.sleep(SLEEP_TIME)
    return zip_path_list


def for_story_id_get_chapter_ids(story_id, token, debug=True, secret="56a354ec", did="zpf0001"):
    """
    获取故事id的list
    :param token:
    :param story_id:
    :param debug:
    :param secret:
    :param did:
    :return:
    """
    url = get_test_url(debug)
    uri = "/story/show/"
    # 'version': '3.151.1',
    common_header = ini_common_header()
    common_data = {
        "did": f"{did}",
        "timestamp": f"{str(int(time.time()))}"
    }
    payload = {"story_id": story_id}
    # 将参数加密
    data = concatenate_strings(common_data, payload)
    sign = get_sign(data, secret)
    common_header["sign"] = sign
    common_header['timestamp'] = str(int(time.time()))
    common_header['noise'] = str(random.randrange(100, 999))
    common_header["authorization"] = "Bearer" + " " + token
    common_header["did"] = did

    try:
        response = requests.request("GET", url + uri, headers=common_header, params=payload)
    except Exception as e:
        raise e
    chapter_ids = response.json()["data"]["chapter_ids"]
    return chapter_ids


def parse_action_list_to_json(result_data: list, save_path, action_dict, chunk_size=128):
    """
    解析返回的资源数据，发起请求获取zip文件 存储在固定文件夹 并解压重命名获取行动数据
    解压之后 读取txt内容 洗数据
    到时候要和action_dict.txt 做一个取值
    :param result_data:
    :param save_path:
    :param chunk_size:块大小 怕文件过大 分块写入
    :param action_dict:
    :return:
    """
    target_url_a = "http://spt-cdn.stardustgod.com/spt/"
    target_url_b = "http://spt-akamai.stardustgod.com/spt/"
    if not os.listdir(save_path):
        print("Path is clean")
        pass
    else:
        for file_path, dir_list, files in os.walk(save_path):
            for file_name in files:
                rubbish_file = os.path.join(file_path, file_name)
                os.remove(rubbish_file)
                print(f"Clean {rubbish_file} clear")
    abs_path_list = list()
    index = 0
    try:
        for line in result_data:
            full_url = f"{target_url_a}{line}"
            print(f"Download to {index} --> {full_url}")
            r = requests.get(full_url, stream=True)
            time.sleep(SLEEP_TIME)
            file_abs_name = save_path + "\\" + f"action_{index}.zip"
            with open(file_abs_name, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
            print(f'Download {file_abs_name} done')
            abs_path_list.append(file_abs_name)
            index += 1
    except Exception as e:
        print(f'No.{index} file Error => {e}')

    try:
        # unzip_files
        for line in abs_path_list:
            print(line)
            if zipfile.is_zipfile(line):
                "判断是不是压缩文件"
                with zipfile.ZipFile(line, 'r') as zipf:
                    zipf.extractall(path=save_path)
            # os.remove(line)
            time.sleep(SLEEP_TIME)
        print(f'Unzip  done')
    except Exception as e:
        print(f'Unzip file Error => {e}')

    try:
        for file_path, dir_list, files in os.walk(save_path):
            for file_name in files:
                if file_name.endswith(".zip"):
                    zip_file = os.path.join(file_path, file_name)
                    print(zip_file)
                    os.remove(zip_file)
                    print(f"clean zip file --> {os.path.join(file_path, file_name)}")
    except Exception as e:
        print(f"Delete file error {e}")

    try:
        for file_path, dir_list, files in os.walk(save_path):
            for file_name in files:
                if file_name.endswith(".txt"):
                    json_file = os.path.join(file_path, file_name)
                    with open(json_file, "r", encoding="utf-8") as r:
                        read_data = str(r.read())
                        json_object = json.loads(read_data)
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

    except Exception as e:
        print(f"Delete file error {e}")


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
        result = action_dict.get(value)
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


def main():
    path = os.path.abspath(os.path.join(os.getcwd(), "../../json_package"))
    parse_path = os.path.abspath(os.path.join(os.getcwd(), "../../parse_data_files"))
    # read_json_to_dict(path)
    token = get_app_login_token()
    ids = for_story_id_get_chapter_ids(BOOK_ID, token)
    result_list = get_book_chapter_id_result(token, ids, story_id_change=True, change_id="6660")

    txt_path = os.path.abspath(os.path.join(os.getcwd(), "../../action_book.txt"))
    result_dict = read_txt_to_dict(txt_path)
    parse_action_list_to_json(result_list, save_path=parse_path, action_dict=result_dict)




if __name__ == '__main__':
    main()
