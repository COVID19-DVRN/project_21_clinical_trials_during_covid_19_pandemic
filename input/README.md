# Data description

### Gathering the raw json data of all clinical trials:
A dump of all the clinical trials registered in clinicaltrials.gov can be found [in this link](https://clinicaltrials.gov/api/gui/ref/download_all), both in [xml format](https://ClinicalTrials.gov/AllAPIXML.zip) ([xml schema](https://clinicaltrials.gov/api/info/study_structure?fmt=XML)) and [json format](https://ClinicalTrials.gov/AllAPIJSON.zip) ([json schema](https://clinicaltrials.gov/api/info/study_structure?fmt=JSON)).

### The 2021-06-16 data
I downloded the 2021-06-16 and placed a backup copy here: https://drive.google.com/drive/folders/1tQc5TW_b56aWAkTvpkrlHjOLGiT6NK5g?usp=sharing

At the same day I searched for all the clinical trials that are related to COVID-19. I have tried three different search terms in the [clinicaltrial.gov](https://clinicaltrials.gov/) website: "covid-19", "covid 19", "covid19". All three keywords yielded 5956 studies when we selected "All studies" option (the other option was "Recruiting and not yet recruiting studies"). This is kept as an input in `project_21_clinical_trials_during_covid_19_pandemic/input/raw/studies` directory. Before downloading the trials data, I selected all the columns by going to the "Show/Hide Columns" option.