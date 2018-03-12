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
            var artCount = 0; 
            if (ag.articleCount != null && ag.articleCount > 0) {
                artCount = ag.articleCount; 
            }
            obj['articleCount'] = artCount; // query to get article count            
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

exports.decrementAgencyArticleCount = function(agencyIdString) {
    var agencyId = new ObjectId(agencyIdString); 

    var queryParams = {};
    queryParams._id = agencyId; 
    var query = agency.findOne(queryParams);
    query.exec();
    query.then(function(ag) {
        if (!ag.articleCount) {
            ag.articleCount = 0; 
        }
        else if (ag.articleCount > 0) {
            ag.articleCount = ag.articleCount - 1; 
        }
        ag.save(); 
    });
    return; 
}