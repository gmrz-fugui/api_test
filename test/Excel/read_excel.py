import xlrd
class GetExcel:

    def __init__(self):
        self.case_file = "../TestData/data/test_case.xlsx"

    @staticmethod
    def list_dic(list1, list2):
        """
        two lists merge a dict,a list as key,other list as value
        :param list1:key
        :param list2:value
        :return:dict
        """
        dic = dict(map(lambda x, y: [ x, y ], list1, list2))
        return dic

    @staticmethod
    def merge_cell(sheet_info):
        """
        #handle Merge transverse cells and handle Merge Vertical Cells, assign empty cells,
        :param rlow:row, include row exclusive of row_range
        :param rhigh:row_range
        :param clow:col, include col exclusive of col_range
        :param chigh:col_range
        :param sheet_info:object of sheet
        :return:dic contain all of empty cells value
        """
        merge = {}
        merge_cells = sheet_info.merged_cells
        for (rlow, rhigh, clow, chigh) in merge_cells:
            value_mg_cell = sheet_info.cell_value(rlow, clow)
            if rhigh - rlow == 1:
                # Merge transverse cells
                for n in range(chigh - clow - 1):
                    merge[ (rlow, clow + n + 1) ] = value_mg_cell
            elif chigh - clow == 1:
                # Merge Vertical Cells
                for n in range(rhigh - rlow - 1):
                    merge[ (rlow + n + 1, clow) ] = value_mg_cell
        return merge

    def get_excel(self):
        # 先获取excel所有数据
        apply_dic = [ ]  # 所有用例字典加入此列表
        with xlrd.open_workbook(self.case_file) as workbook:
            name_sheets = workbook.sheet_names()  # 获取Excel的sheet表列表，存储是sheet表名
            for index in name_sheets:  # for 循环读取每一个sheet表的内容
                sheet_info = workbook.sheet_by_name(index)  # 根据表名获取表中的所有内容，sheet_info也是列表，列表中的值是每个单元格里值
                first_line = sheet_info.row_values(0)  # 获取首行，我这里的首行是表头，我打算用表头作为字典的key，每一行数据对应表头的value，每一行组成一个字典
                values_merge_cell = GetExcel.merge_cell(sheet_info)  # 这里是调用处理合并单元格的函数
                for i in range(1, sheet_info.nrows):  # 开始为组成字典准备数据
                    other_line = sheet_info.row_values(i)
                    for key in values_merge_cell.keys():
                        if key[ 0 ] == i:
                            other_line[ key[ 1 ] ] = values_merge_cell[ key ]
                    dic = GetExcel.list_dic(first_line, other_line)  # 调用组合字典的函数，传入key和value，字典生成
                    apply_dic.append(dic)
                return apply_dic
