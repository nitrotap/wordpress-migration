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
