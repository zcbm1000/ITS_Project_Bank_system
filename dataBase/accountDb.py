from datetime import datetime

accounts = [{
        'userId': 'kim',
        'bank': '국민은행',
        'acctNum': '111-222',
        'balance': 50000,
        'writeTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        'userId': 'kim',
        'bank': '카카오뱅크',
        'acctNum': '333-444',
        'balance': 120000,
        'writeTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        'userId': 'kim',
        'bank': '신한은행',
        'acctNum': '555-666',
        'balance': 70000,
        'writeTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]