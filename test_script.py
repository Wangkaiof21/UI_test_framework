from commonlib.baselib.ConnectAdb import connect_device, get_dev_name
from airtest.core.api import G, sleep
from commonlib.baselib.ControlAdb import phone_wake, start_game, stop_game
from commonlib.baselib.PocoDrivers import poco_try_click
from poco.drivers.unity3d import UnityPoco


def test_case(chapter_):
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
        poco_select_chapter(poco, chapter_object=chapter_)
        poco('Play', type='Image').click()
        sleep(5)


    except Exception as e:
        print(f"error {e}")


def first_read_book(poco):
    """
    第一次阅读 要输入女主角名字 这个功能暂时没实现，set_text()不管用
    直接confifirm
    :param poco:
    :return:
    """
    try:
        poco.click([0.5, 0.5])
        poco('Confirm', type='Image').wait(2).click()
    except Exception as e:
        print(f"this chapter is not first read --> {e}")


def poco_select_chapter(poco, chapter_object, debug=False):
    """
    选择章节
    需求1:阅读所有章节
    需求2:阅读固定章节的[前1章,本章节,后1章]
    debug 打开时只接受 int
    :param poco:
    :param chapter_object:
    :param debug:
    :return:返回出章节的list 外层做选择
    """
    # if debug:
    #     if isinstance(chapter_object, int) is None:
    #         return
    # else:

    phone_chapter_list = []
    if len(chapter_object) > len(phone_chapter_list):
        print("The chapter_object is too long ,please check again")
        return phone_chapter_list
    for item in poco('ChapterGrid', type='Node').child():
        phone_chapter_list.append(item)

    for index in range(len(chapter_object)):
        phone_chapter_list[index].click()


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


def poco_try_send_text(poco, input_filed, text):
    """输入Text"""
    time = 2
    while time > 0:
        time -= 1
        try:
            poco(input_filed).set_text(str(text))
            return True
        except Exception as e:
            raise f"输入-【{e}】-或失败"


def poco_connect(local_host, port):
    poco = UnityPoco((local_host, port))
    return poco


def main():
    test_case(chapter_=[0, 1, 2, 3])
    # read_book_task()


if __name__ == '__main__':
    main()
