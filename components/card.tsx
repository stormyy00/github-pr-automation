import { Copy, Download, MoreVertical, Pen } from "lucide-react";
import { Checkbox } from "./ui/checkbox";
import { toast } from "sonner";
import Link from "next/link";

type props = {
  title: string;
  id: string;
  handleConfigure: () => void;
  onClick: () => void;
  checked: boolean;
  created_at: string;
};
const Documents = ({
  title,
  id,
  handleConfigure,
  onClick,
  checked,
  created_at,
}: props) => {
  return (
    <div className=" flex items-center justify-between p-4 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-300">
      <div className="flex items-center gap-4">
        <span onClick={onClick} className="cursor-pointer">
          <Checkbox checked={checked} />
        </span>
        <Link
          href={`documents/${id}`}
          className="text-lg font-medium text-gray-900 hover:text-gray-600 transition duration-200"
        >
          {title} | {created_at}
        </Link>
      </div>
      <div className="flex items-center gap-3 text-gray-500">
        <Pen
          size={20}
          onClick={handleConfigure}
          className="cursor-pointer hover:text-black transition duration-200"
        />
        <Copy
          size={20}
          className="cursor-pointer hover:text-black transition duration-200"
          onClick={() => toast("Copied to clipboard")}
        />
        <Download
          size={20}
          className="cursor-pointer hover:text-black transition duration-200"
          onClick={() => toast("Downloading...")}
        />
        <MoreVertical
          size={20}
          className="cursor-pointer text-gray-400 hover:text-black transition duration-200"
          onClick={() => toast("Hello")}
        />
      </div>
    </div>
  );
};

export default Documents;
