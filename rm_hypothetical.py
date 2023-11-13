from Bio import SeqIO
import os
####有的时候基因注释有很多假设基因，绘图的时候会干扰
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
            # 创建一个空列表来存储要删除的特征
            features_to_remove = []
            # 遍历所有特征
            for feature in record.features:
                # 检查特征是否为CDS类型
                if feature.type == 'CDS':
                    # 检查特征是否包含product注释
                    if 'note'in feature.qualifiers:
                        if 'hypothetical protein' in feature.qualifiers['note']:
                            features_to_remove.append(feature)
                            for gene_feature in record.features:
                                if gene_feature.type == 'gene':
                                    if gene_feature.location == feature.location:
                                        # 将对应的gene特征添加到要删除的特征列表中
                                        features_to_remove.append(gene_feature)
                                        break
                    elif 'product' in feature.qualifiers:
                        # 检查product注释是否为hypothetical protein
                        if 'hypothetical protein' in feature.qualifiers['product']:
                            # 将该特征添加到要删除的特征列表中
                            features_to_remove.append(feature)
                            # 查找对应的gene特征
                            for gene_feature in record.features:
                                if gene_feature.type == 'gene':
                                    if gene_feature.location == feature.location:
                                        # 将对应的gene特征添加到要删除的特征列表中
                                        features_to_remove.append(gene_feature)
                                        break
                else :
                    break
            # 删除要删除的所有特征
            for feature in features_to_remove:
                record.features.remove(feature)
        # 保存修改后的GBK文件
        SeqIO.write(records, os.path.join(directory, filename), 'genbank')
