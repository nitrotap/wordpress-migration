This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

Let's begin with **Step 1: Extracting Data from the WordPress REST API** using Python.

---

## **Step 1: Pulling and Saving Data from WordPress API**

We will fetch **pages, posts, and SEO data** using Python and save it in JSON format for further processing.

### **1.1 Install Required Libraries**

Ensure you have `requests` installed:

```bash
pip install requests
```

### **1.2 Python Script to Fetch WordPress Data**

Create a script `fetch_wordpress_data.py` to retrieve **posts, pages, and SEO metadata** from the WordPress REST API.

```python
import requests
import json
import os

# WordPress API Base URL
WORDPRESS_SITE = "https://nitrotap.co"
API_BASE = f"{WORDPRESS_SITE}/wp-json/wp/v2"

# Directory to save data
DATA_DIR = "wordpress_data"
os.makedirs(DATA_DIR, exist_ok=True)


def fetch_data(endpoint, per_page=100):
    """
    Fetch paginated data from WordPress REST API.
    """
    all_data = []
    page = 1

    while True:
        url = f"{API_BASE}/{endpoint}?per_page={per_page}&page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            all_data.extend(data)
            page += 1
        else:
            print(f"Error fetching {endpoint, page}: {response.status_code}")
            break

    return all_data


def save_json(data, filename):
    """
    Save JSON data to a file.
    """
    with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def fetch_and_save():
    """
    Fetch all necessary WordPress data and save to JSON files.
    """
    print("Fetching posts...")
    posts = fetch_data("posts")
    save_json(posts, "posts.json")

    print("Fetching pages...")
    pages = fetch_data("pages")
    save_json(pages, "pages.json")

    print("Fetching SEO data (if using Yoast SEO)...")
    seo_data = fetch_data("yoast_indexable")  # Yoast SEO
    save_json(seo_data, "seo_data.json")

    print("Fetching categories...")
    categories = fetch_data("categories")
    save_json(categories, "categories.json")

    print("Fetching tags...")
    tags = fetch_data("tags")
    save_json(tags, "tags.json")

    print("Fetching media files...")
    media = fetch_data("media")
    save_json(media, "media.json")

    print("Fetching authors...")
    authors = fetch_data("users")
    save_json(authors, "authors.json")

    print("Fetching comments...")
    comments = fetch_data("comments")
    save_json(comments, "comments.json")

    print("Fetching custom fields (if using ACF)...")
    custom_fields = fetch_data("meta")  # ACF and custom metadata
    save_json(custom_fields, "custom_fields.json")

    print("Fetching redirects (if using Redirection plugin)...")
    redirects = fetch_data("redirection/v1/redirects")  # Redirection plugin API
    save_json(redirects, "redirects.json")

    print("Data extraction complete!")


if __name__ == "__main__":
    fetch_and_save()

```

---

### **1.3 Explanation of the Script**

- **`fetch_data(endpoint, per_page=100)`**
  - Retrieves paginated data from WordPress REST API.
  - Handles pagination automatically.
- **`save_json(data, filename)`**
  - Saves the retrieved data in a structured JSON file.
- **`fetch_and_save()`**
  - Fetches **posts, pages, and SEO metadata (Yoast SEO)**.
  - Saves them as `posts.json`, `pages.json`, and `seo_data.json`.
- **Runs on execution (`if __name__ == "__main__":`)**
  - Ensures the script runs when executed directly.

---

## **Step 2: Run the Script**

Execute the script:

```bash
python fetch_wordpress_data.py
```

This will create a directory `wordpress_data/` with:

- `posts.json`
- `pages.json`
- `seo_data.json` (if Yoast SEO is installed)

---

### **Next Step: Transform Data for PostgreSQL**

Now that we have WordPress content, we need to:

- **Normalize the data** for PostgreSQL.
- **Extract relevant fields** (title, content, meta, timestamps).
- **Prepare SQL schema** for the migration.

Great! Now that we've extracted data from the WordPress REST API, let's proceed with **Step 2: Transforming and Preparing Data for PostgreSQL**.

---

## **Step 2: Transforming and Preparing Data for PostgreSQL**

We'll:

1. **Extract relevant fields** from the JSON data.
2. **Normalize relationships** (e.g., posts with categories, tags, authors).
3. **Prepare SQL schema** for the database.
4. **Write Python scripts** to insert data into PostgreSQL.

---

### **2.1 Install PostgreSQL Dependencies**

Ensure you have `psycopg2` for connecting to PostgreSQL:

```bash
pip install psycopg2
```

---

### **2.2 Define PostgreSQL Schema**

We need a schema that captures:

- **Posts, Pages, Categories, Tags, Authors, Comments, Media, SEO data, and Redirects**.

#### **Schema (`schema.sql`)**

```sql
-- Drop existing tables if needed
DROP TABLE IF EXISTS posts, pages, categories, tags, authors, comments, media, seo_data, redirects CASCADE;

-- Authors Table
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    description TEXT,
    avatar_url TEXT
);

-- Categories Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE,
    description TEXT
);

-- Tags Table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE
);

-- Posts Table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    slug TEXT UNIQUE,
    excerpt TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_id INT REFERENCES authors(id),
    seo_title TEXT,
    seo_description TEXT
);

-- Posts-Categories Relationship Table (Many-to-Many)
CREATE TABLE post_categories (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, category_id)
);

-- Posts-Tags Relationship Table (Many-to-Many)
CREATE TABLE post_tags (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Pages Table
CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    slug TEXT UNIQUE,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seo_title TEXT,
    seo_description TEXT
);

-- Comments Table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    author_name TEXT,
    author_email TEXT,
    content TEXT NOT NULL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Media Table
CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT NOT NULL,
    mime_type TEXT
);

-- Redirects Table
CREATE TABLE redirects (
    id SERIAL PRIMARY KEY,
    old_url TEXT NOT NULL,
    new_url TEXT NOT NULL,
    status_code INT DEFAULT 301
);
```

#### **Apply Schema**

Run:

```bash
psql $DATABASE_URL -f schema.sql
```

---

### **2.3 Transform and Insert Data into PostgreSQL**

Now, let's write a **Python script** to:

1. **Parse the extracted JSON files**.
2. **Insert data into PostgreSQL**.

#### **`migrate_to_postgres.py`**

```python
# pip install psycopg2
import json
import psycopg2
import os

# Load database credentials from environment
DATABASE_URL ="postgres://neondb_owner:npg_DX8uEYZW4NHs@ep-muddy-mountain-a68kkmha-pooler.us-west-2.aws.neon.tech/neondb?sslmode=require"


# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Load JSON files
DATA_DIR = "wordpress_data"

def load_json(filename):
    """Load JSON data from a file."""
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as file:
        return json.load(file)

# Load data
posts = load_json("posts.json")
pages = load_json("pages.json")
categories = load_json("categories.json")
tags = load_json("tags.json")
authors = load_json("authors.json")
comments = load_json("comments.json")
media = load_json("media.json")
seo_data = load_json("seo_data.json")
redirects = load_json("redirects.json")


# Insert Authors
print("Inserting authors...")
for author in authors:
    email = author.get("email", None)  # Handle missing email

    cursor.execute("""
        INSERT INTO authors (id, name, username, email, description, avatar_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            username = EXCLUDED.username,
            description = EXCLUDED.description,
            avatar_url = EXCLUDED.avatar_url;
    """, (author["id"], author["name"], author["slug"], email,
          author.get("description", ""), author.get("avatar_urls", {}).get("96", "")))


# Insert Categories
print("Inserting categories...")
for category in categories:
    cursor.execute("""
        INSERT INTO categories (id, name, slug, description)
        VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, (category["id"], category["name"], category["slug"], category.get("description", "")))

# Insert Tags
print("Inserting tags...")
for tag in tags:
    cursor.execute("""
        INSERT INTO tags (id, name, slug)
        VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, (tag["id"], tag["name"], tag["slug"]))

# Insert Posts
print("Inserting posts...")
for post in posts:
    seo = next((s for s in seo_data if s["object_id"] == post["id"]), {})
    cursor.execute("""
        INSERT INTO posts (id, title, content, slug, excerpt, status, created_at, updated_at, author_id, seo_title, seo_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, (post["id"], post["title"]["rendered"], post["content"]["rendered"], post["slug"],
          post.get("excerpt", {}).get("rendered", ""), post["status"], post["date"], post["modified"], post["author"],
          seo.get("title", ""), seo.get("description", "")))

# Insert Pages
print("Inserting pages...")
for page in pages:
    seo = next((s for s in seo_data if s["object_id"] == page["id"]), {})
    cursor.execute("""
        INSERT INTO pages (id, title, content, slug, status, created_at, updated_at, seo_title, seo_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, (page["id"], page["title"]["rendered"], page["content"]["rendered"], page["slug"],
          page["status"], page["date"], page["modified"], seo.get("title", ""), seo.get("description", "")))

# Insert Comments
print("Inserting comments...")
for comment in comments:
    cursor.execute("""
        INSERT INTO comments (id, post_id, author_name, author_email, content, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, (comment["id"], comment["post"], comment["author_name"], comment["author_email"],
          comment["content"]["rendered"], comment["status"], comment["date"]))

# Insert Redirects
print("Inserting redirects...")
for redirect in redirects:
    cursor.execute("""
        INSERT INTO redirects (id, old_url, new_url, status_code)
        VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, (redirect["id"], redirect["source"], redirect["target"], redirect["code"]))

# Commit changes
conn.commit()
cursor.close()
conn.close()
print("Migration completed successfully!")
```

---

### **Next Step: Integrating with Next.js**

Now that we have our data in **PostgreSQL**, the next step is to **connect it to Next.js via an API route**.

Now that we have migrated the WordPress data into **PostgreSQL**, let's integrate it with **Next.js (App Router) using TypeScript**.

---

## **Step 3: Setting Up Next.js with App Router & TypeScript**
We'll:
1. **Initialize a Next.js project with TypeScript**.
2. **Set up a database connection to Vercel Postgres**.
3. **Create API routes to fetch data**.
4. **Create React components to display posts and pages**.

---

### **3.1 Initialize Next.js with TypeScript**
Run the following command to create a Next.js project:
```bash
npx create-next-app@latest wordpress-migration --typescript --experimental-app
cd wordpress-migration
```
Then install **PostgreSQL client**:
```bash
npm install pg
```

---

### **3.2 Configure Environment Variables**
Create a **`.env.local`** file and add the database connection:
```
DATABASE_URL=postgres://neondb_owner:npg_DX8uEYZW4NHs@ep-muddy-mountain-a68kkmha-pooler.us-west-2.aws.neon.tech/neondb?sslmode=require
```

---

### **3.3 Create Database Connection**
Inside **`lib/db.ts`**, create a helper to connect to PostgreSQL:
```typescript
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export async function query(text: string, params?: any[]) {
  const client = await pool.connect();
  try {
    const result = await client.query(text, params);
    return result.rows;
  } finally {
    client.release();
  }
}
```

---

### **3.4 Create API Routes**
Now, let's create **API routes** to fetch posts, pages, and SEO data.

#### **Get Posts API**
Create a file **`app/api/posts/route.ts`**:
```typescript
import { NextResponse } from "next/server";
import { query } from "@/lib/db";

export async function GET() {
  try {
    const posts = await query("SELECT * FROM posts ORDER BY created_at DESC");
    return NextResponse.json(posts);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch posts" }, { status: 500 });
  }
}
```

---

#### **Get Pages API**
Create **`app/api/pages/route.ts`**:
```typescript
import { NextResponse } from "next/server";
import { query } from "@/lib/db";

export async function GET() {
  try {
    const pages = await query("SELECT * FROM pages ORDER BY created_at DESC");
    return NextResponse.json(pages);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch pages" }, { status: 500 });
  }
}
```

---

#### **Get SEO Data API**
Create **`app/api/seo/route.ts`**:
```typescript
import { NextResponse } from "next/server";
import { query } from "@/lib/db";

export async function GET() {
  try {
    const seoData = await query("SELECT * FROM posts WHERE seo_title IS NOT NULL ORDER BY created_at DESC");
    return NextResponse.json(seoData);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch SEO data" }, { status: 500 });
  }
}
```

---

### **3.5 Create React Components for Displaying Data**
Now, let's create components to display **posts** and **pages**.

#### **Post List Component**
Create **`components/PostList.tsx`**:
```tsx
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
```

---

#### **Page List Component**
Create **`components/PageList.tsx`**:
```tsx
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
```

---

### **3.6 Display Posts and Pages in Next.js**
Modify **`app/page.tsx`** to show the components:
```tsx
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
```

---

### **3.7 Deploy to Vercel**
To deploy, run:
```bash
vercel
```

Ensure you **add environment variables** (`DATABASE_URL`) in Vercel.

---

## **Next Steps**
1. **Enhance SEO Handling**: Use `next-seo` to dynamically inject metadata.
2. **Improve Image Handling**: Upload media to Cloudinary or Vercel Blob Storage.
3. **Add a Search Feature**: Implement full-text search with PostgreSQL.
4. **Handle Authentication**: Use **NextAuth.js** if needed.

---

### ✅ **Migration Summary**
✔ Pulled **WordPress data** →  
✔ Transformed & Inserted into **PostgreSQL** →  
✔ Created **Next.js API Routes** →  
✔ Built **React Components** to display posts/pages →  
✔ **Deployed to Vercel** 🚀  


