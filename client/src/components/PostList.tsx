"use client";

import { useEffect, useState } from "react";

interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

export default function PostList() {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    fetch("/api/posts")
      .then((res) => res.json())
      .then((data) => setPosts(data));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Latest Posts</h1>
      {posts.map((post) => (
        <article key={post.id} className="border p-4 my-2 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold">{post.title}</h2>
          <p className="text-gray-600">{new Date(post.created_at).toLocaleDateString()}</p>
          <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </article>
      ))}
    </div>
  );
}
