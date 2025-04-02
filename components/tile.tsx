import { MoreHorizontal } from "lucide-react";
import { Card, CardContent } from "./ui/card";
// import { Avatar, AvatarFallback } from "./components/ui/avatar";
import { Button } from "./ui/button";
import Link from "next/link";

type TileProps = {
  name: string;
  date: string;
  image: string;
};

const Tile = ({ name, date }: TileProps) => {
  return (
    <Card className="hover:shadow-md transition-shadow duration-200 w-full bg-[#EEF2F4] mt-2">
      <CardContent className="py-1.5 px-2">
        <div className="flex justify-between items-center w-full mb-3">
          <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-cyan-100 text-cyan-600">
            default
          </span>
          <Button variant="ghost" size="icon" className="h-6 w-6 -mr-1">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex justify-between items-end w-full gap-3">
          {/* <Avatar className="w-10 h-10 mb-1 bg-blue-800">
            <AvatarFallback className="text-black text-lg font-medium">
              {image}
            </AvatarFallback>
          </Avatar> */}
          <div className="flex flex-col justify-center items-start gap-1">
            <Link
              href={"/"}
              className="font-medium hover:text-cyan-400 duration-300"
            >
              {name}
            </Link>
            <p className="text-gray-400 text-xs">{date}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default Tile;
