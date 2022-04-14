from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco


class POCO:
    def __init__(self, device):
        # self.android_poco = AndroidUiautomationPoco(device=device)
        self.po = UnityPoco(device=device)