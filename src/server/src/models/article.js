//article model here
'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var agency = mongoose.model('agency'); 

var articleModel = new Schema({
        createdAt: Date,
        createdBy: Schema.Types.ObjectId,//mongoose.Types.ObjectId(string)
        agency: Schema.Types.ObjectId,
        role: Number,//0 - 4
        status: Number,//0 - closed, 1-open
        title: String,
        summary: String,
        approvedBy: Schema.Types.ObjectId,
        tags: [String],
        views: Number,
        description: [{role: Number, value: String}],
        attachments: [{role: Number, value: [String]}],
        sharedUsers: [Schema.Types.ObjectId]
    }, {
        collection: 'articles'
    });

module.exports = mongoose.model('article', articleModel);