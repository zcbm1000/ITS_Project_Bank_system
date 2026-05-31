from config import config
from dataBase import accountDb

from JH_account.accountMenu import activeAccountMenu

def accountMenu(cur_u):
    """메인 메뉴로부터 로그인한 유저 객체를 전달받아 계좌 관리를 수행합니다."""
    while True:
        print("\n=== 계좌 관리 메뉴 ===")
        print("1. 신규 계좌 생성")
        print("0. 메인 화면으로 돌아가기")

        # 사용자가 숫자가 아닌 문자를 입력했을 때 튕기는 현상을 방지하기 위해 예외처리 추가
        try:
            choice = int(input("번호를 선택하세요: "))
        except ValueError:
            print("숫자만 입력 가능합니다.")
            continue

        if choice == config.CREATENEWACCOUNT:
            # 계좌 생성 함수에도 현재 유저 정보를 전달합니다.
            createAccount(cur_u)

            return  # 계좌 생성이 끝나면 메인 메뉴로 돌아가도록 함  

        elif choice == config.BACKTOMAINMENU:
            print("메인 메뉴로 돌아갑니다.")
            break
        else:
            print("올바른 번호를 선택해주세요.")


def createAccount(cur_u):
    """현재 로그인한 사용자에게 새로운 13자리 계좌를 발급하고 동기화합니다."""
    
    # 이미 계좌를 보유하고 있는 경우 추가 생성을 막음
    if cur_u.userAccount is not None:
        print(f"\n오류: 이미 등록된 계좌가 존재합니다. (계좌번호: {cur_u.userAccount})")
        return

    while True:
        account = input("사용할 계좌 번호(13자리)를 입력하세요: ").strip()

        if len(account) != 13:
            print("입력하신 계좌 번호는 13자리가 아닙니다.")
            continue

        if account in accountDb.accounts:
            print("이미 존재하는 계좌 번호입니다.")
            continue

        # 1. 전역 계좌 데이터베이스(accountDb)에 등록
        accountDb.accounts[account] = {
            "balance": 0
        }
        accountDb.save_db()
        
        cur_u.userAccount = account
        print(f"\n계좌 번호 '{account}' 생성이 완료되었습니다.")
        
        # 2. 생성이 끝나자마자 즉시 종호님의 계좌 조회 화면으로 진입함
        activeAccountMenu(cur_u)
        
        # 종호님 메뉴가 다 끝나고 탈출했을 때, 이 입력 루프를 깨부수고 나가기 위해 break를 씀
        break
