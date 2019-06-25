import xlrd


def openExcel():
    book = xlrd.open_workbook("C:\\Users\\user\Desktop\\Book1.xlsx")
    sheet = book.sheet_by_index(0)

    switches = []

    for row in range(1, sheet.nrows):
        switch = str(sheet.row_values(row)).replace("['", '').replace("', '", ' - ').replace("']", '').replace('[', '').replace(", '", ' - ')
        switches.append(switch)

    return switches

# book = xlrd.open_workbook("Test.xlsx")
# sheet = book.sheet_by_index(0)
#
# list_j = []
#
# for k in range(1,sheet.nrows):
#     list_j.append(str(sheet.row_values(k)[j-1]))

if __name__ == '__main__':
    openExcel()