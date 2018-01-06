import pandas as pd
import numpy as np
import parameters as P
import helper_functions as hf


io_data_GHG = pd.read_csv(P.io_table_dollars_path)
cost_GHG = hf.csv_dict_list(P.cost_impact_path)
io_data_water = pd.read_csv(P.io_table_dollars_water_path)
cost_water = hf.csv_dict_list(P.cost_impact_water_path)
water_consumption = hf.csv_dict_list(P.water_consumption_path) 
water_withdrawal = hf.csv_dict_list(P.water_withdrawal_path) 
# Ethanol produciton functional unit (1 kg of ethanol)
etoh_feed_stream_mass_kg = 1 

m2 = {} 
for scenario in P.scenario_range:
    new_data = np.zeros([8,3])
    m2[scenario] = pd.DataFrame(new_data, columns=P.selectivity, index=P.processes)

def FinalImpactModel(SP_common_params, SP_other_params, SP_analysis_params, model):
	if model == 'buttonGHG':
		io_data = io_data_GHG
		cost = cost_GHG

	elif (model == 'buttonConsWater') or (model == 'buttonWithWater'):
		io_data = io_data_water
		cost = cost_water

	m = dict(m2)
	y = {}
	y_cred = {}
	for item in cost.keys():
	    y.update({item:0})
	    y_cred.update({item:0})

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

			y_cred["electricity.{}.kWh".format(SP_analysis_params['facility_electricity'])] = -(
							            cost["electricity.{}.kWh".format(SP_analysis_params['facility_electricity'])] * (
											SP_other_params[selectivity]['electricity_credit'][scenario]))

			biorefinery_direct_ghg = hf.FuelCO2kg(hf.FuelConvertMJ(
			        SP_other_params[selectivity]['ng_input_stream_mass_ww_kg'][scenario],"naturalgas","kg"), "naturalgas")

			if model == 'buttonGHG':

				results_kg_co2e = hf.TotalGHGEmissions(io_data, y, cost, 
				                                       biorefinery_direct_ghg, SP_analysis_params['combustion_direct_ghg'], SP_analysis_params['time_horizon'])
        
				results_kg_co2e_credit = hf.TotalGHGEmissions(io_data, y_cred, cost, 
		                                                      biorefinery_direct_ghg, SP_analysis_params['combustion_direct_ghg'],
		                                                      SP_analysis_params['time_horizon'])

				results_kg_co2e_dict = results_kg_co2e.set_index('products')['ghg_results_kg'].to_dict()
				hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario)
				m[scenario][selectivity] = m[scenario][selectivity] * 1000/27 # converting kg per kg results to g per MJ
				m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                						'electricity.US.kWh']['ghg_results_kg'].iloc[0] * 1000/27)


			elif model == 'buttonConsWater':

				results_kg_co2e = hf.TotalWaterImpacts(io_data, y, cost, 
			                                       water_consumption, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

				results_kg_co2e_credit = hf.TotalWaterImpacts(io_data, y_cred, cost, 
		                                                      water_consumption, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

				results_kg_co2e_dict = results_kg_co2e.set_index('products')['liter_results_kg'].to_dict()
				hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario)
				m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
				m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                						'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)

			elif model == 'buttonWithWater':

				results_kg_co2e = hf.TotalWaterImpacts(io_data, y, cost, 
			                                       water_withdrawal, SP_other_params[selectivity]['biorefinery_direct_withdrawal'][scenario])

				results_kg_co2e_credit = hf.TotalWaterImpacts(io_data, y_cred, cost, 
		                                                      water_consumption, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

				results_kg_co2e_dict = results_kg_co2e.set_index('products')['liter_results_kg'].to_dict()
				hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario)
				m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
				m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                						'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)


	aggregated_data_avg = m['avg'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
	aggregated_data_low = m['low'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
	aggregated_data_high = m['high'][['waterwash', 'iHG-Current', 'iHG-Projected']].T
	aggregated_data_avg_pos = aggregated_data_avg.drop(['electricity_credit'],1)
	# aggregated_data_low_pos = aggregated_data_low.drop(['electricity_credit'],1)
	# aggregated_data_high_pos = aggregated_data_high.drop(['electricity_credit'],1)

	aggregated_data_avg_plot = aggregated_data_avg[list(reversed(aggregated_data_avg.columns.values))]

	error_min = (aggregated_data_avg_pos.sum(axis=1).values - aggregated_data_low.sum(axis=1))
	error_max = (aggregated_data_high.sum(axis=1) - aggregated_data_avg_pos.sum(axis=1)).values
	plt_errors = [error_min, error_max]

	aggregated_data_avg_plot['error_bars_min'] = error_min
	aggregated_data_avg_plot['error_bars_max'] = error_max

	return aggregated_data_avg_plot




