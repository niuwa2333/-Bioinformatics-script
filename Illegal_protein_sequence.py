# 导入xlrd和xlwt模块，用于读写xls格式的表格文件
import xlrd
import xlwt

# 定义一个函数，用于检查一个字符串是否是合法的氨基酸序列
def is_valid_protein_sequence(sequence):
    # 定义一个集合，包含20个天然氨基酸的单字母缩写
    amino_acids = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'}
    # 遍历字符串中的每个字符
    for char in sequence:
        # 如果字符不在氨基酸集合中，说明是非法的字符，返回False
        if char not in amino_acids:
            return False
    # 如果字符串中的所有字符都是合法的氨基酸，返回True
    return True

# 定义一个函数，用于检查和删除含有非法氨基酸序列的表格文件
def check_and_delete_invalid_protein_sequences(file_path):
    # 打开表格文件，读取数据
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)
    # 创建一个新的工作簿，用于存储修改后的数据
    new_workbook = xlwt.Workbook()
    new_sheet = new_workbook.add_sheet('Sheet1')
    # 定义一个变量，用于记录新表格中的行数
    new_row = 0
    # 遍历原表格中的每一行
    for row in range(sheet.nrows):
        # 获取第二列的值，即氨基酸序列
        sequence = sheet.cell_value(row, 1)
        # 检查氨基酸序列是否合法
        if is_valid_protein_sequence(sequence):
            # 如果合法，将该行数据复制到新表格中
            for col in range(sheet.ncols):
                value = sheet.cell_value(row, col)
                new_sheet.write(new_row, col, value)
            # 更新新表格中的行数
            new_row += 1
        else:
            # 如果不合法，打印该行数据，并跳过该行
            print(f'Invalid protein sequence found in row {row + 1}: {sequence}')
    # 保存新表格文件到同一目录下，并返回文件名
    new_file_path = file_path.replace('.xls', '_modified.xls')
    new_workbook.save(new_file_path)
    return new_file_path

# 调用函数，传入表格文件路径
file_path = r''
new_file_path = check_and_delete_invalid_protein_sequences(file_path)
# 打印结果
print(f'Check and delete completed. You can find the modified file here: {new_file_path}')
