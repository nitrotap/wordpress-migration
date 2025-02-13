import { NextResponse } from "next/server";
import { query } from "@/lib/db";

export async function GET() {
  try {
    const posts = await query("SELECT * FROM posts ORDER BY created_at DESC");
    return NextResponse.json(posts);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch posts" + error }, { status: 500 });
  }
}
