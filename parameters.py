io_table_physicalunits_path = "io_tables/io_table_physicalunits.csv"
io_table_physicalunits_water_path = "io_tables/io_table_physicalunits_water.csv"
selectivity = ["iHG-Projected", "iHG-Current", "waterwash"]
# Three ranges for sensitivity:  (a) low; (b) avg; and (c) high  
scenario_range = ["low", "avg", 'high']
processes = ["electricity_credit", "Farming", "Transportation", "Petroleum", "Electricity", "Chemicals_And_Fertilizers", "Direct", "Other"]
energy_content_path = "unit_conversions_and_mw/energy_content_by_mass_and_volume.csv"
fuel_aliases_path = "unit_conversions_and_mw/fuel_aliases.csv"
co2_filepath = "io_tables/impact_vectors/co2_impact.csv"
ch4_filepath = "io_tables/impact_vectors/ch4_impact.csv"
n2o_filepath = "io_tables/impact_vectors/n2o_impact.csv"
co2_water_filepath = "io_tables/impact_vectors_water/co2_impact.csv"
ch4_water_filepath = "io_tables/impact_vectors_water/ch4_impact.csv"
n2o_water_filepath = "io_tables/impact_vectors_water/n2o_impact.csv"
water_consumption_path = "io_tables/impact_vectors_water/water_consumption.csv"
water_withdrawal_path = "io_tables/impact_vectors_water/water_withdrawal.csv"
