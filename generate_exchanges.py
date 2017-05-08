#!/usr/bin/env python3

import sqlite3

def main():
    conn = sqlite3.connect('seng/server/db.sqlite3')
    curs = conn.cursor()

    for code, name in EXCHANGES:
        curs.execute('INSERT INTO server_stockexchange (code, name) VALUES (?, ?)', (code, name))

    conn.commit()


EXCHANGES = [
    ('AX', 'Australian Stock Exchange'),
    ('BR', 'Brussels Stock Exchange'),
    ('HK', 'Hong Kong Stock Exchange'),
    ('JK', 'Jakarta Stock Exchange'),
    ('KS', 'Korea Stock Exchange'),
    ('KL', 'Kuala Lumpur Stock Exchange'),
    ('LG', 'Lagos Stock Exchange'),
    ('L', 'London Stock Exchange'),
    ('OB', 'NASDAQ Dealers - Bulletin Board'),
    ('NS', 'National Stock Exchange of India'),
    ('N', 'New York Stock Exchange'),
    ('NZ', 'New Zealand Stock Exchange'),
    ('O', 'Second Class - Preferred Shares'),
    ('P', 'Pacific Stock Exchange'),
    ('PA', 'Paris Stock Exchange'),
    ('PK', 'Pink Sheets Electronic Quotation'),
    ('SA', 'Sao Paulo Stock Exchange'),
    ('SS', 'Shanghai Stock Exchange'),
    ('SI', 'Singapore Stock Exchange'),
    ('TW', 'Taiwan Stock Exchange'),
    ('T', 'Tokyo Stock Exchange'),
    ('K', 'Toronto Options Exchange'),
    ('TO', 'Toronto Stock Exchange'),
    ('VX', 'virt-x')
]

if __name__ == '__main__':
    main()