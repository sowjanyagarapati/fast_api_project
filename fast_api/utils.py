import pandas as pd




class commonUtils():
    def __init__(self):
        self.columns = ["txn","acc_number","rrn","ifsc_number","bank_name","acc_holder_name","txn_type"]

    def clean_df(self,df):
        narration_list = df["NARRATION"].apply(lambda x: x.split("/")).tolist()
        df2 = pd.DataFrame(narration_list, columns=self.columns)
        df2["rrn"] = df2["rrn"].apply(lambda x: x.split(":")[1])
        df2["acc_holder_name"] = df2["acc_holder_name"].apply(lambda x: x.title())
        return pd.concat([df,df2], axis=1, join="inner").drop_duplicates()

