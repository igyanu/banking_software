from tkinter import Tk, Label, Frame, Entry, Button, messagebox, simpledialog
from tkintertable import TableCanvas, TableModel
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import time
import random
import sqlite3
import gmail

win = Tk()

#title
win.title("My Project")
win.state('zoomed')
win.resizable(width=False, height=False)
win.configure(bg='light green')
header_title = Label(win, text="Banking Automation", font=('arial', 50, 'bold'), bg='light green') 
header_title.pack()
#date
current_date = time.strftime('%d %b, %Y')
header_date = Label(win,text=f"Today:{current_date}", font=('arial', 20, 'bold'), fg='blue', bg='light green') 
header_date.pack(pady=3)
#logo
img = Image.open(r'C:\Users\gyanu\Downloads\banking_software\bank-logo.png').resize((145,145))
bitmap = ImageTk.PhotoImage(img, master=win)
logo_label = Label(win, image=bitmap)
logo_label.place(relx=0, rely=0)

#footer
footer_title = Label(win, text="",font=('arial',20,'normal'), bg='light green')
footer_title.pack(side='bottom')

#main screen
def main_screen():
    frm = Frame(win, highlightbackground='red', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.2, relwidth=1, relheight=.7)
    
    def login_click():

        global uacn, uname
        uacn = int( acn_entry.get() )
        upass= pass_entry.get()
        urole= role_cb.get()

        
        if( urole=='Admin'):
            admin_welcome_page()
            return
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('select adm_account, adm_password from adm where adm_account=?',(uacn,))
            tup = cur_obj.fetchone()
            con_obj.close()
            if(tup==None):
                messagebox.showerror('admin login','invalid admin account')
            if(tup[0]==uacn and tup[1]==upass):
                uacn=tup[2]
                frm.destroy()
                admin_welcome_page()
            else:
                messagebox.showerror('admin login','invalid account/password')
        elif(urole=='User'):
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute( 'select * from users where users_account=? and users_password=?',(uacn, upass))
            tup = cur_obj.fetchone()
            con_obj.close()
            if(tup==None):
                messagebox.showerror('login failed:', "invalid account/password")
            else:
                uname = tup[2]
                frm.destroy()
                user_welcome_page()
       
    def reset_click():
        acn_entry.delete(0,'end')
        pass_entry.delete(0,'end')
    def forgot_click():
        forgot_password_page()

    acn_label = Label(frm, font=('arial', 20, 'bold'), bg='pink', text="account number")
    acn_label.place(relx=.3, rely=.1)
    acn_entry = Entry(frm, width= 18, font=('arial', 20, 'normal' ), bd=4 )
    acn_entry.place(relx=.5, rely=.1)
    acn_entry.focus()

    pass_label = Label(frm, font= ('arial', 20, 'bold'), bg='pink', text="password")
    pass_label.place(relx=.3, rely=.22)
    pass_entry = Entry(frm,width= 18, font=('arial', 20, 'normal'), bd=4, show="*")
    pass_entry.place(relx=.5, rely=.22)

    role_label = Label(frm, font=('arrial',20, 'bold'), text="role", bg='pink')
    role_label.place(relx=.3, rely=.34)
    role_cb = Combobox(frm, width= 17, font=('arial', 20, 'normal'), values=['User', 'Admin'])
    role_cb.current(0)
    role_cb.place ( relx=.5, rely=.34 )

    login_btn = Button(frm, width= 6, font=('arial', 20, 'bold'), text="login", bg='light green', bd=4, command= login_click )
    login_btn.place(relx=.5, rely=.5, relheight=.08)

    reset_btn = Button(frm, width= 7, text="reset", font=('arial',20, 'bold'), bd=4, bg='light green', command= reset_click )
    reset_btn.place(relx=.61, rely=.5, relheight=.08)

    forgot_btn = Button(frm, width= 16 , font=('arial', 20, 'bold'), text="forgot password", bg='light green', bd=4, command= forgot_click )
    forgot_btn.place(relx=.5, rely=.61, relheight=.08)

#  user page
def user_welcome_page():
    frm = Frame(win, highlightbackground='red', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.2, relheight=.7, relwidth=1)

    user_title = Label(frm, text=f"Welcome, {uname}", font=('arial', 20, 'bold'), bg='pink', fg='blue')
    user_title.place(relx=.03, rely=0)

    def logout_click():
        frm.destroy()
        main_screen()
    
    def view_details():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.27, rely=.2, relwidth= .5, relheight=.7)

        title_ifrm = Label(ifrm,text="check balance", font=('arial', 18, 'bold'), bg='white', fg='purple')
        title_ifrm.pack()


        # fetching data from database for filling into entry box
        con_obj = sqlite3.connect(database='bank.sqlite')
        cur_obj = con_obj.cursor()
        cur_obj.execute('select * from users where users_account=?', (uacn,))
        tup = cur_obj.fetchone()
        con_obj.close()
        
        balance_label = Label(ifrm, text=f"Account Number:\t{tup[0]}", font=('arial', 18, 'normal'), bg='white')
        balance_label.place(relx=.04, rely=.2)
        accountno_label = Label(ifrm, text=f"Balance:\t{tup[5]}", font=('arial', 18, 'normal'), bg='white')
        accountno_label.place(relx=.5, rely=.2)

        name_label = Label(ifrm, text=f"Name:\t{tup[2]}", font=('arial', 18, 'normal'), bg='white')
        name_label.place(relx=.04, rely=.35)
        pass_label = Label(ifrm, text=f"Password:  {tup[1]}", font=('arial', 18, 'normal'), bg='white')
        pass_label.place(relx=.5, rely=.35)

        mobile_label = Label(ifrm, text=f"Email:\t{tup[4]}", font=('arial', 18, 'normal'), bg='white')
        mobile_label.place(relx=.04, rely=.5)

        email_label = Label(ifrm, text=f"Mob:\t {tup[3]}", font=('arial', 18, 'normal'), bg='white')
        email_label.place(relx=.04, rely=.62)


        aadhar_label = Label(ifrm, text=f"Aadhar:\t{tup[6]}", font=('arial', 18, 'normal'), bg='white')
        aadhar_label.place(relx=.04, rely=.74)
        opndate_label = Label(ifrm, text=f"A/c Open Date:\t {tup[7]}", font=('arial', 18, 'normal'), bg='white')
        opndate_label.place(relx=.04, rely=.86)
        
    def update_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.27, rely=.2, relwidth=.5, relheight=.7)

        title_ifrm = Label(ifrm,text="update details", font=('arial', 18, 'bold'), bg='white', fg='purple')
        title_ifrm.pack()

        otp = None
        def send_otp():
            nonlocal otp
            otp = random.randint(1000,9999)
            print(otp)

            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            to = cur_obj.execute('select users_email from users where users_account=?',(uacn,)).fetchone()[0]
            con_obj.close()
            try:
                gmail_con = gmail.GMail("email id", "app password")
                body = f'''Welcome to SBI bank !! \n
Someone tried to update details.
If not you then change password immediately. \n
OTP for verification is: {otp}
                '''
                mail= gmail.Message(to= to, subject="verification", text=body)
                gmail_con.send(mail)
            except:
                print("can't send otp probably due to internet")

            otpsend_btn.destroy()
            messagebox.showinfo('verification','otp sent to your mail enter to verify')
            otp_entry.place(relx=.32, rely=.4)
            otp_verify_btn.place(relx=.36, rely=.76, relheight=.13)
        
# updating entered value
        def update_entries():
            
            uname = name_entry.get()
            umobile= mobile_entry.get()
            uemail= email_entry.get()
            upassword= pass_entry.get()

            if(not uname.strip()):
                messagebox.showerror('name update',"invalid name")
                return
            elif(not umobile.isdigit() or len(umobile)!=10):
                messagebox.showerror('mobile update',"invalid mobile number")
                return
            elif(not upassword.strip()):
                messagebox.showerror('password update',"invalid password")
                return
            # now validating email
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            old_mail = cur_obj.execute('select users_email from users where users_account=?',(uacn,)).fetchone()[0]
            con_obj.close()
            if(old_mail != uemail):
                otp = random.randint(1000,9999)
                print(otp)
                try:
                    gmail_con = gmail.GMail("email id", "app password")
                    body = f'''Welcome to SBI bank !!
Someone tried to add this email as their email for SBI Bank.
If not you then ignore.

OTP for update verification is: {otp}
                    '''
                    mail= gmail.Message(to= uemail, subject="verification", text=body)
                    gmail_con.send(mail)
                except:
                    messagebox.showerror('email update', 'problem occured while sending otp through email')
                    return
                entd_otp = simpledialog.askinteger('email','enter otp to verify')
                if(otp != entd_otp ):
                    messagebox.showinfo('email update', 'invalid otp')
                    return

            try:
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj= con_obj.cursor()
                cur_obj.execute('update users set users_name=?, users_password=?, users_email=?, users_mobile=? where users_account=?', 
                                (uname, upassword, uemail, umobile, uacn))
                con_obj.commit()
                con_obj.close()
                messagebox.showinfo('update','details updated')
            except:
                con_obj.close()
                messagebox.showerror('update', 'some error occured')

# fetching data from database for filling into entry box
        def update_window():
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('select * from users where users_account=?', (uacn,))
            tup = cur_obj.fetchone()
            con_obj.close()

            name_label.place(relx=.04, rely=.2)
            name_entry.insert(0,tup[2])
            name_entry.place(relx=.04, rely=.3)
            
            pass_label.place(relx=.54, rely=.2)
            pass_entry.insert(0,tup[1])
            pass_entry.place(relx=.54, rely=.3)
            
            mobile_label.place(relx=.04, rely=.5)
            mobile_entry.insert(0,tup[3])
            mobile_entry.place(relx=.04, rely=.6)
            
            email_label.place(relx=.54, rely=.5)
            email_entry.insert(0,tup[4])
            email_entry.place(relx=.54, rely=.6)
            
            sub_btn.place(relx=.54, rely=.8, relheight=.15)
        
        def verify_otp():
            entd_otp = int(otp_entry.get())
            if(entd_otp==otp):
                msg_label.destroy()
                otp_entry.destroy()
                otp_verify_btn.destroy()
                messagebox.showinfo('verification','verified')
                update_window()
            else:
                messagebox.showerror('verification','incorrect otp')
        
        # before update labels  and buttons
        msg = 'otp verification is required before update'
        msg_label = Label(ifrm, text=msg,font=('arial',15,'bold'), fg='red', bg='white')
        msg_label.place(relx=.25, rely=.15)
        otpsend_btn = Button(ifrm, width= 10, command= send_otp, font=('arial', 20, 'bold'), text="verify", bg='light green', bd=4,  )
        otpsend_btn.place(relx= .37, rely= .48, relheight= .15)

        otp_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        otp_verify_btn= Button(ifrm, width= 10, command= verify_otp, font=('arial', 20, 'bold'), text="submit", bg='light green', bd=4,  )

        # update related label and buttons
        name_label= Label(ifrm, text="name", font=('arial', 18, 'normal'), bg='white')
        name_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        pass_label= Label(ifrm, text="password", font=('arial', 18, 'normal'), bg='white')
        pass_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        mobile_label = Label(ifrm, text="mobile", font=('arial', 18, 'normal'), bg='white')
        mobile_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        email_label= Label(ifrm, text="email", font=('arial', 18, 'normal'), bg='white')
        email_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        sub_btn= Button(ifrm, command=update_entries, width= 6 , font=('arial', 20, 'bold'), text="update", bg='light green', bd=4)

    def deposit_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white')
        ifrm.place(relx=.27, rely=.2, relwidth=.5, relheight=.7)

        title_ifrm = Label(ifrm,text="deposit money", font=('arial', 18, 'bold'), bg='white', fg='purple')
        title_ifrm.pack()

        def deposit():
            uamt = float(amt_entry.get())
            if(uamt<=0):
                messagebox.showerror("withdraw",'please enter positive number')
                return
            
            # depositing money in users account
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('select users_balance from users where users_account=?',(uacn,))
            balance = cur_obj.fetchone()[0]
            cur_obj.execute('update users set users_balance=? where users_account=?',(balance+uamt,uacn) )
            con_obj.commit()
            con_obj.close()
            # maintaining transaction
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('insert into txn (txn_acn, txn_type, txn_date, txn_amount, txn_updatebalance) values(?,?,?,?,?)',
                            (uacn,'Cr(+)',time.strftime('%d-%b-%Y %r'), uamt, balance+uamt) )
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo('deposit',f"amount: {uamt} deposited and updated balance is: {balance+uamt}")

        amt_label = Label(ifrm, text="amount", font=('arial', 18, 'normal'), bg='white')
        amt_label.place(relx=.3, rely=.32)
        amt_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        amt_entry.place(relx=.3, rely=.44)

        deposit_btn = Button(ifrm, width= 8 , font=('arial', 20, 'bold'), text="deposit", bg='light green', bd=4, command=deposit )
        deposit_btn.place(relx=.38, rely=.76, relheight=.13)

    def withdraw_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white')
        ifrm.place(relx=.27, rely=.2, relwidth=.5, relheight=.7)

        title_ifrm = Label(ifrm,text="withdraw cash", font=('arial', 18, 'bold'), bg='white', fg='red')
        title_ifrm.pack()

        otp = None
        def send_otp():
            nonlocal otp
            otp = random.randint(1000,9999)
            print(otp)
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            uemail = cur_obj.execute('select users_email from users where users_account=?',(uacn,)).fetchone()[0]
            con_obj.close()
            try:
                gmail_con = gmail.GMail("email id", "app password")
                body = f'''Welcome to SBI bank !!
Someone tried to withdraw balance.
If not you then change password immediately.

OTP for withdraw verification is: {otp}
                '''
                mail= gmail.Message(to= uemail, subject="verification", text=body)
                gmail_con.send(mail)
                messagebox.showinfo('verification','otp sent to your mail enter to verify') 
            except:
                messagebox.showerror('veriifcation', "error occured while sending otp")

            otpsend_btn.destroy()          
            otp_entry.place(relx=.32, rely=.4)
            otp_verify_btn.place(relx=.36, rely=.76, relheight=.13)
                      
        def verify_otp():
            entd_otp = int(otp_entry.get())
            if(entd_otp==otp):
                msg_label.destroy()
                otp_entry.destroy()
                otp_verify_btn.destroy()
                messagebox.showinfo('verification','verified')

                amt_label.place(relx=.3, rely=.32)
                amt_entry.place(relx=.3, rely=.44)
                withdraw_btn.place(relx=.38, rely=.76, relheight=.13)
            else:
                messagebox.showerror('verification','incorrect otp')
        

        def withdraw():
            uamt = float(amt_entry.get())
            if(uamt<=0):
                messagebox.showerror("withdraw",'please enter positive amount')
                return
            # deducting money from users account
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('select users_balance from users where users_account=?',(uacn,))
            balance = cur_obj.fetchone()[0]
            con_obj.close()
            if(balance<uamt):
                messagebox.showerror("withdraw", f"insuffient balance")
                return
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('update users set users_balance=? where users_account=?',(balance-uamt,uacn) )
            con_obj.commit()
            # maintaining transaction
            cur_obj.execute('insert into txn (txn_acn, txn_type, txn_date, txn_amount, txn_updatebalance) values(?,?,?,?,?)',
                            (uacn,'Db(-)',time.strftime('%d-%b-%Y %r'), uamt, balance-uamt) )
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo('withdraw',f"Amount: {uamt} withdrawn and remaining balance is: {balance-uamt}")

        # initial labels and entry box
        msg = 'otp verification is required to withdraw balance'
        msg_label = Label(ifrm, text=msg,font=('arial',15,'bold'), fg='red', bg='white')
        msg_label.place(relx=.25, rely=.15)
        otpsend_btn = Button(ifrm, width= 10, command= send_otp, font=('arial', 20, 'bold'), text="verify", bg='light green', bd=4,  )
        otpsend_btn.place(relx= .37, rely= .48, relheight= .15)

        # otp entry box and button
        otp_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        otp_verify_btn= Button(ifrm, width= 10, command= verify_otp, font=('arial', 20, 'bold'), text="submit", bg='light green', bd=4,  )

        # amount label, entry and submit button
        amt_label = Label(ifrm, text="amount", font=('arial', 18, 'normal'), bg='white')
        amt_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        withdraw_btn = Button(ifrm, width= 10, command=withdraw, font=('arial', 20, 'bold'), text="withdraw", bg='light green', bd=4,  )

    def transfer_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white')
        ifrm.place(relx=.27, rely=.2, relwidth=.5, relheight=.7)

        title_ifrm = Label(ifrm,text= "transfer money", font=('arial', 18, 'bold'), bg='white', fg='red')
        title_ifrm.pack()

        otp = None
        def send_otp():
            nonlocal otp
            otp = random.randint(1000,9999)
            print(otp)
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            to = cur_obj.execute('select users_email from users where users_account=?',(uacn,)).fetchone()[0]
            con_obj.close()
            try:
                gmail_con = gmail.GMail("email id", "app password")
                body = f'''Welcome to SBI bank !!
Someone tried to transfer balance.
If not you then change password immediately.

OTP for transfer verification is: {otp}
                '''
                mail= gmail.Message(to= to, subject="verification", text=body)
                gmail_con.send(mail)
                messagebox.showinfo('verification','otp sent to your mail enter to verify') 

            except:
                messagebox.showerror('verification', 'error occured while sending otp')

            otpsend_btn.destroy()         
            otp_entry.place(relx=.32, rely=.4)
            otp_verify_btn.place(relx=.36, rely=.76, relheight=.13)
                      
        def verify_otp():
            entd_otp = int(otp_entry.get())
            if(entd_otp==otp):
                msg_label.destroy()
                otp_entry.destroy()
                otp_verify_btn.destroy()
                messagebox.showinfo('verification','verified')

                to_acn_label.place(relx=.3, rely=.3)
                to_acn_entry.place(relx=.3, rely=.4)
                amt_label.place(relx=.3, rely=.55)
                amt_entry.place(relx=.3, rely=.65)
                transfer_btn.place(relx=.4, rely=.76, relheight=.13)
                

            else:
                messagebox.showerror('verification','incorrect otp')
       
    #transferring balance
        def transfer_bal():
            txnamt = int(amt_entry.get())
            to_acn = int(to_acn_entry.get())
            if(to_acn==int(uacn)):
                messagebox.showerror('transfer',"sender and receiver can't be same")
                return
            if(txnamt<=0):
                messagebox.showerror('transfer',f"Please enter valid amount \nNegative or zero amount can't be transferred.")
                return
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            receiver = cur_obj.execute('select * from users where users_account=?',(to_acn,)).fetchone()
            balance = cur_obj.execute('select users_balance from users where users_account=?',(uacn,)).fetchone()[0]
            con_obj.close()

            if( txnamt>balance ):
                messagebox.showerror('transfer',"insuffient balance")
                return
            if(receiver==None):
                messagebox.showerror('tranfer',"invalid receiver")
                return
            
            con_obj = sqlite3.connect(database='bank.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute('update users set users_balance= users_balance + ? where users_account=?',(txnamt,to_acn))
            cur_obj.execute('update users set users_balance= users_balance- ? where users_account=?',(txnamt, uacn))

            # maintaing transaction history for both accounts

            cur_obj.execute('insert into txn (txn_acn, txn_type, txn_date, txn_amount, txn_updatebalance) values(?,?,?,?,?)',
                        (uacn,'Db(-)',time.strftime('%d-%b-%Y %r'), txnamt, balance-txnamt) )
            cur_obj.execute('insert into txn (txn_acn, txn_type, txn_date, txn_amount, txn_updatebalance) values(?,?,?,?,?)',
                        (to_acn,'Cr(+)',time.strftime('%d-%b-%Y %r'), txnamt, receiver[5] + txnamt) )
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('transfer',f'rupees {txnamt} transferred to {receiver[2]}. \n remaining balance is:{balance-txnamt}')
        
        # initial labels and entry box
        msg = 'otp verification is required to transfer balance'
        msg_label = Label(ifrm, text=msg,font=('arial',15,'bold'), fg='red', bg='white')
        msg_label.place(relx=.25, rely=.15)
        otpsend_btn = Button(ifrm, width= 10, command= send_otp, font=('arial', 20, 'bold'), text="verify", bg='light green', bd=4,  )
        otpsend_btn.place(relx= .37, rely= .48, relheight= .15)
        # otp entry box and button
        otp_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        otp_verify_btn= Button(ifrm, width= 10, command= verify_otp, font=('arial', 20, 'bold'), text="submit", bg='light green', bd=4,  )

        # receiver account and amount entrybox and label
        to_acn_label = Label(ifrm, text="to account", font=('arial', 18, 'normal'), bg='white')
        to_acn_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)

        amt_label = Label(ifrm, text="amount", font=('arial', 18, 'normal'), bg='white')
        amt_entry = Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        transfer_btn = Button(ifrm, width= 10 ,command=transfer_bal, font=('arial', 20, 'bold'), text="transfer", bg='light green', bd=4,  )
        
    def history_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white')
        ifrm.place(relx=.27, rely=.2, relwidth=.5, relheight=.7)

        title_ifrm = Label(ifrm,text= "transaction history", font=('arial', 18, 'bold'), bg='white', fg='red')
        title_ifrm.pack()

        # create a frame for table
        tb_frm = Frame(ifrm, highlightbackground='black', highlightthickness=2,  )
        tb_frm.place(relx=.05, rely=.1, relwidth=.99)

        # data
        con_obj= sqlite3.connect('bank.sqlite')
        cur_obj = con_obj.cursor()
        cur_obj.execute('select * from txn where txn_acn=? order by txn_date ',(uacn,))

        data = {}
        i=1
        for tup in cur_obj:
            data.update({
                    f'{i}':
                    {'txn id':f'{tup[0]}', 'txn type':f'{tup[2]}','txn date':f'{tup[3]}',
                      'amount':f'{tup[4]}', 'bal left': f'{tup[5]}'}
            })
            i=i+1
        con_obj.close()
        # create table model
        model = TableModel()
        model.importDict(data)

        # create canvas inside frame
        table = TableCanvas(tb_frm, model=model, editable=True)
        table.show()

#logout button
    logout_btn = Button(frm, text='logout', font=('arial', 20, 'bold'), bg='light green', bd=4, command= logout_click)
    logout_btn.place(relx=.915, rely=0)

# left side
#view account details
    chk_bal_btn = Button(frm, command= view_details, text='view details', font=('arial', 20, 'bold'), bg='light blue', bd=4)
    chk_bal_btn.place(relx=.03, rely=.30)
    
#update details
    update_btn = Button( frm, text='update details', font=('arial', 20, 'bold'), bg='light blue', bd=4, command=update_click )
    update_btn.place(relx=.03, rely=.45)

#deposit
    deposit_btn = Button(frm, text='deposit', font=('arial', 20, 'bold'), bg='green',fg='white', bd=4, command=deposit_click )
    deposit_btn.place(relx=.03, rely=.6)
    
#right side
#withdraw
    withdraw_btn = Button(frm, text='withdraw', font=('arial', 20, 'bold'), bg='red',fg='white', bd=4, command=withdraw_click )
    withdraw_btn.place(relx=.85, rely=.3)

#transfer
    trans_btn = Button(frm, text="transfer", font=('arial', 20, 'bold'), bg='red',fg='white', bd=4,command=transfer_click)
    trans_btn.place(relx=.85, rely=.45)

#view transaction
    transaction_btn = Button(frm,command=history_click, text='transactions', font=('arial', 20, 'bold'), bg='green',fg='white', bd=4,  )
    transaction_btn.place(relx=.85, rely=.6)

#admin page
def admin_welcome_page():
    frm = Frame(win, highlightbackground='red', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.2, relheight=.7, relwidth=1)

    admin_title = Label(frm, text="Welcome, Admin", font=('arial', 20, 'bold'), bg='pink', fg='blue')
    admin_title.place(relx=.03, rely=0)

    def create_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white')
        ifrm.place(relx=.25, rely=.2, relwidth=.6, relheight=.52)

        title_ifrm = Label(ifrm,text="create user", font=('arial', 18, 'bold'), bg='white', fg='purple')
        title_ifrm.pack()
        
        def open_account():
            uname = name_entry.get()
            umobile = mobile_entry.get()
            uemail = email_entry.get()
            uaadhar = aadhar_entry.get()
            ubalance = 0
            upassword = str(random.randint(100000,999999))

            if(not uname.strip()):
                messagebox.showerror('account open',"invalid name")
                return
            elif(not umobile.isdigit() or len(umobile)!=10):
                messagebox.showerror('account open',"invalid mobile number")
                return
            elif(not uemail.strip()):
                messagebox.showerror('account open',"invalid email")
                return
            if(not uaadhar.strip()):
                messagebox.showerror('account open',"invalid aadhar")
                return
            
            #  verify email by sending otp
            otp= random.randint(1000,9999)
            print(otp)
            #  sending otp
            try:
                gmail_con= gmail.GMail("email id", "app password")
                umsg= f'''Welcome to SBI Bank!!\n\n
otp is: {otp}
                '''
                msg = gmail.Message(to=uemail,subject="verification",text= umsg)
                gmail_con.send(msg)
            except:
                messagebox.showerror('account open','problem occured try later')
                return
            # verifying otp
            def verify(otp):
                    uotp = simpledialog.askinteger('otp','enter otp from email')
                    if(uotp==otp): return True
                    else: return False

            if(verify(otp) or verify(otp) or verify(otp) ):
                    messagebox.showinfo('account open', 'otp verified')
            else: 
                messagebox.showerror('verification','invalid otp')
                return
            
            # opening account
            try:
                con_obj = sqlite3.connect(database = 'bank.sqlite')
                cur_obj = con_obj.cursor()
                cur_obj.execute(
                    '''insert into users(users_password, users_name, users_mobile, users_email, 
                    users_balance, users_aadhar, users_opendate) values (?,?,?,?,?,?,?)''',
                             (upassword, uname, umobile, uemail, ubalance, uaadhar,current_date) )
                con_obj.commit()
                uaccount = cur_obj.execute('select  users_account from users where users_email=?',(uemail,)).fetchone()[0]
                con_obj.close()
                messagebox.showinfo('account open',f'account opened successfully!! \nYou will get account and password on given email')
            except Exception as e:
                print(e)
                messagebox.showerror('account open',f'user exist.\nemail, mobile, aadhar all three should be unique')
                return
            # sending details
            print(f"account: {uaccount} \npassword: {upassword}, \nemail id: {uemail}")
            mail_password(uname, uaccount, upassword, uemail)
            
        def mail_password(uname,uaccount, upassword, uemail):
            gmail_con = gmail.GMail("email id", "app password")
            umsg = f'''Hello, {uname}
            Welcome to State Bank of India  !!!\n
Your account number is: {uaccount}.
Your password is: {upassword}
Kindly change your password as soon you login.

Thanks
            '''
            msg = gmail.Message(to=uemail, subject='Account Open', text=umsg)
            gmail_con.send(msg)

        def reset():
            name_entry.delete(0,'end')
            aadhar_entry.delete(0,'end')
            mobile_entry.delete(0,'end')
            email_entry.delete(0,'end')

        name_label= Label(ifrm, text="name", font=('arial', 18, 'normal'), bg='white')
        name_label.place(relx=.04, rely=.2)
        name_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        name_entry.place(relx=.04, rely=.34)

        aadhar_label = Label(ifrm, text="addhar", font=('arial', 18, 'normal'), bg='white')
        aadhar_label.place(relx=.54, rely=.2)
        aadhar_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        aadhar_entry.place(relx=.54, rely=.34)

        mobile_label = Label(ifrm, text="mobile", font=('arial', 18, 'normal'), bg='white')
        mobile_label.place(relx=.04, rely=.5)
        mobile_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        mobile_entry.place(relx=.04, rely=.62)

        email_label = Label(ifrm, text="email", font=('arial', 18, 'normal'), bg='white')
        email_label.place(relx=.54, rely=.5)
        email_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        email_entry.place(relx=.54, rely=.62)

        open_btn = Button(ifrm, width= 6,command= open_account , font=('arial', 20, 'bold'), text="open", bg='light green', bd=4,  )
        open_btn.place(relx=.73, rely=.8, relheight=.18)

        reset_btn = Button(ifrm,command=reset, width= 6 , font=('arial', 20, 'bold'), text="reset", bg='light green', bd=4,  )
        reset_btn.place(relx=.6, rely=.8, relheight=.18)

    def view_click():
        ifrm =Frame( frm , highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white' )
        ifrm.place(relx=.25, rely=.2, relwidth=.6, relheight=.52 )

        title_ifrm = Label(ifrm,text="view user", font=('arial', 18, 'bold'), bg='white', fg='purple')
        title_ifrm.pack()

        def view():
            user_acn = acn_entry.get()
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            tup = cur_obj.execute('select * from users where users_account=?',(user_acn,)).fetchone()
            con_obj.close()
            if(tup==None):
                messagebox.showerror('admin view','invalid account')
                return
            else:
                acn_label.destroy()
                acn_entry.destroy()
                view_btn.destroy()
                reset_btn.destroy()
                show(user_acn)

# fetching data from database for filling into entry box
        def show(user_acn):
                con_obj = sqlite3.connect(database='bank.sqlite')
                cur_obj = con_obj.cursor()
                cur_obj.execute('select * from users where users_account=?', (user_acn,))
                tup = cur_obj.fetchone()
                cur_obj.close()
                
                balance_label = Label(ifrm, text=f"Balance:\t{tup[5]}", font=('arial', 18, 'normal'), bg='white')
                balance_label.place(relx=.04, rely=.2)
                accountno_label = Label(ifrm, text=f"Account Number:\t{tup[0]}", font=('arial', 18, 'normal'), bg='white')
                accountno_label.place(relx=.5, rely=.2)

                name_label = Label(ifrm, text=f"Name:\t{tup[2]}", font=('arial', 18, 'normal'), bg='white')
                name_label.place(relx=.04, rely=.35)
                pass_label = Label(ifrm, text=f"Password:\t{tup[1]}", font=('arial', 18, 'normal'), bg='white')
                pass_label.place(relx=.5, rely=.35)

                mobile_label = Label(ifrm, text=f"Mobile:\t{tup[3]}", font=('arial', 18, 'normal'), bg='white')
                mobile_label.place(relx=.04, rely=.5)
                email_label = Label(ifrm, text=f"Email:\t{tup[5]}", font=('arial', 18, 'normal'), bg='white')
                email_label.place(relx=.5, rely=.5)

                aadhar_label = Label(ifrm, text=f"Aadhar:\t{tup[6]}", font=('arial', 18, 'normal'), bg='white')
                aadhar_label.place(relx=.04, rely=.65)
                opndate_label = Label(ifrm, text=f"A/c Open Date: {tup[7]}", font=('arial', 18, 'normal'), bg='white')
                opndate_label.place(relx=.5, rely=.65)
# reset
        def reset():
            acn_entry.delete(0,'end')

        acn_label= Label(ifrm, text="account number", font=('arial', 18, 'normal'), bg='white')
        acn_label.place(relx=.4, rely=.3)
        acn_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        acn_entry.place(relx=.35, rely=.42)
        acn_entry.focus()

        view_btn = Button(ifrm,command=view, width= 6 , font=('arial', 20, 'bold'), text="view", bg='light green', bd=4,  )
        view_btn.place(relx=.36, rely=.65, relheight=.18)

        reset_btn = Button(ifrm,command=reset, width= 6, text="reset", font=('arial',20, 'bold'), bd=4, bg='light green', )
        reset_btn.place(relx=.53, rely=.65, relheight=.18)
    
    def delete_click():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure( bg='white')
        ifrm.place(relx=.25, rely=.2, relwidth=.6, relheight=.52 )

        title_label = Label(ifrm,text="delete user", font=('arial', 18, 'bold'), bg='white', fg='purple')
        title_label.place(relx=.4, rely=0)

        def delete():
            user_acn = acn_entry.get()
            con_obj = sqlite3.connect('bank.sqlite')
            cur_obj = con_obj.cursor()
            tup = cur_obj.execute('select * from users where users_account=?',(user_acn,)).fetchone()
            if(tup == None):
                con_obj.close()
                messagebox.showerror('delete','invalid account')
            else:
                cur_obj.execute('delete from users where users_account=?',(user_acn,))
                con_obj.commit()
                con_obj.close()
                messagebox.showinfo('delete', f'account: {user_acn} deleted successfully')

        def reset():
            acn_entry.delete(0,'end')

        acn_label= Label(ifrm, text="account number", font=('arial', 18, 'normal'), bg='white')
        acn_label.place(relx=.4, rely=.3)
        acn_entry= Entry(ifrm, width=20, font=('arial', 18, 'normal'), bd=4)
        acn_entry.place(relx=.35, rely=.42)
        acn_entry.focus()

        delete_btn = Button(ifrm,command=delete, width= 6 , font=('arial', 20, 'bold'), text="delete", bg='light green', bd=4,  )
        delete_btn.place(relx=.36, rely=.65, relheight=.18)

        reset_btn = Button(ifrm,command=reset, width= 6, text="reset", font=('arial',20, 'bold'), bd=4, bg='light green', )
        reset_btn.place(relx=.53, rely=.65, relheight=.18)

    def logout_click():
        frm.destroy()
        main_screen()

#logout btn
    logout_btn = Button(frm, command=logout_click, text='logout', font=('arial', 20, 'bold'), bg='light green', bd=4)
    logout_btn.place(relx=.915, rely=0)

#create user btn
    create_btn = Button(frm, command=create_click, text='create user', font=('arial', 20, 'bold'), bg='green',fg='white', bd=4 )
    create_btn.place(relx=.03, rely=.2)

#view user btn
    view_btn = Button(frm, command=view_click, text='view user', font=('arial', 20, 'bold'), bg='light blue', bd=4 )
    view_btn.place(relx=.03, rely=.35)
    
#delete user btn
    delete_btn = Button(frm, command= delete_click, text='delete user', font=('arial', 20, 'bold'),fg='white', bg='red', bd=4 )
    delete_btn.place(relx=.03, rely=.5)

#password recovery page
def forgot_password_page():
    frm = Frame(win, highlightbackground='red', highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.2, relheight=.7, relwidth=1)

    def back_click():
        frm.destroy()
        main_screen()

    def get_password():

        uentry = entry.get()

        #fetching password from database
        con_obj = sqlite3.connect(database='bank.sqlite')
        cur_obj = con_obj.cursor()     
        ifacn = cur_obj.execute('select users_email, users_password from users where users_account=?',(uentry,)).fetchone()
        ifmob = cur_obj.execute('select users_email, users_password from users where users_mobile=?',(uentry,)).fetchone()
        ifemail = cur_obj.execute('select users_email, users_password from users where users_email=?',(uentry,)).fetchone()
        con_obj.close()
        
        if(ifacn!=None):
            mail_password(ifacn[0],ifacn[1])
        elif(ifmob!=None):
            mail_password(ifmob[0],ifmob[1])
        elif(ifemail!=None):
            mail_password(ifemail[0], ifemail[1])

    def mail_password(to, password):
        print(password)
        try:
            gmail_con = gmail.GMail("email id", "app password")
            body = f'''Welcome to State Bank !!!

                Your password is: {password}
                '''
            msg = gmail.Message(to=to, subject='Password Recovery', text= body)
            gmail_con.send(msg)
            messagebox.showinfo('password recovery',f'password sent to mail {to}')
        except:
            messagebox.showerror('password error','error occured while sending mail')
        back_click()

    #back button
    back_btn = Button(frm, command= back_click , text='back', font=('arial',20,'bold'))
    back_btn.place(relx= 0, rely= 0)

    #entry label, entry box and button
    account_label= Label(frm, font=('arial', 20, 'bold'), bg='pink', text='enter account/mobile/email:')
    account_label.place(relx=.3, rely=.3 )
    entry = Entry(frm, font=('arial', 20, 'normal'), bd=4)
    entry.place(relx=.3, rely=.45)

    submit_btn = Button(frm, text="submit", command=get_password, font=('arial',20, 'bold'), bd=4, bg='light green',width=8)
    submit_btn.place(relx=.38, rely=.6, relheight=.13)


main_screen()
win.mainloop()
