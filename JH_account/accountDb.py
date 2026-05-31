import json
import os
import config

accounts = {}

def save_db():
    with open(config.DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

def load_db():
    global accounts

    if os.path.exists(config.DB_FILE):
        with open(config.DB_FILE, 'r', encoding='utf-8') as f:
            accounts = json.load(f)

def find_account(acc_num):
    for acc in accounts:
        if acc['acc_no'] == acc_num:
            return acc
    return None

def get_balance(acc_num):
    acc = find_account(acc_num)
    if acc:
        return acc['balance']
    return None

def deposit(acc_num, money):
    acc = find_account(acc_num)
    if acc:
        acc['balance'] += money
        save_db()
        return True
    return False

def withdraw(acc_num,money):
    acc = find_account(acc_num)
    if acc and acc['balance'] >= money:
        acc['balance'] -= money
        save_db()
        return True
    return False