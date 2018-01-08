import pandas as pd
import numpy as np
import parameters as P
import helper_functions as hf


io_data_GHG = pd.read_csv(P.io_table_physicalunits_path).fillna(0)
io_data_water = pd.read_csv(P.io_table_physicalunits_water_path).fillna(0)
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

	elif (model == 'buttonConsWater') or (model == 'buttonWithWater'):
		io_data = io_data_water

	m = dict(m2)
	y = {}
	y_cred = {}
	for item in io_data['products']:
	    y.update({item:0})
	    y_cred.update({item:0})

	for selectivity in P.selectivity:
	    for scenario in P.scenario_range:
			y["lysine.us.kg"] = (SP_other_params[selectivity]['chlys_amount'][scenario] * 
								SP_common_params['chlys_percent'][scenario]) 
			y["cholinium.hydroxide.kg"] = (SP_other_params[selectivity]['chlys_amount'][scenario] * 
			                               SP_common_params['cholinium_percent'][scenario])  
			y["cellulase.kg"] = SP_common_params['enzyme'][scenario]
			y["csl.kg"] = SP_other_params[selectivity]['csl.kg'][scenario]
			y["farmedstover.kg"] = SP_other_params[selectivity]['feedstock'][scenario]  
			y["dap.kg"] = SP_other_params[selectivity]['dap.kg'][scenario] 
			y["h2so4.kg"] = SP_other_params[selectivity]['h2so4.kg'][scenario]
			y["naturalgas.MJ"] = (hf.FuelConvertMJ(
			        			SP_other_params[selectivity]['ng_input_stream_mass_ww_kg'][scenario], "naturalgas","kg"))
			y["rail.mt_km"] = ((SP_other_params[selectivity]['chlys_amount'][scenario]/1000) * 
							SP_common_params['chlys_rail_mt_km'][scenario] +
			                	(etoh_feed_stream_mass_kg/1000 * SP_common_params['etoh_distribution_rail'][scenario])) 
			y["flatbedtruck.mt_km"] = ((
			        (SP_other_params[selectivity]['chlys_amount'][scenario]/1000) * 
			        	SP_common_params['chlys_flatbedtruck_mt_km'][scenario]) +
			        		(etoh_feed_stream_mass_kg/1000 * (
			        			SP_common_params['etoh_distribution_truck'][scenario])))
			y["electricity.{}.kWh".format(SP_analysis_params['facility_electricity'])] = (
			    (SP_other_params[selectivity]['electricity_requirements'][scenario]))
			y["hcl.kg"] = SP_other_params[selectivity]['hcl.kg'][scenario]

			y_cred["electricity.{}.kWh".format(SP_analysis_params['facility_electricity'])] = -(
							            (SP_other_params[selectivity]['electricity_credit'][scenario]))

			biorefinery_direct_ghg = hf.FuelCO2kg(hf.FuelConvertMJ(
			        SP_other_params[selectivity]['ng_input_stream_mass_ww_kg'][scenario],"naturalgas","kg"), "naturalgas")

			if model == 'buttonGHG':

				results_kg_co2e = hf.TotalGHGEmissions(io_data, y,
				                                       biorefinery_direct_ghg, SP_analysis_params['combustion_direct_ghg'], SP_analysis_params['time_horizon'])
        
				results_kg_co2e_credit = hf.TotalGHGEmissions(io_data, y_cred, 
		                                                      biorefinery_direct_ghg, SP_analysis_params['combustion_direct_ghg'],
		                                                      SP_analysis_params['time_horizon'])

				results_kg_co2e_dict = results_kg_co2e.set_index('products')['ghg_results_kg'].to_dict()
				hf.AggregateResults(m, results_kg_co2e_dict, selectivity, scenario)
				m[scenario][selectivity] = m[scenario][selectivity] * 1000/27 # converting kg per kg results to g per MJ
				m[scenario][selectivity].loc['electricity_credit'] = (results_kg_co2e_credit[results_kg_co2e_credit['products'] == 
                                                						'electricity.US.kWh']['ghg_results_kg'].iloc[0] * 1000/27)


			elif model == 'buttonConsWater':

				results_water = hf.TotalWaterImpacts(io_data, y, 
			                                       water_consumption, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

				results_water_credit = hf.TotalWaterImpacts(io_data, y_cred,
		                                                      water_consumption, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

				results_water_dict = results_water.set_index('products')['liter_results_kg'].to_dict()
				hf.AggregateResults(m, results_water_dict, selectivity, scenario)
				m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
				m[scenario][selectivity].loc['electricity_credit'] = (results_water_credit[results_water_credit['products'] == 
                                                						'electricity.US.kWh']['liter_results_kg'].iloc[0]/27)

			elif model == 'buttonWithWater':

				results_water = hf.TotalWaterImpacts(io_data, y, 
			                                       water_withdrawal, SP_other_params[selectivity]['biorefinery_direct_withdrawal'][scenario])

				results_kg_co2e_credit = hf.TotalWaterImpacts(io_data, y_cred,
		                                                      water_withdrawal, SP_other_params[selectivity]['biorefinery_direct_consumption'][scenario])

				results_water_dict = results_water.set_index('products')['liter_results_kg'].to_dict()
				hf.AggregateResults(m, results_water_dict, selectivity, scenario)
				m[scenario][selectivity] = m[scenario][selectivity]/27 # converting kg per kg results to g per MJ
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




