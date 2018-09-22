const mongoose = require('mongoose');

//Connect to MongoDB
mongoose.connect('mongodb://');

mongoose.conenction.once('open', function() {

)}
