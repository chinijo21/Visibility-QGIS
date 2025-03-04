from qgis.core import *
import processing

# 1. Load layers
animal_enclosure = QgsProject.instance().mapLayersByName('animal_enclosure')[0]
penas_layer = QgsProject.instance().mapLayersByName('peñas')[0]
dem_layer = QgsProject.instance().mapLayersByName('your_dem_layer')[0]  # Change to DEM name

# 2. Create viewpoints with adjusted heights (modify values as needed)
viewpoints_params = {
    'OBSERVERS': animal_enclosure,
    'DEM': dem_layer,
    'RADIUS': 20000,  # Analysis radius in meters
    'OBSERVER_HEIGHT': 1.6,  # Assuming human eye level
    'TARGET_HEIGHT': 0,  # Height of landscape features i need to change this
    'OUTPUT': 'memory:Animal_Viewpoints'
}
animal_viewpoints = processing.run("visibility:create_viewpoints", viewpoints_params)['OUTPUT']

# 3. Create viewpoints for all peñitas
penas_params = {
    'OBSERVERS': penas_layer,
    'DEM': dem_layer,
    'RADIUS': 20000,
    'OBSERVER_HEIGHT': 3.0,  # Higher position for rock formations
    'TARGET_HEIGHT': 1.6,  # Height of potential observers
    'OUTPUT': 'memory:Peñas_Viewpoints'
}
penas_viewpoints = processing.run("visibility:create_viewpoints", penas_params)['OUTPUT']

# 4. Calculate intervisibility network
intervisibility_params = {
    'OBSERVERS': penas_viewpoints,
    'TARGETS': animal_viewpoints,
    'DEM': dem_layer,
    'OUTPUT_LINES': 'memory:Visibility_Lines',
    'OUTPUT_POINTS': 'memory:Visibility_Points'
}
processing.run("visibility:intervisibility_network", intervisibility_params)

# 5. Cumulative viewshed analysis
cumulative_params = {
    'OBSERVERS': penas_viewpoints,
    'DEM': dem_layer,
    'RADIUS': 20000,
    'OUTPUT': 'memory:Cumulative_Viewshed'
}
cumulative_result = processing.run("visibility:cumulative_viewshed", cumulative_params)['OUTPUT']

# 6. Add results to QGIS
QgsProject.instance().addMapLayer(animal_viewpoints)
QgsProject.instance().addMapLayer(penas_viewpoints)
QgsProject.instance().addMapLayer(intervisibility_params['OUTPUT_LINES'])
QgsProject.instance().addMapLayer(cumulative_result)

print("Analysis complete! Check layers in QGIS:")
print("- Animal Viewpoints\n- Peñas Viewpoints\n- Visibility Lines\n- Cumulative Viewshed")