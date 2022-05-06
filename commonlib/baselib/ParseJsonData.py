#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/5 10:46
# @Author  : WangKai
# @Site    : 
# @File    : ParseJsonData.py
# @Software: PyCharm
import requests
import time
import hmac
import random
import zipfile
import json
from commonlib.baselib.excel import Excel
from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_INFO
from commonlib.baselib.msg_center import MsgCenter
import os
from commonlib.baselib.Config import ConfigView

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
MsgCenter(MODULE_NAME)

SLEEP_TIME = 1
TYPE = "type"
DIALOG_TYPE = "dialog_type"
CONTENT = "content"
ITEM_LIST = 'item_list'
TEST_OR_NOT = 'test_or_not'

DID = "zpf0001"


class InitExcelData:
    def __init__(self, book_id: str, debug: bool, did: str):
        self.debug = debug
        self.book_id = book_id
        self.did = did

    def ini_common_header(self) -> dict:
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

    def get_sign(self, data, secret):
        """
        载荷加密
        :param data:
        :param secret:
        :return:
        """
        line = hmac.new(secret.encode(), data.encode(), digestmod='sha256')
        return line.hexdigest()

    def concatenate_strings(self, common_, payload_) -> str:
        """
        :param common_:加密的基本数据
        :param payload_:加密载荷
        :return:
        """
        result_list_ = []
        # 将两个字典合并
        result_dict_ = dict(common_, **payload_)
        # 将合并的字典key和value用=连接存入列表
        for line in sorted(result_dict_.items()):
            result_list_.append("=".join(line))
        # 将列表用&连接返回字符串
        record_data = '&'.join(result_list_)
        return record_data

    def get_test_url(self) -> str:
        """

        :return:
        """
        if self.debug:
            # 测试服HOST
            return "http://project_x_api.stardustworld.cn/api/v1"
        else:
            # 审核服HOST
            return "http://dev_spt_aws_game_api.stardustgod.com/api/v1"

    def get_login_token(self, secret="56a354ec") -> str:
        """
        获得app登录token
        :param secret: 密钥？
        :return:
        """
        url = self.get_test_url()
        login_header = ConfigView.LOGIN_HEADER
        common_data = {
            "did": f"{self.did}",
            "timestamp": str(int(time.time()))
        }
        payload = {'identity_type': '1',
                   'identifier': self.did
                   }
        # 将需要传入的参数加密
        data = self.concatenate_strings(common_data, payload)
        # # headers赋值
        login_header["sign"] = self.get_sign(data, secret)
        login_header['timestamp'] = str(int(time.time()))
        login_header['noise'] = str(random.randrange(100, 999))
        login_header["did"] = self.did
        token = ""
        try:
            response = requests.post(url + "/login", headers=login_header, data=payload)
            token = response.json()["data"]["access_token"]
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Get login token => {token}")
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Login error => {e}")
        return token

    def get_book_msg(self, token, secret="56a354ec"):
        """
        获取故事id的list
        :param token:
        :param secret:
        :return:
        """
        url = self.get_test_url()
        uri = "/story/show/"
        # 'version': '3.151.1',
        common_header = self.ini_common_header()
        common_data = {
            "did": self.did,
            "timestamp": f"{str(int(time.time()))}"
        }
        payload = {"story_id": self.book_id}
        # 将参数加密
        data = self.concatenate_strings(common_data, payload)
        sign = self.get_sign(data, secret)
        common_header["sign"] = sign
        common_header['timestamp'] = str(int(time.time()))
        common_header['noise'] = str(random.randrange(100, 999))
        common_header["authorization"] = f"Bearer {token}"
        common_header["did"] = self.did
        book_name = ""
        chapter_ids = ""
        try:
            response = requests.request("GET", url + uri, headers=common_header, params=payload)
            book_name = response.json()['data']['name']
            chapter_ids = response.json()["data"]["chapter_ids"]
            LogMessage(level=LOG_INFO, module=MODULE_NAME,
                       msg=f"Get book msg => book_name: {book_name}, book_chapters: {chapter_ids}")
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Get book ids error => {e}")
        return chapter_ids, book_name

    def get_book_chapter_id_result(self, token, story_chapter_ids: list, secret="56a354ec", change_id=None):

        """
        666010190001
        实际上是6660 + 10190001 书籍的id + ？
        所以我们要先通过接口获取书籍信息 书籍id 有多少章节 拼接字段
        从章节id获取资源数据 取资源数据的path 拼接 行动数据的zip
        后面需要封装request库，
        :param token:
        :param secret:加密字段
        :param change_id:拼接的字段
        :param story_chapter_ids:章节列表
        :return:
        """
        zip_path_list = list()
        for ch_id in story_chapter_ids:
            if change_id:
                full_id = str(f"{change_id}{ch_id}")
            else:
                full_id = str(ch_id)
            url = self.get_test_url()
            uri = "/story/chapter/actions/"
            # 'version': '3.151.1',
            common_header = self.ini_common_header()
            common_data = {
                "did": self.did,
                "timestamp": str(int(time.time()))
            }
            payload = {"story_chapter_id": full_id}
            # 将参数拼接
            data = self.concatenate_strings(common_data, payload)
            # 将参数加密
            sign = self.get_sign(data, secret)
            common_header["sign"] = sign
            common_header['timestamp'] = str(int(time.time()))
            common_header['noise'] = str(random.randrange(100, 999))
            common_header['did'] = self.did
            common_header["authorization"] = "Bearer" + " " + token
            try:
                response = requests.request("GET", url + uri, headers=common_header, params=payload)
                action_file_path = response.json().get("data").get("action_file").get("path")
                zip_path_list.append(action_file_path)
            except Exception as e:
                LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Get book action zip error => {e}")
            time.sleep(SLEEP_TIME)
        return zip_path_list

    def parse_action_list_to_json(self, result_data: list, save_path, action_dict, lua_action_dict, chunk_size=128):
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
        # target_url_b = "http://spt-akamai.stardustgod.com/spt/"
        if not os.listdir(save_path):
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Path is clean")
            pass
        else:
            for file_path, dir_list, files in os.walk(save_path):
                for file_name in files:
                    rubbish_file = os.path.join(file_path, file_name)
                    os.remove(rubbish_file)
                    LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Clean {rubbish_file} clear")
        abs_path_list = list()
        index = 0
        try:
            for line in result_data:
                full_url = f"{target_url_a}{line}"
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Download to {index} --> {full_url}")
                r = requests.get(full_url, stream=True)
                time.sleep(SLEEP_TIME)
                file_abs_name = save_path + "\\" + f"action_{index}.zip"
                with open(file_abs_name, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        fd.write(chunk)
                LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Download {file_abs_name} done")
                abs_path_list.append(file_abs_name)
                index += 1
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f'No.{index} file Error => {e}')

        try:
            # unzip_files
            for line in abs_path_list:
                if zipfile.is_zipfile(line):
                    "判断是不是压缩文件"
                    with zipfile.ZipFile(line, 'r') as zipf:
                        zipf.extractall(path=save_path)
                time.sleep(SLEEP_TIME)
            LogMessage(level=LOG_INFO, module=MODULE_NAME, msg='Unzip  done')
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f'Unzip file Error => {e}')

        try:
            for file_path, dir_list, files in os.walk(save_path):
                for file_name in files:
                    if file_name.endswith(".zip"):
                        zip_file = os.path.join(file_path, file_name)
                        os.remove(zip_file)
                        LogMessage(level=LOG_INFO, module=MODULE_NAME,
                                   msg=f"clean zip file --> {os.path.join(file_path, file_name)}")
        except Exception as e:
            LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Delete file error {e}")

        action_result = self.wash_action_datas(save_path, action_dict, lua_action_dict, )
        return action_result

    def wash_action_datas(self, file_path_, txt_, lua_):
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
                                items_data = self.get_key_datas(line.get(ITEM_LIST), txt_, lua_)
                                reline = self.init_new_line(line_dict=line, item_data=items_data)
                                new_action_list.append(reline)
                            # 把条目分组
                            # for date, items in groupby(action_list, key=itemgetter('dialog_no')):
                            #     new_action_list.append(list(items))
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

    def get_key_datas(self, lines, txt_file_data, lua_file_data) -> dict:
        """
        整个ITEM_LIST 进行转换 重新包装
        :param lines: ITEM_LIST
        :param txt_file_data: 行动字典
        :param lua_file_data: lua字典 行动字典的下级 目前只有一个特殊判断就是rename
        :return:
        """
        result_list_ = list()
        for line in lines:
            # 以后有更多需要的"content"里面的值，在这里加，例如文字对话: text_ = line.get("content").get("text_content", "")
            result_dict = dict()
            # 这里要做双重转换 step 1 根据lua文件转换
            result_dict[DIALOG_TYPE] = self.matching_dictionary_to_language(
                str(line.get("content").get("dialog_type", "")), lua_file_data)

            # 这里要做双重转换 step 2 根据action_list.txt文件转换
            result_dict[TYPE] = self.matching_dictionary_to_language(str(line.get(TYPE)), txt_file_data)
            result_list_.append(result_dict)
        # 这里需要做一个数据转换成文字 且拼接 多个字典
        # [{'dialog_type': 'voiceover', 'type': 'play_dialog'}, {'dialog_type': '', 'type': 'object_scene_move'}...]转换成
        # [{'dialog_type': 'voiceover', 'type': 'play_dialog,object_scene_move'}]
        result_list_ = self.dict_datas_to_string(result_list_)
        return result_list_

    def init_new_line(self, line_dict: dict, item_data: dict) -> dict:
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

    def dict_datas_to_string(self, action_line: list) -> dict:
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

    def matching_dictionary_to_language(self, value: str, action_dict: dict):
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

    def read_txt_to_dict(self, fp):
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
                    new_ = line.replace("\n    ", "").replace("\n", '').replace(",", "").replace("//", "").replace(" ",
                                                                                                                   "")
                    if "=" in new_:
                        key, value = new_.split("=")
                        action_name_dict[value] = key
            except Exception as e:
                LogMessage(level=LOG_ERROR, msg=f"Change dict error {e}", module=MODULE_NAME)
                return {}
        return action_name_dict

    def read_lua_to_dict(self, fp):
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
                    new_ = line.replace("\n    ", "").replace("\n", '').replace(",", "").replace("//", "").replace(" ",
                                                                                                                   "")
                    if "=" in new_:
                        key, value = new_.split("=")
                        action_name_dict[value] = key
            except Exception as e:
                LogMessage(level=LOG_ERROR, msg=f"Change dict error {e}", module=MODULE_NAME)
                return {}
        return action_name_dict

    def write_action_book_data(self, action_data, excel_fp: str, start_row=2) -> None:
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


if __name__ == '__main__':
    SWITCH_INDEX = True
    # 方便测试用的开关
    txt_path = os.path.abspath(os.path.join(os.getcwd(), "../../action_book.txt"))
    lua_path = os.path.abspath(os.path.join(os.getcwd(), "../../StoryDialogType.lua"))
    parse_path = os.path.abspath(os.path.join(os.getcwd(), "../../parse_data_files"))

    if SWITCH_INDEX:
        BOOK_ID = "10190"
        DEBUG_ = False
        a = InitExcelData(book_id=BOOK_ID, debug=DEBUG_, did=DID)
        token_ = a.get_login_token()
        chapters, book = a.get_book_msg(token=token_)
        result_list = a.get_book_chapter_id_result(token=token_, story_chapter_ids=chapters)

        # 获取 action type 对应的字典
        txt_result_dict = a.read_txt_to_dict(txt_path)
        # 获取 lua type 对应的字典
        lua_result_dict = a.read_lua_to_dict(lua_path)

        results = a.parse_action_list_to_json(result_list, save_path=parse_path, action_dict=txt_result_dict,
                                              lua_action_dict=lua_result_dict)
        new_excel_name = f"../../excel_package/{book}.xlsx"
        excel_path = os.path.abspath(os.path.join(os.getcwd(), new_excel_name))
        a.write_action_book_data(action_data=results, excel_fp=excel_path)

    elif SWITCH_INDEX is False:
        BOOK_ID = "666010190"
        DEBUG_ = True  # True代表访问的是测试服的url接口 False则是审核服
        a = InitExcelData(book_id=BOOK_ID, debug=DEBUG_, did=DID)
        token_ = a.get_login_token()
        chapters, book = a.get_book_msg(token=token_)
        result_list = a.get_book_chapter_id_result(token=token_, story_chapter_ids=chapters, change_id="6660")

        # 获取 action type 对应的字典
        txt_result_dict = a.read_txt_to_dict(txt_path)
        # 获取 lua type 对应的字典
        lua_result_dict = a.read_lua_to_dict(lua_path)

        results = a.parse_action_list_to_json(result_list, save_path=parse_path, action_dict=txt_result_dict,
                                              lua_action_dict=lua_result_dict)
        new_excel_name = f"../../excel_package/{book}.xlsx"
        excel_path = os.path.abspath(os.path.join(os.getcwd(), new_excel_name))
        a.write_action_book_data(action_data=results, excel_fp=excel_path)
