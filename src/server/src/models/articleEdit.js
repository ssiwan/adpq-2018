'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var articleEditModel = new Schema({
    createdBy: {type: Schema.Types.ObjectId, ref: 'user'},
    articleId: {type: Schema.Types.ObjectId, ref: 'article'},
    status: Number,
    createdAt: Date
}, {
    collection: 'articleEdits'
});

module.exports = mongoose.model('articleEdit', articleEditModel); 