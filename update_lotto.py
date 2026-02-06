import requests
import json
import os

DATA_FILE = 'data.json'

def get_latest_draw_no():
    # 대략적인 시작일로부터 현재 회차 계산 가능 (생략)
    # 여기서는 기존 데이터의 마지막 회차 + 1부터 시도
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data[0]['drwNo'] + 1
    return 1100 # 시작 회차 설정

def update():
    draw_no = get_latest_draw_no()
    new_data = []
    
    while True:
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={draw_no}"
        resp = requests.get(url).json()
        
        if resp.get('returnValue') == 'fail':
            break
            
        numbers = [resp[f'drwtNo{i}'] for i in range(1, 7)]
        new_data.insert(0, {"drwNo": draw_no, "numbers": numbers, "date": resp['drwNoDate']})
        draw_no += 1

    if new_data:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                old_data = json.load(f)
                new_data.extend(old_data)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
