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
    desc = clean_description(row.get('description', ''))
    input_text = row.get('input', '')
    output_text = row.get('output', '')
    sample_input = row.get('sample_input', '')
    sample_output = row.get('sample_output', '')
    hint = row.get('hint', '')

    md_parts = []

    md_parts.append("### 题目背景")
    md_parts.append(desc if desc else "（无）")
    md_parts.append("")

    md_parts.append("### 输入格式")
    md_parts.append(input_text if input_text else "（无）")
    md_parts.append("")

    md_parts.append("### 输出格式")
    md_parts.append(output_text if output_text else "（无）")
    md_parts.append("")

    md_parts.append("### 输入输出样例")

    md_parts.append("#### 输入")
    if sample_input and sample_input.strip():
        md_parts.append("```")
        md_parts.append(sample_input)
        md_parts.append("```")
    else:
        md_parts.append("（无）")
    md_parts.append("")

    md_parts.append("#### 输出")
    if sample_output and sample_output.strip():
        md_parts.append("```")
        md_parts.append(sample_output)
        md_parts.append("```")
    else:
        md_parts.append("（无）")
    md_parts.append("")

    if hint and hint.strip():
        md_parts.append("### 提示")
        md_parts.append(hint)

    return '\n'.join(md_parts)


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
            if not title:
                desc_first = row.get('description', '').split('\n')[0].strip()
                title = re.sub(r'^\*\*|\*\*$', '', desc_first)

            submission_req = json.dumps([
                {"name": "answer", "type": "source code", "file_name": "answer.code"}
            ], ensure_ascii=False)

            statement_md = build_statement_md(row)

            records.append({
                'pid': row.get('pid', ''),
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
                f"INSERT INTO problems_contents (id, statement, statement_md) VALUES (@last_id, '', '{escape_sql_string(rec['statement_md'])}');\n")
            f.write("\n")

        f.write("COMMIT;\n")

    print(f"✅ SQL已生成到 {output_sql_file}")
    print(f"共处理 {len(records)} 道题")


if __name__ == '__main__':
    import os

    # 如果没有指定CSV文件，就找最新的 hdu_contest_*.csv
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        import glob

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