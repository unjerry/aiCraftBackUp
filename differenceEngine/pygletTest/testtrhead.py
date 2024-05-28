import threading
import time


def background_task():
    """后台任务函数"""
    while True:
        print("后台线程正在运行...")
        time.sleep(3)  # 每3秒打印一次


# 创建一个线程对象
thread = threading.Thread(target=background_task)

# 设置为后台线程，这样主线程退出时不会等待它
thread.setDaemon(True)

# 启动线程
thread.start()

# 主线程的操作，比如：
print("主线程正在运行...")
time.sleep(10)  # 主线程休眠10秒
print("主线程结束。")
