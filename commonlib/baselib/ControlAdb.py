from commonlib.baselib.log_message import LogMessage, LOG_ERROR, LOG_INFO


def phone_wake(dev):
    """

    :param dev: G.DEVICE
    :return:
    """
    LogMessage(module="phone_wake", level=LOG_INFO, msg=f"wake phone")
    dev.wake()


def start_game(dev, package):  # 启动游戏
    """

    :param dev: G.DEVICE
    :param package:
    :return:
    """
    dev.start_app(package)
    LogMessage(module="start_game", level=LOG_INFO, msg=f"start game {package}")


def stop_game(dev, package):
    """

    :param dev: G.DEVICE
    :param package:
    :return:
    """
    dev.stop_app(package)
    LogMessage(module="stop_game", level=LOG_INFO, msg=f"stop game {package}")
    return True


def clear_game_data(dev, package):
    """

    :param dev: G.DEVICE
    :param package:
    :return:
    """
    dev.clear_app(package)
    LogMessage(module="stop_game", level=LOG_INFO, msg=f"clean game {package}")
