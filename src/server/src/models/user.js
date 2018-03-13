'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var userModel = new Schema({
    name: {first: String, last: String},
    email: String,
    phone: String,
    agency: {type: Schema.Types.ObjectId, ref: 'agency'},
    role: Number,// 1 - 4. 0 is guest
    createdAt: Date,
    updatedAt: Date,
    salt: String,
    hashedPassword: String, 
    allowUploads: Number,
    isDeleted: Number
}, {
    collection: 'users'
});

module.exports = mongoose.model('user', userModel); 