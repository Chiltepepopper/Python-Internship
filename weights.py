import sys
import os
import libpysal
import geopandas
from libpysal.weights import Queen, Rook, KNN
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('..'))


libpysal.examples.available()
libpysal.examples.explain('mexico')
pth = libpysal.examples.get_path("mexicojoin.shp")
gdf = geopandas.read_file(pth)
ax = gdf.plot(edgecolor='grey', facecolor='w')
ax.set_axis_off()
w_rook = Rook.from_dataframe(gdf)
f,ax = w_rook.plot(gdf, ax=ax,
                   edge_kws=dict(color='r', linestyle=':', linewidth=1),
                   node_kws=dict(marker=''))
ax.set_axis_off()
gdf.head()
w_queen = Queen.from_dataframe(gdf)

ax = gdf.plot(edgecolor='grey', facecolor='w')
f, ax = w_queen.plot(gdf, ax=ax,
                    edge_kws=dict(color='r', linestyle=':', linewidth=1),
                    node_kws=dict(marker=''))
ax.set_axis_off()

