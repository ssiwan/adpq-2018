'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var tagModel = new Schema({
        value: String
    }, {
        collection: 'tags'
    });

module.exports = mongoose.model('tag', tagModel);