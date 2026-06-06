import sqlite3
con_obj = sqlite3.connect(database='bank.sqlite')
cur_obj = con_obj.cursor()
cur_obj.execute('''create table users(
                    users_account integer primary key autoincrement,
                    users_password text,
                    users_name text,
                    users_mobile text unique,
                    users_email text unique,
                    users_balance float,
                    users_aadhar text unique,
                    users_opendate text)
                '''
)

cur_obj.execute('''create table txn(
                txn_id integer primary key autoincrement,
                txn_acn integer,
                txn_type text,
                txn_date text,
                txn_amount float,
                txn_updatebalance float
                )'''
)

print("created")

con_obj.close()

