import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String


def populate_db_csv(file_name, db_url):
    """ This function populate our db with data"""

    df = pd.read_csv(file_name)
    df.columns = [c.lower() for c in df.columns]

    engine = create_engine(db_url)

    df.to_sql("timeline", engine, if_exists="append",
              index=False, dtype={'asin': String, 'brand': String,
                                  'id': String, 'source': String,
                                  'stars': Integer, 'timestamp': Integer})




