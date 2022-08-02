# droneSQL
Create a database management system (DBMS) for a customized multi-sensor unmanned aircraft system.

Geopackages are a relational DBMS constructed with sqlite3. Since sqlite3 lacks some functionality in comparison to a conventional SQL server it needs the spatialite extension to format geometries to a GIS readable BLOB (binary large object). Feel free to change the point geometry to any of the acceptable [types](https://www.gaia-gis.it/gaia-sins/spatialite-cookbook-5/cookbook_topics.02.html). If no lines/points/polygons display in QGIS this means QGIS is unable to read your geometry and you can see this if you try to pan to one of your attributes. QGIS will display an error saying it was unable to find a geometry. 

All commands below are run in the terminal/console. Ensure to configure the required input and output file destinations if running within an IDE, such as PyCharm or similar. 

# Install Scripts
```
cd <desired_workspace>
git clone https://github.com/MattyD797/droneSQL.git
cd droneSQL
```

# Required Packages 
```
pip install sqlite3
pip install spatialite
pip install rosbag
```

These are the only packages required on my raspberry pi 4B, but you may need to install more depending on the system and your default python packages. Install any of these as well, if required: datetime, pandas, functools, argparse.

# Command Line
```
python droneGPKG.py -i <bag_file_path> -o <gpkg_output_path>
```

# Example BAG Files
Are stored in the bags directory. Currently, the repository only has bates landing 1 and 2 (blF1.bag and blF2.bag). 

## Progress
- [X] Verify microcontrollers (e.g. RAM, Zero or Zero 2 W) of existing Raspberrys, interface with Robot Operating System (ROS).
- [X] Install SQLite database code from pi repository (easy and straightforward).
- [X] Develop modular code (C functions) to call for writing data to database.
- [X] Test/verify.
- [X] Install a geopackage template (use default template or develop code to create).
- [X] Design GIS data models for the kinds of data collected by the drone.
- [X] Develop modular code (e.g. Python/C functions) to call for writing data to geopackage/database.
- [X] Test/verify.
- [ ] Check for single and double precision of coordinates.
- [ ] Test each remotely from existing drone.
- [ ] Port to Team’s drone for testing.
