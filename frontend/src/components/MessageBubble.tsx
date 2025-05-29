import { FaRobot, FaUserCircle } from "react-icons/fa";

interface MessageBubbleProps {
  sender: "bot" | "user";
  text: string;
  references?: string[];
  pulse?: boolean;
}

const MessageBubble = ({
  sender,
  text,
  references,
  pulse,
}: MessageBubbleProps) => {
  const isUser = sender === "user";

  return (
    <div className={`w-full flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="relative max-w-[80%]">
        <div
          className={`absolute z-10 w-7 h-7 rounded-full flex items-center justify-center ${
            isUser
              ? "right-[-10px] top-[-10px] bg-gray-300 text-black"
              : "left-[-10px] top-[-10px] bg-nestle text-white"
          }`}
        >
          {isUser ? <FaUserCircle size={14} /> : <FaRobot size={14} />}
        </div>

        <div
          className={`relative z-0 break-words px-4 py-3 rounded-lg whitespace-pre-wrap ${
            isUser
              ? "bg-[#e4e4e7] text-[#416497] text-left"
              : `bg-nestle text-white text-left ${pulse ? "animate-pulse" : ""}`
          }`}
        >
          {text}
        </div>

        {!isUser && references && references.length > 0 && (
          <div className="mt-2 flex items-center gap-2 pl-1">
            <span className="text-xs text-nestle">References:</span>
            <div className="flex gap-1">
              {references.map((ref, idx) => (
                <a
                  key={idx}
                  href={ref}
                  target="_blank"
                  rel="noreferrer"
                  className="relative z-30 w-4 h-7 flex items-center justify-center text-xs font-semibold text-white bg-nestle rounded-md border-b-2 border-white hover:opacity-90 transition"
                >
                  {idx + 1}
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
