import csv
import os
import re
import yaml
from pathlib import Path


def parse_problem_number(problem_dir_name):
    """解析题目目录名，返回数字编号"""
    # 提取目录名中的数字部分
    match = re.search(r'\d+', problem_dir_name)
    if match:
        return int(match.group())
    return None


def read_statement_from_md(md_file_path):
    """从markdown文件读取statement内容"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content
    except Exception as e:
        print(f"  ❌ 读取statement失败 {md_file_path}: {e}")
        return ""


def read_title_from_yaml(yaml_file_path):
    """从problem.yaml文件读取title"""
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # 获取title字段
            title = data.get('title', '')
            return title.strip() if title else ""
    except Exception as e:
        print(f"  ❌ 读取title失败 {yaml_file_path}: {e}")
        return ""


def main():
    # 获取raw目录路径（假设脚本在项目根目录运行）
    script_dir = Path(__file__).parent
    raw_dir = script_dir / 'raw'

    if not raw_dir.exists():
        print(f"❌ raw目录不存在: {raw_dir}")
        return

    # 获取raw目录下的所有子目录
    problem_dirs = []
    for item in raw_dir.iterdir():
        if item.is_dir():
            # 检查目录名是否为数字（或包含数字）
            num = parse_problem_number(item.name)
            if num is not None:
                problem_dirs.append((num, item))

    # 按数字排序
    problem_dirs.sort(key=lambda x: x[0])

    if not problem_dirs:
        print("❌ 在raw目录下没有找到有效的题目目录")
        return

    print(f"找到 {len(problem_dirs)} 个题目目录")

    results = []

    for idx, (problem_num, problem_dir) in enumerate(problem_dirs, 1):
        print(f"\n正在处理第 {idx} 题 (目录: {problem_dir.name}) ...")

        # 构建文件路径
        problem_yaml = problem_dir / 'problem.yaml'
        problem_md = problem_dir / 'problem_zh.md'

        # 读取title
        title = ""
        if problem_yaml.exists():
            title = read_title_from_yaml(problem_yaml)
        else:
            print(f"  ⚠️ 未找到problem.yaml: {problem_yaml}")

        # 读取statement
        statement = ""
        if problem_md.exists():
            statement = read_statement_from_md(problem_md)
        else:
            print(f"  ⚠️ 未找到problem_zh.md: {problem_md}")

        # 添加到结果
        problem_data = {
            'pid': idx,  # 使用序号作为题目编号（第1题、第2题...）
            'title': title,
            'statement': statement
        }

        results.append(problem_data)
        print(f"  ✅ 成功: PID={idx}, 标题={title[:30]}{'...' if len(title) > 30 else ''}")

    # 保存到CSV文件
    if results:
        filename = f'contest_problems.csv'
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['pid', 'title', 'statement']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\n🎉 完成！共获取 {len(results)} 道题，已保存到 {filename}")

        # 打印摘要信息
        print("\n📋 题目摘要:")
        for problem in results:
            print(f"  第{problem['pid']}题: {problem['title']}")
    else:
        print("❌ 没有获取到任何数据")


if __name__ == '__main__':
    main()