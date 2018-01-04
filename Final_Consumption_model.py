import pandas as pd
import numpy as np
import parameters as P
import helper_functions as hf
import matplotlib.pyplot as plt

io_data = pd.read_csv(P.io_table_dollars_water_path)
cost = hf.csv_dict_list(P.cost_impact_water_path)
water_consumption = hf.csv_dict_list(P.water_consumption_path) 
water_withdrawal = hf.csv_dict_list(P.water_withdrawal_path) 
# Ethanol produciton functional unit (1 kg of ethanol)
etoh_feed_stream_mass_kg = 1 

y = {}
for item in cost.keys():
    y.update({item:0})

m2 = {} 
for scenario in P.scenario_range:
    new_data = np.zeros([7,3])
    m2[scenario] = pd.DataFrame(new_data, columns=P.selectivity, index=P.processes)

def FinalConsumptionModel(SP_common_params, SP_other_params, SP_analysis_params, model):
	m = dict(m2)
	for selectivity in P.selectivity:
	    for scenario in P.scenario_range:
			y["lysine.us.kg"] = cost["lysine.us.kg"] * (SP_other_params[selectivity]['chlys_amount'][scenario] * 
								SP_common_params['chlys_percent'][scenario]) 
			# 58% lysine + 42% ChOH for Chylys production (Stoichiometry) 
			y["cholinium.hydroxide.kg"] = (cost["cholinium.hydroxide.kg"] * 
			                               SP_other_params[selectivity]['chlys_amount'][scenario] * 
			                               SP_common_params['cholinium_percent'][scenario])  
			# 58% lysine + 42% ChOH for Chylys production (Stoichiometry) 
			y["cellulase.kg"] = cost["cellulase.kg"] * SP_common_params['enzyme'][scenario]
			y["csl.kg"] = cost["csl.kg"] * SP_other_params[selectivity]['csl.kg'][scenario]
			y["farmedstover.kg"] = cost["farmedstover.kg"] * SP_other_params[selectivity]['feedstock'][scenario]  
			y["dap.kg"] = cost["dap.kg"] * SP_other_params[selectivity]['dap.kg'][scenario] 
			y["h2so4.kg"] = cost["h2so4.kg"] * SP_other_params[selectivity]['h2so4.kg'][scenario]
			y["naturalgas.MJ"] = cost["naturalgas.MJ"] * (hf.FuelConvertMJ(
			        			SP_other_params[selectivity]['ng_input_stream_mass_ww_kg'][scenario], "naturalgas","kg"))
			y["rail.mt_km"] = (cost["rail.mt_km"] * (SP_other_params[selectivity]['chlys_amount'][scenario]/1000) * 
							SP_common_params['chlys_rail_mt_km'][scenario] +
			                	cost["rail.mt_km"] * (
			                    	etoh_feed_stream_mass_kg/1000 * SP_common_params['etoh_distribution_rail'][scenario])) 
			y["flatbedtruck.mt_km"] = (cost["flatbedtruck.mt_km"] * (
			        (SP_other_params[selectivity]['chlys_amount'][scenario]/1000) * 
			        	SP_common_params['chlys_flatbedtruck_mt_km'][scenario]) +
			        		cost["flatbedtruck.mt_km"] * (etoh_feed_stream_mass_kg/1000 * (
			        			SP_common_params['etoh_distribution_truck'][scenario])))
			y["electricity.{}.kWh".format(SP_analysis_params['facility_electricity'])] = (
			    cost["electricity.{}.kWh".format(SP_analysis_params['facility_electricity'])] * (
			        SP_other_params[selectivity]['electricity_requirements'][scenario]))
			y["hcl.kg"] = cost["hcl.kg"] * SP_other_params[selectivity]['hcl.kg'][scenario]

			biorefinery_direct_ghg = hf.FuelCO2kg(hf.FuelConvertMJ(
			        SP_other_params[selectivity]['ng_input_stream_mass_ww_kg'][scenario],"naturalgas","kg"), "naturalgas")


			results_kg_co2e = hf.TotalWaterConsumption(io_data, y, cost, 
			                                       water_consumption, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

			results_kg_co2e_dict = results_kg_co2e.set_index('products')['liter_results_kg'].to_dict()

			hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario)

			m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ


	aggregated_data_avg = m['avg'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
	aggregated_data_low = m['low'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
	aggregated_data_high = m['high'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
	aggregated_data_avg['electricity_credit'] = [0, -0.006, -0.08]
	aggregated_data_low['electricity_credit'] = [0, -0.009, -0.09]
	aggregated_data_high['electricity_credit'] = [0, -0.005, -0.06]
	aggregated_data_avg_pos = aggregated_data_avg.drop(['electricity_credit'],1)
	aggregated_data_low_pos = aggregated_data_low.drop(['electricity_credit'],1)
	aggregated_data_high_pos = aggregated_data_high.drop(['electricity_credit'],1)

	aggregated_data_avg_plot = aggregated_data_avg[list(reversed(aggregated_data_avg.columns.values))]

	error_min = (aggregated_data_low.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1)).values*(-1)
	error_max = (aggregated_data_high.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1)).values
	plt_errors = [error_min, error_max]

	aggregated_data_avg_plot['error_bars_min'] = error_min
	aggregated_data_avg_plot['error_bars_max'] = error_max

	return aggregated_data_avg_plot




