

def placement(element, row=0, column=0, sticky='nw', padx=(10, 0), pady=(0, 0), ipady=0, columnspan=1,
                                                                                                                                              border=2, relief='groove'):
    
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
