# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:54:11 2019

@author: DPCN
"""
def get_the_envelope(item,county,bufferdist=0):
    thequery = """NAME = '"""+county+"""'"""
    sdf_county = item.layers[0].query(where=thequery).df
    geom_bbox = arcgis.geometry.Geometry(sdf_county.spatial.bbox)
    geom_buffer = arcgis.geometry.buffer([geom_bbox],sdf_county.spatial.sr,unit='METERS',distances=bufferdist)[0]
    geom_proj_bbox = arcgis.geometry.project([geom_buffer],26910,4326)[0]
    return geom_proj_bbox.extent
item_roads = arcgis.gis.Item(my_gis,'69bdef90525d46e6b8100bca4eed7cb9')
envelope = get_the_envelope(item_roads,'Riverside',200)


print('Getting template map data...')
itemid_wm_template = '3953a9f8d76345ad8802623301217508'
item_wm_template = arcgis.gis.Item(my_gis,itemid_wm_template)

data_wm_definition = item_wm_template.get_data()

for op_lyr in data_wm_definition['operationalLayers']:
    
    if op_lyr['title']=='Vegetation Point':
        op_lyr['url']   = '{}/0'.format(item_hfv.url)
        op_lyr['itemId'] = item_hfv.id
    
    elif op_lyr['title']=='Vegetation Project':
        op_lyr['url']   = '{}/1'.format(item_hfv.url)
        op_lyr['itemId'] = item_hfv.id
        
    elif op_lyr['title']=='Inspection Scope':
        op_lyr['layerDefinition'] = {'definitionExpression': "NAME = '"+county+"'"}


print('Creating map copy...') 
item_map = arcgis.mapping.WebMap().save({
    'title': 'Demo Map - '+county,
    'snippet': 'DevSummit',
    'tags': ['DevSummit',county],
    'typeKeywords': [
        'ArcGIS Online',
        'Collector',
        'Data Editing',
        'Explorer Web Map',
        'Map',
        'Offline',
        'Online Map',
        'Web Map'
        ]
    })


    # Push Updates To Map
item_map.update(
    {
        'text': data_wm_definition,
        'extent': '{},{},{},{}'.format(
            envelope[0],
            envelope[1],
            envelope[2],
            envelope[3]
        ),
        'spatialReference': '4326'
    }
)
