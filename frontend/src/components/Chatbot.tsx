import { useState } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import { sendChatMessage, refreshChatbotData } from "../api/chat";
import { FaRobot } from "react-icons/fa";

export type Message = {
  sender: "bot" | "user";
  text: string;
  references?: string[];
  pulse?: boolean;
};

const defaultBotIntro: Message = {
  sender: "bot",
  text: `Hey! I'm Smartie, your personal MadeWithNestlé assistant.  
Ask me anything, and I’ll quickly search the entire site to find the answers you need!`,
};

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [chatHistory, setChatHistory] = useState<Message[]>([defaultBotIntro]);
  const [showTyping, setShowTyping] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const toggleChat = () => setIsOpen(true);

  const handleClose = () => {
    setIsOpen(false);
    setChatHistory([defaultBotIntro]);
    setInput("");
  };

  const handleMinimize = () => setIsOpen(false);

  const handleSend = async () => {
    if (!input.trim() || isRefreshing) return;

    const userMessage: Message = { sender: "user", text: input };
    setChatHistory((prev) => [...prev, userMessage]);
    setInput("");
    setShowTyping(true);

    try {
      const { reply, references } = await sendChatMessage(input);
      const botMessage: Message = {
        sender: "bot",
        text: reply,
        references,
      };

      setTimeout(() => {
        setChatHistory((prev) => [...prev, botMessage]);
        setShowTyping(false);
      }, 600);
    } catch (error) {
      console.error("Error contacting chatbot:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, something went wrong." },
      ]);
      setShowTyping(false);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);

    setChatHistory((prev) => [
      ...prev,
      {
        sender: "bot",
        text: "Refreshing content... Please wait a moment...",
        pulse: true,
      },
    ]);

    try {
      await refreshChatbotData();

      setTimeout(() => {
        setChatHistory((prev) =>
          prev
            .map((msg) => (msg.pulse ? { ...msg, pulse: false } : msg))
            .concat({
              sender: "bot",
              text: "Smartie is ready again! Ask me anything.",
            })
        );
        setIsRefreshing(false);
      }, 10000);
    } catch (err) {
      console.error("Refresh failed", err);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "Refresh failed. Please try again later." },
      ]);
      setIsRefreshing(false);
    }
  };

  return (
    <div className="absolute bottom-4 right-4 z-50">
      {!isOpen ? (
        <button
          onClick={toggleChat}
          className="bg-nestle text-white p-3 rounded-full shadow-lg hover:scale-105 transition-transform"
          aria-label="Open Chatbot"
        >
          <span className="sr-only">Open Chatbot</span>
          <span role="img" aria-label="chat">
            <FaRobot size={20} />
          </span>
        </button>
      ) : (
        <div className="w-96 max-w-[90vw] h-[500px] bg-white rounded-2xl shadow-xl flex flex-col overflow-hidden border border-gray-300 transform transition-all duration-300 ease-out translate-y-0 opacity-100">
          <ChatHeader
            onClose={handleClose}
            onMinimize={handleMinimize}
            onRefresh={handleRefresh}
          />
          <ChatMessages messages={chatHistory} showTyping={showTyping} />
          <ChatInput
            input={input}
            onInputChange={setInput}
            onSend={handleSend}
            disabled={isRefreshing}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;
