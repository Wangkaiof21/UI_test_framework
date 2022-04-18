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


def for_book_chapter_id_get_action_list(token, debug=True, secret="56a354ec", did="zpf0001",
                                        story_chapter_id="666010190001"):
    """
    666010190001 实际上是66601019+0001 书籍的id + ？
    所以我没要先通过接口获取书籍信息 书籍id 有多少章节 拼接字段
    从章节id获取行动数据 行动数据是个list 到时候要和action_dict.txt 做一个取值

    后面需要封装request库，选择url的方法

    :param token:
    :param debug:
    :param secret:
    :param did:
    :param story_chapter_id:
    :return:
    """
    if debug:
        # 测试服HOST
        url = "http://project_x_api.stardustworld.cn/api/v1"
    else:
        # 审核服HOST
        url = "http://dev_spt_aws_game_api.stardustgod.com/api/v1"

    uri = "/story/chapter/actions/"
    # 'version': '3.151.1',
    common_header = {'timestamp': '',
                     'sign': '',
                     'noise': '',
                     'did': '',
                     'version': '3.170.1',
                     'channel': 'AVG10003',
                     'package-name': 'com.stardust.spotlight',
                     'Accept-Language': 'en',
                     'dlevel': '_medium',
                     'authorization': ''
                     }

    common_data = {
        "did": f"{did}",
        "timestamp": f"{str(int(time.time()))}"
    }

    payload = {"story_chapter_id": story_chapter_id}
    # 将参数加密
    data = concatenate_strings(common_data, payload)
    sign = get_sign(data, secret)
    common_header["sign"] = sign
    common_header['timestamp'] = str(int(time.time()))
    common_header['noise'] = str(random.randrange(100, 999))
    common_header['did'] = did
    common_header["authorization"] = "Bearer" + " " + token
    # print("common_header", repr(common_header))

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
    if debug:
        # 测试服HOST
        url = "http://project_x_api.stardustworld.cn/api/v1"
    else:
        # 审核服HOST
        url = "http://dev_spt_aws_game_api.stardustgod.com/api/v1"

    uri = "/story/show/"
    # 'version': '3.151.1',
    common_header = {'timestamp': '',
                     'sign': '',
                     'noise': '',
                     'did': '',
                     'version': '3.170.1',
                     'channel': 'AVG10003',
                     'package-name': 'com.stardust.spotlight',
                     'Accept-Language': 'en',
                     'dlevel': '_medium',
                     'authorization': ''
                     }

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
    print(response.json())
    chapter_ids = response.json()["data"]["chapter_ids"]
    print(chapter_ids)
    return chapter_ids


def main():
    # path = os.path.abspath(os.path.join(os.getcwd(), "../../json_package"))
    # read_json_to_dict(path)
    token = get_app_login_token()
    ids = for_story_id_get_chapter_ids(BOOK_ID, token)
    # ids = for_story_id_get_chapter_ids("10414", token)
    for ch_id in ids:
        ch_id = "6660"+str(ch_id)
        result = for_book_chapter_id_get_action_list(token, story_chapter_id=ch_id)
        print(repr(result))
        break




if __name__ == '__main__':
    main()
