import streamlit as st
import re
import os

import numpy as np
import pandas as pd
from ruamel.yaml import YAML
yaml = YAML(typ='rt')

from onboarding_utils import *

# UI
tab_config_exporter, tab_stubby = st.tabs(["Config Exporter", "Stubby Commands"])


def clear_folder(folder_path):
    """
    Removes all files from the specified folder.
    Leaves subdirectories intact.
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # os.unlink is an alias for os.remove
            # else:
            #     print(f"Skipping directory: {file_path}")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
    print(f"All files removed from '{folder_path}'.")

with tab_config_exporter:
    helper_option = st.selectbox(
        "Select operation",
        ("Export Reporting Entity Config", "Export Virtual Entity Config", "Update Etags"),
        index=None,
        placeholder="Select operation...",
    )
    if helper_option=="Export Reporting Entity Config":
        file_export_path = st.text_input("File Export Path")
        building_config_file = st.file_uploader("Building Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)
        abel_config_file = st.file_uploader("ABEL Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)
        use_abel_flags = st.checkbox("Use 'operation' and 'update_mask' from ABEL config", value=True)

        abel_config = None
        building_config = None

        save_folder = "files"
        clear_folder(f'./{save_folder}')

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        if building_config_file:
            building_config_bytes = building_config_file.read()
            building_config_bytes = building_config_bytes.decode("UTF-8")

            with open(f"{save_folder}/{building_config_file.name}", "w") as f:
                f.write(building_config_bytes)

            with open(f"{save_folder}/{building_config_file.name}", 'r') as f:
                building_config = yaml.load(f)
                f.close()
            os.remove(f"{save_folder}/{building_config_file.name}")

        if abel_config_file:     
            abel_config_bytes = abel_config_file.read()
            abel_config_bytes = abel_config_bytes.decode("UTF-8")

            with open(f"{save_folder}/{abel_config_file.name}", "w") as f:
                f.write(abel_config_bytes)

            with open(f"{save_folder}/{abel_config_file.name}", 'r') as f:
                abel_config = yaml.load(f)
                f.close()
            clear_folder(f'./{save_folder}')

        export = st.button("Export")
        if export:
            if building_config and abel_config and file_export_path:
                status = export_update_config(building_config, abel_config, use_abel_flags, file_export_path)

                if len(status['errors']) > 0:
                    st.write("Errors found:")
                    st.write([_ for _ in status['errors']])
                if len(status['saved_files']) > 0:
                    st.write("Saved files:")
                    st.write([_ for _ in status['saved_files']])
                if len(status['added_entities']) > 0:
                    st.write("Added entities:")
                    st.write([_ for _ in status['added_entities']])
    if helper_option=="Export Virtual Entity Config":
        file_export_path = st.text_input("File Export Path")
        building_config_file = st.file_uploader("Building Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)
        abel_config_file = st.file_uploader("ABEL Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)
        use_abel_flags = st.checkbox("Use 'operation' and 'update_mask' from ABEL config", value=True)

        abel_config = None
        building_config = None

        save_folder = "files"

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        if building_config_file:
            building_config_bytes = building_config_file.read()
            building_config_bytes = building_config_bytes.decode("UTF-8")

            with open(f"{save_folder}/{building_config_file.name}", "w") as f:
                f.write(building_config_bytes)

            with open(f"{save_folder}/{building_config_file.name}", 'r') as f:
                building_config = yaml.load(f)
                f.close()
            os.remove(f"{save_folder}/{building_config_file.name}")

        if abel_config_file:     
            abel_config_bytes = abel_config_file.read()
            abel_config_bytes = abel_config_bytes.decode("UTF-8")

            with open(f"{save_folder}/{abel_config_file.name}", "w") as f:
                f.write(abel_config_bytes)

            with open(f"{save_folder}/{abel_config_file.name}", 'r') as f:
                abel_config = yaml.load(f)
                f.close()
            os.remove(f"{save_folder}/{abel_config_file.name}")

        export = st.button("Export")
        if export:
            if building_config and abel_config and file_export_path:
                status = export_add_config(building_config, abel_config, use_abel_flags, file_export_path)

                if len(status['errors']) > 0:
                    st.write("Errors found:")
                    st.write([_ for _ in status['errors']])
                if len(status['saved_files']) > 0:
                    st.write("Saved files:")
                    st.write([_ for _ in status['saved_files']])
                if len(status['added_entities']) > 0:
                    st.write("Added entities:")
                    st.write([_ for _ in status['added_entities']])

    if helper_option=="Update Etags":
        file_export_path = st.text_input("File Export Path")
        building_config_file = st.file_uploader("Building Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)
        abel_config_file = st.file_uploader("ABEL Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)

        abel_config = None
        building_config = None

        save_folder = "files"

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        if building_config_file:
            building_config_bytes = building_config_file.read()
            building_config_bytes = building_config_bytes.decode("UTF-8")

            with open(f"{save_folder}/{building_config_file.name}", "w") as f:
                f.write(building_config_bytes)

            with open(f"{save_folder}/{building_config_file.name}", 'r') as f:
                building_config = yaml.load(f)
                f.close()
            os.remove(f"{save_folder}/{building_config_file.name}")

        if abel_config_file:     
            abel_config_bytes = abel_config_file.read()
            abel_config_bytes = abel_config_bytes.decode("UTF-8")

            with open(f"{save_folder}/{abel_config_file.name}", "w") as f:
                f.write(abel_config_bytes)

            with open(f"{save_folder}/{abel_config_file.name}", 'r') as f:
                abel_config = yaml.load(f)
                f.close()
            os.remove(f"{save_folder}/{abel_config_file.name}")

        export = st.button("Export")
        if export:
            if building_config and abel_config:
                status = update_etags(building_config, abel_config, file_export_path)

                if len(status['errors']) > 0:
                    st.write("Errors found:")
                    st.write([_ for _ in status['errors']])
                if len(status['saved_files']) > 0:
                    st.write("Saved files:")
                    st.write([_ for _ in status['saved_files']])

with tab_stubby:

    st.subheader('Stubby Commands')
    dbapi_option = st.selectbox(
        "Select operation",
        ("Export Building Config", "Onboard Building"),
        index=None,
        placeholder="Select operation...",
    )
    if dbapi_option=='Export Building Config':
        building_code_input = st.text_input('Building Code')
        if building_code_input:
            building_split = str.split(building_code_input.lower(), "-")
            if len(building_split)==3:
                building_country = building_split[0]
                building_city = building_split[1]
                building_code = building_split[2]
        entity_guids_input = st.text_input('Guids (optional)')
        if entity_guids_input:
            entity_guids = re.sub(r"[, \n]+", ',', entity_guids_input)
            entity_guids = set(entity_guids.split(","))
            entity_guids = ",".join(f"'{guid}'" for guid in entity_guids)
        
        if building_code_input:
            if entity_guids_input:
                st.code(
                    f"""
                    stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.ExportBuildingConfig --deadline=60000 --print_status_extensions --proto2 "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', 
                    profile:'projects/digitalbuildings/profiles/MaintenanceOps',instance_guid:[{entity_guids}]"
                    """,
                    wrap_lines=True
                    )
            else:
                st.code(
                    f"""
                    stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.ExportBuildingConfig --deadline=60000 --print_status_extensions --proto2 "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps'"
                    """,
                    wrap_lines=True
                    )

        operation_input = st.text_input('Operation ID')
        output_path_input = st.text_input('Output Path (optional)')
        if operation_input:
            if output_path_input:
                st.code(
                    f"""
                    stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.GetOperation  --print_status_extensions --proto2 --outfile={output_path_input} --binary_output "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps', operation_name: '{operation_input}'"
                    """,
                    wrap_lines=True
                    )
            else:
                st.code(
                    f"""
                    stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.GetOperation  --print_status_extensions --proto2 --binary_output "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps', operation_name: '{operation_input}'"
                    """,
                    wrap_lines=True
                    )

    if dbapi_option=='Onboard Building':
        building_code_input = st.text_input('Building Code')
        if building_code_input:
            building_split = str.split(building_code_input.lower(), "-")
            if len(building_split)==3:
                building_country = building_split[0]
                building_city = building_split[1]
                building_code = building_split[2]

        config_input = st.text_input('Config Path')
        
        if building_code_input and config_input and len(building_split)==3:
            st.code(
                f"""
                stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.OnboardBuilding --print_status_extensions --proto2 "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps'" --set_field "topology_file=readfile({config_input})"
                """,
                wrap_lines=True
                )

        operation_input = st.text_input('Operation ID')
        output_path_input = st.text_input('Output Path (optional)')
        if operation_input:
            if output_path_input:
                st.code(
                    f"""
                    stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.GetOperation  --print_status_extensions --proto2 --outfile={output_path_input} --binary_output "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps', operation_name: '{operation_input}'"
                    """,
                    wrap_lines=True
                    )
            else:
                st.code(
                    f"""
                    stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.GetOperation  --print_status_extensions --proto2 --binary_output "name: 'projects/digitalbuildings/countries/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps', operation_name: '{operation_input}'"
                    """,
                    wrap_lines=True
                    )
