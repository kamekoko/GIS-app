const fs = require('fs');

const start = [36.39326604089627, 136.52501053249725];
const end = [36.37429836513503, 136.52831501381425];

const minLon = Math.min(start[0], end[0]) - 0.03;
const maxLon = Math.max(start[0], end[0]) + 0.03;
const minLat = Math.min(start[1], end[1]) - 0.03;
const maxLat = Math.max(start[1], end[1]) + 0.03;

const bbox = [ //[min lon, max lon][min lat, max lat]
  [minLon, maxLon],
  [minLat, maxLat]
];
// console.log(bbox);

const jsonObject = JSON.parse(fs.readFileSync('./out3.geojson', 'utf8'));

console.log('{\n\t"type": "FeatureCollection",\n\t "features": [');

var count = 0;

jsonObject.features.forEach((obj) => {
  // count++;
  // if (count > 2) return;
  // console.log(obj.geometry.coordinates[0][0][0] + " , " + obj.geometry.coordinates[0][0][1]);

  if (obj.geometry.coordinates[0][0][0] > minLat &&
      obj.geometry.coordinates[0][0][0] < maxLat &&
      obj.geometry.coordinates[0][0][1] > minLon &&
      obj.geometry.coordinates[0][0][1] < maxLon) {
        console.log(JSON.stringify(obj, null, "  "));
        console.log(',');
    }
});

console.log(']\n}');
