'use strict';

var mongoose = require('mongoose'),
    jwt = require('jsonwebtoken'), 
    users = mongoose.model('user');

var ObjectId = mongoose.Types.ObjectId; 

//temp function 
exports.signIn = function(req, res) {
    var userEmail = req.body.email; 
    var queryParams = {};
    queryParams.email = userEmail;
    var query = users.findOne(queryParams);

    query.exec()
        .catch(function (err) {
            res.send(err);
        });  
    
    query.then(function(user) {
        if (!user) {
            res.json({error: 'User not found'});
            return;
        }
        else {
            res.json({token: jwt.sign({exp: Math.floor(Date.now() / 1000) + ( 7 * 24 * 60 * 60), userId: user._id.toString(), role: user.role}, req.PK)});
            //set token expiring at a week 
        }
    });  
}