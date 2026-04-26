import requests
import time
import urllib.parse


def main():
    # 配置信息
    TOKEN = "7A6tvPpacVu5NpwLQ4chUE2VYmKmRagqPLCsJF84NWo31DtM6IwaDVnGu4wq"  # 使用新的 token
    BASE_URL = "http://dut-cpc.cn"

    # 题目 ID 范围
    start_id = 83
    end_id = 95

    # 重置类型（normal 或其他）
    reset_type = "normal"

    # Cookie（从您提供的请求中复制最新的）
    COOKIE_STRING = "pma_lang=zh_CN; uoj_username=admin; uoj_username_checksum=286c66fbce991b3b9331d75885c80738; uoj_remember_token=epBkl4u3Kepe0BdA8FULr3NHpZSf2SsZbjrz1QqCKk8pn1QLg0cXAXzSl60Z; uoj_remember_token_checksum=e03b4eef7d53d572bcd75fe4cab7d34d; uoj_preferred_language=C%2B%2B14; UOJSESSID=shrdjbb4044a3hofphnnjaj2c9; phpMyAdmin=tnnp3fnaqub6dgp804qugrmc6o; pmaUser-1=PU3nNSwt%2B0v0uyncSVfswk4tp3n7OcKZ65ul%2BXwyEt3ynr0obQr9NHuO%2BJI%3D; pmaAuth-1=qPXQgI2baggQXY7haSXf4o1ZcdiEGzA4qwcsZ6dc86GJ5zkJjw3Sw0FpC4e1alYotzlUNZm4oLiWOp55MxJFMOur%2F%2F6CKvOkBVao4ZH0ZL314WEy3EI9"

    # 创建 session
    session = requests.Session()

    # 设置 Cookie
    for cookie in COOKIE_STRING.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            session.cookies.set(name, value)

    # 读取 CSV 获取题目原标题
    import csv
    csv_file = "contest_problems.csv"
    titles = {}
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=start_id):
            titles[idx] = row.get('title', '').strip()

    # 逐个重置题目
    print(f"开始重置题目，ID 范围: {start_id} ~ {end_id}\n")

    for problem_id in range(start_id, end_id + 1):
        title = titles.get(problem_id, f"题目{problem_id}")
        print(f"正在重置题目 {problem_id}: {title}...")

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': BASE_URL,
            'Referer': f'{BASE_URL}/problem/{problem_id}/manage/data/reset',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        # 构建 POST 数据
        data = {
            '_token': TOKEN,
            'title': title,
            'type': reset_type,
            'submit-init_problem': 'init_problem'
        }

        try:
            url = f"{BASE_URL}/problem/{problem_id}/manage/data/reset"
            resp = session.post(url, headers=headers, data=data)

            if resp.status_code == 200:
                if 'success' in resp.text.lower() or '成功' in resp.text or resp.text.strip() == '':
                    print(f"  ✅ 重置成功")
                else:
                    print(f"  ⚠️ 响应: {resp.text[:100]}")
            else:
                print(f"  ❌ HTTP {resp.status_code}")

        except Exception as e:
            print(f"  ❌ 异常: {e}")

        time.sleep(0.5)

    print("\n🎉 重置完成！")


if __name__ == '__main__':
    main()