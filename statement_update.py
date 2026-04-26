import requests
import csv
import time
import urllib.parse


def main():
    # 配置信息
    TOKEN = "Pui7quK6g2cbx1qnJVIBxqppeOqTf1B8euviWSi3IrygAz3wsm4YZyzwOzfG"  # 固定 token
    BASE_URL = "http://dut-cpc.cn"

    # 题目 ID 范围（SQL 导入后得到的实际 ID）
    start_id = 83  # 请根据实际情况修改
    end_id = 95  # 请根据实际情况修改

    # 固定的 tags（URL 编码后的值）
    PROBLEM_TAGS = "hdu春季联赛,2025"
    # 解码后的中文：hdu春季联赛，2025

    # Cookie（从您提供的请求中复制）
    COOKIE_STRING = "pma_lang=zh_CN; UOJSESSID=atj30vb4a1809gmv1b948f3sok; phpMyAdmin=gf6qk6qon12c2bh0atu3vumsq5; uoj_username=admin; uoj_username_checksum=286c66fbce991b3b9331d75885c80738; uoj_remember_token=epBkl4u3Kepe0BdA8FULr3NHpZSf2SsZbjrz1QqCKk8pn1QLg0cXAXzSl60Z; uoj_remember_token_checksum=e03b4eef7d53d572bcd75fe4cab7d34d; pmaUser-1=giM2%2BhzfHmCI2%2FMBCv8u5Nnjcuis33Q4%2Bg0kUW0GTlD8WxNhTnCj60Q24JY%3D; pmaAuth-1=n39OghUq0i6cXJXtCA56kt5Y1CS1NW%2BMTQwYqnqBKBGOpgpKdQbIQKjIcIz7zt8xbDCzL2vg4LdTNyxCOBU0zbOxoLdzUOxveyfsI2Ruu%2BzQEiCD1j15"

    # 读取 CSV 文件
    csv_file = "hdu_contest_1150.csv"  # 根据实际文件名修改
    problems = []

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            problems.append({
                'title': row.get('title', '').strip(),
                'statement_md': build_statement_md(row)
            })

    # 创建 session 并设置 Cookie
    session = requests.Session()

    # 解析并设置 Cookie
    for cookie in COOKIE_STRING.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            session.cookies.set(name, value)

    # 逐个提交题目
    print(f"开始提交题目，ID 范围: {start_id} ~ {end_id}")
    print(f"共 {len(problems)} 道题\n")

    for idx, problem in enumerate(problems):
        problem_id = start_id + idx
        if problem_id > end_id:
            print(f"⚠️ 题目数量超过 ID 范围，停止提交")
            break

        print(f"正在提交题目 {problem_id}: {problem['title']}...")

        # 动态设置 headers
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': BASE_URL,
            'Referer': f'{BASE_URL}/problem/{problem_id}/manage/statement',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }

        # 构建 POST 数据
        data = {
            '_token': TOKEN,
            'problem_title': problem['title'],
            'problem_tags': PROBLEM_TAGS,  # 使用固定的 tags

            'problem_content_md': problem['statement_md'],
            'problem_is_hidden': 'on',  # 勾选隐藏
            'save-problem': ''
        }

        try:
            url = f"{BASE_URL}/problem/{problem_id}/manage/statement"
            resp = session.post(url, headers=headers, data=data)

            if resp.status_code == 200:
                if 'success' in resp.text.lower() or resp.text.strip() == '':
                    print(f"  ✅ 成功")
                else:
                    print(f"  ⚠️ 响应: {resp.text[:100]}")
            else:
                print(f"  ❌ HTTP {resp.status_code}")

        except Exception as e:
            print(f"  ❌ 异常: {e}")

        time.sleep(1)

    print("\n🎉 提交完成！")


def build_statement_md(row):
    """从 CSV 行构建 statement_md"""
    import re

    def clean_description(desc):
        if desc:
            desc = re.sub(r'\*\*注：请到 Clarifications 中查看公告！\*\*\n\n?', '', desc)
            desc = re.sub(r'注：请到 Clarifications 中查看公告！\n\n?', '', desc)
            desc = desc.strip()
        return desc

    desc = clean_description(row.get('description', ''))
    input_text = row.get('input', '')
    output_text = row.get('output', '')
    sample_input = row.get('sample_input', '')
    sample_output = row.get('sample_output', '')
    hint = row.get('hint', '')

    md_parts = []

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


if __name__ == '__main__':
    main()