import { FiX, FiChevronDown } from "react-icons/fi";
import { FaRobot } from "react-icons/fa";

interface ChatHeaderProps {
  onClose: () => void;
  onMinimize: () => void;
}

const ChatHeader = ({ onClose, onMinimize }: ChatHeaderProps) => (
  <div className="bg-nestle text-white p-4 flex items-center justify-between">
    <div className="flex items-center gap-2 font-semibold text-lg">
      <FaRobot size={20} />
      SMARTIE
    </div>
    <div className="flex items-center gap-3">
      <button onClick={onMinimize} title="Minimize" className="hover:scale-105">
        <FiChevronDown size={20} />
      </button>
      <button onClick={onClose} title="Close" className="hover:scale-105">
        <FiX size={20} />
      </button>
    </div>
  </div>
);

export default ChatHeader;
