# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 20:30:37 2019

@author: dpcn
"""

url = ''
lyr_update = arcgis.features.FeatureLayer(url,my_gis)

fset = lyr_update.query()

counter = 1
for feature in fset.features:
    new_id = 'ID_'+str(counter).zfill(5)
    feature.set_value('AUTO_ID',new_id)
    counter += 1
    
    
lyr_update.edit_features(updates=fset.features)