"use client";
import { useState, useEffect } from "react";
import Toolbar from "./toolbar";
import { ITEMS } from "@/data/mock";
import Tile from "./tile";
import { COLUMNS } from "@/data/columns";
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
} from "@tanstack/react-table";
import { Filters } from "@/types/table";
import Table from "./table";
import { Loader2Icon } from "lucide-react";

const Dashboard = () => {
  const [data, setData] = useState(ITEMS);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<Filters[]>([
    { id: "title", value: "" },
  ]);
  const searchableItems = COLUMNS.filter(({ searchable }) => searchable).map(
    ({ accessorKey }) => accessorKey,
  );

  const tableInstance = useReactTable({
    columns: COLUMNS,
    data: data,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      columnFilters: filters,
    },
  });
  useEffect(() => {
    fetch("/api/pull-requests", {
      method: "GET",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setData(data);
        // setSearch(data);
      })
      .catch((error) => {
        console.error("Error fetching newsletters:", error);
        setLoading(false);
      })
      .finally(() => setLoading(false));
  }, []);

  // const handleConfigure = () => {
  // console.log("hello");
  // setPopup({
  //   ...popup,
  //   visible: true,
  // });
  // };
  return (
    <div className="w-full flex flex-col items-center gap-5">
      <Toolbar
        searchableItems={searchableItems}
        filters={filters}
        setFilters={setFilters}
        tableInstance={tableInstance}
      />
      <div className="mx-10 m-4 text-[#608F97] font-bold text-2xl px-10 w-full">
        Recently Reviewed
        <div className="flex gap-4 grid grid-cols-5">
          {data.map(({ title, created_at, user }, index) => (
            <Tile key={index} title={title} date={created_at} name={user} />
          ))}
        </div>
      </div>
      {/* <div className="mx-10 m-4 text-[#608F97] font-bold text-2xl px-10 w-full">
        Recently Merged
        <div className="flex gap-4 w-full">
          {DOCS.map(({ title, text }, index) => (
            <Tile key={index} name={title} date={text} image={"M"} />
          ))}
        </div>
      </div> */}
      <div className="px-10 w-full flex justify-center">
        {loading ? (
          <Loader2Icon size={40} className="animate-spin" />
        ) : (
          <Table tableInstance={tableInstance} />
        )}
      </div>
    </div>
  );
};

export default Dashboard;
