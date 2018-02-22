//article model here
'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var articleModel = new Schema({
        createdAt: Date,
        createdBy: Schema.Types.ObjectId,//mongoose.Types.ObjectId(string)
        agency: {type: Schema.Types.ObjectId, ref: 'agency'},
        role: Number,//0 - 4
        status: Number,//0 - open, 1 - published, 2 - declined
        title: String,
        summary: String,
        approvedBy: Schema.Types.ObjectId,
        tags: [{type: Schema.Types.ObjectId, ref: 'tags'}],
        views: Number,
        description: [{role: Number, value: String}],
        attachments: [{role: Number, value: [String]}],
        sharedUsers: [Schema.Types.ObjectId]
    }, {
        collection: 'articles'
    });

module.exports = mongoose.model('article', articleModel);