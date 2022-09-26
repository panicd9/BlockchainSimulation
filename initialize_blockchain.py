from datetime import datetime

from block import Block


def initialize_blockchain():
    transactions = []
    transaction_data = {'from': 'Darko', 'to': 'Igor', 'value': '30', 'timestamp': '2011-11-04 00:05:23.111'}
    transactions.append(transaction_data)
    transaction_data = {'from': 'Igor', 'to': 'Stefan', 'value': '10', 'timestamp': '2012-11-07 00:05:13.222'}
    transactions.append(transaction_data)
    transaction_data = {'from': 'Stefan', 'to': 'Darko', 'value': '10', 'timestamp': '2013-11-09 00:11:13.333'}
    transactions.append(transaction_data)
    transaction_data = {'from': 'Darko', 'to': 'Stefan', 'value': '20', 'timestamp': '2014-11-04 00:05:23.111'}
    transactions.append(transaction_data)
    transaction_data = {'from': 'Stefan', 'to': 'Igor', 'value': '5', 'timestamp': '2015-11-07 00:05:13.222'}
    transactions.append(transaction_data)
    transaction_data = {'from': 'Stefan', 'to': 'Darko', 'value': '10', 'timestamp': '2016-11-09 00:11:13.333'}
    transactions.append(transaction_data)

    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))

    block_0 = Block(
        transactions=transactions,
        timestamp=timestamp_0
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:19.222'))
    block_1 = Block(
        transactions=transactions,
        timestamp=timestamp_1,
        previous_block=block_0
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    block_2 = Block(
        transactions=transactions,
        timestamp=timestamp_2,
        previous_block=block_1
    )

    return block_2
