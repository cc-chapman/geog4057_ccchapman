"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy
import os
import ee
import pandas as pd

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

if __name__ == "__main__":

    workspace = arcpy.GetParameterAsText(0)
    csv_file = arcpy.GetParameterAsText(1)
    outfc_name = arcpy.GetParameterAsText(2)
    epsg = int(arcpy.GetParameterAsText(3))

    getGeeElevation(workspace,csv_file,outfc_name,epsg=4326)
