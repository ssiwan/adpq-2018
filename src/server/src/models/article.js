//article model here
'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var articleModel = new Schema({
        createdAt: Date,
        createdBy: {type: Schema.Types.ObjectId, ref: 'user'},
        agency: {type: Schema.Types.ObjectId, ref: 'agency'},
        role: Number,//0 - 2
        status: Number,//0 - open, 1 - published, 2 - declined
        title: String,
        summary: String,
        approvedBy: Schema.Types.ObjectId,//{type: Schema.Types.ObjectId, ref: 'users'},
        tags: [{type: Schema.Types.ObjectId, ref: 'tags'}],
        comments: [{type: Schema.Types.ObjectId, ref: 'articleComment'}],//ref article comments
        views: Number,
        type: Number, //dud for now
        description: String,
        attachments: [String],
        sharedUsers: [Schema.Types.ObjectId],
        articleEdits: [{type: Schema.Types.ObjectId, ref: 'articleEdit'}]      
    }, {
        collection: 'articles'
    });

module.exports = mongoose.model('article', articleModel);