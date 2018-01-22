import SuperPro_data as SP_data
import json
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--path', help='this is the xls file path')
parser.add_argument('--feedstock', choices=['corn_stover','sorgum'], help='Foo the program')
parser.add_argument('--preprocess', choices=['waterwash', 'iHG-Current', 'iHG-Projected'], help='Foo the program')

args=parser.parse_args()

result = SP_data.SuperPro_translate(args.path, args.feedstock)

with open('static/SuperPro_data_{}.js'.format(args.preprocess), 'w') as outfile:
    json.dump(result, outfile)
