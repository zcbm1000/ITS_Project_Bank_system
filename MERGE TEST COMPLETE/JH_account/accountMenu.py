from config import config
from dataBase import accountDb as accdb
from KS_banktransfer_dir.KS_BankTrensfer import bankMain as openDaejeonBank

# [수정 전] money = int(input()) 처리가 블록 내부에서 중복 실행되어 금액을 연달아 두 번 입력해야 하는 치명적인 버그가 있었음
# [수정 후] 중복 코드를 단일 입력 구조로 정돈하고, 메뉴 분기에 '3'번 대전뱅크 연동 통로를 개설함
# [왜 이렇게 해야 하는가] 사용자가 금액을 정확히 한 번만 입력하게 오류를 잡고, 조회/입출금 화면에서 이체 기능(경선 모듈)으로 유기적으로 이어지게 하기 위함
def activeAccountMenu(cur_u):
    accdb.load_db()
    acc_num = cur_u.userAccount  # 로그인한 유저의 계좌를 바로 가져옴
    print(f"\n계좌 연결 성공 (회원 계좌: {acc_num})")

    while True:
        # 종호님의 get_balance 함수를 활용해 상단에 현재 잔액 상태를 실시간으로 출력합니다.
        balance = accdb.get_balance(acc_num)
        print(f"\n현재 잔액: {balance if balance is not None else 0}원")
        print('1. 입금    2. 출금    3. 대전뱅크(이체/내역)    0. 종료')
        menu = input('선택: ').strip()

        if menu == '0':
            accdb.save_db()
            break

        # 3번 선택 시 경선님의 독립된 대전뱅크 파일 함수로 진입 제어합니다.
        if menu == '3':
            openDaejeonBank(cur_u)
            continue

        try:
            money = int(input('금액: '))
        except ValueError:
            print('오류: 금액은 숫자만 입력 가능합니다.')
            continue

        if menu == config.MENU_DEPOSIT:
            if accdb.deposit(acc_num, money):
                print('입금 완료')
            else:
                print('계좌 없음')

        elif menu == config.MENU_WITHDRAW:
            if accdb.withdraw(acc_num, money):
                print('출금 완료')
            else:
                print('잔액 부족 또는 계좌 없음')

        else:
            print('잘못된 입력입니다.')