import pandas as pd
import numpy as np
import parameters as P
import helper_functions as hf
from unit_conversions_and_mw.feedstock_conversions import *


io_data = pd.read_csv(P.io_table_physicalunits_path).fillna(0)
water_consumption = hf.csv_dict_list(P.water_consumption_path)
water_withdrawal = hf.csv_dict_list(P.water_withdrawal_path)
# Ethanol produciton functional unit (1 kg of ethanol)
etoh_feed_stream_mass_kg = 1



def FinalImpactModel(SP_params, model, fuel='ethanol'):
    # Returns a dataframe of of all GHG emissions in the form of kg CO2e per MJ enthanol  or 
    # water impacts in the form of Liters per MJ enthanol per process
    #
    # Args:
    #  SP_common_params: common parameters dictionary
    #  SP_other_params: process specific parameters dictionary
    #  SP_analysis_params: analysis parameters dictionary
    #  model: string refering to whether the GHG model or the water model is run. Options are:
    #  'buttonGHG', 'buttonConsWater', 'buttonWithWater' for the GHG model, the water consumption model and
    #  the withdrawal model respectively
    
    # Returns:
    #  The net GHG emissions (kg CO2e) for the product life cycle by sector for model = 'buttonGHG'
    #  The net consumption water impacts (liters) for the product life cycle by sector for model = 'buttonConsWater'
    #  The net withdrawal water impacts (liters) for the product life cycle by sector for model = 'buttonWithWater'
    if fuel == 'jet_fuel':
        selectivities = P.sections
    else:
        selectivities = P.selectivity

    m = {} 
    if fuel == 'ethanol':
        for scenario in P.scenario_range:
            new_data = np.zeros([len(P.processes),len(selectivities)])
            m[scenario] = pd.DataFrame(new_data, columns=selectivities, index=P.processes)
    else:
        for scenario in P.scenario_range:
            new_data = np.zeros([len(selectivities), 1])
            m[scenario] = pd.DataFrame(new_data, columns=['All'], index=selectivities)

    for selectivity in selectivities:
        for scenario in P.scenario_range:
            y = {}
            y_cred = {}
            for item in io_data['products']:
                y.update({item:0})
                y_cred.update({item:0})
            biorefinery_direct_ghg = 0
            cooled_water_ghg = 0
            if fuel == 'ethanol':
                ionic_liquid_amount = SP_params[selectivity]['ionicLiquid_amount'][scenario]
                feedstock_amount = SP_params[selectivity]['feedstock.kg'][scenario]
            if fuel == 'jet_fuel':
                ionic_liquid_amount = SP_params['IL_Pretreatment']['ionicLiquid_amount'][scenario]
                feedstock_amount = SP_params["Feedstock_Supply_Logistics"]['feedstock.kg'][scenario]
            if 'acid.kg' in SP_params[selectivity].keys():
                if (SP_params[selectivity]['acid'] == 'hcl'):
                    y["hcl.kg"] = SP_params[selectivity]['acid.kg'][scenario] * ionic_liquid_amount
                elif (SP_params[selectivity]['acid'] == 'h2so4'):
                    y["h2so4.kg"] = SP_params[selectivity]['acid.kg'][scenario] * ionic_liquid_amount
            if 'ionicLiquid_amount' in SP_params[selectivity].keys():
                y["lysine.us.kg"] = ionic_liquid_amount * feedstock_amount * 0.58
                y["cholinium.hydroxide.kg"] = ionic_liquid_amount * 0.42  
            if 'cellulase_amount' in SP_params[selectivity].keys():
                y["cellulase.kg"] = SP_params[selectivity]['cellulase_amount'][scenario] * cellulose[SP_params['analysis_params']['feedstock']] * feedstock_amount
            if 'csl.kg' in SP_params[selectivity].keys():
                y["csl.kg"] = SP_params[selectivity]['csl.kg'][scenario]/1000 * sugars[SP_params['analysis_params']['feedstock']] * feedstock_amount
            if 'feedstock.kg' in SP_params[selectivity].keys():
                if SP_params['analysis_params']['feedstock'] == 'corn_stover':
                    y["farmedstover.kg"] = feedstock_amount
                if SP_params['analysis_params']['feedstock'] == 'sorghum':
                    y["sorghum.kg"] = feedstock_amount
                if SP_params['analysis_params']['feedstock'] == 'mixed':
                    y["sorghum.kg"] = feedstock_amount * 0.4
                    y["farmedstover.kg"] = feedstock_amount * 0.4
                    y["farmedmiscanthus.kg"] = feedstock_amount * 0.2
                    y["switchgrass.kg"] = feedstock_amount * 0.2
            if 'dap.kg' in SP_params[selectivity].keys():
                y["dap.kg"] = SP_params[selectivity]['dap.kg'][scenario]/1000 * sugars[SP_params['analysis_params']['feedstock']] * feedstock_amount
            if 'caoh.kg' in SP_params[selectivity].keys():
                y["lime.kg"] = SP_params[selectivity]['caoh.kg'][scenario]
            if 'naoh.kg' in SP_params[selectivity].keys():
                y["naoh.kg"] = SP_params[selectivity]['naoh.kg'][scenario]
            if 'hydrogen.kg' in SP_params[selectivity].keys():
                y["h2.kg"] = SP_params[selectivity]['hydrogen.kg'][scenario]
            if 'ng_input_stream_MJ' in SP_params[selectivity].keys():
                y["naturalgas.MJ"] = SP_params[selectivity]['ng_input_stream_MJ'][scenario] * (hf.FuelConvertMJ(1, "ethanol", "kg"))
            if 'octane_ltr' in SP_params[selectivity].keys():
                y["gasoline.MJ"] = (hf.FuelConvertMJ(SP_params[selectivity]['octane_ltr'][scenario]/0.789, "gasoline", "liter"))

            if (fuel == 'ethanol') or (selectivity == "Transportation"):
                y["rail.mt_km"] = ((ionic_liquid_amount * feedstock_amount/1000) * 
                                SP_params['common']['IL_rail_km'][scenario] +
                                (etoh_feed_stream_mass_kg/1000 * SP_params['common']['etoh_distribution_rail'][scenario]) +
                                (feedstock_amount/1000) * 
                                SP_params['common']['feedstock_distribution_rail'][scenario])
                y["flatbedtruck.mt_km"] = (((ionic_liquid_amount * feedstock_amount/1000) * 
                                                SP_params['common']['IL_flatbedtruck_mt_km'][scenario]) +
                                            (etoh_feed_stream_mass_kg/1000 * (
                                                SP_params['common']['etoh_distribution_truck'][scenario])) +
                                            (feedstock_amount/1000) * 
                                                SP_params['common']['feedstock_distribution_truck'][scenario])

            if 'electricity' in SP_params[selectivity].keys():
                y["electricity.{}.kWh".format(SP_params['analysis_params']['facility_electricity'])] = (
                                                            SP_params[selectivity]['electricity'][scenario]/0.789)
            if 'electricity_credit' in SP_params[selectivity].keys():
                y_cred["electricity.{}.kWh".format(SP_params['analysis_params']['facility_electricity'])] = -(
                                                            SP_params[selectivity]['electricity_credit'][scenario]/0.789)
            
            if 'ng_input_stream_MJ' in SP_params[selectivity].keys():
                biorefinery_direct_ghg += hf.FuelCO2kg(
                    SP_params[selectivity]['ng_input_stream_MJ'][scenario] * (
                        hf.FuelConvertMJ(1, "ethanol","kg")), "naturalgas") 
            if 'octane_ltr' in SP_params[selectivity].keys():
                biorefinery_direct_ghg += (hf.FuelCO2kg(hf.FuelConvertMJ(
                        SP_params[selectivity]['octane_ltr'][scenario]/0.789,"gasoline", "liter"), "gasoline"))
            if 'direct_GHG' in SP_params[selectivity].keys():
                biorefinery_direct_ghg += SP_params[selectivity]['direct_GHG'][scenario]
            if 'cooling_water' in SP_params[selectivity].keys():
                SP_params[selectivity]['water_direct_withdrawal'][scenario] += SP_params[selectivity]['cooling_water'][scenario]
                cooled_water_ghg += SP_params[selectivity]['cooling_water'][scenario] * hf.CooledWaterCO2kg('cooling_water')
            if 'chilled_water' in SP_params[selectivity].keys():
                SP_params[selectivity]['water_direct_withdrawal'][scenario] += SP_params[selectivity]['chilled_water'][scenario]
                cooled_water_ghg += SP_params[selectivity]['chilled_water'][scenario] * hf.CooledWaterCO2kg('chilled_water')
            if 'steam_low' in SP_params[selectivity].keys():
                cooled_water_ghg += SP_params[selectivity]['steam_low'][scenario] * hf.CooledWaterCO2kg('steam_low')
            if 'steam_high' in SP_params[selectivity].keys():
                cooled_water_ghg += SP_params[selectivity]['steam_high'][scenario] * hf.CooledWaterCO2kg('steam_high')
  

            if model == 'buttonGHG':

                results_kg_co2e = hf.TotalGHGEmissions(io_data, y,
                                                       biorefinery_direct_ghg, cooled_water_ghg, SP_params['analysis_params']['time_horizon'])

                results_kg_co2e_credit = hf.TotalGHGEmissions(io_data, y_cred, 
                                                              biorefinery_direct_ghg, cooled_water_ghg,
                                                              SP_params['analysis_params']['time_horizon'])

                results_kg_co2e_dict = results_kg_co2e.set_index('products')['ghg_results_kg'].to_dict()
                hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario, fuel)
                if fuel == 'ethanol':
                    m[scenario][selectivity] = m[scenario][selectivity] * 1000/27 # converting kg per kg results to g per MJ
                    m[scenario][selectivity].loc['electricity_credit'] = (
                        results_kg_co2e_credit[results_kg_co2e_credit['products'] == 'electricity.US.kWh']['ghg_results_kg'].iloc[0] * 1000/27)
                else:
                    m[scenario]['All'][selectivity] = m[scenario]['All'][selectivity] * 1000/27 # converting kg per kg results to g per MJ


            elif model == 'buttonConsWater':
                if 'water_direct_consumption' in SP_params[selectivity]:
                    direct_water_consumption = SP_params[selectivity]['water_direct_consumption'][scenario]
                else:
                    direct_water_consumption = 0

                results_water = hf.TotalWaterImpacts(io_data, y, 
                                                   water_consumption, direct_water_consumption)

                results_water_credit = hf.TotalWaterImpacts(io_data, y_cred,
                                                              water_consumption, direct_water_consumption)

                results_water_dict = results_water.set_index('products')['liter_results_kg'].to_dict()
                hf.AggregateResults(m, results_water_dict, selectivity, scenario, fuel)
                if fuel == 'ethanol':
                    m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
                    m[scenario][selectivity].loc['electricity_credit'] = (results_water_credit[results_water_credit['products'] == 
                                                                        'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)
                else:
                    m[scenario]['All'][selectivity] = m[scenario]['All'][selectivity]/27 # converting kg per kg results to g per MJ

            elif model == 'buttonWithWater':
                if 'water_direct_withdrawal' in SP_params[selectivity]:
                    direct_water_withdrawal = SP_params[selectivity]['water_direct_withdrawal'][scenario]
                else:
                    direct_water_withdrawal = 0

                results_water = hf.TotalWaterImpacts(io_data, y, 
                                                   water_withdrawal, direct_water_withdrawal)

                results_kg_co2e_credit = hf.TotalWaterImpacts(io_data, y_cred,
                                                              water_withdrawal, direct_water_withdrawal)

                results_water_dict = results_water.set_index('products')['liter_results_kg'].to_dict()
                hf.AggregateResults(m, results_water_dict, selectivity, scenario, fuel)
                if fuel == 'ethanol':
                    m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
                    m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                                        'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)
                else:
                    m[scenario]['All'][selectivity] = m[scenario]['All'][selectivity]/27 # converting kg per kg results to g per MJ


    if fuel == 'ethanol':
        aggregated_data_avg = m['avg'][selectivities].T
        aggregated_data_low = m['low'][selectivities].T
        aggregated_data_high = m['high'][selectivities].T
        
        if 'electricity_credit' in aggregated_data_avg.columns.values:
            aggregated_data_avg_pos = aggregated_data_avg.drop(['electricity_credit'],1)
        if 'steam_low_credit' in aggregated_data_avg.columns.values:
            aggregated_data_avg_pos = aggregated_data_avg.drop(['steam_low_credit'],1)
        if 'water_direct_consumption_credit' in aggregated_data_avg.columns.values:
            aggregated_data_avg_pos = aggregated_data_avg.drop(['water_direct_consumption_credit'],1)

    else:
        aggregated_data_avg = m['avg'].T
        aggregated_data_low = m['low'].T
        aggregated_data_high = m['high'].T
        aggregated_data_avg_pos = aggregated_data_avg


    aggregated_data_avg_plot = aggregated_data_avg[list(reversed(aggregated_data_avg.columns.values))]

    error_min = (aggregated_data_low.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1).values)*(-1)
    error_max = (aggregated_data_high.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1)).values

    aggregated_data_avg_plot['error_bars_min'] = error_min
    aggregated_data_avg_plot['error_bars_max'] = error_max

    return aggregated_data_avg_plot




