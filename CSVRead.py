import pandas


def openCSV():
    switches = pandas.read_csv('C:\\Users\\user\Desktop\\Book1.csv')
    print(switches)

    for switch in switches:
        print(switch)
    return switches
    #
    # book = c.open_workbook("C:\\Users\\user\Desktop\\Book1.xlsx")
    # sheet = book.sheet_by_index(0)
    #
    # switches = []
    #
    # for row in range(1, sheet.nrows):
    #     switch = str(sheet.row_values(row)).replace("['", '').replace("', '", ' - ').replace("']", '').replace('[', '').replace(", '", ' - ')
    #     switches.append(switch)

    # return switches


if __name__ == '__main__':
    openCSV()