# Explanation of the Script
# load_json(filename) → Loads JSON files from wordpress_data/.
# transform_posts(posts) → Extracts id, title, content, slug, date, modified from WordPress posts.
# transform_pages(pages) → Similar to posts, but for WordPress pages.
# transform_seo(seo_data) → Extracts Yoast SEO metadata, including title, description, and canonical URL.
# save_sql(statements, filename) → Saves SQL INSERT statements to a .sql file.
# main() → Orchestrates the process.
import json
import os

# Load JSON data
DATA_DIR = "wordpress_data"
OUTPUT_DIR = "sql_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_json(filename):
    """Load JSON data from a file."""
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as file:
        return json.load(file)


def transform_posts(posts):
    """Convert posts JSON to SQL INSERT statements."""
    sql_statements = []
    for post in posts:
        sql = f"""
        INSERT INTO posts (wp_id, title, content, slug, created_at, updated_at)
        VALUES (
            {post['id']}, 
            '{post['title']['rendered'].replace("'", "''")}', 
            '{post['content']['rendered'].replace("'", "''")}', 
            '{post['slug']}', 
            '{post['date']}',
            '{post['modified']}'
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())
    
    return sql_statements


def transform_pages(pages):
    """Convert pages JSON to SQL INSERT statements."""
    sql_statements = []
    for page in pages:
        sql = f"""
        INSERT INTO pages (wp_id, title, content, slug, created_at, updated_at)
        VALUES (
            {page['id']}, 
            '{page['title']['rendered'].replace("'", "''")}', 
            '{page['content']['rendered'].replace("'", "''")}', 
            '{page['slug']}', 
            '{page['date']}',
            '{page['modified']}'
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def transform_seo(seo_data):
    """Convert SEO metadata JSON to SQL INSERT statements."""
    sql_statements = []
    for item in seo_data:
        sql = f"""
        INSERT INTO seo_metadata (wp_id, post_type, meta_title, meta_description, focus_keyword, canonical_url)
        VALUES (
            {item['id']}, 
            '{item['object_sub_type']}', 
            '{item.get('title', '').replace("'", "''")}', 
            '{item.get('description', '').replace("'", "''")}', 
            '{item.get('focus_keyword', '').replace("'", "''")}', 
            '{item.get('canonical', '')}'
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def save_sql(statements, filename):
    """Save SQL statements to a file."""
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as file:
        file.write("\n".join(statements))
    print(f"Saved SQL to {filename}")


def main():
    print("Loading WordPress data...")
    posts = load_json("posts.json")
    pages = load_json("pages.json")
    seo_data = load_json("seo_data.json")

    print("Transforming data...")
    post_sql = transform_posts(posts)
    page_sql = transform_pages(pages)
    seo_sql = transform_seo(seo_data)

    print("Saving SQL files...")
    save_sql(post_sql, "posts.sql")
    save_sql(page_sql, "pages.sql")
    save_sql(seo_sql, "seo_metadata.sql")

    print("Data transformation complete!")


if __name__ == "__main__":
    main()
