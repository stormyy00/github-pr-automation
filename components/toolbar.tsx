// import { useState } from "react";
import { Search } from "lucide-react";
import { Input } from "./ui/input";
import { Filters } from "@/types/table";
import { Table } from "@tanstack/react-table";
import { Document } from "@/types/table";
import Select from "./select";

interface ToolbarProps {
  searchableItems: (string | undefined)[];
  filters: Filters[];
  setFilters: (value: Filters[]) => void;
  tableInstance: Table<Document>;
}

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

  const handleSearch = (id: string, value: unknown) => {
    const updatedFilters = filters
      .filter(({ id: filterId }: { id: string }) => filterId !== search.search)
      .concat({ id, value });
    setFilters(updatedFilters);
  };

  return (
    <div className="flex justify-between gap-2 items-center w-full bg-gray-100 px-6 py-4">
      <div className="w-1/6">
        <Select
          options={[
            { label: "Merged ", value: "merged" },
            { label: "Pending", value: "pending" },
            { label: "Reviewed", value: "review" },
          ]}
        />
      </div>
      <div className="flex items-center gap-2 w-1/2">
        <div className="relative flex-grow bg-white rounded-lg">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search size={16} className="text-gray-400" />
          </div>
          <Input
            value={value as string}
            onChange={(e) =>
              search.search && handleSearch(search.search, e.target.value)
            }
            placeholder="Search Documents"
            className="pl-10 pr-4 py-2 w-full rounded-full border border-gray-500 focus:ring-2 focus:ring-gray-200 focus:border-gray-400 text-sm"
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
