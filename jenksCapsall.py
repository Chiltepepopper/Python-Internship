import libpysal
import geopandas as gpd
import mapclassify as mc

columbus = gpd.read_file(libpysal.examples.get_path('columbus.shp'))
q5 = mc.Quantiles(columbus.CRIME, k=5)
q5.plot(columbus)
q5.plot(columbus, axis_on=False)
q5.plot(columbus, axis_on=False, cmap='Blues')
