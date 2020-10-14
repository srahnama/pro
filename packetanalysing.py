import numpy as np
import pandas as pd
import re
df = pd.read_csv("packets1.csv", sep=",")
str = '80  >  57244 [ACK] Seq=153969187 Ack=245 Win=14720 Len=1460 [TCP segment of a reassembled PDU]'
# print(df['Info'][134033])
new_df = df.head(50)
print( re.search(r"Seq=([0-9]+)", str).group(1))
print( re.search(r"Len=([0-9]+)", str).group(1))
print( re.search(r"\[[A-Z]*?\]", str).group())
pd.set_option('display.max_rows', df.shape[0]+1)
new_df.loc[:, 'Seq'] = None 
new_df.loc[:, 'Len'] = None 
new_df.loc[:, 'Flag'] = None 
# new_df['Len'] = None
# new_df['Flag'] = None
for index, row in new_df.iterrows():
    if re.search(r"Seq=([0-9]+)", row.Info)  is not None:
        new_df.loc[index,'Seq'] = re.search(r"Seq=([0-9]+)", row.Info).group(1)
    if re.search(r"\[[A-Z]*?\]", row.Info)  is not None:
        new_df.loc[index,'Flag'] = re.search(r"\[[A-Z]*?\]", row.Info).group()
    if re.search(r"Len=([0-9]+)", row.Info)  is not None:
        new_df.loc[index,'Len'] = re.search(r"Len=([0-9]+)", row.Info).group(1)

# print(new_df[['Seq','Len']])

output_df = pd.DataFrame(columns=new_df.columns.tolist())


# flags => \[[A-Z]*?\]

for index, row in new_df.iterrows():
    if row.Seq !=None:
        len = int(row.Len)
        # print(row)
        seq = int(row.Seq)
        next_seq = len + seq
        output_df = output_df.append(row, ignore_index=True)
        new_df = new_df.drop(new_df.index[index], axis=0)
        for i, r in new_df.iterrows():
            if r.Seq !=None:
                if int(r.Seq) == next_seq:
                    next_seq = int(r.Seq) + len
                    output_df = output_df.append(row, ignore_index=True)
                    new_df = new_df.drop(new_df.index[i], axis=0)
                    print(output_df)
    output_df = output_df.append(pd.Series([np.nan]), ignore_index = True)


print(output_df)