# coding=utf-8

import xlrd

def __normalize_excel_data_from_file(data):
    return list(map(lambda row: row[:2], data))

def read_from_excel_file(Workbook_path, sheet_name):
    book = xlrd.open_workbook(Workbook_path)
    sheet = book.sheet_by_name(sheet_name)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    return __normalize_excel_data_from_file(data)

data = read_from_excel_file('sample.xlsx', 'For C8 between lines')
print(data)
