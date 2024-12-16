import arcpy
import os
import ee
import pandas as pd

"""
example usage:
python project2.py C:\Users\cecil\Documents\programming\geog4057_ccchapman\project\project2 boundary.csv pnt_elev3.shp 32119
"""

def getGeeElevation(workspace,csv_file,outfc_name,epsg=4326):
    """
    workspace: directory that contains input and output
    csv_file: input csv filename
    epsg: wkid code for the spatial reference, e.g. 4326 for WGS GCS
    """
    
    # Read the CSV file
    csf_file = os.path.join(workspace,csv_file)
    df = pd.read_csv(csv_file)
    dem = ee.Image('USGS/3DEP/10m')
    geometrys = [ee.Geometry.Point([x,y],f'EPSG:{epsg}') for x,y in zip(df['X'], df['Y'])]
    fc = ee.FeatureCollection(geometrys)
    origin_info = fc.getInfo()
    sampled_fc = dem.sampleRegions(collection=fc,scale=10,geometries=True)
    sampled_info = sampled_fc.getInfo()
    for ind, itm in enumerate(origin_info['features']):
        itm['properties'] = sampled_info['features'][ind]['properties']
    
    fcname = os.path.join(workspace,outfc_name)
    if arcpy.Exists(fcname):
        arcpy.management.Delete(fcname)
    arcpy.management.CreateFeatureclass(workspace,outfc_name,geometry_type='POINT',spatial_reference=epsg)
    arcpy.management.AddField(fcname,field_name='elevation',field_type='FLOAT')

    with arcpy.da.InsertCursor(fcname,['SHAPE@','elevation']) as cursor:
        for feat in origin_info['features']:
        # get the coordinates and create a point geometry
            coords = feat['geometry']['coordinates']
            pnt = arcpy.PointGeometry(arcpy.Point(coords[0],coords[1]),spatial_reference=32119)
        # get the properties and write it to elevation
            elev = feat['properties']['elevation']
            cursor.insertRow([pnt,elev])

def main():
    import sys
    try:
        ee.Initialize()
    except:
        ee.Authenticate()
        # ee.Initialize()
        # If you need to specifiy the project, comment out the line above and comment in the line below
        ee.Initialize(project='ee-cecilzchapman-lsu')
        workspace = sys.argv[1]
        csv_file = sys.argv[2]
        outfc_name = sys.argv[3]
        epsg = int(sys.argv[4])
        
        getGeeElevation(workspace=workspace,csv_file=csv_file,outfc_name=outfc_name,epsg=epsg)
        # getGeeElevation(workspace=r'C:\Users\cecil\Documents\programming\geog4057_ccchapman\project\project2',csv_file='boundary.csv',outfc_name='pnt_elev2',epsg=32119)
    

if __name__ == '__main__':
    main()
    
