import sqlalchemy as sql
import pandas as pd
from rssa.utils.constants import *
class MySql:
    def __init__(self):
        self.connection = sql.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                            format(SQL_USERNAME, SQL_PASSWORD,
                                                   SQL_HOSTNAME, SQL_DBNAME))
    def read(self, tablename, columns = None):
        selection = "*"
        if columns is not None:
            selection = ",".join(columns)
        query = "select " + selection + " from {}".format(tablename)
        df = pd.read_sql(query, con=self.connection)
        return df

    def write(self, df, tablename):
        df.to_sql(name=tablename, con=self.connection, index=False, if_exists='append')