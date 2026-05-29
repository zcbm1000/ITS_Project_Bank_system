from config_2 import config
from dataBase_2 import accountDb


def accountMenu():
    while True:
        print("\n=== 계좌 관리 메뉴 ===")
        print("1. 신규 계좌 생성")
        print("0. 메인 화면으로 돌아가기")

        choice = int(input("번호를 선택하세요: "))

        if choice == config.CREATENEWACCOUNT:
            createAccount()

        elif choice == config.BACKTOMAINMENU:
            print("메인 메뉴로 돌아갑니다.")
            break


def createAccount():
    while True:
        account = input("사용할 계좌 번호(13자리)를 입력하세요: ")


        if len(account) != 13:
            print("입력하신 계좌 번호는 13자리가 아닙니다.")
            continue

        if account in accountDb.accounts:
            print("이미 존재하는 계좌 번호입니다.")
            continue

        accountDb.accounts[account] = {
            "balance": 0
        }

        print(f"계좌 번호 '{account}' 생성이 완료되었습니다.")
        return   
