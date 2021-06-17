# -*- coding: utf-8 -*-

"""
Summary:
    
Input:
    
Output
    
"""
import json

def grab_single_nct_json_from_whole_dump(nct_number, json_dump_dir):
	nct_dictionary = f"{json_dump_dir}/{nct_number[:7].upper()}xxxx/{nct_number.upper()}.json"
	try:
		with open(nct_dictionary,"r") as f:
			json_doc = json.load(f)
		return json_doc
	except:
		print(f"Current NCT file for {nct_number} is not found in the directory")