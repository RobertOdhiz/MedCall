import axios from "axios";
import dotenv from "dotenv";
dotenv.config();

const BASE_URL = process.env.BACKEND_URL;

export const analyzeText = async (userId, message) => {
  const response = await axios.post(`${BASE_URL}/api/analyze`, {
    slack_user_id: userId,
    input_text: message
  });

  return response.data.ai_response;
};
