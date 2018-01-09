var analysis_params = {
    'time_horizon': 100,
    'facility_electricity': 'US',
    'combustion_direct_ghg': 0
    }

var common_params = {
    'etoh_distribution_truck': {
        'low': 45,
        'avg': 50,
        'high': 55
    },
    'etoh_distribution_rail': {
        'low': 120,
        'avg': 135,
        'high': 150
    },
    'enzyme': {
        'low': 0.027,
        'avg': 0.03,
        'high': 0.033
    },
    'chlys_percent': {
        'low': 0.58,
        'avg': 0.58,
        'high': 0.58
    },
    'cholinium_percent': {
        'low': 0.42,
        'avg': 0.42,
        'high': 0.42
    },
    'chlys_rail_mt_km': {
        'low': 160,
        'avg': 160,
        'high': 160
    },
    'chlys_flatbedtruck_mt_km': {
        'low': 80,
        'avg': 80,
        'high': 80
    }
};

var other_params = {
    "iHG-Projected": {
        'chlys_amount': {
            'low': 0.027,
            'avg': 0.03,
            'high': 0.033
        },
        'electricity_requirements': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'feedstock': {
            'low': 4.23,
            'avg': 4.7,
            'high': 5.17
        },
        'electricity_credit': {
            'low': 1.4,
            'avg': 0.85,
            'high': 0.1
        },
        'csl.kg': {
            'low': 0.06,
            'avg': 0.06,
            'high': 0.06
        },
        'dap.kg': {
            'low': 0.017,
            'avg': 0.017,
            'high': 0.017
        },
        'h2so4.kg': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'hcl.kg': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'ng_input_stream_mass_ww_kg': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'biorefinery_direct_withdrawal': {
            'low': 5.31,
            'avg': 5.9,
            'high': 6.49
        },
        'biorefinery_direct_consumption': {
            'low': 5.76,
            'avg': 6.4,
            'high': 7.04
        }
    },
    "iHG-Current": {
        'chlys_amount': {
            'low': 0.14,
            'avg': 0.16,
            'high': 0.18
        },
        'electricity_requirements': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'feedstock': {
            'low': 4.23,
            'avg': 4.7,
            'high': 5.17
        },
        'hcl.kg': {
            'low': 0.18,
            'avg': 0.18,
            'high': 0.18
        },
        'electricity_credit': {
            'low': 0.5,
            'avg': 0.1,
            'high': 0.01
        },
        'csl.kg': {
            'low': 0.05,
            'avg': 0.05,
            'high': 0.05
        },
        'dap.kg': {
            'low': 0.01,
            'avg': 0.01,
            'high': 0.01
        },
        'h2so4.kg': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'ng_input_stream_mass_ww_kg': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'biorefinery_direct_withdrawal': {
            'low': 5.76,
            'avg': 6.4,
            'high': 7.04
        },
        'biorefinery_direct_consumption': {
            'low': 5.76,
            'avg': 6.4,
            'high': 7.04
        }
    },
    "waterwash": {
        'chlys_amount': {
            'low': 0.15,
            'avg': 0.17,
            'high': 0.18
        },
        'electricity_requirements': {
            'low': 1.26,
            'avg': 1.4,
            'high': 1.54
        },
        'feedstock': {
            'low': 4.9,
            'avg': 5.47,
            'high': 6.01
        },
        'ng_input_stream_mass_ww_kg': {
            'low': 1.1,
            'avg': 1.31,
            'high': 1.4
        },
        'electricity_credit': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'csl.kg': {
            'low': 0.06,
            'avg': 0.06,
            'high': 0.06
        },
        'dap.kg': {
            'low': 0.01,
            'avg': 0.01,
            'high': 0.01
        },
        'hcl.kg': {
            'low': 0,
            'avg': 0,
            'high': 0
        },
        'h2so4.kg': {
            'low': 0.002,
            'avg': 0.002,
            'high': 0.002
        },
        'biorefinery_direct_withdrawal': {
            'low': 0.9,
            'avg': 1.3,
            'high': 1.7
        },
        'biorefinery_direct_consumption': {
            'low': 0.9,
            'avg': 1.3,
            'high': 1.7
        }
    }
};

var processes = ["electricity_credit", "Electricity", "Chemicals_And_Fertilizers", "Petroleum", "Transportation", "Farming", "Direct", "Other"];

$.getJSON( "static/data.js", function(input_json) {
  console.log(input_json);
 });

document.getElementById("common_combustion_direct_ghg").value = analysis_params.combustion_direct_ghg;
document.getElementById("common_enzyme").value = common_params.enzyme['avg'];
document.getElementById("common_chlys_percent").value = common_params.chlys_percent['avg'];
document.getElementById("common_cholinium_percent").value = common_params.cholinium_percent['avg'];
document.getElementById("common_etoh_distribution_truck").value = common_params.etoh_distribution_truck['avg'];
document.getElementById("common_etoh_distribution_rail").value = common_params.etoh_distribution_rail['avg'];
document.getElementById("common_chlys_rail_mt_km").value = common_params.chlys_rail_mt_km['avg'];
document.getElementById("common_chlys_flatbedtruck_mt_km").value = common_params.chlys_flatbedtruck_mt_km['avg'];

document.getElementById("waterwash_chlys_amount").value = other_params['waterwash']['chlys_amount']['avg'];
document.getElementById("waterwash_feedstock").value = other_params['waterwash']['feedstock']['avg'];
document.getElementById("waterwash_csl.kg").value = other_params['waterwash']['csl.kg']['avg'];
document.getElementById("waterwash_dap.kg").value = other_params['waterwash']['dap.kg']['avg'];
document.getElementById("waterwash_hcl.kg").value = other_params['waterwash']['hcl.kg']['avg'];
document.getElementById("waterwash_h2so4.kg").value = other_params['waterwash']['h2so4.kg']['avg'];
document.getElementById("waterwash_ng_input_stream_mass_ww_kg").value = other_params['waterwash']['ng_input_stream_mass_ww_kg']['avg'];
document.getElementById("waterwash_electricity_requirements").value = other_params['waterwash']['electricity_requirements']['avg'];
document.getElementById("waterwash_electricity_credit").value = other_params['waterwash']['electricity_credit']['avg'];

document.getElementById("iHG-Current_chlys_amount").value = other_params['iHG-Current']['chlys_amount']['avg'];
document.getElementById("iHG-Current_feedstock").value = other_params['iHG-Current']['feedstock']['avg'];
document.getElementById("iHG-Current_csl.kg").value = other_params['iHG-Current']['csl.kg']['avg'];
document.getElementById("iHG-Current_dap.kg").value = other_params['iHG-Current']['dap.kg']['avg'];
document.getElementById("iHG-Current_hcl.kg").value = other_params['iHG-Current']['hcl.kg']['avg'];
document.getElementById("iHG-Current_h2so4.kg").value = other_params['iHG-Current']['h2so4.kg']['avg'];
document.getElementById("iHG-Current_ng_input_stream_mass_ww_kg").value = other_params['iHG-Current']['ng_input_stream_mass_ww_kg']['avg'];
document.getElementById("iHG-Current_electricity_requirements").value = other_params['iHG-Current']['electricity_requirements']['avg'];
document.getElementById("iHG-Current_electricity_credit").value = other_params['iHG-Current']['electricity_credit']['avg'];

document.getElementById("iHG-Projected_chlys_amount").value = other_params['iHG-Projected']['chlys_amount']['avg'];
document.getElementById("iHG-Projected_feedstock").value = other_params['iHG-Projected']['feedstock']['avg'];
document.getElementById("iHG-Projected_csl.kg").value = other_params['iHG-Projected']['csl.kg']['avg'];
document.getElementById("iHG-Projected_dap.kg").value = other_params['iHG-Projected']['dap.kg']['avg'];
document.getElementById("iHG-Projected_hcl.kg").value = other_params['iHG-Projected']['hcl.kg']['avg'];
document.getElementById("iHG-Projected_h2so4.kg").value = other_params['iHG-Projected']['h2so4.kg']['avg'];
document.getElementById("iHG-Projected_ng_input_stream_mass_ww_kg").value = other_params['iHG-Projected']['ng_input_stream_mass_ww_kg']['avg'];
document.getElementById("iHG-Projected_electricity_requirements").value = other_params['iHG-Projected']['electricity_requirements']['avg'];
document.getElementById("iHG-Projected_electricity_credit").value = other_params['iHG-Projected']['electricity_credit']['avg'];


var input_dict = {};
input_dict.other_params = other_params;
input_dict.common_params = common_params;
input_dict.analysis_params = analysis_params;


function electricitySelect() {
  var myList=document.getElementById("myList");
  input_dict.analysis_params.facility_electricity = myList.options[myList.selectedIndex].value;
}

function lifetimeSelect() {
  var myList=document.getElementById("myVals");
  input_dict.analysis_params.time_horizon = myList.options[myList.selectedIndex].value;
}     

$("input").change(function(event) {
    to_replace = event.target.name + '_';
    if (event.target.placeholder == "value") {
      key = event.target.id.replace(to_replace, '');
      if (key in common_params) {
        common_params[key]['avg'] = parseFloat(document.getElementById(event.target.id).value);
        error_id = 'common_error_' + key
        common_params[key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * common_params[key]['avg'];
        common_params[key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * common_params[key]['avg'];
      }
      else if (key in analysis_params){
        analysis_params[key] = parseFloat(document.getElementById(event.target.id).value);
      }
      else {
        other_params[event.target.name][key]['avg'] = parseFloat(document.getElementById(event.target.id).value);
        error_id = event.target.name + '_error_' + key
        other_params[event.target.name][key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * other_params[event.target.name][key]['avg'];
        other_params[event.target.name][key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * other_params[event.target.name][key]['avg'];
      }}
    else if (event.target.placeholder == "error") {
      to_replace = event.target.name + '_error_';
      key = event.target.id.replace(to_replace, '');
      if (key in common_params) {
        error_id = 'common_error_' + key
        target_id = error_id.replace('_error', '')
        common_params[key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * common_params[key]['avg'];
        common_params[key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * common_params[key]['avg'];
      }
      else {
        error_id = event.target.name + '_error_' + key
        target_id = error_id.replace('_error', '')
        other_params[event.target.name][key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * other_params[event.target.name][key]['avg'];
        other_params[event.target.name][key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * other_params[event.target.name][key]['avg'];
      }}

    input_dict.other_params = other_params;
    input_dict.common_params = common_params;
    input_dict.analysis_params = analysis_params;
  });

var run_GHG_button = document.getElementById('buttonGHG');
run_GHG_button.addEventListener('mouseover', function() {
    run_GHG_button.style['background-color'] = '#ccc';
});
run_GHG_button.addEventListener('mouseout', function() {
    run_GHG_button.style['background-color'] = '#eee';
});
var run_water_button = document.getElementById('buttonWithWater');
run_water_button.addEventListener('mouseover', function() {
    run_water_button.style['background-color'] = '#ccc';
});
run_water_button.addEventListener('mouseout', function() {
    run_water_button.style['background-color'] = '#eee';
});

var run_cons_water_button = document.getElementById('buttonConsWater');
run_cons_water_button.addEventListener('mouseover', function() {
    run_cons_water_button.style['background-color'] = '#ccc';
});
run_cons_water_button.addEventListener('mouseout', function() {
    run_cons_water_button.style['background-color'] = '#eee';
});


var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}


$("var").click(function(event) {

    var plot_data = [];
    input_dict.model = event.target.id
    $.ajax({
      url: "/ParametersList",
      type: 'POST',
      data: JSON.stringify(input_dict),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      success: function(data) {
        for (i=0; i<processes.length; i++){
          if (processes[i] != 'Other') {
          var trace = {
            x: ['waterwash', 'iHG-Current', 'iHG-Projected'],
            y: [data[processes[i]]['waterwash'],
                data[processes[i]]['iHG-Current'],
                data[processes[i]]['iHG-Projected']],
            name: processes[i],
            type: 'bar',
            width: 0.7
          }}
          else {
            var trace = {
            x: ['waterwash', 'iHG-Current', 'iHG-Projected'],
            y: [data[processes[i]]['waterwash'],
                data[processes[i]]['iHG-Current'],
                data[processes[i]]['iHG-Projected']],
            name: processes[i],
            type: 'bar',
            width: 0.7,
            error_y: {
              type: 'data',
              symmetric: false,
              array: [data.error_bars_max['waterwash'], 
                      data.error_bars_max['iHG-Current'], 
                      data.error_bars_max['iHG-Projected']],
              arrayminus: [data.error_bars_min['waterwash'], 
                           data.error_bars_min['iHG-Current'], 
                           data.error_bars_min['iHG-Projected']]
            }
          }}

          plot_data.push(trace);
        }
            total_ww = 0
            total_ihc = 0
            total_ihp = 0
        for (i=0; i<processes.length; i++){
            total_ww += data[processes[i]]['waterwash']
            total_ihc += data[processes[i]]['iHG-Current']
            total_ihp += data[processes[i]]['iHG-Projected']}

        var trace_marker = {
            x: ['waterwash', 'iHG-Current', 'iHG-Projected'],
            y: [total_ww,
                total_ihc,
                total_ihp],
            mode: 'markers',
            showlegend: false,
            marker: {
                color: '#rgba(59, 57, 53, 0.1)',
                size: 7,
                line: {
                    width: 2,
                }
          }}

        plot_data.push(trace_marker);
        if (input_dict.model == 'buttonGHG'){
            y_axis_label = 'kg CO<sub>2</sub>(eq) per MJ';
        }

        else if (input_dict.model == 'buttonConsWater'){
            y_axis_label = 'Water Consumption [Liters per MJ]';
        }

        else if (input_dict.model == 'buttonWithWater'){
            y_axis_label = 'Water Withdrawal [Liters per MJ]';
        }


        var layout = {barmode: 'relative', height: 400, width: 700, margin: {l: 50,
                                                                             r: 50,
                                                                             b: 50,
                                                                             t: 20},
                      yaxis: {title: y_axis_label,
                              titlefont: {
                                family: 'Arial, sans-serif',
                                size: 16,
                                color: 'black'
                              }},
                      xaxis: {title: 'Pretreatment methods',
                              titlefont: {
                                family: 'Arial, sans-serif',
                                size: 16,
                                color: 'black'
                              }},
                      legend: {traceorder: 'reversed'}
                              
            };

          Plotly.newPlot('chart', plot_data, layout);

          }});
    });
