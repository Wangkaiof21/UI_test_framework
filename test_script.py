from commonlib.baselib.ConnectAdb import connect_device, get_dev_name
from airtest.core.api import G, sleep
from commonlib.baselib.ControlAdb import phone_wake, start_game, stop_game


def test_case():
    try:

        dev_name = get_dev_name()
        a = connect_device(ip="127.0.0.1:5037", devices_names=dev_name,
                           log_path="C:\\Users\\王凯\\Desktop\\test_file\\UI_test_framework\\logs", adb_path=1)
        phone_wake(G.DEVICE)
        stop_game(G.DEVICE, "com.stardust.spotlight")
        start_game(G.DEVICE, "com.stardust.spotlight")
        sleep(8)
    except Exception as e:
        print(f"error {e}")


def read_book_task():
    pass


def main():
    test_case()


if __name__ == '__main__':
    main()
