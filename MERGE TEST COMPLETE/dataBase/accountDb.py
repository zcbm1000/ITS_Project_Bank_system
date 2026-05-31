# ==========================================================
# dataBase/accountDb.py
# 역할: 계좌 데이터를 파일(json)과 메모리에 보관하는 창고
# ==========================================================

import json
from config import config

accounts = {}

# [수정 전] config.DB_FILE을 참조하여 수경의 user_db.json 파일을 덮어쓰는 위험이 있었음
# [수정 후] 종호가 정의한 고유 파일 상수인 config.ACCOUNT_DB_FILE을 사용하도록 변경함
# [왜 이렇게 해야 하는가] 회원 정보 파일과 계좌 정보 파일이 서로 분리되어 온전히 저장되도록 격리하기 위함
def save_db():
    with open(config.ACCOUNT_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

def load_db():
    global accounts
    try:
        with open(config.ACCOUNT_DB_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                accounts = json.loads(content)
    except FileNotFoundError:
        accounts = {}
    except json.JSONDecodeError:
        accounts = {}

def get_balance(acc_num):
    if acc_num in accounts:
        return accounts[acc_num]['balance']
    return None

# [수정 전] 입금 처리 시 거래 내역 리스트(history)가 누락되어 이체 내역 조회가 불가능했음
# [수정 후] 입금 발생 시 'history' 키가 없으면 빈 리스트를 생성하도록 안전 코드를 추가함
# [왜 이렇게 해야 하는가] 경선의 대전뱅크 이체 내역 기능과 연동 시 데이터 구조 깨짐을 방지하기 위함
def deposit(acc_num, money):
    if acc_num in accounts:
        accounts[acc_num]['balance'] += money
        if 'history' not in accounts[acc_num]:
            accounts[acc_num]['history'] = []
        save_db()
        return True
    return False

# [수정 전] 출금 처리 시 거래 내역 리스트(history) 누락 버그 발생 위험
# [수정 후] 'history' 키 생성 제어 방어 코드를 적용함
# [왜 이렇게 해야 하는가] 경선의 이체 로직이 종호의 계좌 DB 구조 위에서 에러 없이 정합성을 유지하도록 매핑하기 위함
def withdraw(acc_num, money):
    if acc_num in accounts and accounts[acc_num]['balance'] >= money:
        accounts[acc_num]['balance'] -= money
        if 'history' not in accounts[acc_num]:
            accounts[acc_num]['history'] = []
        save_db()
        return True
    return False