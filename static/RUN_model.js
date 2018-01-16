var analysis_params = {
    'time_horizon': 100,
    'facility_electricity': 'US',
    'ionic_liquid': 'chlys',
    'feedstock': 'corn_stover'
    }

var processes = ["electricity_credit", "Electricity", "Chemicals_And_Fertilizers", "Petroleum", "Transportation", "Farming", "Direct", "Other"];
var selectivity = ["iHG-Projected", "iHG-Current", "waterwash"];


//     function ReadFile(event) {
//         var reader = new FileReader();
//         reader.onload = onReaderLoad;
//         reader.readAsText(event.target.files[0]);
//     }

//     function onReaderLoad(event){
//         console.log(event.target.result);
//         var obj = JSON.parse(event.target.result);
//         console.log(obj);
//     }


// $(".buttonSuperPro").click(function(event) {
//     target_id_super = event.target.id.replace("SuperPro_", '')
//     file = ReadFile(event)
//     console.log(file)

    // $.getJSON( "static/test.js", function(super_params) {
    //     for (item in input_dict.params[target_id_super]) {
    //         if (input_dict.params[pre_process][item]['avg'] == input_dict.params[pre_process][item]['low']){
    //             error_value = 0;
    //         }
    //         else {
    //             error_value = Math.round(((input_dict.params[pre_process][item]['avg'] - input_dict.params[pre_process][item]['low'])/input_dict.params[pre_process][item]['avg'])*10)/10
    //         }
    //         if (item in super_params){
    //             input_dict.params[target_id_super][item]['avg'] = super_params[item]
    //             input_dict.params[target_id_super][item]['low'] = super_params[item] * (1 - error_value)
    //             input_dict.params[target_id_super][item]['high'] = super_params[item] * (1 + error_value)
    //         }
    //         else {
    //             input_dict.params[target_id_super][item]['avg'] = 0
    //             input_dict.params[target_id_super][item]['low'] = 0
    //             input_dict.params[target_id_super][item]['high'] = 0
    //         }
    //     }
    // for (item in input_dict.params[target_id_super]){
    //     input_val_id = target_id_super + "_" + item;
    //     input_val = document.getElementById(input_val_id);
    //     input_val.value = input_dict.params[target_id_super][item]['avg']
    // }
//    });
// });

// Set parameter values
var input_dict = {};

$.getJSON( "static/parameter_names.js", function(params_alias) {
    $.getJSON( "static/defaultParams.js", function(default_params) {
        for (pre_process in default_params) {
            parent_id = pre_process + "_params"
            for (item in default_params[pre_process]) {
                if (item == 'acid'){
                    continue
                }
                else {
                    var span_class = document.createElement("span");
                    span_class.className = "tooltip-wrap";
                    if (default_params[pre_process][item]['avg'] == default_params[pre_process][item]['low']){
                        error_value = 0;
                    }
                    else {
                        error_value = Math.round(((default_params[pre_process][item]['avg'] - default_params[pre_process][item]['low'])/default_params[pre_process][item]['avg'])*10)/10
                    }
                    html_text = (params_alias[item] + " = " + 
                                "</span><input placeholder='value' name=" + pre_process + 
                                " type='text' id=" + pre_process + "_" + item + " value=" + default_params[pre_process][item]['avg'] + ">"+
                                "<span>+/-</span><input placeholder='error' name=" + pre_process + 
                                " type='text' id=" + pre_process + "_error_" + item +" value=" + error_value +" ><br/>")
                    span_class.insertAdjacentHTML("afterbegin", html_text)
                    parent = document.getElementById(parent_id);
                    parent.appendChild(span_class)
            }}
        };

    input_dict.params = default_params;
    input_dict.params.analysis_params = analysis_params;
    });
});


$(".buttonSuperPro").click(function(event) {
    target_id_super = event.target.id.replace("SuperPro_", '')
    $.getJSON( "static/test.js", function(super_params) {
        for (item in input_dict.params[target_id_super]) {
            if (input_dict.params[pre_process][item]['avg'] == input_dict.params[pre_process][item]['low']){
                error_value = 0;
            }
            else {
                error_value = Math.round(((input_dict.params[pre_process][item]['avg'] - input_dict.params[pre_process][item]['low'])/input_dict.params[pre_process][item]['avg'])*10)/10
            }
            if (item in super_params){
                input_dict.params[target_id_super][item]['avg'] = super_params[item]
                input_dict.params[target_id_super][item]['low'] = super_params[item] * (1 - error_value)
                input_dict.params[target_id_super][item]['high'] = super_params[item] * (1 + error_value)
            }
            else {
                input_dict.params[target_id_super][item]['avg'] = 0
                input_dict.params[target_id_super][item]['low'] = 0
                input_dict.params[target_id_super][item]['high'] = 0
            }
        }
    for (item in input_dict.params[target_id_super]){
        input_val_id = target_id_super + "_" + item;
        input_val = document.getElementById(input_val_id);
        input_val.value = input_dict.params[target_id_super][item]['avg']
    }
    });
});


function electricitySelect() {
  var myList=document.getElementById("myList");
  input_dict.params.analysis_params.facility_electricity = myList.options[myList.selectedIndex].value;
}

function lifetimeSelect() {
  var myList=document.getElementById("myVals");
  input_dict.params.analysis_params.time_horizon = myList.options[myList.selectedIndex].value;
}  

function feedstockSelect() {
  var myList=document.getElementById("myFeedstock");
  input_dict.params.analysis_params.feedstock = myList.options[myList.selectedIndex].value;
}   

function ionicLiquidSelect() {
  var myList=document.getElementById("myILs");
  input_dict.params.analysis_params.ionic_liquid = myList.options[myList.selectedIndex].value;
  $.getJSON( "static/water_direct_IL.js", function(water_IL) {
    for (var i = 0; i < selectivity.length; i++) {
        input_dict.params[selectivity[i]]['biorefinery_direct_consumption']['avg'] = water_IL[input_dict.params.analysis_params['ionic_liquid']][selectivity[i]];
        input_dict.params[selectivity[i]]['biorefinery_direct_withdrawal']['avg'] = water_IL[input_dict.params.analysis_params['ionic_liquid']][selectivity[i]];
        document.getElementById(selectivity[i] + '_biorefinery_direct_consumption').value = input_dict.params[selectivity[i]]['biorefinery_direct_consumption']['avg'];
        document.getElementById(selectivity[i] + '_biorefinery_direct_withdrawal').value = input_dict.params[selectivity[i]]['biorefinery_direct_withdrawal']['avg'];
        error_id_cons = selectivity[i] + '_error_biorefinery_direct_consumption'
        error_id_with = selectivity[i] + '_error_biorefinery_direct_withdrawal'
        input_dict.params[selectivity[i]]['biorefinery_direct_consumption']['low'] = (1 - parseFloat(document.getElementById(error_id_cons).value)) * input_dict.params[selectivity[i]]['biorefinery_direct_consumption']['avg'];
        input_dict.params[selectivity[i]]['biorefinery_direct_consumption']['high'] = (1 + parseFloat(document.getElementById(error_id_cons).value)) * input_dict.params[selectivity[i]]['biorefinery_direct_consumption']['avg'];
        input_dict.params[selectivity[i]]['biorefinery_direct_withdrawal']['low'] = (1 - parseFloat(document.getElementById(error_id_with).value)) * input_dict.params[selectivity[i]]['biorefinery_direct_withdrawal']['avg'];
        input_dict.params[selectivity[i]]['biorefinery_direct_withdrawal']['high'] = (1 + parseFloat(document.getElementById(error_id_with).value)) * input_dict.params[selectivity[i]]['biorefinery_direct_withdrawal']['avg'];
        }
    })
}   

function acidSelect(id) {
  var myList=document.getElementById(id);
  process_key = id.replace('_acid', '')
  input_dict.params[process_key]['acid'] = myList.options[myList.selectedIndex].value;
}   

$("body").on("change", "input", function(){
    to_replace = event.target.name + '_';
    if (event.target.placeholder == "value") {
      key = event.target.id.replace(to_replace, '');
      if (key in input_dict.params.common) {
        input_dict.params.common[key]['avg'] = parseFloat(document.getElementById(event.target.id).value);
        error_id = 'common_error_' + key
        input_dict.params.common[key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * input_dict.params.common[key]['avg'];
        input_dict.params.common[key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * input_dict.params.common[key]['avg'];
      }
      else if (key in input_dict.params.analysis_params){
        input_dict.params.analysis_params[key] = parseFloat(document.getElementById(event.target.id).value);
      }
      else {
        input_dict.params[event.target.name][key]['avg'] = parseFloat(document.getElementById(event.target.id).value);
        error_id = event.target.name + '_error_' + key
        input_dict.params[event.target.name][key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * input_dict.params[event.target.name][key]['avg'];
        input_dict.params[event.target.name][key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * input_dict.params[event.target.name][key]['avg'];
      }}
    else if (event.target.placeholder == "error") {
      to_replace = event.target.name + '_error_';
      key = event.target.id.replace(to_replace, '');
      if (key in input_dict.params.common) {
        error_id = 'common_error_' + key
        target_id = error_id.replace('_error', '')
        input_dict.params.common[key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * input_dict.params.common[key]['avg'];
        input_dict.params.common[key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * input_dict.params.common[key]['avg'];
      }
      else {
        error_id = event.target.name + '_error_' + key
        target_id = error_id.replace('_error', '')
        input_dict.params[event.target.name][key]['low'] = (1 - parseFloat(document.getElementById(error_id).value)) * input_dict.params[event.target.name][key]['avg'];
        input_dict.params[event.target.name][key]['high'] = (1 + parseFloat(document.getElementById(error_id).value)) * input_dict.params[event.target.name][key]['avg'];
      }}
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
    console.log(input_dict)
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
            y_axis_label = 'g CO<sub>2</sub>(eq) per MJ';
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
