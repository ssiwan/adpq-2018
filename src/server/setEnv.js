'use strict'

const fs = require('fs')

var localStr = "var APIURL = \"http://localhost:3001/api/v1/\";\nvar SocialMediaURL = \"http://localhost:3001/\";"
var stagingStr = "var APIURL = \"https://adpq-staging.hotbsoftware.com/api/v1/\";\nvar SocialMediaURL = \"https://adpq-staging.hotbsoftware.com/\";"
var productionStr = "var APIURL = \"https://adpq.hotbsoftware.com/api/v1/\";\nvar SocialMediaURL = \"https://adpq.hotbsoftware.com/\";"

var str
switch (process.env.NODE_ENV) {
    case 'local':
        str = localStr
        break;
    case 'staging':
        str = stagingStr
        break;
    case 'production':
        str = productionStr
        break;
    default:
        str = stagingStr
        break;
}

fs.writeFile("./src/public/js/constants.js", str, function(err) {
    if (err) { return console.log(err) }
}); 