import express from "express";
import { WebClient } from "@slack/web-api";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const router = express.Router();
const slackClient = new WebClient(process.env.SLACK_BOT_TOKEN);
const BASE_URL = "http://localhost:8000"; // Replace if deployed
const messageHistory = new Map(); // In-memory history per user

// Slack Event Endpoint
router.post("/", async (req, res) => {
  const { type, challenge, event } = req.body;

  // 🔁 Handle Slack URL Verification
  if (type === "url_verification") {
    return res.status(200).send({ challenge });
  }

  // ✅ Respond immediately to prevent Slack retries
  res.sendStatus(200);

  // ❌ Skip irrelevant events
  if (!event || (!event.type && !event.text)) return;
  if (event.subtype === "bot_message" || event.bot_id) return;

  // ✅ Process message or mention
  if (event.type === "message" || event.type === "app_mention") {
    const userInput = event.text;
    const userId = event.user;
    const channelId = event.channel;

    // Step 1: Get existing history or init
    if (!messageHistory.has(userId)) {
      messageHistory.set(userId, []);
    }

    const history = messageHistory.get(userId);

    // Step 2: Add the new message
    history.push({ role: "user", content: userInput });

    // Step 3: Keep only the last 20 items (10 turns)
    const trimmedHistory = history.slice(-20);

    try {
      // Step 4: Send to backend with history
      const response = await axios.post(`${BASE_URL}/api/analyze`, {
        slack_user_id: userId,
        input_text: trimmedHistory,
      });

      const aiResponse = response.data.ai_response;

      // Step 5: Append assistant reply to history
      trimmedHistory.push({ role: "assistant", content: aiResponse });

      // Step 6: Save updated history
      messageHistory.set(userId, trimmedHistory);

      // Step 7: Respond to Slack
      await slackClient.chat.postMessage({
        channel: channelId,
        text: `<@${userId}> ${aiResponse}`,
      });
    } catch (err) {
      console.error("❌ AI request failed:", err);
      await slackClient.chat.postMessage({
        channel: channelId,
        text: `<@${userId}> Sorry, something went wrong processing your message.`,
      });
    }
  }
});

export default router;
