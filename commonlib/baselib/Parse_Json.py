import requests
import time
import hmac
import random
import zipfile
import json
from commonlib.baselib.excel import Excel
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_DEBUG, LOG_WARN, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
import os

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
MsgCenter(MODULE_NAME)

BOOK_ID = "666010190"
# BOOK_ID = "10190"
SLEEP_TIME = 1
TYPE = "type"
DIALOG_TYPE = "dialog_type"
CONTENT = "content"
ITEM_LIST = 'item_list'
TEST_OR_NOT = 'test_or_not'
DEBUG_ = True


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


def get_app_login_token(debug=DEBUG_, secret="56a354ec", did="zpf0001"):
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
    print(f"token --> {token}")
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


def get_test_url(debug=DEBUG_):
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


def get_book_chapter_id_result(token, story_chapter_ids: list, debug=DEBUG_, secret="56a354ec", did="zpf0001",
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
        print(full_id)
        print(repr(common_header))
        print(url + uri)
        try:
            response = requests.request("GET", url + uri, headers=common_header, params=payload)
            action_file_path = response.json().get("data").get("action_file").get("path")
            zip_path_list.append(action_file_path)
        except Exception as e:
            raise e
        time.sleep(SLEEP_TIME)

        break

    return zip_path_list


def list_to_str(d_list):
    ret_str = ""
    for line in d_list:
        for k, v in line.items():
            ret_str += v + ","
    return ret_str


def for_story_id_get_chapter_ids(story_id, token, debug=DEBUG_, secret="56a354ec", did="zpf0001"):
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
    print(repr(response.json()))
    book_name = response.json()['data']['name']
    chapter_ids = response.json()["data"]["chapter_ids"]
    print("00019", chapter_ids)
    return chapter_ids, book_name


def parse_action_list_to_json(result_data: list, save_path, action_dict, lua_action_dict, chunk_size=128):
    """
    解析返回的资源数据，发起请求获取zip文件 存储在固定文件夹 并解压重命名获取行动数据
    解压之后 读取txt内容 洗数据
    到时候要和action_dict.txt 做一个取值
    :param result_data:
    :param save_path:章节txt保存路径
    :param chunk_size:块大小 怕文件过大 分块写入
    :param action_dict:
    :param lua_action_dict:
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

    action_result = wash_action_datas(save_path, action_dict, lua_action_dict, )
    return action_result


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


def write_action_book_data(action_data, excel_fp: str, start_row=2) -> None:
    """
    写入数据
    :param action_data:
    :param excel_fp:
    :param start_row:
    :return:
    """
    # 防止重复写入数据 创建文件夹之前 先清除文件
    for file_path, dir_list, files in os.walk(os.path.dirname(excel_fp)):
        for file_name in files:
            rubbish_file = os.path.join(file_path, file_name)
            os.remove(rubbish_file)

    excel = Excel(excel_fp, new_flag=True)
    for index in range(len(action_data)):
        # ch_name = str(action_data[index].keys())
        for ch, value in action_data[index].items():
            excel.records_write(ch, records=value, start_row=start_row)
    # excel.sheet_delete("Sheet")
    excel.save(backup=False)


def main():
    if DEBUG_:
        parse_path = os.path.abspath(os.path.join(os.getcwd(), "../../parse_data_files"))
        # 获取token
        token = get_app_login_token()
        # 获取书籍章节列表,书籍名字
        ids, bk_name = for_story_id_get_chapter_ids(BOOK_ID, token)
        # 拼接书籍章节列表
        result_list = get_book_chapter_id_result(token, ids, story_id_change=True, change_id="6660")

        # 获取 action type 对应的字典
        txt_path = os.path.abspath(os.path.join(os.getcwd(), "../../action_book.txt"))
        txt_result_dict = read_txt_to_dict(txt_path)
        # 获取 lua type 对应的字典
        lua_path = os.path.abspath(os.path.join(os.getcwd(), "../../StoryDialogType.lua"))
        lua_result_dict = read_lua_to_dict(lua_path)

        # 发起网络请求 获得action zip ，解压，删除zip文件获取txt文件，读取txt文件组装成一本书的action数据结构
        results = parse_action_list_to_json(result_list, save_path=parse_path, action_dict=txt_result_dict,
                                            lua_action_dict=lua_result_dict)

        # 把action data 写入进 xlsx 中等待解析
        new_excel_name = f"../../excel_package/{bk_name}.xlsx"
        excel_path = os.path.abspath(os.path.join(os.getcwd(), new_excel_name))
        write_action_book_data(action_data=results, excel_fp=excel_path)


if __name__ == '__main__':
    main()
