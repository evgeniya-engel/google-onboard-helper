import streamlit as st
import re

import numpy as np
import pandas as pd
from ruamel.yaml import YAML

# UI
tab_config_exporter, tab_stubby = st.tabs(["Config Exporter", "Stubby Commands"])


with tab_config_exporter:
    helper_option = st.selectbox(
        "Select operation",
        ("Export Update Config", "Export Add Config", "Update Etags"),
        index=None,
        placeholder="Select operation...",
    )
    if helper_option=="Export Update Config":
        building_config_file = st.file_uploader("Building Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)
        abel_config_file = st.file_uploader("ABEL Config", type=None, accept_multiple_files=False, key=None, help=None, on_change=None)

        if building_config_file:
            building_config_bytes = building_config_file.getvalue()
            with open(building_config_bytes, 'r') as f:
                building_config = yaml.load(f)
                f.close()
            st.write([key for key in building_config.keys()])
        if abel_config_file:     
            abel_config_bytes = abel_config_file.getvalue()
            with open(abel_config_bytes, 'r') as f:
                abel_config = yaml.load(f)
                f.close()
            st.write([key for key in abel_config.keys()])


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
            entity_guids = entity_guids.split(",")
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
        
        if building_code_input and config_input:
            st.code(
                f"""
                stubby call blade:google.cloud.digitalbuildings.v1alpha1.digitalbuildingsservice-prod google.cloud.digitalbuildings.v1alpha1.DigitalBuildingsService.OnboardBuilding --print_status_extensions --proto2 "name: 'projects/digitalbuildings/{building_country}/cities/{building_city}/buildings/{building_code}', profile:'projects/digitalbuildings/profiles/MaintenanceOps'" --set_field "topology_file=readfile({config_input})"
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