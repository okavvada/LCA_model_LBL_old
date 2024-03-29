from __future__ import division
import xlrd
import pandas as pd
import numpy as np
import json
import numbers
import unit_conversions_and_mw.feedstock_conversions as feedstock_data
from unitconvert import massunits, volumeunits


hhv_ethanol = 29.7 # MJ/kg
density_ethanol = 0.789 #kg/L
hhv_jet_fuel = 46.396 # MJ/kg
density_jet_fuel = 0.840 #kg/L
density_methane = 0.000656 #kg/Lc
hhv_methane = 52.2 # MJ/kg

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
    "ChLy": "ionicLiquid_amount",
    "Hydrolase": "cellulase_amount",
    "Methane": "ng_input_stream_MJ",
    "NaOH (50% w/w)": "naoh.kg",
    "Octane": "octane_ltr",
    "Std Power": "electricity_requirements",
    "Stover": "feedstock.kg",
    "WWT nutrients": "caoh.kg",
    "Sulfuric Acid": "acid.kg",
    "Water": "water_direct_consumption",
    "Hydrogen": "h2.kg",
    "Std Power": "electricity",
    "Cooling Water": "cooling_water",
    "Chilled Water": "chilled_water"
}

sections = ["Feedstock supply logistics", "Feedstock handling", "Pretreatment", "Hydrolysis and fermentation", "Wastewater treatment", "Hydrogenation",
            "Recovery and separation", "Lignin utilization"]

sections_translate = {  "Feedstock supply logistics": "Feedstock_Supply_Logistics",
                        "Feedstock handling": "Feedstock_Handling_and_Preparation", 
                        "Pretreatment": "IL_Pretreatment", 
                        "Hydrolysis and fermentation": "Enzymatic_Hydrolysis_and_Fermentation", 
                        "Wastewater treatment": "Wastewater_Treatment",
                        "Hydrogenation": "Hydrogeneration_and_Oligomerization",
                        "Recovery and separation": "Recovery_and_Separation", 
                        "Lignin utilization": "Lignin_Utilization"}

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

def getMaterialsPerSection(results, worksheet, section):
    results.update({section:{}}) 
    for row, title in enumerate(worksheet.col_values(0)):
        if title == '4.1.2 MATERIAL COST - BREAKDOWN BY SECTION':
            start_row = row
        if title == '4.1.3 MATERIAL COST - BREAKDOWN BY MATERIAL TYPE':
            end_row = row
    for row, title in enumerate(worksheet.col_values(0)[start_row:end_row]):
        if title == section:
            pretreat_start_row = start_row+row   
            for row, title in enumerate(worksheet.col_values(0)[pretreat_start_row:end_row]):
                if title == 'TOTAL':
                    pretreat_end_row = pretreat_start_row+row
                    break
            if section == "Feedstock supply logistics":
                value_sum = 0
                for rows in np.arange(pretreat_start_row+2, pretreat_end_row-1):
                    amount = worksheet.cell(rows, 2).value
                    if (isinstance(amount, numbers.Number) == False) and (',' in amount):
                        amount = amount.replace(',','')
                    amount = float(amount)
                    value_sum += amount
                values = [value_sum,worksheet.cell(rows, 3).value]
                results[section].update({'Stover':values})
            else:
                for rows in np.arange(pretreat_start_row+2, pretreat_end_row):
                    values = [worksheet.cell(rows, 2).value,worksheet.cell(rows, 3).value]
                    results[section].update({worksheet.cell(rows, 0).value:values})
        else:
            continue
    return results

def getUtilitiesPerSection(results, worksheet, section):
    for row, title in enumerate(worksheet.col_values(0)):
        if title == '8.2 UTILITIES COST - BREAKDOWN BY SECTION':
            start_row = row
        if title == '8.3 UTILITIES COST - BREAKDOWN BY UTILITY TYPE':
            end_row = row
    for row, title in enumerate(worksheet.col_values(0)[start_row:end_row]):
        if title == section:
            start_section = start_row + row
            end_section = end_row
            for row, title in enumerate(worksheet.col_values(0)[start_section+1:end_row]):
                if (title in sections):
                    end_section = start_section + row
                    break
            for row, title in enumerate(worksheet.col_values(0)[start_section:end_section]):
                if title == 'Utility':
                    utility_start_row = start_section + row
                    for row, title in enumerate(worksheet.col_values(0)[utility_start_row:end_row]):
                        if title == 'TOTAL':
                            utility_end_row = utility_start_row+row
                            break
                    for rows in np.arange(utility_start_row+1, utility_end_row):
                        values = [worksheet.cell(rows, 2).value,worksheet.cell(rows, 3).value]
                        if section in results.keys():
                            results[section].update({worksheet.cell(rows, 0).value:values})
                        else:
                            results.update({section:{}})
                            results[section].update({worksheet.cell(rows, 0).value:values})
        else:
            continue

    return results

def getEthanolProduced(worksheet):
    for row, title in enumerate(worksheet.col_values(1)):
        if title == 'Cost Basis Annual Rate':
            value_index = next(i for i, j in enumerate(worksheet.row_values(18)[2:]) if j) + 2
            unit_index = next(i for i, j in enumerate(worksheet.row_values(18)[value_index+1:]) if j) + value_index + 1
            ethanol_val = worksheet.cell(row, value_index).value
            ethanol_unit = worksheet.cell(row, unit_index).value
    return [ethanol_val, ethanol_unit]

def getJetFuelProduced(worksheet):
    for row, title in enumerate(worksheet.col_values(0)):
        if title == 'Unit Production Ref. Rate':
            amount = worksheet.cell(row, 1).value
            unit = worksheet.cell(row, 2).value
            if (isinstance(amount, numbers.Number) == False) and (',' in amount):
                amount = amount.replace(',','')
            amount = float(amount)
    return [amount, unit]

def convertToKg(fuel, fuel_name):
    unit_str = fuel[1].replace(' ', '')
    if fuel_name == 'ethanol':
        density_fuel = density_ethanol
    if fuel_name == 'jet_fuel':
        density_fuel = density_jet_fuel

    if '(' in unit_str:
        unit_str = unit_str[:unit_str.index('(')]
    elif 'U' in unit_str:
        unit_str = unit_str[:unit_str.index('U')]
    if unit_str == 'gal':
        fuel_kg = fuel[0] * 3.78 * density_fuel

    elif unit_str == 'kg':
        fuel_kg = fuel[0]

    elif unit_str == 'l':
        fuel_kg = fuel[0] * density_fuel

    elif unit_str == 'lb':
        fuel_kg = fuel[0] * 0.453592

    else:
        print("units not found")
        return

    return fuel_kg


def setSuperProNames(result_json):
    results_names = {}
    for key, value in result_json.iteritems():
        if key in SuperPro_names.keys():
            results_names.update({SuperPro_names[key]:value})
        else:
            results_names.update({key:value})
    return results_names

def setSIUnits(result_json):
    results_units = {}
    for key, value in result_json.iteritems():
        if (isinstance(value[0], numbers.Number) == False) and (',' in value[0]):
            value[0] = value[0].replace(',','')
        value[0] = float(value[0])
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

def SuperPro_translate(path, feedstock, fuel_name, preprocess):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)
    result_units = {}
    results = {}

    if fuel_name == 'ethanol':
        getValueUnitIndex(results, worksheet, 'Bulk Material')
        getValueUnitIndex(results, worksheet, 'Utility')

        result_names = setSuperProNames(results)
        result = setSIUnits(result_names)

        ethanol = getEthanolProduced(worksheet)
        fuel_kg = convertToKg(ethanol, fuel_name)

        fuel_MJ = fuel_kg * hhv_ethanol
        fuel_l = fuel_kg / density_ethanol
        result_units.update({preprocess:result})

    if fuel_name == 'jet_fuel':
        for section in sections:
            results = getMaterialsPerSection(results, worksheet, section)
            results = getUtilitiesPerSection(results, worksheet, section)

        for sector in results.keys():
            result_names = setSuperProNames(results[sector])
            units = setSIUnits(result_names)
            result_units.update({sector:units})

        jet_fuel = getJetFuelProduced(worksheet)
        fuel_kg = convertToKg(jet_fuel, fuel_name)

        fuel_MJ = fuel_kg * hhv_jet_fuel
        fuel_l = fuel_kg / density_jet_fuel

    if fuel_name == 'ethanol':
        feedstock_amnt = result_units[preprocess]['feedstock.kg']

    if fuel_name == 'jet_fuel':
        feedstock_amnt = result_units['Feedstock supply logistics']['feedstock.kg']

    cellulose_amnt = feedstock_data.cellulose[feedstock]
    sugar_amnt = feedstock_data.sugars[feedstock]

    final_results = {}
    for sector in result_units.keys():
        process_results = {}
        for key, value in result_units[sector].iteritems():
            if key == 'caoh.kg':
                result = value / fuel_kg
            if key == 'cellulase_amount':
                result = value / (cellulose_amnt * feedstock_amnt)
            if key == 'csl.kg':
                result = value / (sugar_amnt * feedstock_amnt) * 1000
            if key == 'acid.kg':
                result = value / (result_units[sector]['ionicLiquid_amount'])
                process_results.update({'acid':"h2so4"})
            if key == 'dap.kg':
                result = value / (sugar_amnt * feedstock_amnt) * 1000
            if key == 'electricity':
                result = value / fuel_kg
            if key == 'feedstock.kg':
                result = value / fuel_kg
            if key == 'ionicLiquid_amount':
                result = value / feedstock_amnt
            if key == 'naoh.kg':
                result = value / fuel_kg
            if key == 'ng_input_stream_MJ':
                result = value * density_methane * hhv_methane / (fuel_MJ)
            if key == 'octane_ltr':
                result = value / fuel_l
            if key == 'water_direct_consumption':
                result = value / fuel_kg
                process_results.update({'water_direct_withdrawal':result})
            if key == 'cooling_water':
                result = value / fuel_kg
            if key == 'chilled_water':
                result = value / fuel_kg
            if 'Steam' in key:
                result = value / fuel_kg
                temp = key.replace('Steam', '')
                temp = int(temp.replace('C', ''))
                if temp < 500:
                    if 'steam_low' in process_results.keys():
                        process_results['steam_low'] += result
                    else:
                        process_results.update({'steam_low':result})
                elif temp > 500:
                    if 'steam_high' in process_results.keys():
                        process_results['steam_high'] += result
                    else:
                        process_results.update({'steam_high':result})

            process_results.update({key:result})
        final_results.update({sector:process_results})
    if fuel_name == 'ethanol':
        output = final_results
    if fuel_name == 'jet_fuel':
        output = {}
        for key in final_results.keys():
            output.update({sections_translate[key]:final_results[key]})
            output.update({'Transportation':{}})


    return output

