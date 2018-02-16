'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var agencyModel = new Schema({
        value: String
    }, {
        collection: 'agencies'
    });

module.exports = mongoose.model('agency', agencyModel);