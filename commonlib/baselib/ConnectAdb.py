from airtest.core.api import auto_setup, sleep, shell, wake, home
import os

path = ""


def connect_device(ip: str, devices_name: str, log_path: str, adb_path, method=None, ) -> bool:
    """
    链接手机端 调用方法
    auto_setup(__file__, devices=["Android://127.0.0.1:5037/SJE5T17B17","Android://127.0.0.1:5037/SJE5T17B18"])
    :param ip:本地ip 貌似是固定的
    :param devices_name:从adb devices获取
    :param adb_path:
    :param method:针对手机配置
    :param log_path:链接log存放path
    :return:
    """
    index_time = 10
    while index_time > 0:
        index_time -= 1
        try:
            config = f"android://{ip}/{devices_name}"
            print(f"Connect to {config}")
            auto_setup(__file__, devices=[config], logdir=log_path, compress=90)
            home()
            return True
        except Exception as e:
            print(f"Connect failed error :{e}")
            return False


def get_dev_name() -> list:
    """
    获取设备号
    :return:
    """
    cmd = "adb devices"
    result = os.popen(cmd)
    result = result.read()
    devices_list = []
    for line in result.split("\n"):
        if "\t" in line:
            get_name = line.split("\t")
            devices_list.append(get_name[0])
    return devices_list


if __name__ == '__main__':
    name_ = get_dev_name()
    a = connect_device(ip="127.0.0.1:5037", devices_name=name_[0],
                       log_path="C:\\Users\\王凯\\Desktop\\test_file\\UI_test_framework\\logs", adb_path=1)
    # print(a)
