const router = require("express").Router();
const User = require("../models/user");
const jwt = require("jsonwebtoken");
const { authenticateToken } = require("./userAuth");

router.post("/sign-up", async (req, response) => {
  try {
    const { username, email, password, address } = req.body;

    // check if the user length is >4
    if (username.length < 4)
      response.status(400).json({ message: "username length should be > 3" });
    // username already present

    const existingUsername = await User.findOne({ username: username });
    if (existingUsername) {
      response.status(400).json({ message: "username already present" });
    }
    // email already present
    const existingEmail = await User.findOne({ email: email });
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
    response.status(500).json({ message: error });
  }
});

router.post("/sign-in", async (req, response) => {
  try {
    const { username, password } = req.body;

    const existingUser = await User.findOne({ username: username });
    if (!existingUser) {
      response.status(400).json({ message: "Invalid Credentials" });
    }

    // check password
    if (password === existingUser.password) {
      const authClaims = [
        { name: existingUser.username },
        { role: existingUser.role },
      ];
      const token = jwt.sign({ authClaims }, "bookStore123", {
        expiresIn: "30d", // expires in 30 days.
      });
      response.status(200).json({
        id: existingUser._id,
        role: existingUser.role,
        token: token,
        message: "Signin Successfull",
      });
    } else {
      response.status(400).json({ message: "Invalid Credentials" });
    }
  } catch (error) {
    response.status(500).json({ message: error });
  }
});

router.get(
  "/get-user-information",
  authenticateToken,
  async (req, response) => {
    try {
      const { id } = req.headers;
      const data = await User.findById(id);
      return response.status(200).json(data);
    } catch (error) {
      response.status(500).json({ message: error });
    }
  }
);

router.put("/update-address", authenticateToken, async (req, response) => {
  try {
    const { id } = req.headers;
    const { address } = req.body.address;
    const data = await User.findByIdAndUpdate(id, { address: address });
    return response
      .status(200)
      .json({ message: "Address updated successfully." });
  } catch (error) {
    response.status(500).json({ message: error });
  }
});

module.exports = router;
