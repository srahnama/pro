import numpy as np
import pandas as pd
import re
df = pd.read_csv("packets1.csv", sep=",")

new_df = df.head(50)

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

# print(new_df.head(33))

output_df = pd.DataFrame(columns=new_df.columns.tolist())


# flags => \[[A-Z]*?\]

# for index, row in new_df.iterrows():
#     if row.Seq ==None or int(row.Len) == 0:
# new_df
#  = new_df.dropna(how='all')
new_df =new_df.replace(to_replace='None', value=np.nan).dropna()
print(new_df, new_df.size)
for index, row in new_df.iterrows():
    # if int(row.Len) > 0:

    if index < new_df.shape[0]:

        df_len = int(row.Len)
        # print(row)
        seq = int(row.Seq)
        next_seq = df_len + seq
        output_df = output_df.append(row)
        new_df.drop([new_df.index[index]], axis=0, inplace=True)
        
        for i, r in new_df.iterrows():
            # if r.Seq != None and int(r.Len) > 0:
            if i < new_df.shape[0]:
                if int(r.Seq) == next_seq:
                    print(int(r.Seq) , next_seq)
                    # print(next_seq) 
                    output_df = output_df.append(r)
                    # print(new_df[i], new_df.size)
                    new_df.drop([new_df.index[i]], axis=0, inplace=True)
                    next_seq = next_seq + df_len
            # break   
                    # print(output_df)
        output_df = output_df.append(pd.Series([np.nan]), ignore_index = True)


print(output_df)