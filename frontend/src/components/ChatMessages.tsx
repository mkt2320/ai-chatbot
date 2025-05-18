import { useEffect, useRef } from "react";
import type { Message } from "./Chatbot";
import MessageBubble from "./MessageBubble";

interface ChatMessagesProps {
  messages: Message[];
  showTyping?: boolean;
}

const ChatMessages = ({ messages, showTyping }: ChatMessagesProps) => {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gray-50 text-sm">
      {messages.map((msg, i) => (
        <MessageBubble
          key={i}
          sender={msg.sender}
          text={msg.text}
          references={msg.references}
        />
      ))}
      {showTyping && (
        <div className="text-xs text-gray-500 pl-2 animate-pulse">
          Smartie is typing...
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
};

export default ChatMessages;
