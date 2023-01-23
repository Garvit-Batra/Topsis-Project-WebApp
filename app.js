require("dotenv").config();
const express = require("express");
const bodyParser = require("body-parser");
var nodemailer = require("nodemailer");
const { spawn } = require("child_process");
const upload = require("express-fileupload");
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static("public"));
app.use(upload());
const port = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.post("/", (req, res) => {
  if (req.files) {
    let file = req.files.file;
    let fileName = file.name;
    file.mv("./uploads/" + fileName, function (err) {
      if (err) {
        console.log(err);
      } else {
        res.sendFile(__dirname + "/greetings.html");
      }
    });
  }
  const python = spawn("python", [
    "102017132.py",
    "./uploads/" + req.files.file.name,
    req.body.weights,
    req.body.impact,
    "result.csv",
  ]);
  let transporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 465,
    secure: true,
    auth: {
      type: "OAuth2",
      user: process.env.MAIL_USERNAME,
      clientId: process.env.OAUTH_CLIENTID,
      clientSecret: process.env.OAUTH_CLIENT_SECRET,
      refreshToken: process.env.OAUTH_REFRESH_TOKEN,
      accessToken: process.env.ACCESS_TOKEN,
    },
  });
  const mailOptions = {
    from: process.env.MAIL,
    to: req.body.email,
    subject: "Email is here!",
    attachments: [
      {
        filename: "result.csv",
        path: "result.csv",
      },
    ],
  };
  transporter.sendMail(mailOptions, function (err, data) {
    if (err) {
      console.log("Error " + err);
    } else {
      console.log("Email sent successfully");
    }
    transporter.close();
  });
});

app.listen(port, () => console.log("Server started on port 3000"));
