import sqlite3

def checkTableExists(conn, tablename):
    '''check if table already exists
    :param conn: Connection object
    :param tablename: name of table
    :return: boolean if table exists
    '''
    dbcur = conn.cursor()
    dbcur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name=''' +'"'+
                  tablename +'"')
                  
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
        conn = spatialite.connect(db_file)
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

def add_features(conn, df_final_filt, table_name):
    '''
    Add a feature into the feature table. Utilizes the function add_feat
    :param conn:
    :param feat:
    :param table_name:
    :return: feat id
    '''
    sqlcheck = '''SELECT COUNT(*) FROM ''' + table_name

    cur = conn.cursor()
    count = cur.execute(sqlcheck)
    if list(count)[0][0] == 0:
        for i,row in df_final_filt.iterrows():
            X = row.longitude
            Y = row.latitude
            Z = row.depth
            point_wkt = 'POINTZ({0} {1} {2})'.format(X, Y, Z)

            
            feature = (row.flourescence,
                       point_wkt)

            
            add_feat(cur, feature, table_name)   
    else:
        print(table_name + " Already Filled: "+ "Cannot fill an already filled feature table.")
    conn.commit()
    cur.close()
    return cur.lastrowid

def add_feat(cur, feat, table_name):
    sql = " INSERT INTO sample_feature_table(real_attribute, geom) VALUES(?, GeomFromText(?, 4326))"
    print(feat)
    cur.execute(sql, feat)
    return cur.lastrowid
    
def add_geometry(conn, geom, num):
    
    sqlcheck = '''SELECT COUNT(*) FROM gpkg_geometry_columns'''
    sql = " INSERT INTO gpkg_geometry_columns(table_name, column_name, geometry_type_name, srs_id, z, m) VALUES(?,?,?,?,?,?)"

    cur = conn.cursor()
    count = cur.execute(sqlcheck)
    
    if list(count)[0][0] < num:
        cur.execute(sql, geom)
    else:
        print("Geometry Already Identified")
    conn.commit()
    cur.close()
    return cur.lastrowid

def add_content(conn, cont, num):
    sqlcheck = '''SELECT COUNT(*) FROM gpkg_contents'''
    sql = " INSERT INTO gpkg_contents(table_name, data_type, identifier, description, last_change, min_x, min_y, max_x, max_y, srs_id) VALUES(?,?,?,?,?,?,?,?,?,?)"

    cur = conn.cursor()
    count = cur.execute(sqlcheck)
    if list(count)[0][0] < num:
        cur.execute(sql, cont)
    else:
        print("Content Already Updated with " + str(num) + " features")

    conn.commit()
    cur.close()
    return cur.lastrowid

def add_geometry_column(conn, table_name, column_name, srs_id):
    sql = "SELECT AddGeometryColumn('" + table_name + "', '" + column_name + "', " + str(srs_id) + ", 'POINTZ', 'XYZ')"
    print(sql)
    cur = conn.cursor()
    print(cur.execute(sql).fetchone()[0])
    conn.commit()
    cur.close()
    return cur.lastrowid
    
