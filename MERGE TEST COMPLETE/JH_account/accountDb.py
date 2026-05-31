import json
from config import config

accounts = {}

# [수정 전] config.DB_FILE을 바라보게 되어 회원 정보 데이터 파일을 통째로 날려버릴 위험이 존재했음
# [수정 후] 종호 파트 고유의 config.ACCOUNT_DB_FILE을 참조하여 열고 저장하도록 수정함
# [왜 이렇게 해야 하는가] 종호의 계좌 데이터가 격리된 'account.json' 파일에만 안전하게 쓰이도록 보장하기 위함
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

# [수정 전] 입금 시 거래 내역(history) 리스트 구조가 정의되지 않아 경선의 내역 기능 실행 시 KeyError 크래시가 발생했음
# [수정 후] 'history' 키 존재 여부를 체크하여 없으면 빈 리스트를 생성하는 안전 방어 코드를 추가함
# [왜 이렇게 해야 하는가] 경선의 대전뱅크 이체/내역 기능이 종호의 데이터 창고 구조 위에서 깨지지 않고 상호 연동되게 하기 위함
def deposit(acc_num, money):
    if acc_num in accounts:
        accounts[acc_num]['balance'] += money
        if 'history' not in accounts[acc_num]:
            accounts[acc_num]['history'] = []
        save_db()
        return True
    return False

# [수정 전] 출금 로직에 거래(이체) 내역을 담을 리스트 연동 구조가 누락되어 있었음
# [수정 후] 'history' 리스트 구조 방어 확인 코드를 똑같이 배치함
# [왜 이렇게 해야 하는가] 이체나 출금 로그 기록 시 공용 데이터 저장 포맷의 정합성과 일관성을 유지하기 위함
def withdraw(acc_num, money):
    if acc_num in accounts and accounts[acc_num]['balance'] >= money:
        accounts[acc_num]['balance'] -= money
        if 'history' not in accounts[acc_num]:
            accounts[acc_num]['history'] = []
        save_db()
        return True
    return False