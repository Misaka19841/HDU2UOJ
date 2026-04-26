import csv
import re
import json
import sys


def clean_description(desc):
    if desc:
        desc = re.sub(r'\*\*注：请到 Clarifications 中查看公告！\*\*\n\n?', '', desc)
        desc = re.sub(r'注：请到 Clarifications 中查看公告！\n\n?', '', desc)
        desc = desc.strip()
    return desc


def build_statement_md(row):
    # 直接使用statement列内容
    statement = row.get('statement', '').strip()

    # 将所有的 ## 替换为 ###
    statement = statement.replace('##', '###')

    return statement


def escape_sql_string(s):
    if s is None:
        return ''
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "''")
    return s


def generate_sql(csv_file, output_sql_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        records = []

        for row in reader:
            title = row.get('title', '').strip()
            pid = row.get('pid', '')

            # 如果title为空，使用PID作为备用
            if not title:
                title = f"题目 {pid}"

            submission_req = json.dumps([
                {"name": "answer", "type": "source code", "file_name": "answer.code"}
            ], ensure_ascii=False)

            # 构建statement_md（直接使用statement列，并替换##为###）
            statement_md = build_statement_md(row)

            records.append({
                'pid': pid,
                'title': title,
                'submission_req': submission_req,
                'statement_md': statement_md
            })

    with open(output_sql_file, 'w', encoding='utf-8') as f:
        f.write("START TRANSACTION;\n\n")

        for i, rec in enumerate(records, start=1):
            f.write(f"-- 题目 {i}: PID = {rec['pid']}, 标题 = {rec['title']}\n")
            f.write(
                f"INSERT INTO problems (title, submission_requirement) VALUES ('{escape_sql_string(rec['title'])}', '{escape_sql_string(rec['submission_req'])}');\n")
            f.write("SET @last_id = LAST_INSERT_ID();\n")
            f.write(
                f"INSERT INTO problems_contents (id, statement, statement_md) VALUES (@last_id, '', '{escape_sql_string(rec['statement_md'])}');\n\n")

        f.write("COMMIT;\n")

    print(f"✅ SQL已生成到 {output_sql_file}")
    print(f"共处理 {len(records)} 道题")


if __name__ == '__main__':
    import os
    import glob

    # 如果没有指定CSV文件，就找最新的 contest_problems.csv
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_files = glob.glob('contest_problems.csv')
        if not csv_files:
            csv_files = glob.glob('hdu_contest_*.csv')

        if csv_files:
            csv_file = csv_files[-1]  # 取最新的
            print(f"自动选择CSV文件: {csv_file}")
        else:
            csv_file = input("请输入CSV文件名: ").strip()

    if os.path.exists(csv_file):
        output_sql = csv_file.replace('.csv', '.sql')
        generate_sql(csv_file, output_sql)
    else:
        print(f"❌ 未找到文件: {csv_file}")