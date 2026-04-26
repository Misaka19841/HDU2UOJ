import requests
import os
import time
from pathlib import Path


def main():
    # 配置信息
    TOKEN = "Pui7quK6g2cbx1qnJVIBxqppeOqTf1B8euviWSi3IrygAz3wsm4YZyzwOzfG"
    BASE_URL = "http://dut-cpc.cn"

    # 题目 ID 范围
    start_id = 83
    end_id = 95

    # 数据文件目录（存放 206.zip, 207.zip 等）
    data_dir = Path("./Compressed")

    # Cookie
    COOKIE_STRING = "pma_lang=zh_CN; UOJSESSID=atj30vb4a1809gmv1b948f3sok; uoj_username=admin; uoj_username_checksum=286c66fbce991b3b9331d75885c80738; uoj_remember_token=epBkl4u3Kepe0BdA8FULr3NHpZSf2SsZbjrz1QqCKk8pn1QLg0cXAXzSl60Z; uoj_remember_token_checksum=e03b4eef7d53d572bcd75fe4cab7d34d; phpMyAdmin=t75b761h8nqclt2ed3bilvfkjn; pmaUser-1=dcQYt0q6lOgRInPWUfJJ3ZM72ZzBfyY4hkRKuvAWNPNH2pfwVGli5chuMHE%3D"

    # 创建 session
    session = requests.Session()

    # 设置 Cookie
    for cookie in COOKIE_STRING.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            session.cookies.set(name, value)

    # 获取所有 zip 文件并按数字排序
    zip_files = []
    for zip_file in data_dir.glob("*.zip"):
        # 提取文件名中的数字（如 206.zip -> 206）
        try:
            num = int(zip_file.stem)
            zip_files.append((num, zip_file))
        except ValueError:
            print(f"⚠️ 跳过非数字命名的文件: {zip_file.name}")
            continue

    if not zip_files:
        print(f"❌ 在 {data_dir} 中没有找到有效的 zip 文件")
        return

    # 按数字排序
    zip_files.sort(key=lambda x: x[0])

    # 检查数量是否匹配
    expected_count = end_id - start_id + 1
    if len(zip_files) != expected_count:
        print(f"⚠️ 警告: 找到 {len(zip_files)} 个 zip 文件，但题目范围需要 {expected_count} 个")

    print(f"找到 {len(zip_files)} 个 zip 文件，将按顺序上传到题目 {start_id} ~ {end_id}")
    for idx, (num, zip_file) in enumerate(zip_files, start=1):
        print(f"  {idx}. {zip_file.name} (原始编号: {num}) -> 题目ID: {start_id + idx - 1}")

    print(f"\n开始上传测试数据...\n")

    for idx, (original_num, zip_file) in enumerate(zip_files, start=1):
        problem_id = start_id + idx - 1

        print(f"[{idx}/{len(zip_files)}] 正在上传 {zip_file.name} 到题目 {problem_id}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
            'Origin': BASE_URL,
            'Referer': f'{BASE_URL}/problem/{problem_id}/manage/data',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        with open(zip_file, 'rb') as f:
            files = {
                'problem_data_file': (zip_file.name, f, 'application/x-zip-compressed'),
                'problem_data_file_submit': (None, 'submit')
            }
            data = {
                '_token': TOKEN
            }

            try:
                url = f"{BASE_URL}/problem/{problem_id}/manage/data"
                resp = session.post(url, headers=headers, files=files, data=data)

                if resp.status_code == 200:
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