from rssa.dal import MySql
if __name__ == "__main__":
    sql = MySql()
    df = sql.read("sports")
    print(df.shape)
    print(df.head())
    df.to_csv("C:\\Users\keyur.ja\\data.csv")