'use strict';

var mongoose = require('mongoose'),
    tags = mongoose.model('tags');
mongoose.Promise = Promise;

//GET /tags
exports.getTags = function (req, res) {
    var returnlist = [];  
    var query = tags.find();
    
    query.exec().catch(function (err) {
        res.json({'error':'Query error'});
    });  
    
    query.then(function(tgs, blah) {
        tgs.forEach(function(tg) {
                var obj = {};
                obj["id"] = tg._id.toString(); 
                obj["name"] = tg.value;
                returnlist.push(obj);
            });
        res.json({'data': returnlist}); 
    });
};

exports.convertTags = function(tags) {
    
}    