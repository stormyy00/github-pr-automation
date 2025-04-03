import { NextResponse, NextRequest } from "next/server";

export const POST = async (req: NextRequest) => {
  const { id } = await req.json();
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/merge-pr/${id}`,
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    return NextResponse.json({ item: data });
  } catch (error) {
    console.error("Error fetching data:", error);
    return NextResponse.json(
      { error: "Failed to fetch data" },
      { status: 500 },
    );
  }
};
