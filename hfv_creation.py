# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:29:27 2019

@author: dpcn
"""



county = 'Riverside'

print('Setting up base data...')
item_base_data = arcgis.gis.Item(my_gis,'11f10170934c413c8db8a40563ed9a4a')
flc_base_data = arcgis.features.FeatureLayerCollection.fromitem(item_base_data)


print('Creating hosted feature view...')
item_hfv = flc_base_data.manager.create_view('Vegetation_'+county)
flc_hfv = arcgis.features.FeatureLayerCollection.fromitem(item_hfv)


print('Configuring editing ability and tracking...')
flc_hfv.manager.update_definition({
        'capabilities': 'Query, Editing, Update, Sync, Create, Update, Delete, ChangeTracking',
    })

print('Updating definition and templates in layers...')
for layer in flc_hfv.layers:
    types = [dict(feat_type) for feat_type in layer.properties.types]
    for feat_type in types:
        feat_type['templates'][0]['prototype']['attributes']['COUNTY']=county
    
    layer.manager.update_definition({
                'viewDefinitionQuery': "COUNTY = '{}'".format(county),
                'types':types
            })

print('Moving new hosted feature view to a folder...')
item_hfv.move('Demo for DevSummit')


    