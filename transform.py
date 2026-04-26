#!/usr/bin/env python3
import re
import zipfile
import shutil
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


def get_checker_type(out_file_path):
    """根据输出文件内容判断使用哪个checker"""
    with open(out_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if is_pure_integers(content):
        return "ncmp"
    else:
        return "wcmp"


def process_problem(problem_dir, output_dir):
    """处理单个题目目录"""
    problem_num = problem_dir.name
    testdata_dir = problem_dir / "testdata"

    if not testdata_dir.exists():
        print(f"  ⚠️ {problem_num}: testdata目录不存在，跳过")
        return False

    # 查找所有 .in 文件
    in_files = sorted(testdata_dir.glob("*.in"))

    if not in_files:
        print(f"  ⚠️ {problem_num}: testdata目录中没有找到.in文件，跳过")
        return False

    print(f"\n处理题目 {problem_num}: 找到 {len(in_files)} 个测试点")

    # 创建临时目录
    temp_dir = Path(f"temp_{problem_num}")
    temp_dir.mkdir(exist_ok=True)

    try:
        test_cases = []

        # 处理每个测试点
        for idx, in_file in enumerate(in_files, start=1):
            # 查找对应的 .out 或 .ans 文件
            out_file = None
            for suffix in ['.out', '.ans']:
                possible_out = testdata_dir / f"{in_file.stem}{suffix}"
                if possible_out.exists():
                    out_file = possible_out
                    break

            if not out_file:
                print(f"  ⚠️ {problem_num}: 找不到 {in_file.stem} 对应的输出文件，跳过此测试点")
                continue

            # 重命名为 m{idx}.in 和 m{idx}.ans
            new_in_name = f"m{idx}.in"
            new_ans_name = f"m{idx}.ans"

            with open(in_file, 'r', encoding='utf-8') as src, \
                    open(temp_dir / new_in_name, 'w', encoding='utf-8') as dst:
                dst.write(src.read())

            with open(out_file, 'r', encoding='utf-8') as src, \
                    open(temp_dir / new_ans_name, 'w', encoding='utf-8') as dst:
                dst.write(src.read())

            test_cases.append({
                'idx': idx,
                'in_file': new_in_name,
                'ans_file': new_ans_name
            })

            # 只检查第一个测试点来判断checker类型（所有测试点使用同一个checker）
            if idx == 1:
                checker_type = get_checker_type(out_file)

        if not test_cases:
            print(f"  ❌ {problem_num}: 没有有效的测试点")
            return False

        n_tests = len(test_cases)

        # 创建 problem.conf
        conf_content = f"""n_tests {n_tests}
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
use_builtin_checker {checker_type}
"""
        with open(temp_dir / "problem.conf", 'w', encoding='utf-8') as f:
            f.write(conf_content)

        # 打包为 zip 文件到 Compressed 目录
        zip_path = output_dir / f"{problem_num}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in temp_dir.iterdir():
                zf.write(file, file.name)

        print(f"  ✅ 已创建 {problem_num}.zip (测试点: {n_tests}, checker: {checker_type})")
        return True

    except Exception as e:
        print(f"  ❌ {problem_num}: 处理失败 - {e}")
        return False
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    raw_dir = Path("raw")
    compressed_dir = Path("Compressed")

    if not raw_dir.exists():
        print(f"❌ raw目录不存在: {raw_dir}")
        return

    # 创建 Compressed 目录
    compressed_dir.mkdir(exist_ok=True)

    # 获取raw目录下的所有子目录（题目目录）
    problem_dirs = []
    for item in raw_dir.iterdir():
        if item.is_dir():
            # 检查目录名是否为数字
            if item.name.isdigit():
                problem_dirs.append(item)

    if not problem_dirs:
        print("❌ 在raw目录下没有找到有效的题目目录（数字命名的目录）")
        return

    # 按数字排序
    problem_dirs.sort(key=lambda x: int(x.name))

    print(f"找到 {len(problem_dirs)} 个题目目录:")
    for p in problem_dirs:
        print(f"  - {p.name}")

    success_count = 0

    for problem_dir in problem_dirs:
        if process_problem(problem_dir, compressed_dir):
            success_count += 1

    print(f"\n🎉 完成！成功处理 {success_count}/{len(problem_dirs)} 个题目，结果保存在 Compressed 目录")


if __name__ == "__main__":
    main()