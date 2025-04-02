import { NextResponse } from "next/server";

export const GET = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/health", {
      mode: "cors",
    });
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
