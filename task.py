import os
import time
import sqlite3
import argparse
from contents import *
from discord_webhook import *


def main(first_time_run=False):
    # check db file
    if not os.path.exists(os.path.join('.', LOCAL_SQLLIST_FILE)):
        conn = sqlite3.connect(LOCAL_SQLLIST_FILE)
        c = conn.cursor()
        c.execute('CREATE TABLE matches (id text primary key, match_id text, player_id int, created_at text)')
        conn.commit()
    # calculate wait time base on person to avoid exceed api limit
    # if u can manually change your IP, you can reduce it
    wait_time = int(((24 * 30 * 3600) / 50000) * len(PERSON) * 1.2)

    # query DB size, if DB is empty remind first time run
    if not first_time_run:
        conn = sqlite3.connect(LOCAL_SQLLIST_FILE)
        c = conn.cursor()
        c.execute('SELECT count(*) from matches;')
        db_size = c.fetchone()
        if db_size[0] == 0:
            choice = input("本地数据库没有任何记录, 确定将所有ID近期20场比赛记录一次性发送么?(Y/N): ")
            if choice == 'N' or choice == 'n':
                first_time_run = True

    while True:
        for p in PERSON:
            uid = p[0]
            name = p[1]
            try:
                open_dota_matches_refresh(uid)
                # wait 10s to refresh recent matches and avoid exceed discord message limit
                time.sleep(10)
                result = get_recent_matches(uid)
                for match in result:
                    # connect DB
                    conn = sqlite3.connect(LOCAL_SQLLIST_FILE)
                    cursor = conn.cursor()
                    # query match
                    cursor.execute('SELECT * FROM matches where match_id = {} and player_id = {}'.format(match['match_id'], uid))
                    # match not in DB
                    if not cursor.fetchone():
                        print('find new match: {}, uid: {}, name: {}'.format(match['match_id'], uid, name))
                        if not first_time_run:
                            analyse_one_match(match, name=name)
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO matches VALUES ({}, {}, {}, {})".format(
                            str(match['match_id']) + str(uid),
                            match['match_id'],
                            uid,
                            time.time()))
                        conn.commit()
            except Exception as e:
                print('get recent matches fail: {}'.format(e))
        print('task completed {}, wait time: {}, next time {}\r'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            wait_time,
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + wait_time))), end='')
        if first_time_run:
            first_time_run = False
        time.sleep(wait_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='', usage='', description='')
    parser.add_argument('-f', help='First time run, add all matches into DB without notice', action='store_true')
    args = parser.parse_args()
    first_time_run = args.f
    if first_time_run:
        main(first_time_run=True)
    else:
        main()
