# 1. 회원 관련 상수

MAX_NAME_LENGTH = 20                    # 회원 이름 최대 길이
MIN_NAME_LENGTH = 2                     # 회원 이름 최소 길이
PASSWORD_MIN_LENGTH = 8                 # 비밀번호 최소 길이
PASSWORD_MIN_LENGTH = 20                # 비밀번호 최대 길이
MAX_LOGIN_FAIL = 5                      # 최대 로그인 실패 횟수
# 비밀번호는 최소 8자 이상, 이름은 2~20자 사이로 제한합니다.

# 2. 계좌 관련
MAX_ACCOUNT_COUNT = 3                   # 최대 계좌 보유 개수
ACCOUNT_NUMBER_LENGTH = 14              # 계좌 번호 길이
MIN_BALANCE = 0                         # 최소 잔액
DAILY_WITHDRAW_LIMIT = 1000000          # 일일 출금 한도 (원)
MIN_TRANSACTION_AMOUNT = 1000           # 최소 거래 금액 (원)
DEFAULT_BANK = '기본 은행명'              # 기본 은행명
# 거래는 최소 1,000원부터 가능하며, 하루 출금 한도는 100만원입니다.

# 3. 거래 관련
DEPOSIT = 'deposit'                     # 입금
WITHDRAW = 'withdraw'                   # 출금
TRANSFER = 'transfer'                   # 계좌 이체
# 3-1 거래 상태
SUCCESS = 'success'                     # 이체,입금,출금 성공
FAIL = 'fail'                           # 이체,입금,출금 실패
# 거래 타입과 상태는 문자열로 관리합니다.

# 4. 메모 관련
MAX_MEMO_COUNT = 100                    # 최대 메모 개수
MAX_MEMO_TITLE_LENGTH = 30              # 메모 제목 최대 길이
MAX_MEMO_LENGTH = 1000                  # 메모 내용 최대 길이
# 메모는 최대 100개까지, 제목은 30자, 내용은 1,000자까지 가능합니다.

# 5. 할 일(Todo) 관련
MAX_MUST_COUNT = 50                     # 최대 할 일 개수
MAX_MUST_TITLE_LENGTH = 30              # 할 일 제목 최대 길이
MAX_MUST_LENGTH = 500                   # 할 일 내용 최대 길이
DEFAULT_DUE_DAYS = 0                    # 기본 마감일 (당일)
# 5-1 할 일 상태
MUST_COMPLETE = True                    # 할 일 완료
MUST_INCOMPLETE = False                 # 할 일 미완료
# 5-2 우선순위
PRIORITY_HIGH = 'high'                  # 높음
PRIORITY_MEDIUM = 'medium'              # 보통
PRIORITY_LOW = 'low'                    # 낮음