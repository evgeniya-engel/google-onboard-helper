import numpy as np
import pandas as pd
# import ruamel.yaml as yaml
from ruamel.yaml import YAML

yaml = YAML(typ='rt')

def export_update_config(building_config, abel_config, abel_flags, dump_path, entity_list = None, max_items = 50):
    '''
    Exports Onboard-Update config yaml. If there are more than 100 Entities to update, multiple config files will be exported to prevent DB API operation deadline errors.
    Args:
        building_config_path: path to building config export
        abel_config_path: path to ABEL config
        dump_path: path to the new onboard-update yaml
        entity_list: list of Entity Guids, if only need to export a config for select Entities. Default: None, all entities will be exported.
    '''
    MAX_ITEMS_PER_CONFIG = max_items

    new_abel_config = {}
    if entity_list:
        for key, val in abel_config.items():
            if key in entity_list:
                new_abel_config[key] = val
        abel_config = new_abel_config.copy()

    config_top = {}
    config_top['CONFIG_METADATA'] = {'operation': "UPDATE"}
    building = [{key: val} for key, val in building_config.items() if val.get('type') and val['type']=='FACILITIES/BUILDING'][0]
    config_top = config_top | building

    num_reporting_entities = len([key for key, val in abel_config.items() if 'translation' in val])
    print(f'{num_reporting_entities} reporting entities found')

    update_config = {}
    entity_counter = 0
    chunk_counter = 1

    status = {
            'errors': [],
            'added_entities': [],
            'saved_files': []
            }

    for idx, items in enumerate(abel_config.items()):
        key = items[0]
        val = items[1]

        if val.get('translation'):

            if key in building_config.keys():

                if building_config[key].get('etag'):
                    etag = str(building_config[key].get('etag'))
                else: etag = 'MISSING ETAG'

                if not abel_flags:
                    val['operation'] =  'UPDATE'
                    val['update_mask'] = ['type', 'translation']

                update_config[key] = {'etag': etag} \
                                | val

                status['added_entities'].append(key)
                entity_counter += 1
            else: status['errors'].append(f'Not in building config: {key}')
        else: pass

        if entity_counter!=0 and any([entity_counter%MAX_ITEMS_PER_CONFIG==0, idx==len(abel_config.keys())-1]):
            
            new_file_name = dump_path.replace('.yaml', f'_pt{chunk_counter}.yaml')
            update_config = config_top | update_config

            with open(new_file_name, 'w') as f:
                for key, value in update_config.items():
                    yaml.dump({key: value}, f)
                    f.write('\n')
                f.close()
            status['saved_files'].append(f"{entity_counter} entities saved in {new_file_name}.")

            update_config = {}
            chunk_counter += 1
            entity_counter = 0
        else: pass
    return status


def export_add_config(building_config, abel_config, abel_flags, dump_path):
    '''
    Exports Onboard-Add config yaml.
    Args:
        building_config_path: path to building config export (export a new building config after Onboard-Update operation!)
        abel_config_path: path to ABEL config
        dump_path: path to the new onboard-add yaml
    '''
    status = {
            'errors': [],
            'added_entities': [],
            'saved_files': []
            }

    config_top = {}
    config_top['CONFIG_METADATA'] = {'operation': "UPDATE"}
    building = [{key: val} for key, val in building_config.items() if val.get('type') and val['type']=='FACILITIES/BUILDING'][0]
    config_top = config_top | building

    add_virtual = {}
    update_virtual = {}
    reporting_add_virtual = {}
    reporting_update_virtual = {}

    for key, val in abel_config.items():

        if val.get('links'):
            if not abel_flags:
                val['operation'] = 'ADD'

            if val.get('operation')=='ADD':
                add_virtual[key] = val
            if val.get('operation')=='UPDATE':
                update_virtual[key] = val

            for link in val['links']:
                if link in abel_config:
                    link_data = abel_config[link]
                elif link in building_config:
                    link_data = building_config[link]
                else:
                    link_data = {}
                    status['errors'].append(f'Link {link} from {val.get('code')} (guid: {key}) not found in abel and building config.')

                if link_data.get('operation'):
                    link_data.pop('operation')
                if link_data.get('update_mask'):
                    link_data.pop('update_mask')
                if link_data.get('etag'):
                    link_data['etag'] = str(link_data['etag'])

                if val.get('operation')=='ADD':
                    if link not in reporting_add_virtual:
                        reporting_add_virtual[link] = link_data
                if val.get('operation')=='UPDATE':
                    if link not in reporting_update_virtual:
                        reporting_update_virtual[link] = link_data

    add_config = config_top | reporting_add_virtual | add_virtual
    update_config = config_top | reporting_update_virtual | update_virtual
    if len(reporting_add_virtual) > 0:
        final_file_path = dump_path.replace('.yaml', '_add_virtual.yaml')
        with open(f'{final_file_path}', 'w') as f:
            for key, value in add_config.items():
                yaml.dump({key: value}, f)
                f.write('\n')
            f.close()
            status['saved_files'].append(f"Saved file: {final_file_path}")
    if len(reporting_update_virtual) > 0:
        final_file_path = dump_path.replace('.yaml', '_update_virtual.yaml')
        with open(f'{final_file_path}', 'w') as f:
            for key, value in add_config.items():
                yaml.dump({key: value}, f)
                f.write('\n')
            f.close()
            status['saved_files'].append(f"Saved file: {final_file_path}")

    return status


def update_etags(building_config, onboard_config, file_name):
    '''
    Updates etags in existing onboard config.
    Args:
        building_config_path: path to building config export (export a new building config after Onboard-Update operation!)
        onboard_config_path: path to existing onboard config
    '''
    status = {
            'errors': [],
            'added_entities': [],
            'saved_files': []
            }

    for guid, val in onboard_config.items():
        if guid != 'CONFIG_METADATA' and any([val.get('operation') and val.get('operation').lower()=='update',
                                              val.get('translation')]):
            if building_config[guid].get('etag'):
                onboard_config[guid] = onboard_config[guid] | {'etag': str(building_config[guid]['etag'])}
            else: status['errors'].append(f"No etag for: {guid}, {val.get('code')}")

    new_file_name = file_name.replace('.yaml','_upd.yaml')
    with open(new_file_name, 'w') as f:
        for key, value in onboard_config.items():
            yaml.dump({key: value}, f)
            f.write('\n')
        f.close()
    status['saved_files'].append(f"Saved file: {new_file_name}")

    return status
