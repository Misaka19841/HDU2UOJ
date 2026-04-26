import requests
import os
import time


def main():
    # 配置信息
    TOKEN = "Pui7quK6g2cbx1qnJVIBxqppeOqTf1B8euviWSi3IrygAz3wsm4YZyzwOzfG"
    BASE_URL = "http://dut-cpc.cn"

    # 题目 ID 范围
    start_id = 73
    end_id = 82

    # 数据文件目录（存放 1.zip ~ 10.zip）
    data_dir = "./Compressed"  # 请修改为实际的 zip 文件目录

    # Cookie
    COOKIE_STRING = "pma_lang=zh_CN; UOJSESSID=atj30vb4a1809gmv1b948f3sok; uoj_username=admin; uoj_username_checksum=286c66fbce991b3b9331d75885c80738; uoj_remember_token=epBkl4u3Kepe0BdA8FULr3NHpZSf2SsZbjrz1QqCKk8pn1QLg0cXAXzSl60Z; uoj_remember_token_checksum=e03b4eef7d53d572bcd75fe4cab7d34d; phpMyAdmin=t75b761h8nqclt2ed3bilvfkjn; pmaUser-1=dcQYt0q6lOgRInPWUfJJ3ZM72ZzBfyY4hkRKuvAWNPNH2pfwVGli5chuMHE%3D"

    # 创建 session
    session = requests.Session()

    # 设置 Cookie
    for cookie in COOKIE_STRING.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            session.cookies.set(name, value)

    # 逐个上传 zip 包
    print(f"开始上传测试数据，ID 范围: {start_id} ~ {end_id}\n")

    for idx, problem_id in enumerate(range(start_id, end_id + 1), start=1):
        zip_file = os.path.join(data_dir, f"{idx}.zip")

        if not os.path.exists(zip_file):
            print(f"⚠️ 题目 {problem_id}: 文件不存在 {zip_file}，跳过")
            continue

        print(f"正在上传题目 {problem_id} 的数据 ({zip_file})...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
            'Origin': BASE_URL,
            'Referer': f'{BASE_URL}/problem/{problem_id}/manage/data',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        # 构建 multipart/form-data 请求
        with open(zip_file, 'rb') as f:
            files = {
                'problem_data_file': (f"{idx}.zip", f, 'application/x-zip-compressed'),
                'problem_data_file_submit': (None, 'submit')
            }
            data = {
                '_token': TOKEN
            }

            try:
                url = f"{BASE_URL}/problem/{problem_id}/manage/data"
                resp = session.post(url, headers=headers, files=files, data=data)

                if resp.status_code == 200:
                    # 检查响应
                    if 'success' in resp.text.lower() or '成功' in resp.text:
                        print(f"  ✅ 上传成功")
                    else:
                        print(f"  ⚠️ 响应: {resp.text[:100]}")
                else:
                    print(f"  ❌ HTTP {resp.status_code}")

            except Exception as e:
                print(f"  ❌ 异常: {e}")

        time.sleep(1)

    print("\n🎉 上传完成！")


if __name__ == '__main__':
    main()