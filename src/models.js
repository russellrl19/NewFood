const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// Create a Schema and a Model
const ProviderSchema = new Schema({
    name: String,
    street: String,
    city: String,
    state: String,
    zip: Int32
});

const DriverSchema = new Schema({
    name: String,
    city: String,
    state: String,
    zip: Int32
});

const RecieverSchema = new Schema({
    name: String,
    street: String,
    city: String,
    state: String,
    zip: Int32
});

const FoodSchema = new Schema({
    name: String,
    address: String,
    quantity: Int32,
    description: String,
    expiration: Date
})

const Provider = mongoose.model('Provider', ProviderSchema);
const Driver = mongoose.model('Driver', DriverSchema);
const Receiver = mongoose.model('Receiver', ReceiverSchema);

module.exports = Provider;
module.exports = Driver;
module.exports = Receiver;

// modles.js
export const ProviderSchema {
  return Provider;
}
