import tkinter
import re
import sqlite3
from collections import Counter
from datetime import date
from funct import *


def placement_input_entry(el, row):
    return placement(element=el, row=row, column=i, pady=(10, 0), ipady=2, relief='sunken')


def placement_output_entry(el, column, padx=(10, 0), pady=(10, 0)):
    return placement(element=el, row=i, column=column, padx=padx, pady=(0 if i == 0 else pady), ipady=4)

def for_cash(value):
    for i, vl in enumerate(value):
        if i in range(4) or not (thousand_shorthand_var.get()):
            value[i] = int(value[i])

    if thousand_shorthand_var.get():
        for i in range(4, len(value)):
            value[i] *= 1000
            
def r_p_input():    
    save_transaction(input_regex, r_p_value[0:-1], r_p_name[0:-1], r_p_table, cur, con,1,0)


def r_p_input_init():
    query = gen_query(r_p_name[0:-1], r_p_table)

    cur.execute(query, ([0 for i in r_p_name[0:-1]]))

    con.commit()


def insert_input():
    for i in enumerate(input_entry):
        if i in range(4) or not (thousand_shorthand_var.get()):
            cv_int=1
        else:
            cv_int=0
        
    save_transaction(input_regex, input_entry,  input_name, table_name,cur, con,cv_int,thousand_shorthand_var.get())
    

def sum_col(col, table, arr):
    cur.execute('SELECT sum("{}") FROM "{}"'.format(col, table))
    arr.append(int(cur.fetchone()[0]))


def convert_readonly_el():
    readonly_el = output_value1 + output_value2 + cash_value + [balance_value] + [r_p_value[6]]
    for el in readonly_el:
        convert_readonly(el)


def convert_normal_el():
    normal_el = output_value1 + output_value2 + cash_value + [balance_value] + [r_p_value[6]]
    for el in normal_el:
        convert_normal(el)


def convert_delete_el():
    delete_el = input_entry + output_value + cash_value + r_p_value + [balance_value]
    for el in delete_el:
        delete_value(el)


def total():
    # Arry
    Total = []

    Cash = []
    Cash_type = [1000, 500, 100, 1, 1, 1]

    # Column Name
    input_name_part = input1_name[4:6] + input2_name[0:4]

    input_name_cash = input1_name[0:4] + input2_name[4:6]

    # Query
    for name in input_name_part:
        sum_col(name, table_name, Total)

    for name in input_name_cash:
        sum_col(name, table_name, Cash)

    cur.execute('SELECT * FROM "{}" ORDER BY "ID" DESC LIMIT 1'.format(r_p_table))
    try:
        R_P = cur.fetchall()[0][1:]
    except:
        print("No Entry To Sum1")

    # Cash Details
    for ii, i in enumerate(range(2, 5)):
        cash_label[i].config(text=cash_detail[ii] + str(Cash[ii]))

    # Cash Adjustmaent
    for i, vl in enumerate(Cash_type):
        Cash[i] = Cash[i] * vl

    # Gross Value
    Total_Hand = sum(Total[0:2])
    Total_Cash = sum(Cash[0:6])
    Total_Hand += Total_Cash

    Total_Comp = sum(Total[2:6])
    r_p_closing = int(sum(R_P[0:5]) - R_P[5:6][0])
    Total_Comp += r_p_closing

    reset()

    # Insert Value
    insert_name = {cash_value[0]: Cash[4], cash_value[1]: Cash[5], cash_value[6]: Total_Cash,
                output_value1[2]: Total_Cash, output_value1[3]: Total_Hand, output_value2[0]: r_p_closing,
                output_value2[5]: Total_Comp,
                balance_value: Total_Hand - Total_Comp}

    for i in range(2):
        if Total[i] != 0:
            insert_value(output_value1[i], Total[i])

    for i in range(2, 6):
        if Total[i] != 0:
            insert_value(output_value2[i - 1], Total[i])

    for i, vl in enumerate(R_P[:-1]):
        insert_value(r_p_value[i], int(vl))
    insert_value(r_p_value[6], r_p_closing)

    for ii, i in enumerate(range(2, 6)):
        insert_value(cash_value[i], Cash[ii])

    for cell, vl in insert_name.items():
        insert_value(cell, vl)

    convert_readonly_el()

    search_id.grid_forget()


def reset():
    convert_normal_el()
    convert_delete_el()


def submit():
    insert_input()
    r_p_input()
    

    try:
        total()
    except:
        print("No Entry To Sum2")


if __name__ == "__main__":

    # Name
    input1_name = ["1000", "500", "100", "-", "Suspension", "Voucher"]
    input2_name = ["Bill", "Loan: R.", "Loan: PCT", "Income V.", "Bundle L.", "Bundle S."]

    output1_name = [" Suspense Total", " Voucher Total", " Cash Total", " Total (Hand)"]
    output2_name = [" R/P (C/D)", " T. Bill", " T. Loan: R.", " T. Loan: PCT", " T. Income V.", " Total (Comp.)"]

    cash_name = [" Bundle L.", " Bundle S.", " 1000", " 500", " 100", " Others", " Total (Cash)"]
    cash_detail = ["  1000 X ", "  500 X ", "  100 X "]

    r_p_name = [" R/P (B/D)", " (+) I.V. & Loan", " (+) Bill (Pre)", " (+) Reception I.", " (+) Pharmacy I.",
                " (-) Posted V.", " R/P (C/D)"]

    styleOpts1 = {'width': 12, 'justify': 'center'}
    styleBold = {'font': 'Helvetica 8 bold'}
    styleIW = {'width': 10}
    styleID = {'width': styleOpts1['width'], 'font': styleBold['font']}

    input_regex = re.compile(r'^[-+]?[\d]*\.?[\d]+$')

    color = ['#eaeaea', '#71c9ce', '#d3d4d8', '#ffa5a5', '#eab4f8', '#4ecca3']

    # Main  Window
    mainWindow = tkinter.Tk()
    mainWindow.config(bg='#eaeaea')
    mainWindow.title("Transaction:-  EPK International (Pvt) Ltd.")
    mainWindow.geometry('1165x680+30+0')

    # Frame
    input_frame = tkinter.Frame(mainWindow, bg=color[0])
    output_frame = tkinter.Frame(mainWindow, bg=color[0])


    def arrayCalc(arr, fn):
        arrRes = [fn(name) for name in arr]
        return arrRes


    def create_input_button(name):
        return tkinter.Button(input_frame, text=name, height=1, cursor="hand2", **styleIW)


    def create_input_entry(name):
        return tkinter.Entry(input_frame, textvariable=name + "_var", **styleOpts1)


    def create_input_entry2(name):
        return tkinter.Entry(output_frame, textvariable=name + "_var", **styleOpts1)


    def create_input_entryRP(name):
        return tkinter.Entry(output_frame, **styleOpts1)


    def create_output_label(name):
        return tkinter.Label(output_frame, text=name, width=styleOpts1['width'], anchor="w")


    # Element
    input_button1 = arrayCalc(input1_name, create_input_button)
    input_button2 = arrayCalc(input2_name, create_input_button)

    input_entry1 = arrayCalc(input1_name, create_input_entry)
    input_entry2 = arrayCalc(input2_name, create_input_entry)

    output_label1 = arrayCalc(output1_name, create_output_label)
    output_label2 = arrayCalc(output2_name, create_output_label)

    cash_label = arrayCalc(cash_name, create_output_label)
    r_p_label = arrayCalc(r_p_name, create_output_label)

    output_value1 = arrayCalc(output1_name, create_input_entry2)
    output_value2 = arrayCalc(output2_name, create_input_entry2)

    cash_value = arrayCalc(cash_name, create_input_entry2)
    r_p_value = arrayCalc(r_p_name, create_input_entryRP)

    thousand_shorthand_var = tkinter.IntVar()
    thousand_shorthand = tkinter.Checkbutton(input_frame, text="(000)?", variable=thousand_shorthand_var, bg=color[5],
                                            cursor="hand2")

    balance_button = tkinter.Button(output_frame, text="Balance", width=11, anchor="w", bg='#f3f798', cursor="hand2")
    balance_value = tkinter.Entry(output_frame, width=12, justify='center', state='readonly', **styleBold)

    submit_button = tkinter.Button(input_frame, text="Submit", width=10, height=1, command=submit, bg='#1891ac',
                                fg='white', cursor="hand2")

    def colorize(els, clr):
        for el in els:
            el.config(bg=clr)
        
    # Color
    colorize(input_button1 + input_button2, color[1])
    colorize(input_entry1 + input_entry2, color[2])
    colorize(output_label1, color[3])
    colorize(output_label2, color[4])
    colorize(cash_label, color[5])
    colorize(r_p_label, color[1])


    input_name = input1_name + input2_name
    input_entry = input_entry1 + input_entry2
    input_button = input_button1, input_button2

    output_name = output1_name + output2_name
    output_value = output_value1 + output_value2

    bold_el = [output_value1[3], output_value2[5], cash_value[6], r_p_value[6]]
    for el in bold_el:
        el.config(**styleBold)

    convert_readonly_el()

    # Database
    today = date.today()
    date = today.strftime("%b-%d-%Y")
    table_name = "Transaction: " + str(date)
    r_p_table = "Receipt_Payment: " + str(date)

    con = sqlite3.connect('../Transactions.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS "{1}" (
                            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "{0[0]}" REAL, "{0[1]}" REAL, "{0[2]}" REAL,"{0[3]}" REAL, "{0[4]}" REAL, "{0[5]}" REAL,
                            "{0[6]}" REAL, "{0[7]}" REAL, "{0[8]}" REAL,"{0[9]}" REAL, "{0[10]}" REAL, "{0[11]}" REAL)"""
                .format(input_name, table_name))

    cur.execute("""CREATE TABLE IF NOT EXISTS "{1}" (
                            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "{0[0]}" REAL, "{0[1]}" REAL, "{0[2]}" REAL,"{0[3]}" REAL, "{0[4]}" REAL, "{0[5]}" REAL, "{0[6]}" REAL)"""
                .format(r_p_name, r_p_table))

    # Placement
    input_frame.grid(row=0, column=0, padx=(30, 100), pady=(15, 305))
    output_frame.grid(row=0, column=1, pady=(78, 0))

    for i, (ib1, ib2, ie1, ie2) in enumerate(list(zip(input_button1, input_button2, input_entry1, input_entry2))):
        placement(element=ib1, row=1, column=i)
        placement(element=ib2, row=3, column=i, pady=(30, 0))

        placement_input_entry(ie1, row=2)
        placement_input_entry(ie2, row=4)

    for i, (ol1, ov1) in enumerate(list(zip(output_label1, output_value1))):
        placement_output_entry(ol1, column=0)
        placement_output_entry(ov1, column=1)

    for i, (ol2, ov2) in enumerate(list(zip(output_label2, output_value2))):
        placement_output_entry(ol2, column=2, padx=(40, 0))
        placement_output_entry(ov2, column=3)

    for i, (cl, cv) in enumerate(list(zip(cash_label, cash_value))):
        i += len(output_label1) + 3
        placement_output_entry(cl, column=0, pady=((40, 0) if i == 7 else (10, 0)))
        placement_output_entry(cv, column=1, pady=((40, 0) if i == 7 else (10, 0)))

    for i, (rpl, rpv) in enumerate(list(zip(r_p_label, r_p_value))):
        i += len(output_label2) + 1
        placement_output_entry(rpl, column=2, padx=(40, 0), pady=((40, 0) if i == 7 else (10, 0)))
        placement_output_entry(rpv, column=3, pady=((40, 0) if i == 7 else (10, 0)))

    placement(element=thousand_shorthand, row=5, column=1, pady=(30, 0))

    placement(element=balance_value, row=len(output_label1) + 1, column=1, pady=(10, 0), ipady=4)
    placement(element=balance_button, row=len(output_value1) + 1, column=0, pady=(10, 0), ipady=2)

    placement(element=submit_button, row=5, column=5, pady=(30, 0), ipady=2)


    # Search (messy, latter must be fixed)

    def last_id():
        cur.execute('SELECT MAX("ID") from "{}"'.format(table_name))
        try:
            search_id_vl = int(cur.fetchall()[0][0])
        except:
            search_id_vl = 0
        return search_id_vl


    search_id_vl = last_id()
    search_id = tkinter.Label(input_frame, text=str(search_id_vl), width=6, pady=6, anchor="s", bg='#eaeaea')


    def search():
        placement(element=search_id, row=0, column=5, pady=(10, 20), padx=(30, 0))
        search_id.config(relief="flat", text=str(search_id_vl))

        cur.execute('SELECT * FROM "{}" WHERE "ID"=?'.format(table_name), (search_id_vl,))
        search_value = cur.fetchall()[0][1:]

        for i, el in enumerate(input_entry):
            delete_value(el)
            if search_value[i] != 0:
                insert_value(el, int(search_value[i]))


    def update_vl():
        value = gen_value(input_entry, input_regex)
        for_cash(value)

        for i in range(len(input_name)):
            query = 'UPDATE "{}" SET "{}"="{}" WHERE "ID" = ?'.format(table_name, input_name[i], value[i])

            cur.execute(query, (search_id_vl,))
            con.commit()
        total()


    def previous_entry():
        global search_id_vl
        if search_id_vl != 1:
            search_id_vl -= 1
            search()


    def next_entry():
        global search_id_vl

        if search_id_vl < last_id():
            search_id_vl += 1
            search()


    def last_entry():
        global search_id_vl

        search_id_vl = last_id()
        search()


    # img location
    img_search = tkinter.PhotoImage(file="icon/Search-icon.png")
    img_update = tkinter.PhotoImage(file="icon/Save-icon.png")
    img_previous = tkinter.PhotoImage(file="icon/Previous-icon.png")
    img_next = tkinter.PhotoImage(file="icon/Next-icon.png")
    img_refresh = tkinter.PhotoImage(file="icon/Refresh-icon.png")
    img_delete = tkinter.PhotoImage(file="icon/Delete-icon.png")


    def icon_btn(cmd, img):
        return tkinter.Button(input_frame, command=cmd, width=45, height=41, bg='#eaeaea', cursor="hand2", image=img)
    
    btn_cmd= [last_entry, update_vl, previous_entry, next_entry, total, total]
    btn_img= [img_search, img_update, img_previous, img_next, img_refresh, img_delete]
    
    btn_list = [icon_btn(icon_cmd, icon_img) for icon_cmd,icon_img in list(zip(btn_cmd, btn_img))]

    for i, el in enumerate(btn_list):
        placement(element=btn_list[i], row=0, column=0, padx=((60*(i+1)), 0), pady=(0, 15), ipady=2, columnspan=6)


    try:
        total()
    except:
        print("No Entry To Sum")

    mainWindow.mainloop()
