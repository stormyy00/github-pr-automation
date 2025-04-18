import { useState } from "react";
import { ChevronDown, PlusCircle, Search } from "lucide-react";
import { Input } from "./ui/input";
import { Filters } from "@/types/table";
import { Table } from "@tanstack/react-table";
import { Document } from "@/types/table";
import Select from "./select";
import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";
import Add from "./add";

interface ToolbarProps {
  searchableItems: (string | undefined)[];
  filters: Filters[];
  setFilters: (value: Filters[]) => void;
  tableInstance: Table<Document>;
  repositories: string[];
  setRepositories: (value: string[]) => void;
}

const Toolbar = ({
  searchableItems,
  filters,
  setFilters,
  repositories,
  setRepositories,
}: ToolbarProps) => {
  const search = { search: searchableItems[0] };

  const value = filters.find(({ id }) => id === search.search)?.value || "";
  const [loading, setLoading] = useState(false);

  const [popup, setPopup] = useState({
    title: "",
    visible: false,
    name: "",
    organization: "",
    isValidating: false,
    isValid: false,
    message: "",
    color: "",
  });
  console.log(popup);

  const addRepository = () => {
    if (!popup.isValid) {
      setPopup({
        ...popup,
        isValidating: false,
        isValid: false,
        message: "Repository is not valid. Please validate before adding.",
      });
      return;
    }

    fetch("/api/config", {
      method: "POST",
      body: JSON.stringify({
        name: popup.name,
        organization: popup.organization,
      }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setRepositories((prev) => [...prev, popup.name]);
        toast.success("Repository added successfully!");
        setLoading(false);
        setPopup({ ...popup, visible: false });
      })
      .catch((error) => {
        console.error("Error fetching newsletters:", error);
        setLoading(false);
      });
  };

  const validateRepository = () => {
    if (!popup.name || !popup.organization) {
      setPopup({
        ...popup,
        isValidating: false,
        isValid: false,
        message: "Please enter both repository name and organization.",
      });
      return;
    }

    setPopup({
      ...popup,
      isValidating: true,
      message: "Validating repository...",
    });

    fetch("/api/search", {
      method: "POST",
      body: JSON.stringify({
        name: popup.name,
        organization: popup.organization,
      }),
    })
      .then((res) => {
        if (!res.ok) {
          if (res.status === 404) {
            return null;
          }
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (data) {
          setPopup({
            ...popup,
            isValidating: false,
            isValid: true,
            message: `Repository "${popup.name}" found in ${popup.organization}!`,
          });
        } else {
          setPopup({
            ...popup,
            isValidating: false,
            isValid: false,
            message: `Repository "${popup.name}" not found in ${popup.organization}. Please check your inputs.`,
          });
        }
      })
      .catch((error) => {
        setPopup({
          ...popup,
          isValidating: false,
          isValid: false,
          message: `Error validating repository: ${error.message}`,
        });
      });
  };

  const handleSearch = (id: string, value: unknown) => {
    const updatedFilters = filters
      .filter(({ id: filterId }: { id: string }) => filterId !== search.search)
      .concat({ id, value });
    setFilters(updatedFilters);
  };

  return (
    <div className="flex justify-between gap-2 items-center w-full bg-gray-100 px-6 py-4">
      <div className="flex w-1/4 justify-between gap-5">
        <Select
          placeholder="Status"
          options={[
            { label: "Merged ", value: "merged" },
            { label: "Pending", value: "pending" },
            { label: "Reviewed", value: "review" },
          ]}
        />
        <Select
          placeholder="Repository"
          options={repositories.map((repo) => ({
            label: repo,
            value: repo,
          }))}
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
        <Button
          onClick={() => setPopup({ ...popup, visible: true })}
          className="bg-gray-200 text-gray-600 text-sm font-medium rounded-full hover:bg-gray-300 hover:text-gray-700 transition-colors"
        >
          <PlusCircle />
        </Button>
      </div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="outline"
            className="bg-blue-50 text-blue-600 hover:bg-blue-100 border-blue-200"
          >
            Actions
            <ChevronDown size={16} className="ml-2" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem className="text-blue-600 font-medium">
            Merge
          </DropdownMenuItem>
          <DropdownMenuItem className="text-green-600 font-medium">
            Approve
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <div className="flex flex-col justify-center items-end">
        <span className=" text-gray-600 text-base">Welcome back,</span>
        <span className="font-semibold text-xl text-cyan-600">Jonathan</span>
      </div>
      <Add
        popup={popup}
        setPopup={setPopup}
        loading={loading}
        onClick={addRepository}
        validate={validateRepository}
      />
    </div>
  );
};

export default Toolbar;
