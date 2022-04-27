import os
from commonlib.baselib.excel import Excel
from commonlib.baselib.msg_center import MsgCenter
from commonlib.baselib.log_message import LOG_DEBUG

TEST_OR_NOT = 'test_or_not'

def ddd(fp):
    for file_path, dir_list, files in os.walk(os.path.dirname(fp)):
        for file_name in files:
            rubbish_file = os.path.join(file_path, file_name)
            os.remove(rubbish_file)



if __name__ == '__main__':

    g = "C:\\Users\\王凯\Desktop\\test_file\\UI_test_framework\\logs\\1650958324572.jpg"
    ddd(g)

