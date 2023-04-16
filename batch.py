import os
import time
import subprocess
from subprocess import PIPE
from dotenv import load_dotenv

load_dotenv()

# 最大実行回数
NUMBER_OF_EXECUTIONS = os.getenv("NUMBER_OF_EXECUTIONS")
# 実行間隔（秒）
EXECUTION_INTERVAL = os.getenv("EXECUTION_INTERVAL")

def execution():
    for i in range(int(NUMBER_OF_EXECUTIONS)):
        print(str(i) + "回目の実行開始。")
        subprocess.run(["python", "detect.py"], stdout=PIPE, stderr=PIPE)
        print(str(i) + "回目の実行完了。データベースが更新されました。")
        time.sleep(int(EXECUTION_INTERVAL))

def main():
    print("処理間隔：" + str(EXECUTION_INTERVAL) + "秒")
    print("実行回数：" + str(NUMBER_OF_EXECUTIONS) + "回")
    execution()
    print("全てのタスクが終了しました。")

main()