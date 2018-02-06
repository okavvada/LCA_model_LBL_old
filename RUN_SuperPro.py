import SuperPro_data as SP_data
import json
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--path', help='this is the xls file path')
parser.add_argument('--feedstock', choices=['corn_stover','sorgum'], help='Select your feedstock')
parser.add_argument('--fuel', choices=['ethanol','jet_fuel'], help='Select your fuel')
parser.add_argument('--preprocess', choices=['waterwash', 'iHG-Current', 'iHG-Projected', 'All'], help='Select the preprocessing step')

args=parser.parse_args()

result = SP_data.SuperPro_translate(args.path, args.feedstock, args.fuel, args.preprocess)

with open('static/SuperPro_data_{}.js'.format(args.preprocess), 'w') as outfile:
    json.dump(result, outfile)
