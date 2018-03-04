'use strict';

var mongoose = require('mongoose'),
    agency = mongoose.model('agency');
var articleController = require('./articleController');

var ObjectId = mongoose.Types.ObjectId; 

//GET /agencies
exports.getAgencies = function (req, res) {
    var returnlist = [];

    var query = agency.find();   
    query.exec().catch(function () {
        res.send("error"); 
    });

    query.then(function(agencies) {
        agencies.forEach(function(ag, index) {
            var obj = {};
            obj['name'] = ag.value;
            obj['id'] = ag._id;
            //getArticleCount function here?
            obj['articleCount'] = index; // query to get article count            
            returnlist.push(obj); 
        })
        res.json({'data': returnlist});//will probably standardize later
    })
};

//**************************** API internal functions ***********//

exports.incrementAgencyArticleCount = function(agencyIdString) {
    var agencyId = new ObjectId(agencyIdString); 

    var queryParams = {};
    queryParams._id = agencyId; 
    var query = agency.findOne(queryParams);
    query.exec();
    query.then(function(ag) {
        if (!ag.articleCount) {
            ag.articleCount = 1; 
        }
        else {
            ag.articleCount = ag.articleCount + 1; 
        }
        ag.save(); 
    });
    return; 
}