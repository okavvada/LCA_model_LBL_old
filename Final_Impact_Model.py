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

m2 = {} 
for scenario in P.scenario_range:
    new_data = np.zeros([8,3])
    m2[scenario] = pd.DataFrame(new_data, columns=P.selectivity, index=P.processes)


def FinalImpactModel(SP_params, model):
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

    m = dict(m2)
    y = {}
    y_cred = {}
    for item in io_data['products']:
        y.update({item:0})
        y_cred.update({item:0})

    for selectivity in P.selectivity:
        for scenario in P.scenario_range:
            if (SP_params[selectivity]['acid'] == 'hcl'):
              y["hcl.kg"] = SP_params[selectivity]['acid.kg'][scenario] * SP_params[selectivity]['ionicLiquid_amount'][scenario]
              y["h2so4.kg"] = 0

            elif (SP_params[selectivity]['acid'] == 'h2so4'):
              y["h2so4.kg"] = SP_params[selectivity]['acid.kg'][scenario] * SP_params[selectivity]['ionicLiquid_amount'][scenario]
              y["hcl.kg"] = 0

            y["lysine.us.kg"] = SP_params[selectivity]['ionicLiquid_amount'][scenario] * SP_params[selectivity]['feedstock'][scenario] * 0.58
            y["cholinium.hydroxide.kg"] = SP_params[selectivity]['ionicLiquid_amount'][scenario] * 0.42  
            y["cellulase.kg"] = SP_params[selectivity]['cellulase_amount'][scenario] * cellulose[SP_params['analysis_params']['feedstock']] * SP_params[selectivity]['feedstock'][scenario]
            y["csl.kg"] = SP_params[selectivity]['csl.kg'][scenario]/1000 * sugars[SP_params['analysis_params']['feedstock']] * SP_params[selectivity]['feedstock'][scenario]
            y["farmedstover.kg"] = SP_params[selectivity]['feedstock'][scenario]  
            y["dap.kg"] = SP_params[selectivity]['dap.kg'][scenario]/1000 * sugars[SP_params['analysis_params']['feedstock']] * SP_params[selectivity]['feedstock'][scenario]
            y["lime.kg"] = SP_params[selectivity]['caoh.kg'][scenario]
            y["naoh.kg"] = SP_params[selectivity]['naoh.kg'][scenario]
            y["naturalgas.MJ"] = SP_params[selectivity]['ng_input_stream_MJ'][scenario] * (hf.FuelConvertMJ(1, "ethanol", "kg"))
            y["gasoline.MJ"] = (hf.FuelConvertMJ(SP_params[selectivity]['octane_ltr'][scenario]/0.789, "gasoline", "liter"))
            y["rail.mt_km"] = ((SP_params[selectivity]['ionicLiquid_amount'][scenario]/1000) * 
                                SP_params['common']['IL_rail_km'][scenario] +
                                (etoh_feed_stream_mass_kg/1000 * SP_params['common']['etoh_distribution_rail'][scenario]) +
                                (SP_params[selectivity]['feedstock'][scenario]/1000) * 
                                SP_params['common']['feedstock_distribution_rail'][scenario])
            y["flatbedtruck.mt_km"] = (((SP_params[selectivity]['ionicLiquid_amount'][scenario]/1000) * 
                                            SP_params['common']['IL_flatbedtruck_mt_km'][scenario]) +
                                            (etoh_feed_stream_mass_kg/1000 * (
                                                SP_params['common']['etoh_distribution_truck'][scenario])) +
                                            (SP_params[selectivity]['feedstock'][scenario]/1000) * 
                                                SP_params['common']['feedstock_distribution_truck'][scenario])
            y["electricity.{}.kWh".format(SP_params['analysis_params']['facility_electricity'])] = (
                                                            SP_params[selectivity]['electricity_requirements'][scenario]/0.789)

            y_cred["electricity.{}.kWh".format(SP_params['analysis_params']['facility_electricity'])] = -(
                                                            SP_params[selectivity]['electricity_credit'][scenario]/0.789)

            biorefinery_direct_ghg = hf.FuelCO2kg(SP_params[selectivity]['ng_input_stream_MJ'][scenario] * (hf.FuelConvertMJ(1, "ethanol","kg")), "naturalgas") + (
                    hf.FuelCO2kg(hf.FuelConvertMJ(
                        SP_params[selectivity]['octane_ltr'][scenario]/0.789,"gasoline", "liter"), "gasoline"))

            

            if model == 'buttonGHG':

                results_kg_co2e = hf.TotalGHGEmissions(io_data, y,
                                                       biorefinery_direct_ghg, SP_params['analysis_params']['time_horizon'])
        
                results_kg_co2e_credit = hf.TotalGHGEmissions(io_data, y_cred, 
                                                              biorefinery_direct_ghg,
                                                              SP_params['analysis_params']['time_horizon'])

                results_kg_co2e_dict = results_kg_co2e.set_index('products')['ghg_results_kg'].to_dict()
                hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario)
                m[scenario][selectivity] = m[scenario][selectivity] * 1000/27 # converting kg per kg results to g per MJ
                m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                                        'electricity.US.kWh']['ghg_results_kg'].iloc[0] * 1000/27)


            elif model == 'buttonConsWater':

                results_water = hf.TotalWaterImpacts(io_data, y, 
                                                   water_consumption, SP_params[selectivity]['biorefinery_direct_consumption'][scenario])

                results_water_credit = hf.TotalWaterImpacts(io_data, y_cred,
                                                              water_consumption, SP_params[selectivity]['biorefinery_direct_consumption'][scenario])

                results_water_dict = results_water.set_index('products')['liter_results_kg'].to_dict()
                hf.AggregateResults(m, results_water_dict, selectivity, scenario)
                m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
                m[scenario][selectivity].loc['electricity_credit'] = (results_water_credit[results_water_credit['products'] == 
                                                                        'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)

            elif model == 'buttonWithWater':

                results_water = hf.TotalWaterImpacts(io_data, y, 
                                                   water_withdrawal, SP_params[selectivity]['biorefinery_direct_withdrawal'][scenario])

                results_kg_co2e_credit = hf.TotalWaterImpacts(io_data, y_cred,
                                                              water_withdrawal, SP_params[selectivity]['biorefinery_direct_consumption'][scenario])

                results_water_dict = results_water.set_index('products')['liter_results_kg'].to_dict()
                hf.AggregateResults(m, results_water_dict, selectivity, scenario)
                m[scenario][selectivity] = m[scenario][selectivity]/27 # converting Liters per kg results to Liters per MJ
                m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                                        'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)


    aggregated_data_avg = m['avg'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
    aggregated_data_low = m['low'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
    aggregated_data_high = m['high'][['waterwash', 'iHG-Current', 'iHG-Projected']].T

    aggregated_data_avg_pos = aggregated_data_avg.drop(['electricity_credit'],1)

    aggregated_data_avg_plot = aggregated_data_avg[list(reversed(aggregated_data_avg.columns.values))]

    error_min = (aggregated_data_low.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1).values)*(-1)
    error_max = (aggregated_data_high.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1)).values

    aggregated_data_avg_plot['error_bars_min'] = error_min
    aggregated_data_avg_plot['error_bars_max'] = error_max

    return aggregated_data_avg_plot




