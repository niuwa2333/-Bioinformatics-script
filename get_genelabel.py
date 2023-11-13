from Bio import SeqIO, Entrez
import os
###使用entrez从NCBI批量获取，需要使用API_KEY避免请求频率限制，or加上sleep（）
# 设置Entrez电子邮件地址
Entrez.email = ""
Entrez.api_key = ""
# 指定目录
directory = ''

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    # 检查文件是否为GBK格式
    if filename.endswith('.gbk'):
        # 读取GBK文件
        records = list(SeqIO.parse(os.path.join(directory, filename), 'genbank'))
        # 遍历所有记录
        for record in records:
            # 遍历所有特征
            for feature in record.features:
                # 检查特征是否包含protein_id注释
                if 'protein_id' in feature.qualifiers:
                    # 获取protein_id
                    protein_id = feature.qualifiers['protein_id'][0]
                    # 使用Entrez.efetch()函数从NCBI Protein数据库中获取数据
                    handle = Entrez.efetch(db='protein', id=protein_id, rettype='gb', retmode='text')
                    # 读取返回的数据
                    protein_record = SeqIO.read(handle, 'genbank')
                    handle.close()
                    # 检查protein_record是否包含gene注释
                    if 'gene' in protein_record.annotations:
                        # 获取基因符号
                        gene_symbol = protein_record.annotations['gene'][0]
                        # 将基因符号添加到特征的注释中
                        feature.qualifiers['gene'] = [gene_symbol]
                        print(gene_symbol)
        # 保存修改后的GBK文件
        SeqIO.write(records, os.path.join(directory, filename), 'genbank')
