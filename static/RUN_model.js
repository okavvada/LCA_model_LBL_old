var analysis_params = {
    'time_horizon': 100,
    'facility_electricity': 'US',
    'ionic_liquid': 'chlys',
    'feedstock': 'corn_stover',
    'fuel': 'ethanol'
    }

var common_params = {
    "IL_rail_km": {"high": 160, "avg": 160, "low": 160, "units": "km"},
    "IL_flatbedtruck_mt_km": {"high": 80, "avg": 80, "low": 80, "units": "km"},
    "etoh_distribution_rail": {"high": 150, "avg": 135, "low": 120, "units": "km"},
    "etoh_distribution_truck": {"high": 55, "avg": 50, "low": 45, "units": "km"},
    "feedstock_distribution_rail": {"high": 0, "avg": 0, "low": 0, "units": "km"}, 
    "feedstock_distribution_truck": {"high": 72, "avg": 80, "low": 88, "units": "km"}}


var processes = ["electricity_credit", "Electricity", "Chemicals_And_Fertilizers", "Petroleum", "Transportation", "Farming", "Direct", "Other"];
var selectivity = ["iHG-Projected", "iHG-Current", "waterwash"];
var parameter_path = "static/defaultParams.js";
var sections_all = ["Feedstock_Supply_Logistics", "Feedstock_Handling_and_Preparation", "Transportation", "IL_Pretreatment",
      "Enzymatic_Hydrolysis_and_Fermentation", "Recovery_and_Separation", "Hydrogeneration_and_Oligomerization",
      "Wastewater_Treatment", "Lignin_Utilization", "Byproducts"]


// Set parameter values
var input_dict = {};

$("#myFuels").change(function() {
  html_text = "<button class='accordion' id='common'>Common Parameters</button><div id = 'common_params' class='panel'>"+
              "<form><span class='tooltip-wrap'><strong>GWP time horizon [years] = </strong></span>"+
                    "<select id='myVals' onchange='lifetimeSelect()''><option value='100'>100</option><option value='20'>20</option></select></form>"+
              "<form><span class='tooltip-wrap'><strong>biorefinary electricity source [region] </strong></span>"+
                      "<select id='myList' onchange='electricitySelect()''><option value='US'>US</option><option value='NG'>NG</option>"+
                          "<option value='NGCC'>NGCC</option><option value='NG'>Coal</option><option value='Lignin'>Lignin</option>"+
                          "<option value='Renewables'>Renewables</option><option value='WECC'>WECC Mix</option><option value='MRO'>MRO Mix</option>"+
                          "<option value='SPP'>SPP Mix</option><option value='TRE'>TRE Mix</option><option value='SERC'>SERC Mix</option><option value='RFC'>RFC Mix</option>"+
                          "<option value='NPCC'>NPCC Mix</option><option value='FRCC'>FRCC Mix</option></select></form>"+
              "<form><span class='tooltip-wrap'><strong>feedstock = </strong></span><select id='myFeedstock' onchange='feedstockSelect()'>"+
                          "<option value='corn_stover'>Corn Stover</option><option value='sorghum'>Sorghum</option></select></form>"+
              "<form><span class='tooltip-wrap'><strong>ionic liquid = </strong></span><select id='myILs' onchange='ionicLiquidSelect()'>"+
                          "<option value='chlys'>[Ch][Lys]</option></select></form></div>"
    parent = document.getElementById('acc');
    parent.insertAdjacentHTML("beforeend", html_text)

  if (analysis_params.fuel == 'ethanol'){
    parameter_path = "static/defaultParams.js";
    if (document.getElementById(sections_all[0]) !== null) {
      var element_3 = document.getElementById('common');
      var element_4 = document.getElementById('common_params');
      element_3.parentNode.removeChild(element_3);
      element_4.parentNode.removeChild(element_4);
      for (var i = 0; i < sections_all.length; i++) {
      var element = document.getElementById(sections_all[i]);
      var element_2 = document.getElementById(sections_all[i]+"_params");
          element.parentNode.removeChild(element);
          element_2.parentNode.removeChild(element_2);
          $("br").remove();
        }
    }

    html_text = "<br/><button class='accordion' id='waterwash'>Waterwash Process</button><br/>" +
                "<button class='accordion' id='iHG-Current'>iHG-Current Process</button><br/>" +
                "<button class='accordion' id='iHG-Projected'>iHG-Projected Process</button>"
    parent = document.getElementById('acc');
    parent.insertAdjacentHTML("beforeend", html_text)

    for (var i = 0; i < selectivity.length; i++) {
      parent_id = selectivity[i];
      html_text = "<div id='" + parent_id + "_params' class='panel'>" +
                  "<div class='buttonSuperPro' id='SuperPro_" + parent_id + "'>Use SuperPro Values</div>" +
                  "<div class='buttonDefault' id='default_" + parent_id + "'>Use Default Values</div>" +
                    "<form><span class='tooltip-wrap'><strong>acid selection = </strong></span>" +
                      "<select id='" + parent_id + "_acid' onchange='acidSelect('" + parent_id + "_acid')'>" +
                      "<option value='h2so4'>H2SO4</option><option value='hcl'>HCl</option>" +
                  "</select></form></div>" 
      parent = document.getElementById(parent_id);
      parent.insertAdjacentHTML("afterend", html_text)
    }
  }

  if (analysis_params.fuel == 'jet_fuel'){
    parameter_path = "static/defaultParams_jetFuels.js";
    if (document.getElementById(selectivity[0]) !== null) {
      var element_3 = document.getElementById('common');
      element_3.parentNode.removeChild(element_3);
      for (var i = 0; i < selectivity.length; i++) {
        var element = document.getElementById(selectivity[i]);
            element.parentNode.removeChild(element);
        var element_2 = document.getElementById(selectivity[i]+"_params");
            element_2.parentNode.removeChild(element_2);
            $("br").remove();
          }}
        html_text = "<br/>"

        superpro_button = "<div class='buttonSuperPro' id='SuperPro_All'>Use SuperPro Values</div>" +
                          "<div class='buttonDefault' id='default_All'>Use Default Values</div>"
        parent = document.getElementById('acc');
        superpro_parent = document.getElementById('buttonWithWater')
        superpro_parent.insertAdjacentHTML("afterend", superpro_button)
        parent.insertAdjacentHTML("beforeend", html_text)

    for (var i = 0; i < sections_all.length; i++) {
        html_text = "<button class='accordion' id='" + sections_all[i] + "'>" + sections_all[i] + " Process</button><br/>"
        parent = document.getElementById('acc');
        parent.insertAdjacentHTML("beforeend", html_text)
  }
    for (var i = 0; i < sections_all.length; i++) {
      parent_id = sections_all[i];
      if (parent_id === 'IL_Pretreatment') {
        html_text = "<div id='" + parent_id + "_params' class='panel'>" +
                      "<form><span class='tooltip-wrap'><strong>acid selection = </strong></span>" +
                        "<select id='" + parent_id + "_acid' onchange='acidSelect('" + parent_id + "_acid')'>" +
                        "<option value='h2so4'>H2SO4</option><option value='hcl'>HCl</option>" +
                    "</select></form></div>" 
        parent = document.getElementById(parent_id);
        parent.insertAdjacentHTML("afterend", html_text)
      }
      else {
        html_text = "<div id='" + parent_id + "_params' class='panel'>"
        parent = document.getElementById(parent_id);
        parent.insertAdjacentHTML("afterend", html_text)}
      }
    }
  

$.getJSON( "static/parameter_names.js", function(params_alias) {
    $.getJSON( parameter_path, function(default_params) {
        for (pre_process in default_params) {
            parent_id = pre_process + "_params"
            if (parent_id === 'Transportation_params') {
                for (item in common_params) {
                          var span_class = document.createElement("span");
                          span_class.className = "tooltip-wrap";
                          if (item['avg'] == item['low']){
                              error_value = 0;
                          }
                          else {
                              error_value = Math.round(((common_params[item]['avg'] - common_params[item]['low'])/common_params[item]['avg'])*10)/10
                          }

                          html_text = (params_alias[item] + " = " + 
                                      "</span><input placeholder='value' name=" + pre_process + 
                                      " type='text' id=" + pre_process + "_" + common_params[item] + " value=" + common_params[item]['avg'] + ">"+
                                      "<span>+/-</span><input placeholder='error' name=" + pre_process + 
                                      " type='text' id=" + pre_process + "_error_" + common_params[item] +" value=" + error_value +" ><br/>")
                          span_class.insertAdjacentHTML("afterbegin", html_text)
                          parent = document.getElementById(parent_id);
                          parent.appendChild(span_class)
            }}
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
      }

    input_dict.params = default_params;
    input_dict.params.analysis_params = analysis_params;
    input_dict.params.common = common_params;
    });
});

  var acc = document.getElementsByClassName("accordion");
  for (var i = 0; i < acc.length; i++) {
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

$(".buttonSuperPro").click(function(event) {
    target_id_super = event.target.id.replace("SuperPro_", '')
    if (analysis_params.fuel == 'jet_fuel'){
      target_id_super = 'All';
    }
    path = "static/SuperPro_data_" + target_id_super + ".js"
    $.getJSON(path).done(function(super_params) {
      for (name in super_params){
        for (item in input_dict.params[name]) {
            if (item['avg'] == item['low']){
                error_value = 0;
            }
            else {
                error_value = Math.round(((item['avg'] - item['low'])/item['avg'])*10)/10
            }
            if (item in super_params[name]){
                input_dict.params[name][item]['avg'] = super_params[name][item]
                input_dict.params[name][item]['low'] = super_params[name][item] * (1 - error_value)
                input_dict.params[name][item]['high'] = super_params[name][item] * (1 + error_value)
            }
        }
      for (item in input_dict.params[name]){
          input_val_id = name + "_" + item;
          input_val = document.getElementById(input_val_id);
          input_val.value = input_dict.params[name][item]['avg']
      }}
    }).fail(function(){alert("The SuperPro data is not formated correctly. Run the `RUN_SuperPro.py` first to generate the .js file in the static folder. For more details see documentation.")});
});

$(".buttonDefault").click(function(event) {
    target_id_def = event.target.id.replace("default_", '')
    if (analysis_params.fuel == 'jet_fuel'){
      target_id_def = 'All';
      parameter_path = "static/defaultParams_jetFuels.js";}
    else if (analysis_params.fuel == 'ethanol'){
      parameter_path = "static/defaultParams.js";}
    $.getJSON(parameter_path, function(default_params) {
      for (name in default_params){
        for (item in input_dict.params[name]) {
            if (item['avg'] == item['low']){
                error_value = 0;
            }
            else {
                error_value = Math.round(((item['avg'] - item['low'])/item['avg'])*10)/10
            }
            if (item in default_params[name]){
                input_dict.params[name][item]['avg'] = default_params[name][item]['avg']
                input_dict.params[name][item]['low'] = default_params[name][item]['avg'] * (1 - error_value)
                input_dict.params[name][item]['high'] = default_params[name][item]['avg'] * (1 + error_value)
            }
        }
    for (item in input_dict.params[name]){
        input_val_id = name + "_" + item;
        input_val = document.getElementById(input_val_id);
        input_val.value = input_dict.params[name][item]['avg']
    }}
    });
});

});

function fuelSelect() {
  var myList=document.getElementById("myFuels");
  analysis_params.fuel = myList.options[myFuels.selectedIndex].value;
}

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
  console.log(input_dict)
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
        sectors = [];
        processes = []
        for (sector in data) {
          sectors.push(sector)
        }
        console.log(data)
        var index_1 = sectors.indexOf('error_bars_max');
        sectors.splice(index_1, 1);
        var index_2 = sectors.indexOf('error_bars_min');
        sectors.splice(index_2, 1);
        for (preproc in data[sectors[0]]) {
          processes.push(preproc)
        }
        for (i=0; i<sectors.length; i++){
          y = []
          errors_max = []
          errors_min = []
          for (j=0; j<processes.length; j++){
            y.push(data[sectors[i]][processes[j]])
            errors_max.push(data.error_bars_max[processes[j]])
            errors_min.push(data.error_bars_min[processes[j]])
          }
          if (input_dict.params.analysis_params.fuel == 'ethanol') {
            if (i != sectors.length - 2) {
            var trace = {
              x: processes,
              y: y,
              name: sectors[i],
              type: 'bar',
              width: 0.7
            }}
            else {
              var trace = {
              x: processes,
              y: y,
              name: sectors[i],
              type: 'bar',
              width: 0.7,
              error_y: {
                type: 'data',
                symmetric: false,
                array: errors_max,
                arrayminus: errors_min
              }
            }}
          }
          else if (input_dict.params.analysis_params.fuel == 'jet_fuel') {
            var trace = {
              x: processes,
              y: y,
              name: sectors[i],
              type: 'bar',
              width: 0.4
            }}
          

          plot_data.push(trace);
        }
            total_ww = 0
            total_ihc = 0
            total_ihp = 0
        // for (i=0; i<processes.length; i++){
        //     total_ww += data[processes[i]]['waterwash']
        //     total_ihc += data[processes[i]]['iHG-Current']
        //     total_ihp += data[processes[i]]['iHG-Projected']}

        // var trace_marker = {
        //     x: ['waterwash', 'iHG-Current', 'iHG-Projected'],
        //     y: [total_ww,
        //         total_ihc,
        //         total_ihp],
        //     mode: 'markers',
        //     showlegend: false,
        //     marker: {
        //         color: '#rgba(59, 57, 53, 0.1)',
        //         size: 7,
        //         line: {
        //             width: 2,
        //         }
        //   }}

        // plot_data.push(trace_marker);
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
