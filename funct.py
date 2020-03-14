import tkinter
import re
import sqlite3
from collections import Counter
from datetime import date

def placement(element, row=0, column=0, sticky='nw', padx=(10, 0), pady=(0, 0), ipady=0, columnspan=1,                                                                                                                                             border=2, relief='groove'):
    
    element.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady, ipady=ipady, columnspan=columnspan)
    element.config(border=border, relief=relief)


def gen_value(cell, regex):
    input_value = [regex.search(el.get().replace(',', '')) for el in cell if el]
    value = [float(vl.group()) if vl else 0 for vl in input_value]

    return value


def col_name(col):
    col_name = ",".join(['"' + i + '"' for i in col])
    return col_name


def ques_input(col):
    ques_input = ",".join(["?" for i in col])
    return ques_input


def gen_query(col, table):      # Need [col_name(),ques_input()]
    query = 'INSERT INTO "{}" ('.format(table) + col_name(col) + ') VALUES (' + ques_input(col) + ')'
    return query


def insert_value(insert_cell, insert_vl):
    insert_cell.insert(0, '{:,}'.format(insert_vl))


def insert_value_rp(insert_cell, insert_vl):
    insert_cell.insert(0, insert_vl)


def save_transaction(regx, cell, col, table,cursor, connection,convert_int, thousand_shorthand):
    
    value = gen_value(cell, regx)

    for i, vl in enumerate(value):
        if convert_int:
            value[i] = int(value[i])

    if thousand_shorthand:
        for i in range(4, len(value)):
            value[i] *= 1000
    
    query = gen_query(col, table)

    if Counter(value)[0] != len(value):
        cursor.execute(query, ([i for i in value]))

    connection.commit()

def convert_readonly(element):
    element.config(state='readonly')


def convert_normal(element):
    element.config(state='normal')


def delete_value(element):
    element.delete(0, tkinter.END)
    
