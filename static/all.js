

function RunModel() {

  var Parameters = {};

  document.getElementById("common_enzyme").onchange = function() {
      a = document.getElementById("common_enzyme").value;
      return a
  }
  document.getElementById("common_chlys_percent").onchange = function() {
      b = document.getElementById("common_chlys_percent").value;
      return b
  }
  document.getElementById("common_cholinium_percent").onchange = function() {
      c = document.getElementById("common_cholinium_percent").value;
      return c
  }
  document.getElementById("common_etoh_distribution_truck").onchange = function() {
      d = document.getElementById("common_etoh_distribution_truck").value;
      return d
  }

  document.getElementById("common_etoh_distribution_rail").onchange = function() {
      e = document.getElementById("common_etoh_distribution_rail").value;
      return e
  }
  
  var run_button = document.getElementById('controlTextEnergy');
  run_button.addEventListener('mouseover', function() {
      run_button.style['background-color'] = '#e6e9ed';
    });
  run_button.addEventListener('mouseout', function() {
      run_button.style['background-color'] = '#fff';
    });

  console.log(a)

  run_button.addEventListener('click', function() {
    console.log(a)

  });
// element = document.getElementById('map');

// element.addEventListener('click', function(event) {

// 		$.getJSON("/lat_lng", {
// 			a: a,
// 			b: b,
// 			c: c,
// 			d: d,
// 			direct: direct
// 		}

// 			var results_text = "<br /><u>Cluster " + "</u> ()<br />Houses: <br />Population:<br />";
//   			var results = document.getElementById('results');
// 			results.style.fontSize = "14px";
// 			var div = document.createElement('div');
// 			div.innerHTML = results_text;
// 			results.appendChild(div);


// 	}); 

}


