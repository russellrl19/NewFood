const require('mocha');
const require('assert');
const Provider = require('../src/provider');
const Driver = require('../src/driver');
const Receiver = require('../src/receiver');

//Describe tests
describe('Saving records', function(){

  //create tests
  it('Saves a record to the database', function(done){

      var char = new Receiver({
        name: 'Commonwealth Catholic Charities',
        type: 'receiver'
        street: '1512 Willow Lawn Drive',
        city: 'Richmond',
        state: 'VA',
        zip: 23230
      });

      var char = new Provider({
        name: 'Food Lion',
        type: 'provider'
        street: '1512 Willow Lawn Drive',
        city: 'Richmond',
        state: 'VA',
        zip: 23230
      });

      var char = new Driver({
        name: 'Ryan Russell',
        type: 'driver'
        city: 'Manassas',
        state: 'VA',
        zip: 20112
      });

    char.save().then(function(){
      assert.(char.isNew === false);
      done();
    });

  });

});
