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
        # 寻找书架
        search_book_lis(poco, book_list_name="Diamond-Free Stories For AD", normal_list='NormalBookList(Clone)',
                        all_button_name='seeall')
        # 从书架找书本
        find_book(poco, book_list='BookOSARoot_CellGroupPrefab(Clone)', books_name="see_all_book(Clone)",
                  target_book_name="Behind Closed Doors")
        # reset book
        poco('Reset', type='Node').click()
        poco('ComfirmBtn', type='Button').wait(2).click()
        poco('Play', type='Image').click()
    except Exception as e:
        print(f"error {e}")


def find_book(poco, book_list, books_name, target_book_name):
    """

    :param poco: object
    :param book_list: 书架名
    :param books_name: 书架书的view_name
    :param target_book_name: 目标书本
    :return:
    """
    for item in poco(book_list, type='Node'):
        for line in item.child(books_name):
            flag = line.child("Views").child("Book_name")
            if flag.attr('TMP_Text') == target_book_name:
                flag.click()
                break


def search_book_lis(poco, book_list_name: str, normal_list: str, all_button_name: str) -> None:
    """
    搜寻合适的书架
    :param poco:
    :param book_list_name:
    :param normal_list:
    :param all_button_name:
    :return:
    """
    index = poco(normal_list, type='Node')
    for i in range(7):
        if index and index.child("title").attr('TMP_Text') == book_list_name:
            sleep(2)
            index.child(all_button_name).wait(2).click()
            print(f"Try click the {index.child(all_button_name)}")
            break
        else:
            try:
                point_a = [0.5, 0.55]
                center = [0.5, 0.1]
                poco.swipe(point_a, center)
                sleep(2)
                # index.child(all_button_name).wait(2).click()
            except Exception as e:
                print(f"Find book list error -> {e}")


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
