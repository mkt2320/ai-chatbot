import { useState } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

export type Message = {
  sender: "bot" | "user";
  text: string;
  references?: string[];
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

  const toggleChat = () => setIsOpen(true);

  const handleClose = () => {
    setIsOpen(false);
    setChatHistory([defaultBotIntro]);
    setInput("");
  };

  const handleMinimize = () => {
    setIsOpen(false);
  };

  const handleSend = () => {
    if (!input.trim()) return;
    setChatHistory((prev) => [...prev, { sender: "user", text: input }]);
    setInput("");
    setTimeout(() => {
      setChatHistory((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `Here’s a placeholder answer to: **${input}** 🧠`,
          references: [
            "https://www.madewithnestle.ca/recipes",
            "https://www.madewithnestle.ca/brands",
          ],
        },
      ]);
    }, 1000);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {!isOpen ? (
        <button
          onClick={toggleChat}
          className="bg-nestle text-white p-3 rounded-full shadow-lg hover:scale-105 transition-transform"
          aria-label="Open Chatbot"
        >
          <span className="sr-only">Open Chatbot</span>
          <span role="img" aria-label="chat">
            💬
          </span>
        </button>
      ) : (
        <div className="w-96 h-[500px] bg-white rounded-2xl shadow-xl flex flex-col overflow-hidden border border-gray-300 animate-fade-in">
          <ChatHeader onClose={handleClose} onMinimize={handleMinimize} />
          <ChatMessages messages={chatHistory} />
          <ChatInput
            input={input}
            onInputChange={setInput}
            onSend={handleSend}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;
