time_horizon = 100
io_table_dollars_path = "io_tables/io_table_dollars.csv"
cost_impact_path = "io_tables/impact_vectors/cost_impact.csv"
facility_electricity = "US"
# Ethanol produciton functional unit (1 kg of ethanol)
etoh_feed_stream_mass_kg = 1 
combustion_direct_ghg = 0
selectivity = ["iHG-Projected", "iHG-Current", "waterwash"]
# Three ranges for sensitivity:  (a) low; (b) avg; and (c) high  
scenario_range = ["low", "avg", 'high']
processes = ["Farming", "Transportation", "Petroleum", "Electricity", "Chemicals_And_Fertilizers","Direct", "Other"]
energy_content_path = "unit_conversions_and_mw/energy_content_by_mass_and_volume.csv"
fuel_aliases_path = "unit_conversions_and_mw/fuel_aliases.csv"
co2_filepath = "io_tables/impact_vectors/co2_impact.csv"
ch4_filepath = "io_tables/impact_vectors/ch4_impact.csv"
n2o_filepath = "io_tables/impact_vectors/n2o_impact.csv"
