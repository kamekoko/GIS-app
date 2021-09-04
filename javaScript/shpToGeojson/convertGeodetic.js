const fs = require('fs');
const cblxy = require('./cblxy.js');

// japan to world
function get_world_latlng(lat, lng) {
  var world_lat = lat - lat * 0.00010695 + lng * 0.000017464 + 0.0046017,
  world_lng = lng - lat * 0.000046038 - lng * 0.000083043 + 0.010040;
  return {
    lat: world_lat,
    lng: world_lng
  };
}


// world to japan
function get_japan_latlng(lat, lng) {
  var japan_lat = lat * 1.000106961 - lng * 0.000017467 - 0.004602017,
  japan_lng = lng * 1.000083049 + lat * 0.000046047 - 0.010041046;
  return {
    lat: japan_lat,
    lng: japan_lng
  };
}


// initialize the geojson
console.log('{\n\t"type": "FeatureCollection",\n\t "features": [');

// convert geojson
const farmlandObject = JSON.parse(fs.readFileSync('./out-farmland.geojson', 'utf8'));

var count = 0;

farmlandObject.features.forEach((obj) => {
  if (count != 0) console.log('\t\t,');
  count++;
  console.log('\t\t{\n\t\t\t"type": "Feature",\n\t\t\t"properties": {\n\t\t\t\t"stroke": "#000",\n\t\t\t\t"stroke-opacity": 0.8,\n\t\t\t\t"stroke-width": 2,\n\t\t\t\t"fill": "#ff0",\n\t\t\t\t"fill-opacity": 0.5\n\t\t\t},\n\t\t\t"geometry": {\n\t\t\t\t"type": "Polygon",\n\t\t\t\t"coordinates": [');
  console.log('\t\t\t\t\t[');
  var list = obj.geometry.coordinates[0];
  for (var i in list) {
    var y = list[i][0];
    var x = list[i][1];
    var latlng = cblxy.xy2bl(x, y);
    console.log(latlng);
    var newLatlng = get_world_latlng(latlng[0], latlng[1]);
    console.log('\t\t\t\t\t\t[\n\t\t\t\t\t\t\t' + newLatlng.lng + ',\n\t\t\t\t\t\t\t' + newLatlng.lat + '\n\t\t\t\t\t\t]');
  }
  console.log('\t\t\t\t\t]');
  console.log('\t\t\t\t]\n\t\t\t}\n\t\t}');
  // obj.coordinates.forEach((elem) => {
  //   console.log('\t\t\t\t[');
  //   elem.forEach((elemelem) => {
  //     var lng = elemelem[0];
  //     var lat = elemelem[1];
  //     var latlng = get_world_latlng(lat, lng);
  //     console.log('\t\t\t\t\t[\n\t\t\t\t\t\t' + latlng.lng + ',\n\t\t\t\t\t\t' + latlng.lat + '\n\t\t\t\t\t]');
  //   });
  //   console.log('\t\t\t\t]\n');
  // });
  // console.log('\t\t\t\t]\n\t\t\t}\n\t\t}');
});

console.log('\t]\n}');
