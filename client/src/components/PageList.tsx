"use client";

import { useEffect, useState } from "react";

interface Page {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

export default function PageList() {
  const [pages, setPages] = useState<Page[]>([]);

  useEffect(() => {
    fetch("/api/pages")
      .then((res) => res.json())
      .then((data) => setPages(data));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Website Pages</h1>
      {pages.map((page) => (
        <article key={page.id} className="border p-4 my-2 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold">{page.title}</h2>
          <p className="text-gray-600">{new Date(page.created_at).toLocaleDateString()}</p>
          <div dangerouslySetInnerHTML={{ __html: page.content }} />
        </article>
      ))}
    </div>
  );
}
