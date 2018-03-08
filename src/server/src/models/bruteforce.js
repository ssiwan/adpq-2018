'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var bfModel = new Schema({
  "_id": String,
  "data": {
    "count": Number,
    "lastRequest": Date,
    "firstRequest": Date
  },
  "expires": Date
});

module.exports = mongoose.model('bruteforce', bfModel);