from __future__ import division
import xlrd
import pandas as pd
import json
import unit_conversions_and_mw.feedstock_conversions as feedstock_data
from unitconvert import massunits, volumeunits


hhv_ethanol = 29.7 # MJ/kg
density_ethanol = 0.789 #kg/L
density_methane = 0.000656 #kg/Lc
hhv_methane = 52.2 # MJ/kg

results = {}

unit_types = {
    "mass": ['kg', 'g', 'lb'],
    "volume": ['l', 'ft3(STP)', 'gal(STP)', 'ml', 'km3(STP)', 'm3(STP)', 'cm3(STP)', 'oz'],
}

unit_translate = {
    'kg': 'kg', 
    'g': 'g',
    'oz': 'oz',
    'lb': 'lb',
    'MT': 'MT',
    'ton': 'ton',
    'Ml': 'megaliters', 
    'kl': 'kiloliters', 
    'l': 'l', 
    'ml': 'ml', 
    'ft3(STP)': 'ft3',
    'gal(STP)': 'gal',
    'kW-h': 'kW-h',
}

SuperPro_names = {
    "Corn Liquor": "csl.kg",
    "Diammonium phos": "dap.kg",
    "EMIM Acetate": "ionicLiquid_amount",
    "Hydrolase": "cellulase_amount",
    "Methane": "ng_input_stream_MJ",
    "NaOH (50% w/w)": "naoh.kg",
    "Octane": "octane_ltr",
    "Std Power": "electricity_requirements",
    "Stover": "feedstock",
    "WWT nutrients": "caoh.kg"
}

def getValueUnitIndex(results, worksheet, title):
    for row, heading in enumerate(worksheet.col_values(1)):
        if heading == title:
            start_row = row
            for row, heading in enumerate(worksheet.col_values(1)[start_row:]):
                if heading == 'TOTAL':
                    end_row = start_row+row
                    break
    value_index = worksheet.row_values(start_row).index("Annual\nAmount")
    unit_index = value_index + 1 + next(i for i, j in enumerate(worksheet.row_values(start_row+1)[value_index+1:]) if j)

    for row, item in enumerate(worksheet.col_values(1)[start_row+1:end_row]):
        results.update({item: [worksheet.cell(start_row+row+1, value_index).value, worksheet.cell(start_row+row+1, unit_index).value]})

def getEthanolProduced(worksheet):
    for row, title in enumerate(worksheet.col_values(1)):
        if title == 'Cost Basis Annual Rate':
            value_index = next(i for i, j in enumerate(worksheet.row_values(18)[2:]) if j) + 2
            unit_index = next(i for i, j in enumerate(worksheet.row_values(18)[value_index+1:]) if j) + value_index + 1
            ethanol_val = worksheet.cell(row, value_index).value
            ethanol_unit = worksheet.cell(row, unit_index).value
    return [ethanol_val, ethanol_unit]

def convertToKg(ethanol):
    unit_str = ethanol[1].replace(' ', '')
    if '(' in unit_str:
        unit_str = unit_str[:unit_str.index('(')]
    elif 'U' in unit_str:
        unit_str = unit_str[:unit_str.index('U')]
    if unit_str == 'gal':
        ethanol_kg = ethanol[0] * 3.78 * density_ethanol

    elif unit_str == 'kg':
        ethanol_kg = ethanol[0]

    elif unit_str == 'l':
        ethanol_kg = ethanol[0] * density_ethanol

    elif unit_str == 'lb':
        ethanol_kg = ethanol[0] * 0.453592

    else:
        print ("units not found")
        return

    return ethanol_kg


def setSuperProNames(result_json):
    results_names = {}
    for key, value in SuperPro_names.iteritems():
        if key in result_json.keys():
            results_names.update({value:result_json[key]})
    return results_names

def setSIUnits(result_json):
    results_units = {}
    for key, value in result_json.iteritems():
        unit = unit_translate[value[1]]
        if value[1] in unit_types['mass']:
            real_unit = massunits.MassUnit(value[0], unit, 'kg').doconvert()
        elif value[1] in unit_types['volume']:
            real_unit = volumeunits.VolumeUnit(value[0], unit, 'l').doconvert()         
        else:
            if value[1] == 'ton':
                real_unit = value[0] * 907.18500036199
            elif value[1] == 'MT':
                real_unit = value[0] * 1000
            else:
                real_unit = value[0]
                    
        results_units.update({key:real_unit})   
    return results_units

def SuperPro_translate(path, feedstock):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)

    getValueUnitIndex(results, worksheet, 'Bulk Material')
    getValueUnitIndex(results, worksheet, 'Utility')

    result_names = setSuperProNames(results)
    result_units = setSIUnits(result_names)

    ethanol = getEthanolProduced(worksheet)
    ethanol_kg = convertToKg(ethanol)
    feedstock_amnt = result_units['feedstock']
    ethanol_MJ = ethanol_kg * hhv_ethanol
    ethanol_l = ethanol_kg / density_ethanol
    cellulose_amnt = feedstock_data.cellulose[feedstock]
    sugar_amnt = feedstock_data.sugars[feedstock]

    final_results = {}
    for key, value in result_units.iteritems():
        if key == 'caoh.kg':
            result = value / ethanol_kg
        if key == 'cellulase_amount':
            result = value / (cellulose_amnt * feedstock_amnt)
        if key == 'csl.kg':
            result = value / (sugar_amnt * feedstock_amnt) * 1000
        if key == 'dap.kg':
            result = value / (sugar_amnt * feedstock_amnt) * 1000
        if key == 'electricity_requirements':
            result = value / ethanol_kg
        if key == 'feedstock':
            result = value / ethanol_kg
        if key == 'ionicLiquid_amount':
            result = value / feedstock_amnt
        if key == 'naoh.kg':
            result = value / ethanol_kg
        if key == 'ng_input_stream_MJ':
            result = value * density_methane * hhv_methane / (hhv_ethanol * ethanol_kg)
        if key == 'octane_ltr':
            result = value / ethanol_l
        final_results.update({key:result})

    return final_results

