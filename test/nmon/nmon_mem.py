import xlrd
def nmon_mem(file):
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name('MEM')
    rows_data = []  # 以二维数组的方式保存每一列数据
    mem_data = []  # 存放每列计算后的内存占用率
    for i in range(1, sheet.nrows):
        rows_data.append(sheet.row_values(i))

    for j in rows_data:
        # print(j, '\t', (j[1] - j[5] - j[10] - j[13]) / j[1] * 100)
        mem_data.append((j[1] - j[5] - j[10] - j[13]) / j[1] * 100)
    num = 0
    for x in mem_data:
        num += x
    mem = num / len(mem_data)
    print('平均内存占用率：', "%.1f" % float(mem))
    print('平均内存占用：', "%.2f" % float(16 * 1024 * mem / 100))

if __name__ == '__main__':
    f = r'D:\Desktop\gmrz\性能测试报告\UAP5.4.1性能测试报告\指纹\单交易\注册\mysql\220\Sheet.xlsx'
    nmon_mem(file=f)
