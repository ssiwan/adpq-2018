var config = require('./config'),
    express = require('express'),
    app = express(),
    mongoose = require('mongoose'),
    bodyParser = require('body-parser'),
    port = process.env.port || 3001;

var cors = require('cors');

//connect to db
mongoose.Promise = global.Promise;

const options = {
    user: config.dbUser,
    pass: config.dbPassword,
    auth: {
        authdb: 'admin'
    }
};

mongoose.connect(config.dbUrl, options).then(() => {
    var db = mongoose.connection;
    db.on('error', console.error.bind(console, 'MongoDB connection error:'));
    
    //models
    require('./models/tag');
    require('./models/user');
    require('./models/agency');
    require('./models/articleComment');
    require('./models/article');

    //cors 
    app.use(cors()); 

    //body parser
    app.use(bodyParser.urlencoded({ extended: true }));
    app.use(bodyParser.json()); 
    
    //routes
    var routes = require('./routes'); //import routes
    routes(app, config.apiParseKey, config.AWSKeys);

    app.use(express.static(require('path').join(__dirname, 'public')));

    app.get('/', (req, res) => {
        res.sendFile('/index.html', {root : __dirname + 'public'})
    })

    app.listen(port, () => {
        console.log('Server listening on port 3001')
    });
    
}, error => {
    console.log(error)
});