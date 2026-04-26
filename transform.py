#!/usr/bin/env python3
import re
import zipfile
from pathlib import Path


def is_pure_integers(content):
    """检查内容是否只包含整数（每行可以是多个整数，空格分隔）"""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        for part in parts:
            if not re.match(r'^-?\d+$', part):
                return False
    return True


def main():
    raw_dir = Path("raw")
    compressed_dir = Path("Compressed")

    # 创建 Compressed 目录
    compressed_dir.mkdir(exist_ok=True)

    for i in range(1001, 1011):
        num = i - 1000

        in_file = raw_dir / f"{i}.in"
        out_file = raw_dir / f"{i}.out"

        if not in_file.exists() or not out_file.exists():
            print(f"警告: {i} 的文件不存在，跳过")
            continue

        # 读取输出文件内容
        with open(out_file, 'r') as f:
            content = f.read()

        # 判断使用哪个 checker（都命名为 m1）
        if is_pure_integers(content):
            judger = "ncmp"
        else:
            judger = "wcmp"

        # 创建临时目录
        temp_dir = Path(f"temp_{num}")
        temp_dir.mkdir(exist_ok=True)

        try:
            # 复制文件，都重命名为 m1.in 和 m1.ans
            with open(in_file, 'r') as src, open(temp_dir / "m1.in", 'w') as dst:
                dst.write(src.read())

            with open(out_file, 'r') as src, open(temp_dir / "m1.ans", 'w') as dst:
                dst.write(src.read())

            # 创建 problem.conf
            conf_content = f"""n_tests 1
n_ex_tests 0
n_sample_tests 0
input_pre m
input_suf in
output_pre m
output_suf ans
time_limit 1
memory_limit 512
output_limit 64
use_builtin_judger on
use_builtin_checker {judger}
"""
            with open(temp_dir / "problem.conf", 'w') as f:
                f.write(conf_content)

            # 打包为 zip 文件到 Compressed 目录
            zip_path = compressed_dir / f"{num}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in temp_dir.iterdir():
                    zf.write(file, file.name)

            print(f"已创建 Compressed/{num}.zip (使用 {judger})")

        finally:
            # 清理临时目录
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

    print("完成！生成了 Compressed/1.zip 到 Compressed/10.zip")


if __name__ == "__main__":
    main()