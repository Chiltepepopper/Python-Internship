from libpysal.weights.contiguity import Queen
import libpysal
from libpysal import examples
import matplotlib.pyplot as plt
import geopandas as gpd
from splot.libpysal import plot_spatial_weights

examples.explain('tokyo')
gdf = gpd.read_file(examples.get_path('tokyomet262.shp'))
gdf.head()
weights = Queen.from_dataframe(gdf)
plot_spatial_weights(weights, gdf)
plt.show()
wnp = libpysal.weights.util.nonplanar_neighbors(weights, gdf)
plot_spatial_weights(wnp, gdf)
plt.show()
plot_spatial_weights(wnp, gdf, nonplanar_edge_kws=dict(color='#4393c3'))
plt.show()