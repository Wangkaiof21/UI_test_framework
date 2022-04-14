from time import sleep
from poco.exceptions import PocoNoSuchNodeException


def poco_try_click(poco, parent, click_name, description="", wait_time=0.5, try_time=1, sleep_time=0):
    """
    尝试点击的元素
    :param poco:
    :param parent:
    :param click_name:
    :param description:
    :param wait_time:
    :param try_time:
    :param sleep_time:
    :return:
    """
    print(f"{description}尝试点击{click_name}")
    if parent == click_name:
        try:
            poco(click_name).click()
            print(f"发现{description}按钮，并点击")
            sleep(sleep_time)
            return True
        except Exception as e:
            print(f"Error click {e}")
            return False
    elif poco(parent).offspring(click_name).wait(wait_time).exists():
        try:
            poco(parent).offspring(click_name).click()
            print(f"发现{description}按钮，并点击")
            return True
        except:
            return False
    else:
        # mylog.info("未发现-【{}】-元素".format(ClickName))
        # mylog.info("未发现-【{}】-元素".format(ClickName))
        return False
