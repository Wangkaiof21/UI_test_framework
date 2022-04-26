from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from commonlib.baselib.log_message import LogMessage, LOG_INFO, LOG_ERROR
import os


class POCO:
    def __init__(self, device):
        # self.android_poco = AndroidUiautomationPoco(device=device)
        self.po = UnityPoco(device=device)
