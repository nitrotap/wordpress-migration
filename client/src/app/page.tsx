import PostList from "@/components/PostList";
import PageList from "@/components/PageList";

export default function Home() {
  return (
    <main className="p-6">
      <h1 className="text-3xl font-bold">WordPress to Next.js Migration</h1>
      <PostList />
      <PageList />
    </main>
  );
}
