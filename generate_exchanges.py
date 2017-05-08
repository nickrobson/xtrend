#!/usr/bin/env python3

import sqlite3

def main():
    conn = sqlite3.connect('seng/server/db.sqlite3')
    curs = conn.cursor()

    curs.execute('DELETE FROM server_stockexchange')

    for code, name in EXCHANGES:
        curs.execute('INSERT INTO server_stockexchange (code, name) VALUES (?, ?)', (code, name))

    conn.commit()


EXCHANGES = [
    ('AX', 'Australian Stock Exchange'),
    ('BR', 'Brussels Stock Exchange'),
    ('HK', 'Hong Kong Stock Exchange'),
    ('JK', 'Jakarta Stock Exchange'),
    ('K', 'Toronto Options Exchange'),
    ('KL', 'Kuala Lumpur Stock Exchange'),
    ('KS', 'Korea Stock Exchange'),
    ('L', 'London Stock Exchange'),
    ('LG', 'Lagos Stock Exchange'),
    ('OB', 'NASDAQ Dealers - Bulletin Board'),
    ('N', 'New York Stock Exchange'),
    ('NS', 'National Stock Exchange of India'),
    ('NZ', 'New Zealand Stock Exchange'),
    ('O', 'Second Class - Preferred Shares'),
    ('P', 'Pacific Stock Exchange'),
    ('PA', 'Paris Stock Exchange'),
    ('PK', 'Pink Sheets Electronic Quotation'),
    ('SA', 'Sao Paulo Stock Exchange'),
    ('SI', 'Singapore Stock Exchange'),
    ('SS', 'Shanghai Stock Exchange'),
    ('T', 'Tokyo Stock Exchange'),
    ('TO', 'Toronto Stock Exchange'),
    ('TW', 'Taiwan Stock Exchange'),
    ('UL', '(not publically traded)'),
    ('VX', 'virt-x'),
]

if __name__ == '__main__':
    main()