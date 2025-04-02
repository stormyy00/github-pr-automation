// import { useState } from "react";
import { Plus, Search } from "lucide-react";
import { Input } from "./ui/input";

type ToolbarProps = {
  searchableItems: string[];
  filters: { id: string; value: unknown }[];
  setFilters: (filters: { id: string; value: unknown }[]) => void;
};

const Toolbar = ({ searchableItems, filters, setFilters }: ToolbarProps) => {
  const search = { search: searchableItems[0] };

  const value = filters.find(({ id }) => id === search.search)?.value || "";

  // const [popup, setPopup] = useState({
  //   title: "",
  //   text: "",
  //   color: "",
  //   visible: false,
  //   onClick: () => {},
  //   button: "",
  // });
  // const ids = Object.keys(checked).filter((id) => checked[id]);

  const handleNewletter = () => {
    fetch("/api/newsletter", {
      method: "POST",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Created newsletter:", data);
        // router.push(`/newsletter/${data.newsletterId}`); slow loading
      })
      .catch((error) => {
        console.error("Error creating newsletters:", error);
      });
  };

  const handleSearch = (id: string, value: unknown) => {
    const updatedFilters = filters
      .filter(({ id: filterId }: { id: string }) => filterId !== search.search)
      .concat({ id, value });
    setFilters(updatedFilters);
  };

  return (
    <div className="flex justify-between items-center w-full bg-gray-100 px-6 py-4">
      <div className="flex items-center gap-2 w-1/2">
        <div className="relative flex-grow bg-white rounded-lg">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search size={16} className="text-gray-400" />
          </div>
          <Input
            value={value}
            onChange={(e) =>
              search.search && handleSearch(search.search, e.target.value)
            }
            placeholder="Search Documents"
            className="pl-10 pr-4 py-2 w-full rounded-full border border-gray-500 focus:ring-2 focus:ring-gray-200 focus:border-gray-400 text-sm"
          />
        </div>
        <div className="flex items-center px-3 py-2 text-sm font-medium text-white bg-[#608F97] rounded-full gap-1 hover:bg-teal-700 transition-colors cursor-pointer">
          <span>New</span>
          <Plus
            size={16}
            onClick={handleNewletter}
            className="cursor-pointer"
          />
        </div>
      </div>
      {/* dropdown or on hover expands to show more stats */}
      <div className="flex items-center gap-8">
        <div className="flex flex-col text-sm text-gray-600">
          <span className="font-medium text-gray-800">Statistics</span>
          <div className="flex gap-2 mt-1">
            <span>Lines: 20</span>
            <span>•</span>
            <span>Documents: 2</span>
            <span>•</span>
            <span>Documents: 2</span>
            <span>•</span>
            <span>Documents: 2</span>
          </div>
        </div>
        <div className="flex flex-col justify-center items-end">
          <span className=" text-gray-600 text-base">Welcome back,</span>
          <span className="font-semibold text-xl text-cyan-600">Jonathan</span>
        </div>
      </div>
    </div>
  );
};

export default Toolbar;
