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
    PROBLEM_TAGS = "校赛"
    # 解码后的中文：hdu春季联赛，2025

    # Cookie（从您提供的请求中复制）
    COOKIE_STRING = "pma_lang=zh_CN; UOJSESSID=atj30vb4a1809gmv1b948f3sok; phpMyAdmin=gf6qk6qon12c2bh0atu3vumsq5; uoj_username=admin; uoj_username_checksum=286c66fbce991b3b9331d75885c80738; uoj_remember_token=epBkl4u3Kepe0BdA8FULr3NHpZSf2SsZbjrz1QqCKk8pn1QLg0cXAXzSl60Z; uoj_remember_token_checksum=e03b4eef7d53d572bcd75fe4cab7d34d; pmaUser-1=giM2%2BhzfHmCI2%2FMBCv8u5Nnjcuis33Q4%2Bg0kUW0GTlD8WxNhTnCj60Q24JY%3D; pmaAuth-1=n39OghUq0i6cXJXtCA56kt5Y1CS1NW%2BMTQwYqnqBKBGOpgpKdQbIQKjIcIz7zt8xbDCzL2vg4LdTNyxCOBU0zbOxoLdzUOxveyfsI2Ruu%2BzQEiCD1j15"

    # 读取 CSV 文件
    csv_file = "contest_problems.csv"  # 使用从raw目录生成的CSV文件
    problems = []

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 读取statement并替换 ## 为 ###
            statement = row.get('statement', '').strip()
            statement = statement.replace('##', '###')

            problems.append({
                'pid': row.get('pid', ''),
                'title': row.get('title', '').strip(),
                'statement': statement  # 使用处理后的statement
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

        print(f"正在提交题目 {problem_id}: PID={problem['pid']}, 标题={problem['title']}...")

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
            'problem_tags': PROBLEM_TAGS,
            'problem_content_md': problem['statement'],  # 使用已替换##为###的statement
            'problem_is_hidden': 'on',
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


if __name__ == '__main__':
    main()