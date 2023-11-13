# 导入Bio.SeqIO模块
from Bio import SeqIO
# 导入os模块，用于操作文件和目录
import os
# 定义输入文件的目录
input_dir = ""
# 定义输出文件的目录，这里设为与输入文件相同
output_dir = ""
# 遍历输入目录中的所有文件
for filename in os.listdir(input_dir):
    # 判断文件是否是gbk格式
    if filename.endswith(".gbk"):
        # 构造输入文件的完整路径
        input_file = os.path.join(input_dir, filename)
        # 构造输出文件的完整路径，将扩展名改为.fasta
        output_file = os.path.join(output_dir, filename.replace(".gbk", ".fasta"))
        # 使用Bio.SeqIO.convert函数进行格式转换
        SeqIO.convert(input_file, "genbank", output_file, "fasta")
        # 打印转换成功的信息
        print(f"Converted {filename} from gbk to fasta")
