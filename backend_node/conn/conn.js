const mongoose = require("mongoose");
// guptashubham95a;
// yaa2MkK6Ts85XjxM;
// require();
const conn = async () => {
  try {
    await mongoose.connect(`${process.env.URI}`);
    console.log("Connected to the database");
  } catch (error) {
    console.log(error);
  }
};
conn();
