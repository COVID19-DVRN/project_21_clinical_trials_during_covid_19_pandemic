# -*- coding: utf-8 -*-

"""
Summary:
    It takes a input file that has a list of NCT trials and then outputs the
    needed columns as a csv file
Input:
    list of NCTs
Output
    CSV file containing the needed row for analysis for the selected NCTs
"""

import pandas as pd
import json
from helpers.ctgov_helper_functions import grab_single_nct_json_from_whole_dump

studies_input_base_dirname = "../input/raw/studies"
condition_name = "covid19"
date_accessed = "20210616"
studies_input_file_basename = f"{condition_name}_{date_accessed}"
studies_input_fname = f"{studies_input_base_dirname}/{studies_input_file_basename}.csv"
df_input_studies = pd.read_csv(studies_input_fname, na_filter = False, dtype=str)
json_dump_dir = f"../input/untracked/AllAPIJSON_{date_accessed}"

headers = [
	"NCTId",
	"StudyFirstSubmitDate",
	"StartDate",
	"StartDateType",
	"InterventionType",
	"InterventionName",
	"InterventionOtherNameList",
	]

list_of_metadata_that_repeats_for_each_intervetion = [
	"NCTId",
	"StudyFirstSubmitDate",
	"StartDate",
	"StartDateType",
]

## First let's create a list of interventions
all_rows = []
for nct_id in df_input_studies["NCT Number"].values:
	current_nct_whole_doc = grab_single_nct_json_from_whole_dump(nct_id,json_dump_dir)
	## In case we did not get a json document we will keep the loop
	if not current_nct_whole_doc:
		print(f"Current NCT file for {nct_id} is not found in the directory")
		continue
	else:
		print(f"Adding NCT file for {nct_id} in the dataframe")
	current_nct_metadata = {}
	current_nct_metadata["NCTId"] = nct_id
	## Adding other metadata
	if "StatusModule" in current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]:
		current_nct_metadata["StudyFirstSubmitDate"] = current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]["StatusModule"]["StudyFirstSubmitDate"] 
		current_nct_metadata["StartDate"] = ""
		current_nct_metadata["StartDateType"] = ""
		if "StartDateStruct" in current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]["StatusModule"]:
			current_nct_metadata["StartDate"] = current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]["StatusModule"]["StartDateStruct"]["StartDate"]
			if "StartDateType" in current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]["StatusModule"]["StartDateStruct"]:
				current_nct_metadata["StartDateType"] = current_nct_whole_doc["FullStudy"]["Study"]\
					["ProtocolSection"]["StatusModule"]["StartDateStruct"]["StartDateType"]


	## maintaining a list for repeated rows coming from the same study
	repeated_rows_for_same_study = []
	## creating the list of the interventions
	list_of_interventions = []
	if "ArmsInterventionsModule" in current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]:
		if "InterventionList" in current_nct_whole_doc["FullStudy"]["Study"]\
				["ProtocolSection"]["ArmsInterventionsModule"]:			
			for intervention in current_nct_whole_doc["FullStudy"]["Study"]\
					["ProtocolSection"]["ArmsInterventionsModule"]["InterventionList"]["Intervention"]:
				current_intervention = {}
				current_intervention["InterventionType"] = intervention["InterventionType"]			
				current_intervention["InterventionName"] = ""
				if "InterventionName" in intervention:
					current_intervention["InterventionName"] = intervention["InterventionName"]
				if "InterventionOtherNameList" not in intervention:
					current_intervention["InterventionOtherNameList"] = ""
				else:
					current_intervention["InterventionOtherNameList"] = "|".join(intervention["InterventionOtherNameList"]["InterventionOtherName"])
				list_of_interventions.append(current_intervention)
	
	if len(list_of_interventions) > 0:
		for intervention in list_of_interventions:
			for metadata in list_of_metadata_that_repeats_for_each_intervetion:
				intervention[metadata] = current_nct_metadata[metadata]
			repeated_rows_for_same_study.append(intervention)
	else:
		## If there was no intervention
		intervention = {}
		intervention["InterventionType"] = ""
		intervention["InterventionName"] = ""
		intervention["InterventionOtherNameList"] = ""
		for metadata in list_of_metadata_that_repeats_for_each_intervetion:
				intervention[metadata] = current_nct_metadata[metadata]
		repeated_rows_for_same_study.append(intervention)
	
	for row in repeated_rows_for_same_study:
		all_rows.append(row)

df = pd.DataFrame(all_rows)

studies_output_base_dirname = "../output/studies"
studies_output_file_basename = f"{studies_input_file_basename}_interventions"
studies_ouput_fname = f"{studies_output_base_dirname}/{studies_output_file_basename}.csv"
df= df[headers]
df.to_csv(studies_ouput_fname,index=False)

## For report
df["InterventionType"].value_counts()