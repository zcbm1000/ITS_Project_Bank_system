from config import config
from sg_mainMenu import main
from sg_mainMenu import database

#  메인메뉴
def main():
    global cur_u
    while True:
        if cur_u is None:
            
            print("\n======= [ 환영합니다 ] =======")
            print("1. 회원 가입 (signUp)")
            print("2. 로그 인 (signIn)")
            print("3. 아이디 찾기 (findId)")
            print("4. 비밀번호 찾기 (findPw)")
            print("0. 프로그램 종료 (Exit)")
            print("==============================")
            sel = input("선택: ")

            if sel == '1':
                main.signUp()
            elif sel == '2':
                main.signIn()
            elif sel == '3':
                main.findId() 
            elif sel == '4':
                main. findPw()  
            elif sel == '0':
                database.save_db(db)
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다.")
        else:
            
            print(f"\n======= [ {cur_u.userName}님 메뉴 ] =======")
            print("1. 계좌 관리 (managementAccount)")
            print("2. 메모 관리 (managementMemo)")
            print("3. 할일 관리 (managementMust)")
            print("4. 회원 정보 관리 (userInfo)")
            print("5. 로그 아웃 (signOut)")
            print("0. 프로그램 종료 (Exit)")
            print("====================================")
            sel = input("선택: ")

            if sel == '1':
                print("\n(계좌 관리 메뉴로 이동합니다...)")
            elif sel == '2':
                print("\n(메모 관리 메뉴로 이동합니다...)")
            elif sel == '3':
                print("\n(할일 관리 메뉴로 이동합니다...)")
            elif sel == '4':
                print("\n(회원 정보 관리 메뉴로 이동합니다...)")
            elif sel == '5':
                cur_u = None
                print("\n로그아웃 되었습니다.")
            elif sel == '0':
                database.save_db(db)
                print("데이터를 저장하고 종료합니다.")
                break
            
            print(f"\n======= [ {cur_u.userName}님 메뉴 ] =======")
            print("1. 계좌 관리 (managementAccount)")
            print("2. 메모 관리 (managementMemo)")
            print("3. 할일 관리 (managementMust)")
            print("4. 회원 정보 관리 (userInfo)")
            print("5. 로그 아웃 (signOut)")
            print("0. 프로그램 종료 (Exit)")
            print("====================================")
            sel = input("선택: ")

            if sel == '1':
                print("\n(계좌 관리 메뉴로 이동합니다...)")
            elif sel == '2':
                print("\n(메모 관리 메뉴로 이동합니다...)")
            elif sel == '3':
                print("\n(할일 관리 메뉴로 이동합니다...)")
            elif sel == '4':
                print("\n(회원 정보 관리 메뉴로 이동합니다...)")
            elif sel == '5':
                cur_u = None
                print("\n로그아웃 되었습니다.")
            elif sel == '0':
                database.save_db(db)
                print("데이터를 저장하고 종료합니다.")
                break