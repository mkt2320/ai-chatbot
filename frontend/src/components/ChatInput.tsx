import { FiSend } from "react-icons/fi";

interface ChatInputProps {
  input: string;
  onInputChange: (val: string) => void;
  onSend: () => void;
  disabled?: boolean;
}

const ChatInput = ({
  input,
  onInputChange,
  onSend,
  disabled,
}: ChatInputProps) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <form
      className="p-3 border-t bg-white"
      onSubmit={(e) => {
        e.preventDefault();
        onSend();
      }}
    >
      <div className="flex items-center w-full border border-gray-300 rounded-full overflow-hidden bg-white focus-within:ring-2 focus-within:ring-nestle">
        <input
          type="text"
          value={input}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={
            disabled ? "Refreshing content..." : "Ask me anything..."
          }
          className="flex-1 px-4 py-2 text-sm outline-none placeholder-gray-400 bg-white disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={disabled}
          aria-label="Send"
          className="h-full px-4 py-2 border-l border-gray-300 text-nestle hover:bg-nestle hover:text-white transition disabled:opacity-50"
        >
          <FiSend size={18} />
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
