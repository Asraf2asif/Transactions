import tkinter
import re
import sqlite3
from collections import Counter

def placement(element, row=0, column=0,  sticky='nw', padx=(10,0), pady=(0,0), ipady=0, border=2, relief='groove'):
        element.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady, ipady=ipady)
        element.config(border=border, relief=relief)
        

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
        
    query = 'INSERT INTO "Transaction" ('+ col_name + ') VALUES ('+ ques_input +')'
 
    if Counter(value)[0] != len(value): cur.execute(query, ([i for i in value]))

    con.commit()


def total():

    Total = []

    input_name_part = input1_name[4:6] +  input2_name[0:4]
    
    for name in input_name_part:
        cur.execute('SELECT sum("{}") FROM "Transaction"'.format(name, ))
        Total.append(int(cur.fetchone()[0]))

    Total_Hand = Total[0] + Total[1]
    Total_Comp = Total[2] + Total[3] + Total[4] + Total[5]
    
    reset()   
    
    for i in range(2):
            if Total[i] != 0:
                    output_value1[i].insert(0, '{:,}'.format(Total[i]))  
    for i in range(2,6):
            if Total[i] != 0:
                    output_value2[i-1].insert(0, '{:,}'.format(Total[i]))

    output_value1[3].insert(0, '{:,}'.format(Total_Hand))       
    output_value2[5].insert(0, '{:,}'.format(Total_Comp))
    
    balance_value.insert(0, '{:,}'.format(Total_Comp - Total_Hand))

    for el in (output_value):   el.config(state='readonly')
    balance_value.config(state='readonly')   
    

def reset():
    
    for el in output_value:   el.config(state='normal')
    balance_value.config(state='normal')
    
    for el in (input_entry + output_value):  el.delete(0, tkinter.END)
    balance_value.delete(0, tkinter.END)
  

def submit():

    insert_input()
    
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

    styleOpts1 = { 'width' : 12,  'justify' : 'center' }

    input_regex = re.compile (r'^[-+]?[\d]*\.?[\d]+$')


# Element
    input_button1 = [tkinter.Button(input_frame, text=name, width=10, height=1, bg='#71c9ce', fg='black') for name in input1_name]
    input_button2 = [tkinter.Button(input_frame, text=name, width=10, height=1, bg='#71c9ce') for name in input2_name]

    input_entry1 = [tkinter.Entry(input_frame, textvariable=name+"_var",  bg='#d3d4d8', **styleOpts1) for name in input1_name]
    input_entry2 = [tkinter.Entry(input_frame, textvariable=name+"_var",  bg='#d3d4d8', **styleOpts1) for name in input2_name]
    
    output_label1 = [tkinter.Label(output_frame, text=name, width=12,  anchor="w", bg='#ffa5a5') for name in output1_name]
    output_label2 = [tkinter.Label(output_frame, text=name, width=12,  anchor="w", bg='#eab4f8') for name in output2_name]
    
    output_value1 = [tkinter.Entry(output_frame, state='readonly', bg='#d3d4d8', **styleOpts1) for name in output1_name]
    output_value2 = [tkinter.Entry(output_frame, state='readonly', **styleOpts1) for name in output2_name]

        
    thousand_shorthand_var = tkinter.IntVar()
    thousand_shorthand =  tkinter.Checkbutton(input_frame, text="(000)?", variable=thousand_shorthand_var, bg='#4ecca3')
    placement(element=thousand_shorthand, row=4, column=1,  pady=(30,0))
    
    input_name = input1_name + input2_name
    input_entry = input_entry1 + input_entry2
    input_button = input_button1, input_button2
    
    output_name = output1_name + output2_name
    output_value = output_value1 + output_value2
    
    output_value1[3].config(font='Helvetica 8 bold')
    output_value2[5].config(font='Helvetica 8 bold')
    

# Database
    con=sqlite3.connect('../Transactions.db')
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS "Transaction" (
                            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "{0[0]}" REAL, "{0[1]}" REAL, "{0[2]}" REAL,"{0[3]}" REAL, "{0[4]}" REAL, "{0[5]}" REAL,
                            "{0[6]}" REAL, "{0[7]}" REAL, "{0[8]}" REAL,"{0[9]}" REAL, "{0[10]}" REAL, "{0[11]}" REAL)"""
                             .format(input1_name + input2_name))
    

 # Placement     
    input_frame.grid(row=0, column=0, padx=(30,100), pady=(40,0))
    output_frame.grid(row=0, column=1, pady=(40,0))

    for i, (ib1, ib2, ie1, ie2) in enumerate(list(zip(input_button1, input_button2, input_entry1, input_entry2))):
        placement(element=ib1, row=0, column=i)
        placement(element=ib2, row=2, column=i,  pady=(30,0))
        
        placement(element=ie1, row=1, column=i,  pady=(10,0), ipady=2, relief='sunken')
        placement(element=ie2, row=3, column=i,  pady=(10,0), ipady=2, relief='sunken')        

    for i, (ol1, ov1) in enumerate(list(zip(output_label1, output_value1))):   
        placement(element=ol1, row=i, column=0,  pady=(0 if i==0 else 10,0), ipady=4)
        placement(element=ov1, row=i, column=1, pady=(0 if i==0 else 10,0), ipady=4)

    for i, (ol2, ov2) in enumerate(list(zip(output_label2, output_value2))):  
        placement(element=ol2, row=i, column=2, padx=(40,0),  pady=(0 if i==0 else 10,0), ipady=4)                     
        placement(element=ov2, row=i, column=3, pady=(0 if i==0 else 10,0), ipady=4)

    
# Balance Button & Value
    balance_button = tkinter.Button(output_frame, text="Balance", width=11, anchor="w", bg='#f3f798')
    balance_value = tkinter.Entry(output_frame, width=12,  justify='center', font='Helvetica 8 bold', state='readonly')
    
    placement(element=balance_value, row=len(output_label1)+1, column=1,  pady=(10,0), ipady=4)
    placement(element=balance_button, row=len(output_value1)+1, column=0,  pady=(10,0), ipady=2)

    
# Submit Button
    submit_button = tkinter.Button(input_frame, text="Submit", width=10, height=1, command=submit, bg='#1891ac', fg='white')
    placement(element=submit_button, row=4, column=5,  pady=(30,0), ipady=2)


    try:  
        total()
    except:
        print("No Entry To Sum")

        
    mainWindow.mainloop()
