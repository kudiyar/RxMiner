import os
import psycopg2

def sum_by_state(cur):
    sql_query = """
        SELECT SUM(total_claim_count), practice_state
        FROM pupd_cleaned
        GROUP BY pupd_cleaned;
    """
    cur.execute(sql_query)
    print("The number of parts: ", cur.rowcount)
    rows = cur.fetchmany(size=10)
    print(rows)

def merge_npi(cur):
    sql_query = """
        SELECT
            pupd.npi,
            pupd.total_claim_count,
            npidata.practice_state
        INTO
            pupd_cleaned
        FROM
            pupd
        LEFT JOIN npidata ON (npidata.npi = pupd.npi AND npidata.last_name = pupd.nppes_provider_last_org_name);
    """
    cur.execute(sql_query)
    print("The number of parts: ", cur.rowcount)
    rows = cur.fetchmany(size=10)
    print(rows)

if __name__ == "__main__":
    user = os.getenv('POSTGRESQL_USER', 'default')
    pswd = os.getenv('POSTGRESQL_PASSWORD', 'default')
    host = os.getenv('POSTGRESQL_HOST_IP', 'default')
    port = os.getenv('POSTGRESQL_PORT', 'default')
    dbname = 'postgres'
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=pswd)
    cur = conn.cursor()
    print("PostgreSQL connected")
    merge_npi(cur)
    sum_by_state(cur)
    cur.close()
    conn.close()