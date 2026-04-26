import requests
import time


def main():
    # 配置信息
    TOKEN = "Pui7quK6g2cbx1qnJVIBxqppeOqTf1B8euviWSi3IrygAz3wsm4YZyzwOzfG"
    BASE_URL = "http://dut-cpc.cn"

    # 题目 ID 范围
    start_id = 73
    end_id = 82

    # Cookie
    COOKIE_STRING = "pma_lang=zh_CN; UOJSESSID=atj30vb4a1809gmv1b948f3sok; uoj_username=admin; uoj_username_checksum=286c66fbce991b3b9331d75885c80738; uoj_remember_token=epBkl4u3Kepe0BdA8FULr3NHpZSf2SsZbjrz1QqCKk8pn1QLg0cXAXzSl60Z; uoj_remember_token_checksum=e03b4eef7d53d572bcd75fe4cab7d34d; phpMyAdmin=t75b761h8nqclt2ed3bilvfkjn; pmaUser-1=PAGsIu721BLGDcC8dN4NUEUcUsjclF2TuMQ0qPrj5PDvbnKG8PaJh7nfUOo%3D; pmaAuth-1=tRfChl%2FDfopQfU4MGVEQhHgF391vI3EXqza2BrpIkkT4CKnbIR%2FinUGEJxaIRPIC3yhurHuieQH1wXB7josWGE7x8k4RXBeze%2FxGLvltv6peBCiJK54m"

    # 创建 session
    session = requests.Session()

    # 设置 Cookie
    for cookie in COOKIE_STRING.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            session.cookies.set(name, value)

    # 逐个发送信号
    print(f"开始发送数据导入信号，ID 范围: {start_id} ~ {end_id}\n")

    for problem_id in range(start_id, end_id + 1):
        print(f"正在处理题目 {problem_id}...")

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': BASE_URL,
            'Referer': f'{BASE_URL}/problem/{problem_id}/manage/data',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        data = {
            '_token': TOKEN,
            'submit-data': 'data'
        }

        try:
            url = f"{BASE_URL}/problem/{problem_id}/manage/data"
            resp = session.post(url, headers=headers, data=data)

            if resp.status_code == 200:
                print(f"  ✅ 信号已发送")
            else:
                print(f"  ❌ HTTP {resp.status_code}")

        except Exception as e:
            print(f"  ❌ 异常: {e}")

        time.sleep(0.5)

    print("\n🎉 全部完成！")


if __name__ == '__main__':
    main()