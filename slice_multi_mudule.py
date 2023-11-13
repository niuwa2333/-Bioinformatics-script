from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os
###切割多于2个或是3个pdif模块的序列
###没加XerC/D标记
def process_files():
    #
    for filename in os.listdir(r''):
        if filename.endswith('.gbk'):
            # 获取序列ID
            seq_id = filename.split('.')[0]
            # 找到对应的pdif_site.txt文件
            pdif_site_file = os.path.join(r'', seq_id, 'pdif_site.txt')
            with open(pdif_site_file, 'r') as f:
                lines = f.readlines()
                new_seq = Seq('')
                new_features = []
                offset = 0
                # 遍历pdif_site.txt文件中记录的位置信息
                for i in range(0, len(lines), 2):
                    start_pos = int(lines[i].split('	')[1])
                    end_pos = int(lines[i+1].split('	')[2])
                    # 切割出特殊子序列的.gbk文件
                    with open(os.path.join(r'', filename), 'r') as gbk_file:
                        record = SeqIO.read(gbk_file, 'genbank')
                        sub_seq = record.seq[start_pos:end_pos+1]
                        new_seq += sub_seq
                        # 更新注释指代位置
                        for feature in record.features:
                            if start_pos <= feature.location.start and feature.location.end <= end_pos:
                                new_feature = feature
                                new_feature.location += offset - start_pos
                                new_features.append(new_feature)
                        offset += len(sub_seq)
                # 创建新的SeqRecord对象
                new_record = SeqRecord(new_seq, id=seq_id, name=seq_id, description=seq_id)
                new_record.annotations['molecule_type'] = record.annotations.get('molecule_type', 'DNA')
                new_record.features = new_features
                # 将特殊子序列合并为新的文件
                with open(os.path.join(r'', seq_id + '.gbk'), 'w') as new_file:
                    SeqIO.write(new_record, new_file, 'genbank')
process_files()