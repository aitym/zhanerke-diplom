import xlrd
book = xlrd.open_workbook('sample.xlsx')
sheet = book.sheet_by_name('For C8 between lines')
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
print(data)
