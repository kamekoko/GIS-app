const request = require('request');

var URL = 'http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/xy2bl.pl?';

request.get({
    uri: URL,
    headers: {'Content-type': 'application/json'},
    qs: {
        // GETのURLの後に付く
        // ?hoge=hugaの部分
        outputType:"json",
        zone:7,
        refFrame:2,
        publicX:-58893.836,
        publicY:28037.020
    },
    json: true
}, function(err, req, data){
    console.log(data);
});
