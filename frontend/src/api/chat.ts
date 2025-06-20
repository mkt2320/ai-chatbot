import axios from "axios";

interface ChatbotResponse {
  reply: string;
  references: string[];
}

const BASE_URL =
  import.meta.env.VITE_BACKEND_URL || "http://172.174.235.83:8000";

export const sendChatMessage = async (
  message: string
): Promise<ChatbotResponse> => {
  const response = await axios.post(
    `${BASE_URL}/chat`,
    { message },
    { timeout: 5000 }
  );
  return response.data;
};

export const refreshChatbotData = async (): Promise<void> => {
  await axios.post(`${BASE_URL}/refresh`, {}, { timeout: 10000 });
};
