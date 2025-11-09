import os
import subprocess
import sys


def run_command(command: list) -> tuple:
    """
    执行终端命令并返回结果
    :param command: 命令列表（如 ["python", "manage.py", "makemigrations"]）
    :return: (是否成功, 输出信息)
    """
    try:
        # 执行命令，捕获 stdout 和 stderr
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # 输出为字符串格式（而非字节）
        )
        return (True, result.stdout)
    except subprocess.CalledProcessError as e:
        # 命令执行失败（返回非0状态码）
        return (False, f"命令执行失败：{e.stderr}")
    except Exception as e:
        # 其他异常（如命令不存在）
        return (False, f"发生错误：{str(e)}")


def main():
    # 检查 manage.py 是否存在
    if not os.path.exists("manage.py"):
        print("错误：未找到 manage.py，请确保脚本在项目根目录执行", file=sys.stderr)
        sys.exit(1)

    # 定义迁移命令
    makemigrations_cmd = ["python", "manage.py", "makemigrations"]
    migrate_cmd = ["python", "manage.py", "migrate"]

    # 执行 makemigrations
    print("===== 开始生成迁移文件（makemigrations） =====")
    success, output = run_command(makemigrations_cmd)
    print(output)
    if not success:
        print("生成迁移文件失败，终止执行", file=sys.stderr)
        sys.exit(1)

    # 执行 migrate
    print("\n===== 开始应用迁移（migrate） =====")
    success, output = run_command(migrate_cmd)
    print(output)
    if not success:
        print("应用迁移失败", file=sys.stderr)
        sys.exit(1)

    print("\n✅ 数据库迁移操作已全部完成")


if __name__ == "__main__":
    main()