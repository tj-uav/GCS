import shapefile
from pygeoif import geometry

geometries = [[
    [38.8781548838115,-77.3764300346375],
    [38.8795413373583,-77.3796486854553],
    [38.877570226617,-77.3796057701111],
    [38.8764343074595,-77.3767948150635],
    [38.8769521552097,-77.3733186721802]],
    [[38.8783720409729,-77.3724174499512],
    [38.8798420104618,-77.3733830451965],
    [38.8809945789057,-77.3758506774902],
    [38.8809611713878,-77.3782968521118],
    [38.8795413373583,-77.3796486854553]] 
]

w = shapefile.Writer(shapeType = shapefile.POLYGONZ, target="testpyshp.shp")
w.field('test','N')
for i,poly in enumerate(geometries):
      w.poly([geometry.from_wkt(poly).exterior.coords])
      w.record(i)

w.save('testpysh')