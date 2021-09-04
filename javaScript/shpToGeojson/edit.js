const fs = require('fs');


// input
const start = [36.39326604089627, 136.52501053249725];
const end = [36.37429836513503, 136.52831501381425];

const minLon = Math.min(start[0], end[0]) - 0.03;
const maxLon = Math.max(start[0], end[0]) + 0.03;
const minLat = Math.min(start[1], end[1]) - 0.03;
const maxLat = Math.max(start[1], end[1]) + 0.03;

const bbox = [
  [minLon, maxLon],
  [minLat, maxLat]
];


// initialize the geojson
console.log('{\n\t"type": "FeatureCollection",\n\t "features": [');

const pointObject = {
	"type": "Feature",
	"properties": { },
	"geometry": {
		"type": "MultiPoint",
		"coordinates": [[136.52501053249725, 36.39326604089627], [136.52831501381425, 36.37429836513503]]
	}
}

console.log(JSON.stringify(pointObject, null, "  "));
console.log(',');


// data collection: forest
const forestObject = JSON.parse(fs.readFileSync('./out3.geojson', 'utf8'));

forestObject.features.forEach((obj) => {
  // range constraint
  if (obj.geometry.coordinates[0][0][0] > minLat &&
      obj.geometry.coordinates[0][0][0] < maxLat &&
      obj.geometry.coordinates[0][0][1] > minLon &&
      obj.geometry.coordinates[0][0][1] < maxLon) {
        console.log(JSON.stringify(obj, null, "  "));
        console.log(',');
    }
});


// data collection: farmland
const farmObject = JSON.parse(fs.readFileSync())

// end of the geojson
console.log(']\n}');
