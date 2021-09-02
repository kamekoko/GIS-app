"use strict";
var shapefile = require("shapefile");

var shp = process.argv[2];

shapefile.read(shp, undefined, {
    encoding: "shift_jis"
  }).then(function(geojson) {
    geojson.features.forEach(function(feature) {
      feature.properties["stroke"] = "#000";
      feature.properties["stroke-opacity"] = 0.8;
      feature.properties["stroke-width"] = 2;
      feature.properties["fill"] = "#ff0";
      feature.properties["fill-opacity"] = 0.5;
    });
    console.log(JSON.stringify(geojson, null, "  "));
  })
  .catch(function(error) {
    console.log(error);
  });
