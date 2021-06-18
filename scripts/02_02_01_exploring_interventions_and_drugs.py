# -*- coding: utf-8 -*-

"""
Summary:
    It takes a input file that has a list of NCT trials and their interventions
    and then does EDA on top of it
Input:
    
Output
    
"""

import pandas as pd
import json
from helpers.ctgov_helper_functions import grab_single_nct_json_from_whole_dump

output_code = "02_02_01"
report_lines = []

condition_name = "covid19"
date_accessed = "20210616"
studies_input_file_basename = f"{condition_name}_{date_accessed}"

studies_input_base_dirname = "../input/raw/studies"
studies_input_fname = f"{studies_input_base_dirname}/{studies_input_file_basename}.csv"
df_trials = pd.read_csv(studies_input_fname)

trials_input_base_dirname = "../output/studies"
trials_input_fname = f"{trials_input_base_dirname}/{studies_input_file_basename}_interventions.csv"
df_interventions = pd.read_csv(trials_input_fname, na_filter = False, dtype=str)
df_interventions["InterventionName_lower"] = df_interventions["InterventionName"].str.lower()

## For report
report_lines.append(f"\nThe count of all the possible interventions applied to {len(df_trials)} {condition_name} trials (found in clinicaltrials.gov) as of {date_accessed} by their type:")
report_lines.append(df_interventions["InterventionType"].value_counts().to_string())
report_lines.append("note that one trial can include multiple different interventions")
report_lines.append(f"\nYou can find all the trial id and the intervention in this file: {trials_input_fname}")

## Now reporting the number of unique interventions by their type
report_lines.append(f"\nThe count of all the possible unique interventions by their type:")
report_lines.append(df_interventions.groupby("InterventionType")["InterventionName_lower"].nunique().sort_values(ascending=False).to_string())

## Now we will generate all the possible unique intervention terms only in a file
unique_interventions_output_base_dirname = "../output"
unique_interventions_output_fname = f"{unique_interventions_output_base_dirname}/{studies_input_file_basename}_unique_intervention_terms_only.csv"
df_unique_interventions = df_interventions.groupby(['InterventionName_lower']).size().reset_index(name='Freq').sort_values(by="Freq",ascending=False)
df_unique_interventions.to_csv(unique_interventions_output_fname, index=False)
report_lines.append(f"\nThe unique {len(df_unique_interventions)} intervention terms are listed in the file {unique_interventions_output_fname}")

## Now we will generate all the possible unique intervention terms by their type in a file
unique_interventions_with_type_output_base_dirname = "../output"
unique_interventions_with_type_output_fname = f"{unique_interventions_output_base_dirname}/{studies_input_file_basename}_unique_interventions_with_type.csv"
df_interventions.groupby(['InterventionType', 'InterventionName_lower']).size().reset_index(name='Freq').sort_values(by="Freq",ascending=False).to_csv(unique_interventions_with_type_output_fname, index=False)
report_lines.append(f"\nThe unique intervention terms and type combinations (e.g. Placebo is listed in different types like Drug, Biological, Other) are listed in the file {unique_interventions_with_type_output_fname}")

with open(f"../output/reports/{output_code}_{studies_input_file_basename}_report.txt", "w") as f:
	f.writelines("\n".join(report_lines))

