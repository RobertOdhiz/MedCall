import express from "express";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import slackEvents from "./routes/slackEvents.js";
import morgan from "morgan";

dotenv.config();

const app = express();
app.use(bodyParser.json());
app.use("/slack/events", slackEvents);
app.use(morgan("dev"));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Slack bot running on http://localhost:${PORT}`);
});
