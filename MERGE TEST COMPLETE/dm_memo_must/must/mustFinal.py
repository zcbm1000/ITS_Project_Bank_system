# ==========================================================
# dm_memo_must/must/mustFinal.py
# 역할: 할일 관리 메뉴 전체 (저장/불러오기 + 입출력 + 흐름)
# ==========================================================

import json
from config import config
from dataBase import mustDb
from datetime import datetime

# [수정 전]
# import os  ← os 모듈 사용
#
# [수정 후]
# os import 제거. loadMust 에서 try/except 로 대체.
# memo_final 과 동일한 이유.

MUST_DB_PATH = 'must_db.json'


def get_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def saveMust():
    with open(MUST_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(mustDb.musts, f, ensure_ascii=False, indent=2)


def loadMust():
    # [수정 전]
    # if os.path.exists(MUST_DB_PATH):
    #     with open(...) as f:
    #         mustDb.musts = json.load(f)
    #
    # [수정 후] try/except FileNotFoundError 로 대체.
    try:
        with open(MUST_DB_PATH, 'r', encoding='utf-8') as f:
            mustDb.musts = json.load(f)
    except FileNotFoundError:
        pass


def initUser(userId):
    if userId not in mustDb.musts:
        mustDb.musts[userId] = []


def managementMust(cur_u):
    userId = cur_u.userId
    loadMust()
    initUser(userId)

    while True:
        print('\n[ 할일 관리 (managementMust) ]')
        print(f'{config.MUST_READ}.mustRead    {config.MUST_WRITE}.mustWrite    {config.MUST_UPDATE}.mustUpdate    {config.MUST_DELETE}.mustDelete    {config.MUST_COMPLETE_TOGGLE}.mustComplete/Incomplete    {config.BACK}.back')
        choice = input('>> ')

        # ---------- mustRead ----------
        if choice == config.MUST_READ:
            musts      = mustDb.musts[userId]
            incomplete = [t for t in musts if t['mustComplete'] == config.MUST_INCOMPLETE]
            complete   = [t for t in musts if t['mustComplete'] == config.MUST_COMPLETE]

            print(f'\n[ ⬜ 미완료 (mustIncomplete) ] {len(incomplete)}개')
            if incomplete:
                for t in incomplete:
                    print(f"  ({t['id']}) [{t['priority']}] [{t['title']}] {t['content']}")
                    print(f"      작성: {t['writeTime']}  |  수정: {t['revisionTime']}")
            else:
                print('  없음')

            print(f'\n[ ✅ 완료 (mustComplete) ] {len(complete)}개')
            if complete:
                for t in complete:
                    print(f"  ({t['id']}) [{t['priority']}] [{t['title']}] {t['content']}")
                    print(f"      작성: {t['writeTime']}  |  수정: {t['revisionTime']}")
            else:
                print('  없음')

        # ---------- mustWrite ----------
        elif choice == config.MUST_WRITE:
            musts = mustDb.musts[userId]
            if len(musts) >= config.MAX_MUST_COUNT:
                print(f'할일은 최대 {config.MAX_MUST_COUNT}개까지 작성할 수 있습니다.')
            else:
                while True:
                    title = input(f'제목을 입력하세요 ({config.MAX_MUST_TITLE_LENGTH}자 이하): ')
                    if len(title) == 0:
                        print('제목을 입력해주세요.')
                    elif len(title) > config.MAX_MUST_TITLE_LENGTH:
                        print(f'{config.MAX_MUST_TITLE_LENGTH}자를 초과했습니다. ({len(title)}자)')
                    else:
                        break

                while True:
                    content = input(f'내용을 입력하세요 ({config.MAX_MUST_LENGTH}자 이하): ')
                    if len(content) == 0:
                        print('내용을 입력해주세요.')
                    elif len(content) > config.MAX_MUST_LENGTH:
                        print(f'{config.MAX_MUST_LENGTH}자를 초과했습니다. ({len(content)}자)')
                    else:
                        break

                while True:
                    print(f'우선순위를 선택하세요: 1.{config.PRIORITY_HIGH}(높음)    2.{config.PRIORITY_MEDIUM}(보통)    3.{config.PRIORITY_LOW}(낮음)')
                    p_choice = input('>> ')
                    if p_choice == '1':
                        priority = config.PRIORITY_HIGH
                        break
                    elif p_choice == '2':
                        priority = config.PRIORITY_MEDIUM
                        break
                    elif p_choice == '3':
                        priority = config.PRIORITY_LOW
                        break
                    else:
                        print('1, 2, 3 중에서 입력하세요.')

                new_id = musts[-1]['id'] + 1 if musts else 1
                now = get_now()
                musts.append({
                    'id': new_id,
                    'title': title,
                    'content': content,
                    'priority': priority,
                    'mustComplete': config.MUST_INCOMPLETE,
                    'writeTime': now,
                    'revisionTime': now
                })
                saveMust()
                print(f'할일이 추가되었습니다. (id: {new_id})')

        # ---------- mustUpdate ----------
        elif choice == config.MUST_UPDATE:
            musts = mustDb.musts[userId]
            if not musts:
                print('수정할 할일이 없습니다.')
            else:
                print('\n[ 수정할 할일 선택 ]')
                for t in musts:
                    status = '✅' if t['mustComplete'] == config.MUST_COMPLETE else '⬜'
                    print(f"  ({t['id']}) {status} [{t['priority']}] [{t['title']}] {t['content']}")

                try:
                    target_id = int(input('수정할 번호: '))
                    target = None
                    for t in musts:
                        if t['id'] == target_id:
                            target = t
                            break

                    if target is None:
                        print('해당 번호의 할일이 없습니다.')
                    else:
                        while True:
                            new_title = input(f'새 제목 ({config.MAX_MUST_TITLE_LENGTH}자 이하, 엔터 시 유지): ')
                            if new_title == '':
                                new_title = target['title']
                                break
                            elif len(new_title) > config.MAX_MUST_TITLE_LENGTH:
                                print(f'{config.MAX_MUST_TITLE_LENGTH}자를 초과했습니다.')
                            else:
                                break

                        while True:
                            new_content = input(f'새 내용 ({config.MAX_MUST_LENGTH}자 이하, 엔터 시 유지): ')
                            if new_content == '':
                                new_content = target['content']
                                break
                            elif len(new_content) > config.MAX_MUST_LENGTH:
                                print(f'{config.MAX_MUST_LENGTH}자를 초과했습니다.')
                            else:
                                break

                        while True:
                            print(f'우선순위 선택 (엔터 시 유지 [{target["priority"]}]): 1.{config.PRIORITY_HIGH}    2.{config.PRIORITY_MEDIUM}    3.{config.PRIORITY_LOW}')
                            p_choice = input('>> ')
                            if p_choice == '':
                                new_priority = target['priority']
                                break
                            elif p_choice == '1':
                                new_priority = config.PRIORITY_HIGH
                                break
                            elif p_choice == '2':
                                new_priority = config.PRIORITY_MEDIUM
                                break
                            elif p_choice == '3':
                                new_priority = config.PRIORITY_LOW
                                break
                            else:
                                print('1, 2, 3 또는 엔터를 입력하세요.')

                        target['title']        = new_title
                        target['content']      = new_content
                        target['priority']     = new_priority
                        target['revisionTime'] = get_now()
                        saveMust()
                        print('할일이 수정되었습니다.')

                except ValueError:
                    print('숫자를 입력하세요.')

        # ---------- mustDelete ----------
        elif choice == config.MUST_DELETE:
            musts = mustDb.musts[userId]
            if not musts:
                print('삭제할 할일이 없습니다.')
            else:
                print('\n[ 삭제할 할일 선택 ]')
                for t in musts:
                    status = '✅' if t['mustComplete'] == config.MUST_COMPLETE else '⬜'
                    print(f"  ({t['id']}) {status} [{t['priority']}] [{t['title']}] {t['content']}")

                try:
                    target_id = int(input('삭제할 번호: '))
                    target = None
                    for t in musts:
                        if t['id'] == target_id:
                            target = t
                            break

                    if target is None:
                        print('해당 번호의 할일이 없습니다.')
                    else:
                        musts.remove(target)
                        saveMust()
                        print('할일이 삭제되었습니다.')

                except ValueError:
                    print('숫자를 입력하세요.')

        # ---------- mustComplete / mustIncomplete 토글 ----------
        elif choice == config.MUST_COMPLETE_TOGGLE:
            musts = mustDb.musts[userId]
            if not musts:
                print('할일이 없습니다.')
            else:
                print('\n[ 완료/미완료 전환할 할일 선택 ]')
                for t in musts:
                    status = '✅' if t['mustComplete'] == config.MUST_COMPLETE else '⬜'
                    print(f"  ({t['id']}) {status} [{t['priority']}] [{t['title']}] {t['content']}")

                try:
                    target_id = int(input('전환할 번호: '))
                    target = None
                    for t in musts:
                        if t['id'] == target_id:
                            target = t
                            break

                    if target is None:
                        print('해당 번호의 할일이 없습니다.')
                    else:
                        if target['mustComplete'] == config.MUST_COMPLETE:
                            target['mustComplete'] = config.MUST_INCOMPLETE
                            new_status = 'mustIncomplete ⬜'
                        else:
                            target['mustComplete'] = config.MUST_COMPLETE
                            new_status = 'mustComplete ✅'

                        target['revisionTime'] = get_now()
                        saveMust()
                        print(f'→ {new_status} 처리되었습니다.')

                except ValueError:
                    print('숫자를 입력하세요.')

        # ---------- back ----------
        elif choice == config.BACK:
            print('할일 메뉴를 종료합니다.')
            break

        else:
            print('올바른 번호를 입력하세요.')
