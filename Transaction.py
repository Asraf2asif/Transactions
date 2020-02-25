import tkinter
import re
import sqlite3
from collections import Counter
from datetime import date


def placement(element, row=0, column=0,  sticky='nw', padx=(10,0), pady=(0,0), ipady=0, border=2, relief='groove'):
        element.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady, ipady=ipady)
        element.config(border=border, relief=relief)


def placement_input_entry(el, row):
        return placement(element=el, row=row, column=i,  pady=(10,0), ipady=2, relief='sunken')


def placement_output_entry(el, column, padx=(10,0), pady=(10,0)):
        return placement(element=el, row=i, column=column, padx=padx, pady=(0 if i==0 else pady), ipady=4)
        

def r_p_input():
    r_p_input = [input_regex.search(el.get()) for el in r_p_value[0:-1] if el]
    value = [float(vl.group()) if vl else 0 for vl in  r_p_input]

    for i,vl in enumerate(value):
        value[i] = int(value[i])
            
    col_name=",".join(['"'+i+'"' for i in r_p_name[0:-1]])
    ques_input = ",".join(["?" for i in r_p_name[0:-1]])
        
    query = 'INSERT INTO "{}" ('.format(r_p_table) + col_name + ') VALUES ('+ ques_input +')'
 
    if Counter(value)[0] != len(value): cur.execute(query, ([i for i in value]))

    con.commit()


def insert_input():
    input_value = [input_regex.search(el.get()) for el in input_entry if el]
    value = [float(vl.group()) if vl else 0 for vl in  input_value]

    for i,vl in enumerate(value):
        if i in range(4) or not(thousand_shorthand_var.get()):
            value[i] = int(value[i])

    if thousand_shorthand_var.get():
        for i in range(4, len(value)):
            value[i] *= 1000
        
    col_name=",".join(['"'+i+'"' for i in input_name])
    ques_input = ",".join(["?" for i in input_name])
        
    query = 'INSERT INTO "{0}" ('.format(table_name) + col_name + ') VALUES ('+ ques_input +')'
 
    if Counter(value)[0] != len(value): cur.execute(query, ([i for i in value]))

    con.commit()


def total():

    Total = []
    Cash = []
    Cash_type = [1000, 500, 100, 1, 1, 1]

    input_name_part = input1_name[4:6] +  input2_name[0:4]
    input_name_cash = input1_name[0:4] +  input2_name[4:6]
    
    for name in input_name_part:
        cur.execute('SELECT sum("{}") FROM "{}"'.format(name, table_name))
        Total.append(int(cur.fetchone()[0]))

    for name in input_name_cash:
        cur.execute('SELECT sum("{}") FROM "{}"'.format(name, table_name))
        Cash.append(int(cur.fetchone()[0]))

    cur.execute('SELECT * FROM "{}" ORDER BY "ID" DESC LIMIT 1'.format(r_p_table))
    
    try:
        R_P = cur.fetchall()[0][1:]
    except:
        R_P = [0]*7
    
    cash_label[2].config(text="  1000 X " + str(Cash[0]))
    cash_label[3].config(text="  500 X " + str(Cash[1]))
    cash_label[4].config(text="  100 X " + str(Cash[2]))
    
    for i, vl in enumerate(Cash_type): Cash[i] = Cash[i] * vl
    
    Total_Hand = sum(Total[0:2])
    Total_Comp = sum(Total[2:6])
    Total_Cash = sum(Cash[0:6])
    Total_Hand += Total_Cash
    
    reset()   
    
    for i in range(2):
            if Total[i] != 0:
                    output_value1[i].insert(0, '{:,}'.format(Total[i]))
                    
    for i in range(2,6):
            if Total[i] != 0:
                    output_value2[i-1].insert(0, '{:,}'.format(Total[i]))

    for i,vl in enumerate(R_P[:-1]):
        r_p_value[i].insert(0, '{:,}'.format(int(vl)))
        
    r_p_closing = int(sum(R_P[0:5]) - R_P[5:6][0])
    Total_Comp += r_p_closing
    
    r_p_value[6].insert(0, '{:,}'.format(r_p_closing))
    
    for ii,i in enumerate(range(2,6)):
        cash_value[i].insert(0, '{:,}'.format(Cash[ii]))
                    
    cash_value[0].insert(0, '{:,}'.format(Cash[4]))
    cash_value[1].insert(0, '{:,}'.format(Cash[5]))
    cash_value[6].insert(0, '{:,}'.format(Total_Cash))
    
    output_value1[2].insert(0, '{:,}'.format(Total_Cash))
    output_value1[3].insert(0, '{:,}'.format(Total_Hand))
    output_value2[0].insert(0, '{:,}'.format(r_p_closing))
    output_value2[5].insert(0, '{:,}'.format(Total_Comp))
     
    balance_value.insert(0, '{:,}'.format(Total_Hand - Total_Comp))

    for el in (output_value):   el.config(state='readonly')
    for el in (cash_value):   el.config(state='readonly')
    balance_value.config(state='readonly')
    r_p_value[6].config(state='readonly')
    
    
def reset():
    
    for el in output_value:   el.config(state='normal')
    for el in cash_value:   el.config(state='normal')
    balance_value.config(state='normal')
    r_p_value[6].config(state='normal')
    
    for el in (input_entry + output_value):  el.delete(0, tkinter.END)
    for el in (cash_value):  el.delete(0, tkinter.END)
    for el in (r_p_value):  el.delete(0, tkinter.END)
    balance_value.delete(0, tkinter.END)
  

def submit():

    insert_input()
    r_p_input()
    
    try:  
        total()
    except:
        print("No Entry To Sum")


if __name__ == "__main__":
    mainWindow = tkinter.Tk()
    mainWindow.config(bg='#eaeaea')
    mainWindow.title("Transaction:-  EPK International (Pvt) Ltd.")
    mainWindow.geometry('1165x680+30+0')


# Frame
    input_frame = tkinter.Frame(mainWindow, bg='#eaeaea')
    output_frame = tkinter.Frame(mainWindow, bg='#eaeaea')


# Name
    input1_name = ["1000","500","100","-","Suspension","Voucher"]
    input2_name= ["Bill", "Loan: R", "Loan: PCT", "Income V", "Bundle L", "Bundle S"]
    
    output1_name = [" Suspense Total", " Voucher Total", " Cash Total", " Total (Hand)"]
    output2_name = [" R/P (C/D)", " T. Bill"," T. Loan: R.", " T. Loan: PCT", " T. Income V.", " Total (Comp.)"]

    cash_name = [" Bundle L.", " Bundle S."," 1000", " 500", " 100", " Others"," Total (Cash)"]
    r_p_name = [" R/P (B/D)", " I.V. & Loan"," Bill (Pre)", " Reception I.", " Pharmacy I.", " Posted V."," R/P (C/D)"]

    styleOpts1 = { 'width' : 12,  'justify' : 'center' }
    styleBold = { 'font' : 'Helvetica 8 bold'}

    input_regex = re.compile (r'^[-+]?[\d]*\.?[\d]+$')


# Element
    input_button1 = [tkinter.Button(input_frame, text=name, width=10, height=1, bg='#71c9ce', fg='black', cursor="hand2") for name in input1_name]
    input_button2 = [tkinter.Button(input_frame, text=name, width=10, height=1, bg='#71c9ce', cursor="hand2") for name in input2_name]

    input_entry1 = [tkinter.Entry(input_frame, textvariable=name+"_var",  bg='#d3d4d8', **styleOpts1) for name in input1_name]
    input_entry2 = [tkinter.Entry(input_frame, textvariable=name+"_var",  bg='#d3d4d8', **styleOpts1) for name in input2_name]
    
    output_label1 = [tkinter.Label(output_frame, text=name, width=12,  anchor="w", bg='#ffa5a5') for name in output1_name]
    output_label2 = [tkinter.Label(output_frame, text=name, width=12,  anchor="w", bg='#eab4f8') for name in output2_name]

    cash_label = [tkinter.Label(output_frame, text=name, width=12,  anchor="w", bg='#4ecca3') for name in cash_name]
    r_p_label = [tkinter.Label(output_frame, text=name, width=12,  anchor="w", bg='#71c9ce') for name in r_p_name]
    
    output_value1 = [tkinter.Entry(output_frame, state='readonly', **styleOpts1) for name in output1_name]
    output_value2 = [tkinter.Entry(output_frame, state='readonly', **styleOpts1) for name in output2_name]

    cash_value = [tkinter.Entry(output_frame, state='readonly', **styleOpts1) for name in cash_name]
    r_p_value = [tkinter.Entry(output_frame, **styleOpts1) for name in r_p_name]

        
    thousand_shorthand_var = tkinter.IntVar()
    thousand_shorthand =  tkinter.Checkbutton(input_frame, text="(000)?", variable=thousand_shorthand_var, bg='#4ecca3', cursor="hand2")
    placement(element=thousand_shorthand, row=4, column=1,  pady=(30,0))
    
    input_name = input1_name + input2_name
    input_entry = input_entry1 + input_entry2
    input_button = input_button1, input_button2
    
    output_name = output1_name + output2_name
    output_value = output_value1 + output_value2
    
    output_value1[3].config(**styleBold)
    output_value2[5].config(**styleBold)
    cash_value[6].config(**styleBold)
    r_p_value[6].config(state='readonly', **styleBold)
    

# Database
    today = date.today()
    date = today.strftime("%b-%d-%Y")
    table_name = "Transaction: " + str(date)
    r_p_table = "Receipt_Payment: " + str(date)
    
    con=sqlite3.connect('../Transactions.db')
    cur=con.cursor()
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
    input_frame.grid(row=0, column=0, padx=(30,100), pady=(40,305))
    output_frame.grid(row=0, column=1, pady=(40,0))
    
    
    for i, (ib1, ib2, ie1, ie2) in enumerate(list(zip(input_button1, input_button2, input_entry1, input_entry2))):
        placement(element=ib1, row=0, column=i)
        placement(element=ib2, row=2, column=i,  pady=(30,0))
        
        placement_input_entry(ie1, row=1)
        placement_input_entry(ie2, row=3)    

    for i, (ol1, ov1) in enumerate(list(zip(output_label1, output_value1))):
        placement_output_entry(ol1, column=0)
        placement_output_entry(ov1, column=1)
        
    for i, (ol2, ov2) in enumerate(list(zip(output_label2, output_value2))):
        placement_output_entry(ol2, column=2, padx=(40,0))
        placement_output_entry(ov2, column=3)

    for i, (cl, cv) in enumerate(list(zip(cash_label, cash_value))):
        i+=len(output_label1) + 3
        placement_output_entry(cl, column=0, pady=((40,0) if i==7 else (10,0)))
        placement_output_entry(cv, column=1, pady=((40,0) if i==7 else (10,0)))
        
    for i, (rpl, rpv) in enumerate(list(zip(r_p_label, r_p_value))):
        i+=len(output_label2) + 1
        placement_output_entry(rpl, column=2, padx=(40,0), pady=((40,0) if i==7 else (10,0)))
        placement_output_entry(rpv, column=3, pady=((40,0) if i==7 else (10,0)))
    
# Balance Button & Value
    balance_button = tkinter.Button(output_frame, text="Balance", width=11, anchor="w", bg='#f3f798', cursor="hand2")
    balance_value = tkinter.Entry(output_frame, width=12,  justify='center',  state='readonly', **styleBold )
    
    placement(element=balance_value, row=len(output_label1)+1, column=1,  pady=(10,0), ipady=4)
    placement(element=balance_button, row=len(output_value1)+1, column=0,  pady=(10,0), ipady=2)

    
# Submit Button
    submit_button = tkinter.Button(input_frame, text="Submit", width=10, height=1, command=submit, bg='#1891ac', fg='white', cursor="hand2")
    placement(element=submit_button, row=4, column=5,  pady=(30,0), ipady=2)


    try:  
        total()
    except:
        print("No Entry To Sum")

        
    mainWindow.mainloop()
