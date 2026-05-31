# ==========================================================
# config/config.py
# 역할: 프로그램 전체에서 쓰는 상수값 모음
# ==========================================================

# ----------------수경-------------------------------------
DB_FILE = "user_db.json"

MSG = {
    "SUCCESS": "요청하신 작업이 완료되었습니다.",
    "FAIL_AUTH": "아이디 또는 비밀번호가 일치하지 않습니다.",
    "EXIST_ID": "이미 존재하는 아이디입니다.",
    "NO_ACCOUNT": "등록된 계좌가 없습니다. 먼저 계좌를 생성해 주세요.",
    "LOW_BALANCE": "잔액이 부족하여 작업을 진행할 수 없습니다."
}

BANK_CONFIG = {
    "MIN_TRANSFER": 1,
    "MAX_TRANSFER": 1000000,
    "INITIAL_BALANCE": 0
}

# ----------------태경-------------------------------------
CREATENEWACCOUNT = 1
BACKTOMAINMENU   = 0

# ----------------경선-------------------------------------
DAEJEON_DB_FILE = "daejeon_bank.json"

DAEJEON_MSG = {
    "FAIL_AUTH": "아이디 또는 비밀번호가 일치하지 않습니다.",
    "NOT_FOUND": "대상을 찾을 수 없거나 정보가 없습니다.",
    "SUCCESS": "처리가 완료되었습니다.",
    "LACK_BALANCE": "잔액이 부족합니다."
}

# ----------------종호-------------------------------------
# [수정 전] ACCOUNT_DB_FILE 상수가 없어 다른 조원의 파일 경로와 충돌할 위험이 있었음
# [수정 후] 종호 파트 고유의 계좌 데이터 파일명을 상수로 명확히 정의함
# [왜 이렇게 해야 하는가] 계좌 보관 창고가 다른 조원의 데이터 파일(user_db.json 등)을 덮어쓰는 구조적 결함을 방지하기 위함
ACCOUNT_DB_FILE = 'account.json'

LOGIN_USER    = 'kim'
MENU_DEPOSIT  = '1'
MENU_WITHDRAW = '2'

# 1. 회원 관련 상수
MAX_NAME_LENGTH     = 20
MIN_NAME_LENGTH     = 2
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 20
MAX_LOGIN_FAIL      = 5

# 2. 계좌 관련
MAX_ACCOUNT_COUNT      = 3
ACCOUNT_NUMBER_LENGTH  = 14
MIN_BALANCE            = 0
DAILY_WITHDRAW_LIMIT   = 1000000
MIN_TRANSACTION_AMOUNT = 1000
DEFAULT_BANK           = '기본 은행명'

# 3. 거래 관련
DEPOSIT  = 'deposit'
WITHDRAW = 'withdraw'
TRANSFER = 'transfer'

SUCCESS = 'success'
FAIL    = 'fail'

# 4. 메모 관련
MAX_MEMO_COUNT        = 100
MAX_MEMO_TITLE_LENGTH = 30
MAX_MEMO_LENGTH       = 1000

# 5. 할일 관련
MAX_MUST_COUNT        = 50
MAX_MUST_TITLE_LENGTH = 30
MAX_MUST_LENGTH       = 500
DEFAULT_DUE_DAYS      = 0

MUST_COMPLETE   = True
MUST_INCOMPLETE = False

PRIORITY_HIGH   = 'high'
PRIORITY_MEDIUM = 'medium'
PRIORITY_LOW    = 'low'

# ----------------메뉴 상수 (신규 추가)-------------------------------------
SIGN_UP = '1'
SIGN_IN = '2'
FIND_ID = '3'
FIND_PW = '4'
EXIT    = '0'

# 로그인 후 메인 메뉴
MANAGEMENT_ACCOUNT = '1'
MANAGEMENT_MEMO    = '2'
MANAGEMENT_MUST    = '3'
USER_INFO          = '4'
SIGN_OUT           = '5'

# [수정 전] 경선의 대전뱅크 메뉴 번호가 상수로 등록되지 않아 숫자가 직접 하드코딩되어 있었음
# [수정 후] 대전뱅크(ks_bank) 내부 전용 메뉴 상수를 등록함
# [왜 이렇게 해야 하는가] 메뉴 번호 변경 요건 발생 시 이 파일 한 곳만 수정하면 전체 모듈에 자동 반영되도록 관리하기 위함
BANK_TRANSFER = '1'
BANK_HISTORY  = '2'
BANK_EXIT     = '3'

# 메모 서브 메뉴
MEMO_READ   = '1'
MEMO_WRITE  = '2'
MEMO_UPDATE = '3'
MEMO_DELETE = '4'

# 할일 서브 메뉴
MUST_READ            = '1'
MUST_WRITE           = '2'
MUST_UPDATE          = '3'
MUST_DELETE          = '4'
MUST_COMPLETE_TOGGLE = '5'

# 공통
BACK = '0'