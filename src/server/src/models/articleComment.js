'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var articleCommentModel = new Schema({
    commenterId: {type: Schema.Types.ObjectId, ref: 'user'},
    articleId: {type: Schema.Types.ObjectId, ref: 'article'},
    comment: String,
    createdAt: Date
}, {
    collection: 'articleComments'
});

module.exports = mongoose.model('articleComment', articleCommentModel); 