"use client";
import { useState, useEffect } from "react";
import Toolbar from "./toolbar";
// import { ITEMS } from "@/data/mock";
import Tile from "./tile";
import { COLUMNS } from "@/data/columns";
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
} from "@tanstack/react-table";
import { Filters } from "@/types/table";
import Table from "./table";

const repo = ["Hackathon.js", "Latex-AI", "REPO"];

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [repositories, setRepositories] = useState([]);
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
    setLoading(true);

    // Fetch pull requests data
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
      })
      .catch((error) => {
        console.error("Error fetching pull requests:", error);
      })
      .finally(() => setLoading(false));

    // Fetch repositories data
    fetch("/api/repositories", {
      method: "GET",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((repos) => {
        console.log("Repositories loaded:", repos);
        setRepositories(repos);
      })
      .catch((error) => {
        console.error("Error fetching repositories:", error);
        // Fallback to empty array if API fails
        setRepositories([]);
      });
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
        repositories={repositories}
        setRepositories={setRepositories}
      />
      <div className="mx-10 m-4 text-[#608F97] font-bold text-2xl px-10 w-full">
        Recently Reviewed
        <div className="gap-4 grid grid-cols-5">
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
        <Table tableInstance={tableInstance} loading={loading} />
      </div>
    </div>
  );
};

export default Dashboard;
