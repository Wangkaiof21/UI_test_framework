def phone_wake(dev):
    """

    :param dev:
    :return:
    """
    print('dev', dev)
    dev.wake()


def start_game(dev, package):  # 启动游戏
    """

    :param dev:
    :param package:
    :return:
    """
    dev.start_app(package)
    print("启动游戏", package)


def stop_game(dev, package):
    """

    :param dev:
    :param package:
    :return:
    """
    dev.stop_app(package)
    print(f"停止游戏{package}")
    return True
