'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var userModel = new Schema({
    name: {first: String, last: String},
    email: String,
    phone: String,
    role: Number,// 1 - 4. 0 is guest
    createdAt: Date,
    updatedAt: Date
}, {
    collection: 'users'
});

module.exports = mongoose.model('user', userModel); 