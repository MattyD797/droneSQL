import sqlite3
import rosbag
import datetime
import pandas as pd
import functools as ft
from createGeoPkge import *

def main():

    #Reads in bag file
    print('Reading Bag File...')
    bag = rosbag.Bag('bags/blF1.bag')

    #Gets all topics encased in bag file
    topics = list(bag.get_type_and_topic_info()[1].keys())
    
    #reads in data encased in location data
    time = []
    latitude = []
    longitude = []
    depth = []
    depth_time = []
    fluor = []
    fluor_time = []

    #Get latitude and longitude data
    print('Processing: '+ topics[2])
    for topic, msg, t in bag.read_messages(topics[2]):
        time.append(str(t.secs)+'.'+str(t.nsecs))
        latitude.append(msg.latitude)
        longitude.append(msg.longitude)

    #convert from epoch to timestamp 
    timesec = [datetime.datetime.fromtimestamp(float(i)).strftime('%Y-%m-%d %H:%M:%S.%f') for i in time]
    df_pos = pd.DataFrame(list(zip(timesec, latitude, longitude)),
                          columns = ["time", "latitude", "longitude"])

    #depth data
    print('Processing: '+ topics[17])
    for topic, msg, t in bag.read_messages(topics[17]):
        depth.append(msg.depth.data)
        depth_time.append(str(t.secs)+'.'+str(t.nsecs))

    #convert from epoch to timestamp 
    depth_timesec = [datetime.datetime.fromtimestamp(float(i)).strftime('%Y-%m-%d %H:%M:%S.%f') for i in depth_time]   
    df_depth = pd.DataFrame(list(zip(depth_timesec, depth)),
                          columns = ["time", "depth"])
    #fluor data
    print('Processing: '+ topics[12])
    for topic, msg, t in bag.read_messages(topics[12]):
        fluor.append(msg.data)
        fluor_time.append(str(t.secs)+'.'+str(t.nsecs))

    #convert from epoch to timestamp 
    fluor_timesec = [datetime.datetime.fromtimestamp(float(i)).strftime('%Y-%m-%d %H:%M:%S.%f') for i in fluor_time]   
    df_fluor = pd.DataFrame(list(zip(fluor_timesec, fluor)),
                          columns = ["time", "flourescence"])

    #TODO: merge dataframes by time

    dfs = [df_pos, df_depth, df_fluor]

    
    df_final = ft.reduce(lambda left, right: pd.merge(left,
                                                      right,
                                                      how='outer',
                                                      on='time'),
                         dfs).sort_values(by='time').reset_index(drop=True)

    
    #interpolate coordinates of depth and fluorescence 
    df_final['latitude'] = df_final.set_index('time')['latitude'].interpolate(method="linear").values
    df_final['longitude'] = df_final.set_index('time')['longitude'].interpolate(method="linear").values
    df_final['depth'] = df_final.set_index('time')['depth'].interpolate(method="linear").values

    #filter out extraneuos data
    start = df_final[df_final['time'] == fluor_timesec[0]].index.tolist()[0]-1
    end = df_final[df_final['time'] == fluor_timesec[-1]].index.tolist()[0]+1
    df_final_filt = df_final.filter(items= range(start,end+1), axis = 0).dropna()
    print(df_final_filt)

    #TODO: create features tables fo fluorescence

    #TODO: add geometry to geometry_columns table
        
    #make gpkg database
    database = "my_geopackage.gpkg"

    sql_create_gpkg_spatial_ref_sys_table = ''' (
                                                  srs_name TEXT NOT NULL,
                                                  srs_id INTEGER PRIMARY KEY,
                                                  organization TEXT NOT NULL,
                                                  organization_coordsys_id INTEGER NOT NULL,
                                                  definition  TEXT NOT NULL,
                                                  description TEXT
                                                );
                                            '''

    srs_def = ("WGS 84",
                            4326,
                            "EPSG",
                            4326,
                            "GEOGCS['WGS 84',DATUM['World Geodetic System 1984',SPHEROID['WGS 84',6378137,298.257223563,AUTHORITY['EPSG','7030']],AUTHORITY['EPSG','6326']],PRIMEM['Greenwich',0,AUTHORITY['EPSG','8901']],UNIT['degree',0.017453292519943278,AUTHORITY['EPSG','9122']],AXIS['Lat',NORTH],AXIS['Lon',EAST],AUTHORITY['EPSG','4326']]",
                            None)
    
    
    sql_create_gpkg_contents_table = ''' (
                                          table_name TEXT NOT NULL PRIMARY KEY,
                                          data_type TEXT NOT NULL,
                                          identifier TEXT UNIQUE,
                                          description TEXT DEFAULT '',
                                          last_change DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
                                          min_x DOUBLE,
                                          min_y DOUBLE,
                                          max_x DOUBLE,
                                          max_y DOUBLE,
                                          srs_id INTEGER,
                                          CONSTRAINT fk_gc_r_srs_id FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys(srs_id)
                                        );
                                     '''

    sql_create_sample_feature_table = ''' (
                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          geometry GEOMETRY,
                                          text_attribute TEXT,
                                          real_attribute REAL,
                                          boolean_attribute BOOLEAN,
                                          raster_or_photo BLOB
                                        );
                                        '''
    
    sql_create_gpkg_geometry_columns_table = ''' (
                                              table_name TEXT NOT NULL,
                                              column_name TEXT NOT NULL,
                                              geometry_type_name TEXT NOT NULL,
                                              srs_id INTEGER NOT NULL,
                                              z TINYINT NOT NULL,
                                              m TINYINT NOT NULL,
                                              CONSTRAINT pk_geom_cols PRIMARY KEY (table_name, column_name),
                                              CONSTRAINT uk_gc_table_name UNIQUE (table_name),
                                              CONSTRAINT fk_gc_tn FOREIGN KEY (table_name) REFERENCES gpkg_contents(table_name),
                                              CONSTRAINT fk_gc_srs FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys (srs_id)
                                            );
                                            '''
                                            
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create gpkg_spatial_ref_sys table
        create_table(conn, sql_create_gpkg_spatial_ref_sys_table, "gpkg_spatial_ref_sys")

        # create gpkg_contents table
        create_table(conn, sql_create_gpkg_contents_table, "gpkg_contents")

        # add gpkg_spatial_ref_sys information
        add_spatial_ref_sys(conn, srs_def)

        #create a sample_feature_table & necessary gpkg_geometry_columns table
        create_table(conn, sql_create_sample_feature_table, "sample_feature_table")
        create_table(conn, sql_create_gpkg_geometry_columns_table, "gpkg_geometry_columns")

        #add features into feature table

        #add geometry column into geometry column tables
        
        
        conn.close()

    else:
        print("Error: cannot create the database connection")

        
if __name__ == '__main__':
    main()
