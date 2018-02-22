'use strict';

var mongoose = require('mongoose'),
    users = mongoose.model('user');

var ObjectId = mongoose.Types.ObjectId; 
var userRole = 0; //to be modified - get user role 

//temp function 
exports.test = function(req, res) {
    res.send('hit'); 
}