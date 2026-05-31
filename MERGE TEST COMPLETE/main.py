# ==========================================================
# sg_mainMenu/mainMenu.py
# 역할: 프로그램 전체 메뉴 흐름 제어 및 독립 모듈들의 실행 트리거
# ==========================================================

from config import config
from sg_mainMenu import memberService
from sg_mainMenu import database

# [오류 수정] 기존 memoFinal 은 실제 파일명(memo_final.py)과 일치하지 않아 메인이 터졌음
# 실제 파일명인 memo_final 에서 managementMemo 를 불러오도록 정정하여 구동 크래시를 방지함
from dm_memo_must.memo.memoFinal import managementMemo
from dm_memo_must.must.mustFinal import managementMust

# [경로 동기화] 주신 오더대로 종호님과 태경님의 고유 패키지 경로를 100% 일치시켜 로드함
from JH_account.accountMenu import activeAccountMenu
from tk_newAccount.newAccount import accountMenu

cur_u = None

def mainMenu():
    global cur_u

    # [오류 수정] 프로그램이 켜질 때 회원 정보를 파일에서 로드하지 않으면 회원가입/로그인이 작동하지 않음
    # memberService 에 선언된 UserInfo 와 Todo 클래스를 인자로 넘겨 데이터베이스를 강제 초기화함
    database.load_db(memberService.UserInfo, memberService.Todo)

    while True:
        if cur_u is None:
            print("\n=== 대전 비즈니스 시스템 ===")
            print("1. 회원 가입")
            print("2. 로그인")
            print("3. 아이디 찾기")
            print("4. 비밀번호 찾기")
            print("0. 종료")
            choice = input("선택: ").strip()
            
            if choice == config.SIGN_UP:
                memberService.signUp()
            elif choice == config.SIGN_IN:
                cur_u = memberService.signIn()
            elif choice == config.FIND_ID:
                memberService.findId()
            elif choice == config.FIND_PW:
                memberService.findPw()
            elif choice == config.EXIT:
                break
        
        # ---------- 로그인 상태 ----------
        else:
            print(f"\n======= [ {cur_u.userName}님 메뉴 ] =======")
            print(f"{config.MANAGEMENT_ACCOUNT}. 계좌 관리 (managementAccount)")
            print(f"{config.MANAGEMENT_MEMO}. 메모 관리 (managementMemo)")
            print(f"{config.MANAGEMENT_MUST}. 할일 관리 (managementMust)")
            print(f"{config.USER_INFO}. 회원 정보 관리 (userInfo)")
            print(f"{config.SIGN_OUT}. 로그 아웃 (signOut)")
            print(f"{config.EXIT}. 프로그램 종료 (Exit)")
            print("====================================")
            choice = input("선택: ").strip()

            if choice == config.MANAGEMENT_ACCOUNT:
                # userAccount 상태에 따라 계좌가 없으면 태경님의 함수로, 있으면 종호님의 함수로 제어권을 넘김
                if cur_u.userAccount is None:
                    accountMenu(cur_u)
                else:
                    activeAccountMenu(cur_u)

            elif choice == config.MANAGEMENT_MEMO:
                managementMemo(cur_u)

            elif choice == config.MANAGEMENT_MUST:
                managementMust(cur_u)

            elif choice == config.USER_INFO:
                print("\n(회원 정보 관리 메뉴로 이동합니다...)")

            elif choice == config.SIGN_OUT:
                cur_u = None
                print("\n로그아웃 되었습니다.")

            elif choice == config.EXIT:
                database.save_db()
                print("데이터를 저장하고 종료합니다.")
                break
            else:
                print("잘못된 입력입니다.")

if __name__ == "__main__":
    mainMenu()