const router = require("express").Router();
const User = require("../models/user");
router.post("/sign-up", async (req, res) => {
  try {
    const { username, email, password, address } = req.body;

    // check if the user length is >4
    if (username.length < 4)
      response.status(400).json({ message: "username length should be > 3" });
    // username already present

    const existingUsername = await User.find({ email: email });
    if (existingUsername) {
      response.status(400).json({ message: "username already present" });
    }
    // email already present
    const existingEmail = await User.find({ username: username });
    if (existingEmail) {
      response.status(400).json({ message: "email already present" });
    }
    // password <6
    if (password.length <= 5)
      response.status(400).json({ message: "password length should be > 5" });

    const newUser = new User({
      email: email,
      password: password,
      username: username,
      address: address,
    });
    await newUser.save();
    return response.status(200).json({ message: "Signup successful" });
  } catch (error) {
    res.status(500).json({ message: "Internal Server Error" });
  }
});

module.exports = router;
