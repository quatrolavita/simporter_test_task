import pandas as pd
from sqlalchemy import create_engine


def populate_db_csv(file_name, db_url):
    """ This function populate our db with data"""

    df = pd.read_csv(file_name)
    df.columns = [c.lower() for c in df.columns]

    engine = create_engine(db_url)

    df.to_sql("timeline", engine, if_exists="append", index=False)




