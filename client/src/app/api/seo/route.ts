import { NextResponse } from "next/server";
import { query } from "@/lib/db";

export async function GET() {
  try {
    const seoData = await query("SELECT * FROM posts WHERE seo_title IS NOT NULL ORDER BY created_at DESC");
    return NextResponse.json(seoData);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch SEO data" + error }, { status: 500 });
  }
}
