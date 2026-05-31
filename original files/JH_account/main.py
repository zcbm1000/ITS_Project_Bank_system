import config
import accountDb as accdb

def main():
    accdb.load_db()

    userId = input('ID 입력: ')
    userPw = input('PW 입력: ')
    if userId != config.LOGIN_USER and userPw != config.LOGIN_USER:
        print('로그인 실패')
        return
    
    print('로그인 성공')

    while True:
        print('\n1. 입금    2. 출금    0. 종료' )
        menu = input('선택: ')

        if menu == '0':
            accdb.save_db()
            break

        acc_num = input('계좌번호: ')
        money = int(input('금액: '))

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

if __name__ == '__main__':
    main()