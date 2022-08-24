# droneSQL
Create a database management system (DBMS) for a customized multi-sensor unmanned aircraft system.

All commands below are run in the terminal/console. Ensure to configure the required input and output file destinations if running within an IDE, such as PyCharm or similar. 

# Install Scripts
```
cd <desired_workspace>
git clone https://github.com/MattyD797/droneSQL.git
cd droneSQL
```

I might advise making an environment via any method of your choosing to ensure package overlap isn't a problem. I used Anaconda (pretty standard), however, this step is optional. 

# Required Packages 
```
pip install sqlite3
pip install spatialite
pip install rosbag
```

These are the only packages required on my raspberry pi 4B, but you may need to install more depending on the system and your default python packages. Install any of these as well, if required: datetime, pandas, functools, argparse. These are all viewable on top of the script files next to the word "import". 

# Command Line
```
# To create a new geopackage
python droneGPKG.py -i <bag_file_path> -o <gpkg_output_path>

#DEBUG: To add SD data into geopackage
python addSD.py -g <geopackage_path> -i <SD_path>

#DEGUB: To add another bag file into geopackage
python addFeatureTable.py -g <geopackage_path> -i <bag_file_path>

#DEGUB: To remove a table (feature or attribute) from geopackage
# Warning: must have at least one feature table in gpkg, otherwise, remake geopackage with droneGPKG.py
python removeFeatureTable.py -g <geopackage_path> -t <table_name>
```

# Example BAG Files
Are stored in the bags directory. Currently, the repository only has bates landing 1 and 2 (blF1.bag and blF2.bag). 

# Edit/Add 
```
git pull
git checkout -b <branch_name>

#change code
git add .
git commit -m "I MADE A CHANCE"
git push
git checkout main
```

# General Problems
### No points/geometry displaying on QGIS

Geopackages are a relational DBMS constructed with sqlite3. Since sqlite3 lacks some functionality in comparison to a conventional SQL server it needs the spatialite extension to format geometries to a GIS readable BLOB (binary large object). Feel free to change the point geometry to any of the acceptable [types](https://www.gaia-gis.it/gaia-sins/spatialite-cookbook-5/cookbook_topics.02.html). If no lines/points/polygons display in QGIS this means QGIS is unable to read your geometry and you can see this if you try to pan to one of your attributes. QGIS will display an error saying it was unable to find a geometry. 

### geopackage or sql table already exists

SQL only allows for uniquely named tables. This means that this table name is already in use. 


