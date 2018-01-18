import SuperPro_data as SP_data
import json
import sys

input_path = sys.argv[1]
feedstock = sys.argv[2]
process = sys.argv[3]


result = SP_data.SuperPro_translate(input_path, feedstock)

with open('static/SuperPro_data_{}.js'.format(process), 'w') as outfile:
    json.dump(result, outfile)
