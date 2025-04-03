import { flexRender, Table as TableType } from "@tanstack/react-table";
import { Document } from "@/types/table";
import { Table, TableBody, TableRow, TableCell } from "./ui/table";
import { Checkbox } from "./ui/checkbox";
import { Download, Link2, MoreHorizontal, Trash } from "lucide-react";

type props = {
  tableInstance: TableType<Document>;
};

const iconSize = 16;
const iconStroke = 2.5;
const iconStyle = "cursor-pointer text-black";

const DocTable = ({ tableInstance }: props) => {
  return (
    <div className="flex flex-col gap-2 w-full">
      <div className="text-[#608F97] font-bold text-2xl">All Files</div>
      <div className="flex flex-row items-center gap-3 bg-gray-100 rounded-full p-2">
        <Checkbox
          id="select-all"
          checked={tableInstance.getIsAllRowsSelected()}
          onClick={tableInstance.getToggleAllRowsSelectedHandler()}
        />
        <div className="text-[#608F97] text-sm">
          {tableInstance.getSelectedRowModel().rows.length} selected
        </div>
        <Download
          size={iconSize}
          strokeWidth={iconStroke}
          className={iconStyle}
        />
        <Trash size={iconSize} strokeWidth={iconStroke} className={iconStyle} />
        <Link2 size={iconSize} strokeWidth={iconStroke} className={iconStyle} />
        <MoreHorizontal
          size={iconSize}
          strokeWidth={iconStroke}
          className={iconStyle}
        />
      </div>
      <Table>
        <TableBody>
          {tableInstance.getRowModel().rows?.map(({ id, getVisibleCells }) => (
            <TableRow key={id}>
              {getVisibleCells().map(({ id, column, getContext }) => (
                <TableCell key={id}>
                  {flexRender(column.columnDef.cell, getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default DocTable;
