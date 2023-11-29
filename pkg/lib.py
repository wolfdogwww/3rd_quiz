import json 
import sqlite3
import os
WANGHONG_DB='wanghong.db' #老師如果你有要改資料庫名子的話改這裡
PASS_JSON='pass.json'

def read_passjson() -> dict:
    """
    讀取pass.json檔案回傳一個字典

    Returns:
        dict: 包含json的檔案(字典的格式)
    """
    with open(PASS_JSON, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def display_menu():
    """
    顯示選單畫面
    
    Returns:
        None: 這個函式沒有返回值。
    """
    print("---------- 選單 ----------")
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")
    print("--------------------------")
    
def create_database():
    """
    建立資料庫名稱為 'wanghong.db'
        
    Returns:
        None: 這個函式沒有返回值。
    """
    
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS members (
        iid INTEGER PRIMARY KEY AUTOINCREMENT,
        mname TEXT NOT NULL,
        msex TEXT NOT NULL,
        mphone TEXT NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    print("=>資料庫已建立")
    conn.commit()
    conn.close()
    
def insert_database():
    """
    把'members.txt'的資料導入 'wanghong.db'
        
    Returns:
        None: 這個函式沒有返回值。
    """
    
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    
    with open('members.txt', 'r',encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split(',')
        mname, msex, mphone = data[0], data[1], data[2]
        cursor.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", (mname, msex, mphone))
        
    cursor.execute("SELECT COUNT(*) FROM members")
    result = cursor.fetchone()
    
    if result:
        print(f"=>異動 {result[0]} 筆記錄")
    conn.commit()
    conn.close()
        
def print_wanghong() -> None:
    """
    輸出'wanghong.db'的資料
    
    Returns:
        None: 這個函式沒有返回值。
    """
    
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT mname, msex, mphone FROM members")
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM members")
    result = cursor.fetchone()
    if result[0]:
        print()
        print("姓名        性別    手機")
        print("-----------------------------")
        for row in rows:
            print(f"{row[0]:　<6} {row[1]}　　{row[2]:　>12}") #草 用超九
        conn.close()
    else:
        print('=>查無資料')
        
        
def add_member() -> None:
    """
    新增member。
    """
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    name = input("請輸入姓名: ")
    sex = input("請輸入性別: ")
    phone = input("請輸入手機: ")       
    print("=>異動 1 筆記錄")
    cursor.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", (name, sex, phone))
    conn.commit()
    conn.close()
def change_member() -> None:
    """
    修改member資料。
    """
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    name = input("請輸入想修改記錄的姓名: ")
    if(name == ''):
        print("=>必須指定姓名才可修改記錄")
    else:
        cursor.execute("SELECT * FROM members WHERE mname = ?", (name,))
        result = cursor.fetchone()
        if result:
            new_sex = input("請輸入要改變的性別: ")
            new_phone = input("請輸入要改變的手機: ")
            print()
            print("原資料：")
            print(f"姓名：{result[1]}，性別：{result[2]}，手機：{result[3]}")
            #執行更新
            cursor.execute("UPDATE members SET msex = ?, mphone = ? WHERE mname = ?", (new_sex, new_phone, name))
            conn.commit()
            
            cursor.execute("SELECT * FROM members WHERE mname = ?", (name,))
            updated_result = cursor.fetchone()
            
            if updated_result:
            # 顯示更新後的資料
                print(f"=>異動 1 筆記錄\n修改後資料：")
                print(f"姓名：{updated_result[1]}，性別：{updated_result[2]}，手機：{updated_result[3]}")
            else:
                print("=>無法找到更新後的記錄")
            
        else:
            print("=>請輸入指定姓名")
        conn.commit()
    conn.close()
def search_phone() -> None:
    """
    查詢指定手機號碼的會員資料。
    """
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    phone = input("請輸入想查詢記錄的手機: ")
    
    cursor.execute("SELECT * FROM members WHERE mphone = ?", (phone,))
    result = cursor.fetchone()
    if result:
        print()
        print("姓名        性別    手機")
        print("-----------------------------")
        print(f"{result[1]:　<6} {result[2]}　　{result[3]:　>12}") #草 用超九
    else:
        print("=>無法找到您查詢記錄的手機")
    conn.commit()
    conn.close()
    
def del_all() -> None:
    """
    刪除所有會員資料。
    """
    conn = sqlite3.connect(WANGHONG_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members")
    result = cursor.fetchone()
    if result:
        print(f"=>異動 {result[0]} 筆記錄")
        cursor.execute("DELETE FROM members")
    conn.commit()
    conn.close()
def menu(number: str) -> None:
    """
    用於判斷在選單時輸入的東西並且處理
    Args:
        number (str): 選單輸入
    Returns:
        None: 這個函式沒有返回值。
    """
    if number=="1": #1 建立資料庫與資料表
        create_database()
    elif number=="2": #2 匯入資料
        insert_database()
    elif number=="3":#3 顯示所有紀錄
        print_wanghong()
    elif number=="4":#4 新增記錄
        add_member()
    elif number=="5":#5 修改記錄
        change_member()
    elif number=="6":#6 查詢指定手機
        search_phone()
    elif number=="7":#7 刪除所有記錄
        del_all()
    