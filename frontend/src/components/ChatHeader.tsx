import { FiX, FiChevronDown, FiRefreshCw } from "react-icons/fi";
import { FaRobot } from "react-icons/fa";

interface ChatHeaderProps {
  onClose: () => void;
  onMinimize: () => void;
  onRefresh: () => void;
}

const ChatHeader = ({ onClose, onMinimize, onRefresh }: ChatHeaderProps) => (
  <div className="bg-nestle text-white p-4 flex items-center justify-between">
    <div className="flex items-center gap-2 font-semibold text-lg">
      <FaRobot size={20} />
      SMARTIE
    </div>
    <div className="flex items-center gap-3">
      <button onClick={onRefresh} title="Refresh" className="hover:scale-105">
        <FiRefreshCw size={16} />
      </button>
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
