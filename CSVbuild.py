import requests
from bs4 import BeautifulSoup
import csv
import time
import sys


def main():
    # 从命令行参数获取 cid，如果没有则使用默认值 1150
    if len(sys.argv) > 1:
        cid = sys.argv[1]
    else:
        cid = input("请输入比赛ID (cid): ").strip()
        if not cid:
            print("使用默认 cid=1150")
            cid = 1150
        else:
            cid = int(cid)

    start_pid = 1001
    end_pid = 1010

    # 您的Cookie
    COOKIE_STRING = "PHPSESSID=dnhfiba277514senne267j7e8h; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaWQiOjExNTAsImlkIjoxMzQ0LCJuYW1lIjoidGVhbTEzNDQiLCJleHAiOjE3Nzk3ODczMzguODI4ODY4fQ.Wvk82t6ShtpQbmXcAJ2yZNlzuZ2CP-VmUI3P4oBxqWE"

    session = requests.Session()

    # 设置Cookie
    for cookie in COOKIE_STRING.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            session.cookies.set(name, value)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://acm.hdu.edu.cn/contest/contest_show.php?cid={cid}',
    }

    results = []

    for pid in range(start_pid, end_pid + 1):
        url = f"https://acm.hdu.edu.cn/contest/problem?cid={cid}&pid={pid}"
        print(f"\n正在爬取 cid={cid}, pid={pid} ...")

        try:
            resp = session.get(url, headers=headers, timeout=10)
            resp.encoding = 'utf-8'

            if 'Contest Login' in resp.text:
                print("  ❌ Cookie已过期")
                break

            soup = BeautifulSoup(resp.text, 'html.parser')

            # 提取标题和编号
            title_h2 = soup.find('h2', class_='problem-print-title')
            if title_h2:
                title_text = title_h2.get_text(strip=True)
                parts = title_text.split(' ', 1)
                pid_value = parts[0]
                title_value = parts[1] if len(parts) > 1 else ''
            else:
                pid_value = str(pid)
                title_value = ''

            problem_data = {
                'pid': pid_value,
                'title': title_value
            }

            blocks = soup.find_all('div', class_='problem-detail-block')

            for block in blocks:
                label_div = block.find('div', class_='problem-detail-label')
                if not label_div:
                    continue

                label_text = label_div.get_text(strip=True)
                value_div = block.find('div', class_='problem-detail-value')

                if not value_div:
                    continue

                content = value_div.get_text(separator='\n', strip=True)

                if label_text == 'Problem Description':
                    problem_data['description'] = content
                elif label_text == 'Input':
                    problem_data['input'] = content
                elif label_text == 'Output':
                    problem_data['output'] = content
                elif label_text == 'Sample Input':
                    problem_data['sample_input'] = content
                elif label_text == 'Sample Output':
                    problem_data['sample_output'] = content
                elif label_text == 'Hint':
                    problem_data['hint'] = content

            default_fields = ['description', 'input', 'output', 'sample_input', 'sample_output', 'hint']
            for field in default_fields:
                if field not in problem_data:
                    problem_data[field] = ''

            results.append(problem_data)
            print(f"  ✅ 成功: PID={pid_value}, 标题={title_value}")

        except Exception as e:
            print(f"  ❌ 异常: {e}")
            results.append({
                'pid': str(pid), 'title': '', 'description': '', 'input': '',
                'output': '', 'sample_input': '', 'sample_output': '', 'hint': ''
            })

        time.sleep(1)

    if results:
        filename = f'hdu_contest_{cid}.csv'
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['pid', 'title', 'description', 'input', 'output',
                          'sample_input', 'sample_output', 'hint']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\n🎉 完成！共获取 {len(results)} 道题，已保存到 {filename}")
    else:
        print("❌ 没有获取到任何数据")


if __name__ == '__main__':
    main()