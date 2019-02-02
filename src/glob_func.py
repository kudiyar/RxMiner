import os
import StringIO
import psycopg2
import sqlalchemy as sa # Package for accessing SQL databases via Python

def cleanColumns(columns):
    cols = []
    for col in columns:
        col = col.replace(' ', '_')
        cols.append(col)
    return cols

def df_to_sql(df, table_name, mode):
    """
    Save DataFrame to .csv, read csv as sql table in memory and copy the table
     directly in batch to PostgreSQL or Redshift.
    """
    data = StringIO.StringIO()
    df.columns = cleanColumns(df.columns)
    df.to_csv(data, header=False, index=False)
    data.seek(0)
    #raw = engine.raw_connection()
    #curs = raw.cursor()
    if mode == 'replace':
        cur.execute("DROP TABLE " + table_name)
        sql_query = """
            COPY %s FROM STDIN WITH
                CSV
                HEADER;
            """
    elif new_table == 0:
        sql_query = """
            COPY %s FROM STDIN WITH
                CSV
                HEADER;
            """
    elif psql == 'psql':
        sql_query = """
            COPY temp FROM STDIN WITH
                CSV
                HEADER;
            INSERT INTO %s SELECT * FROM temp;
            DROP TABLE;
        """
    else:
        sql_query = """
            COPY temp FROM STDIN WITH
                CSV
                HEADER;
            ALTER TABLE %s APPEND FROM temp;
            DROP TABLE;
        """
    empty_table = pd.io.sql.get_schema(df, table_name, con = engine)
    empty_table = empty_table.replace('"', '')
    cur.execute(empty_table)
    cur.copy_expert(sql=sql_query % table_name, file=data)
    cur.connection.commit()