import json
import os

import requests
import time
import hmac
import random

BOOK_ID = "666010190"


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
    if debug:
        # 测试服HOST
        url = "http://project_x_api.stardustworld.cn/api/v1"
    else:
        # 审核服HOST
        url = "http://dev_spt_aws_game_api.stardustgod.com/api/v1"

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


def for_book_chapter_id_get_action_list(token, debug=True, secret="56a354ec", did="zpf0001",
                                        story_chapter_id="666010190001", story_id_change=False, change_id="6660"):
    """
    666010190001 实际上是6660 1019+0001 书籍的id + ？
    所以我们要先通过接口获取书籍信息 书籍id 有多少章节 拼接字段

    从章节id获取行动数据 行动数据是个list 到时候要和action_dict.txt 做一个取值
    后面需要封装request库，
    增加内部修改id功能

    :param token:
    :param debug:debug模式 打开则是测试服 不打开审核服
    :param secret:加密字段
    :param did:唯一标识
    :param story_chapter_id:章节id
    :param story_id_change:打开则是要重新编辑id 现在是暂时在id前面加字段
    :param change_id:需要添加的字段
    :return:
    """
    if story_id_change:
        full_id = f"{change_id}{story_chapter_id}"
    else:
        full_id = story_chapter_id
    url = get_test_url(debug)
    uri = "/story/chapter/actions/"
    # 'version': '3.151.1',
    common_header = ini_common_header()
    common_data = {
        "did": f"{did}",
        "timestamp": f"{str(int(time.time()))}"
    }

    payload = {"story_chapter_id": full_id}
    # 将参数加密
    data = concatenate_strings(common_data, payload)
    sign = get_sign(data, secret)
    common_header["sign"] = sign
    common_header['timestamp'] = str(int(time.time()))
    common_header['noise'] = str(random.randrange(100, 999))
    common_header['did'] = did
    common_header["authorization"] = "Bearer" + " " + token
    try:
        response = requests.request("GET", url + uri, headers=common_header, params=payload)
    except Exception as e:
        raise e
    return response.json()


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


def main():
    # path = os.path.abspath(os.path.join(os.getcwd(), "../../json_package"))
    # read_json_to_dict(path)
    token = get_app_login_token()
    ids = for_story_id_get_chapter_ids(BOOK_ID, token)
    # ids = for_story_id_get_chapter_ids("10414", token)
    index = 0
    for ch_id in ids:
        ch_id = str(ch_id)
        result = for_book_chapter_id_get_action_list(token, story_chapter_id=ch_id, story_id_change=True,
                                                     change_id="6660")
        dir = "C:\\Users\\王凯\\Desktop\\test_file\\UI_test_framework\\parse_data_files"
        file_name = f"{dir}\\result_json_{index}.txt"
        result2 = json.dumps(result)
        with open(file_name, "w+", encoding="utf-8") as w:
            w.write(result2)
        index += 1


if __name__ == '__main__':
    main()
