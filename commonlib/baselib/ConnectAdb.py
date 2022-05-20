from airtest.core.api import auto_setup, sleep, shell, wake, home
from commonlib.baselib.log_message import LogMessage, LOG_INFO, LOG_ERROR
import os

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AdbConnect:
    @staticmethod
    def connect_device(ip: str, devices_names: list, log_path: str, adb_path=None, method=None,
                       compression_ratio=90) -> bool:
        """
        链接手机端 调用方法
        auto_setup(__file__, devices=["Android://127.0.0.1:5037/SJE5T17B17","Android://127.0.0.1:5037/SJE5T17B18"])
        这里设计的有问题 丑 得改 先用着
        :param ip:本地ip 貌似是固定的
        :param devices_names:从adb devices获取列表【】
        :param adb_path:这个是adb.exe的绝对路径 设置了环境变量后 已经废弃使用这个参数
        :param method:针对手机配置
        :param log_path:链接log存放path
        :param compression_ratio:图片压缩比率
        :return:
        """
        for name in devices_names:
            index_time = 10
            while index_time > 0:
                index_time -= 1
                try:
                    config = f"android://{ip}/{name}"
                    LogMessage(level=LOG_INFO, module=MODULE_NAME, msg=f"Connect to {config}")
                    auto_setup(__file__, devices=[config], logdir=log_path, compress=compression_ratio,
                               project_root=BASE_DIR)
                    sleep(1)
                    return True
                except Exception as e:
                    LogMessage(level=LOG_ERROR, module=MODULE_NAME, msg=f"Connect failed error :{e} try again")
                    return False

    @staticmethod
    def get_dev_name() -> list:
        """
        配置了环境变量 则不需要拼接adb的绝对路径 获取设备号
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

    def install_game(self, dev, package, mypath):  # 安装应用
        pass

    def uninstall_game(self, dev, package, mypath):  # 卸载应用
        pass
