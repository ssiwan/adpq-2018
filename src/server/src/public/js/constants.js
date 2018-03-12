'use strict'

var APIURL;
var SocialMediaURL;

switch (process.env.NODE_ENV) {
    case 'local':
        APIURL = "http://localhost:3001/api/v1/";
        SocialMediaURL = "http://localhost:3001/";
        break;
    case 'staging':
        APIURL = "https://adpq-staging.hotbsoftware.com/api/v1/";
        SocialMediaURL = "https://adpq-staging.hotbsoftware.com/";
        break;
    case 'production':
        APIURL = "https://adpq.hotbsoftware.com/api/v1/";
        SocialMediaURL = "https://adpq.hotbsoftware.com/";
        break;
    default:
        APIURL = "https://adpq-staging.hotbsoftware.com/api/v1/";
        SocialMediaURL = "https://adpq-staging.hotbsoftware.com/";
        break;
}