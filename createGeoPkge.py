import sqlite3

def checkTableExists(conn, tablename):
    '''check if table already exists
    :param conn: Connection object
    :param tablename: name of table
    :return: boolean if table exists
    '''
    dbcur = conn.cursor()
    dbcur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name=''' +
                  """'""" +
                  tablename
                  + """'""")
                  
    if dbcur.fetchone()[0]==1 :
        dbcur.close()
        return True 

    dbcur.close()
    return False

def create_connection(db_file):
    '''create a database connection to a SQLite database
    :param db_file: database file
    :return: Connection object or None
    '''
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql, table_name):
    ''' create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    '''
    try:
        if not checkTableExists(conn, table_name):
            c = conn.cursor()
            c.execute(''' CREATE TABLE ''' + table_name + ''' ''' + create_table_sql)
            c.close()
    except Error as e:
        print(e)

def add_spatial_ref_sys(conn, srs_def):
    '''
    Add the spatial reference system (SRS) definitions to the gpkg_spatial_ref_sys_table
    :param conn:
    :param srs_def:
    :return: srs_def id
    '''
    sqlcheck = '''SELECT COUNT(*) FROM gpkg_spatial_ref_sys '''
    
    sql1 = '''INSERT INTO gpkg_spatial_ref_sys(srs_name, srs_id, organization, organization_coordsys_id, definition, description)
             VALUES(?,?,?,?,?,?) '''
    
    sql2 = '''REPLACE INTO gpkg_spatial_ref_sys(srs_name, srs_id, organization, organization_coordsys_id, definition, description)
             VALUES(?,?,?,?,?,?) '''

    cur = conn.cursor()
    count = cur.execute(sqlcheck)
    if count == 0:
        cur.execute(sql1, srs_def)
    if count != 0:
        cur.execute(sql2, srs_def)
    conn.commit()
    cur.close()
    return cur.lastrowid
