import arcpy
from arcpy import env
import os.path as osp
import os
arcpy.env.overwriteOutput = True

cliped = arcpy.GetParameterAsText(0)
shapefile = arcpy.GetParameterAsText(1)
prefix = arcpy.GetParameterAsText(2)
outdir = arcpy.GetParameterAsText(3)
cliped = cliped.split(";")
source_shps = []
rasters = []
if(prefix is None):
    prefix = ''

for item in cliped:
    if('.tif' in item or '.sid' in item or '.ecw' in item):
        rasters.append(item)
    else:
        source_shps.append(item)
mxd = arcpy.mapping.MapDocument('current')
df = arcpy.mapping.ListDataFrames(mxd)[0]

shapefile = arcpy.mapping.ListLayers(
    mxd, shapefile, df)[0]

for raster_name in rasters:
    raster = arcpy.mapping.ListLayers(
        mxd, raster_name, df)[0]
    raster_name_without_subfix = os.path.splitext(raster_name)[0]
    with arcpy.da.SearchCursor(shapefile, ['SHAPE@']) as cursor:
        # arcpy.AddMessage(str(len(cursor)))
        for clipid, row in enumerate(cursor):
            arcpy.AddMessage("Creating Feature Layer for " + str(row[0]))
            # arcpy.MakeFeatureLayer_management(
            #     shapefile, "fLayer", "FID = " + str(row[0]))
            # desc = arcpy.Describe("fLayer")
            extent = row[0].extent
            extent = str(extent.XMin) + " " + str(extent.YMin) + \
                " " + str(extent.XMax) + " " + str(extent.YMax)
            arcpy.AddMessage("extent " + extent)
            arcpy.AddMessage("Clipping raster")
            outraster = osp.join(
                outdir, prefix + raster_name_without_subfix + '_' + str(clipid)+'_.tif')
            arcpy.Clip_management(raster,
                                  extent,
                                  outraster, "", "", "", "MAINTAIN_EXTENT")
    # extent = raster.getExtent()
for shape_name in source_shps:
    source_shp = arcpy.mapping.ListLayers(
        mxd, shape_name, df)[0]
    shape_name_without_subfix = os.path.splitext(shape_name)[0]
    with arcpy.da.SearchCursor(shapefile, "FID") as cursor:
        for clipid, row in enumerate(cursor):
            arcpy.AddMessage("Creating Feature Layer for " + str(row[0]))
            expression = 'FID={}'.format(row[0])
            arcpy.AddMessage(expression)
            arcpy.MakeFeatureLayer_management(
                shapefile, "fLayer", expression)
            # desc = arcpy.mapping.ListLayers(
            #     mxd, "fLayer", df)[0]
            arcpy.AddMessage("Clipping shp")
            outshp = osp.join(
                outdir, prefix + shape_name_without_subfix + '_' + str(clipid)+'_.shp')
            arcpy.analysis.Clip(source_shp,
                                "fLayer",
                                outshp)

arcpy.Delete_management("fLayer")
# arcpy.AddMessage(cliped)
# extent = str(desc.extent.XMin) + " " + str(desc.extent.YMin) + \
#     " " + str(desc.extent.XMax) + " " + str(desc.extent.YMax)
# with arcpy.da.SearchCursor(shapefile, "LINENUM") as cursor:
#     for row in cursor:
#         print("Creating Feature Layer for " + str(row[0]))
#         arcpy.MakeFeatureLayer_management(
#             shapefile, "fLayer", "LINENUM = '" + row[0] + "'")
#         print("Clipping raster")
#         arcpy.Clip_management(
#             raster, extent, r"C:\temp\DEM_" + str(row[0]), "", "fLayer", "MAINTAIN_EXTENT")

# del cursor‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
