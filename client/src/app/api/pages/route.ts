import { NextResponse } from "next/server";
import { query } from "@/lib/db";

export async function GET() {
  try {
    const pages = await query("SELECT * FROM pages ORDER BY created_at DESC");
    return NextResponse.json(pages);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch pages" + error }, { status: 500 });
  }
}
