'use strict';

var mongoose = require('mongoose'),
    tag = mongoose.model('tag');
mongoose.Promise = Promise;

//GET /tags
exports.getTags = function (req, res) {
    var returnlist = []; 

    var query = tag.find();
    
    query.exec().catch(function (err) {
            res.json({'error':'Query error'});
        });  
    
    query.then(function(tags) {
        tags.forEach(function(tg) {
                var obj = {};
                obj["name"] = tg.value;
                returnlist.push(obj);
            });
        res.json({'data': returnlist}); 
    });
};    