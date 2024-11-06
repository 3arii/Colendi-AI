import pandas as pd
import json

workbook = pd.read_excel('tag_data.xlsx')

json_dict = {}

for index, row in workbook.iterrows():
    tag = row['Tag']
    question = row['Question']
    
    if tag not in json_dict:
        json_dict[tag] = {}  
        json_dict[tag]['Questions'] = {}  
        question_counter = 1  

    json_dict[tag]['Questions'][f'Q{question_counter}'] = question
    question_counter += 1

json_object = json.dumps(json_dict, indent=4, ensure_ascii=False)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

