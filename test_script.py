from commonlib.baselib.ConnectAdb import connect_device, get_dev_name
from airtest.core.api import G, sleep
from commonlib.baselib.ControlAdb import phone_wake, start_game, stop_game
from commonlib.baselib.PocoDrivers import poco_try_click
from poco.drivers.unity3d import UnityPoco


def test_case():
    try:
        dev_name = get_dev_name()
        a = connect_device(ip="127.0.0.1:5037", devices_names=dev_name,
                           log_path="C:\\Users\\王凯\\Desktop\\test_file\\UI_test_framework\\logs", adb_path=1)
        phone_wake(G.DEVICE)
        stop_game(G.DEVICE, "com.stardust.spotlight")
        start_game(G.DEVICE, "com.stardust.spotlight")
        sleep(10)
        poco = poco_connect("localhost", 5001)
        poco("Refresh").click()
        sleep(2)
        poco("Chapter(Clone)").click()
        sleep(2)
        poco("Play").click()
    except Exception as e:
        print(f"error {e}")


def poco_connect(local_host, port):
    poco = UnityPoco((local_host, port))
    return poco


def read_book_task():
    book_id = ""
    chapter = [0, 1, 2, 3, 4]


def main():
    test_case()
    read_book_task()


if __name__ == '__main__':
    main()
