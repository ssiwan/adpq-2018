var config = require('./config'),
    express = require('express'),
    app = express(),
    mongoose = require('mongoose'),
    bodyParser = require('body-parser'),
    tag = require('./models/tag'),
    port = process.env.port || 3001;

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
    require('./models/agency');
    require('./models/article');

    //body parser
    app.use(bodyParser.urlencoded({ extended: true }));
    app.use(bodyParser.json()); 
    
    //routes
    var routes = require('./routes'); //import routes
    routes(app);

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