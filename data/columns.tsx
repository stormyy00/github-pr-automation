import { Checkbox } from "@/components/ui/checkbox";
import { CellContext, ColumnDef, Row } from "@tanstack/react-table";
import { Copy, Download, MoreHorizontal, Trash } from "lucide-react";
import { Document } from "@/types/table";

const iconSize = 16;
const iconStroke = 3;
const iconStyle = "cursor-pointer text-[#608F97]";

const generateSelect = <TData extends object>() => ({
  id: "select",
  cell: ({ row }: { row: Row<TData> }) => (
    <Checkbox
      id="select-one"
      checked={row.getIsSelected()}
      onClick={row.getToggleSelectedHandler()}
    />
  ),
  meta: {
    "text-align": "left",
  },
});

export const COLUMNS: (ColumnDef<Document, keyof Document> & {
  searchable?: boolean;
  accessorKey?: string;
})[] = [
  generateSelect(),
  {
    accessorKey: "title",
    searchable: true,
    cell: (props: CellContext<Document, Document["title"]>) => (
      <div className="hover:cursor-pointer">{props.getValue()}</div>
    ),
  },
  {
    accessorKey: "user",
    searchable: true,
    cell: (props: CellContext<Document, Document["user"]>) => (
      <div>by: {props.getValue()}</div>
    ),
  },
  {
    accessorKey: "created_at",
    searchable: true,
    cell: (props: CellContext<Document, Document["created_at"]>) => (
      <div>created: {props.getValue()}</div>
    ),
  },
  {
    accessorKey: "mergable",
    searchable: true,
    cell: (props: CellContext<Document, Document["mergable"]>) => (
      <div>{props.getValue()}</div>
    ),
  },
  {
    accessorKey: "options",
    cell: () => (
      <div className="w-full flex justify-end items-center">
        <div className="flex flex-row gap-2 items-center absolute right-0">
          <Download
            size={iconSize}
            strokeWidth={iconStroke}
            className={iconStyle}
          />
          <Trash
            size={iconSize}
            strokeWidth={iconStroke}
            className={iconStyle}
          />
          <Copy
            size={iconSize}
            strokeWidth={iconStroke}
            className={iconStyle}
          />
          <MoreHorizontal
            size={iconSize}
            strokeWidth={iconStroke}
            className={iconStyle}
          />
        </div>
      </div>
    ),
  },
];
