# Masking water areas in digital elevation models

Digital elevation models (dem) can contain a lot of errors at water areas. The sea areas of Finnish 2m dem for example, can contain several meters of value differences on both sides of 0. This is why it is usually good practice to mask sea areas to value 0 before running any further analyses on them. In the image 1 you can see clearly dem value differences at the sea areas.

<img src='https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/images/value_difference.png'>

Image 1. Water areas of digital elevation models can contain value errors that affect spatial analyses. 

A good practice is to use vector format polygons for masking the water areas. In Finland you can use Topographic database (Maastotietokanta) data. In this example we want to mask the sea areas to value 0 so we use the MTK-Vakavesi file and the layer "meri". Example of the sea polygons on top of the dem in image 2.

<img src='https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/images/sea_polygons.PNG'>

If you don't have acceess to Taito, you can download the MTK-Vakavesi data from [Paituli][1].
The 2m and 10m dem data of Finland is availabe at [File service of open data][2] by NLS. 






[1]:https://avaa.tdata.fi/web/paituli/latauspalvelu?data_id=mml_maasto_10k_2019_gpkg_euref
[2]:https://tiedostopalvelu.maanmittauslaitos.fi/tp/kartta?lang=en


