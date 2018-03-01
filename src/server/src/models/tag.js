'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var tagModel = new Schema({
        value: String,
        articleCount: Number
    }, {
        collection: 'tags'
    });

module.exports = mongoose.model('tags', tagModel);