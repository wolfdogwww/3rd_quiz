from pkg.lib import read_passjson,display_menu,menu

acc_pass = read_passjson() #讀取pass.json

# 將讀取的帳號和密碼儲存在 credentials 字典中
credentials = {}
for entry in acc_pass:
    credentials[entry['帳號']] = entry['密碼']
    
accinput=input("請輸入帳號：")
passinput = input("請輸入密碼：")

if accinput in credentials and credentials[accinput] == passinput: #判斷輸入是否正確
    while(True):
        display_menu()
        input_menu = str(input("請輸入您的選擇 [0-7]: "))
        if input_menu =="" or input_menu=="0":
            break
        elif input_menu > "7":
            print("=>無效的選擇")
        
        elif input_menu >= "0" and input_menu <= "7":
            menu(input_menu)
            
        print()
    # 這裡執行後續的功能，比如顯示選單或者其他操作
else:
    print("=>帳密錯誤，程式結束")