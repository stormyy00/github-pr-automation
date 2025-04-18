import { NextRequest, NextResponse } from "next/server";

export const POST = async (req: NextRequest) => {
  const { name, organization } = await req.json();
  console.log(name, organization);
  try {
    // const response = await fetch(
    //   `https://api.github.com/search/repositories?q=${name}+org:${organization}`,
    //   {
    //     method: "GET",
    //     headers: {
    //       "Content-Type": "application/json",
    //       Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
    //     },
    //   }
    // );
    // if (!response.ok) {
    //   console.error(`Error: ${response.status}`);
    //   return NextResponse.json(
    //     { error: `Error: ${response.status}` },
    //     { status: 500 }
    //   );
    // }
    // const data = await response.json();
    // console.log(data)
    return NextResponse.json({ status: 200 });
  } catch {
    console.log("Error in search route");
    return NextResponse.json(
      { error: "Error in search route" },
      { status: 500 },
    );
  }
};
