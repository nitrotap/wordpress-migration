import json
import os

# Load JSON data
DATA_DIR = "wordpress_data"
OUTPUT_DIR = "sql_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_json(filename):
    """Load JSON data from a file."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def escape(value):
    """Escape single quotes in SQL strings and handle None values."""
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"

def transform_posts(posts):
    """Convert posts JSON to SQL INSERT statements."""
    sql_statements = []
    for post in posts:
        sql = f"""
        INSERT INTO posts (wp_id, title, content, slug, status, author_id, featured_media, created_at, updated_at)
        VALUES (
            {post['id']}, 
            {escape(post['title']['rendered'])}, 
            {escape(post['content']['rendered'])}, 
            {escape(post['slug'])}, 
            {escape(post.get('status', 'publish'))},
            {post.get('author', 'NULL')}, 
            {post.get('featured_media', 'NULL')}, 
            {escape(post['date'])},
            {escape(post['modified'])}
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())
    
    return sql_statements


def transform_seo(seo_data, existing_post_ids):
    """Convert SEO metadata JSON to SQL INSERT statements only for existing posts."""
    sql_statements = []
    for item in seo_data:
        if item['post_id'] not in existing_post_ids:
            print(f"Skipping SEO data for missing post_id: {item['post_id']}")  # Debugging output
            continue  # Skip inserting SEO data for posts that do not exist

        sql = f"""
        INSERT INTO seo_data (post_id, title, meta_description, canonical_url, og_title, og_description, og_image, twitter_card, schema)
        VALUES (
            {item['post_id']}, 
            {escape(item.get('title', ''))}, 
            {escape(item.get('meta_description', ''))}, 
            {escape(item.get('canonical_url', ''))}, 
            {escape(item.get('og_title', ''))}, 
            {escape(item.get('og_description', ''))}, 
            {escape(item.get('og_image', ''))}, 
            {escape(item.get('twitter_card', ''))}, 
            {escape(json.dumps(item.get('schema', {})))}
        ) 
        ON CONFLICT (post_id) DO UPDATE 
        SET title = EXCLUDED.title,
            meta_description = EXCLUDED.meta_description,
            canonical_url = EXCLUDED.canonical_url,
            og_title = EXCLUDED.og_title,
            og_description = EXCLUDED.og_description,
            og_image = EXCLUDED.og_image,
            twitter_card = EXCLUDED.twitter_card,
            schema = EXCLUDED.schema;
        """
        sql_statements.append(sql.strip())

    return sql_statements



def transform_categories(categories):
    """Convert categories JSON to SQL INSERT statements."""
    sql_statements = []
    for category in categories:
        sql = f"""
        INSERT INTO categories (wp_id, name, slug, description)
        VALUES (
            {category['id']}, 
            {escape(category['name'])}, 
            {escape(category['slug'])}, 
            {escape(category.get('description', ''))}
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def transform_tags(tags):
    """Convert tags JSON to SQL INSERT statements."""
    sql_statements = []
    for tag in tags:
        sql = f"""
        INSERT INTO tags (wp_id, name, slug)
        VALUES (
            {tag['id']}, 
            {escape(tag['name'])}, 
            {escape(tag['slug'])}
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def transform_media(media, existing_post_ids):
    """Convert media JSON to SQL INSERT statements, ensuring referenced post exists."""
    sql_statements = []
    for item in media:
        post_id = item.get('post', None)

        # If post_id exists but is not in the database, skip it
        if post_id and post_id not in existing_post_ids:
            print(f"⚠️ Skipping media entry {item['id']} (post_id {post_id} not found)")
            continue

        # Convert None values to NULL for SQL compatibility
        post_id_sql = "NULL" if post_id is None else str(post_id)

        sql = f"""
        INSERT INTO media (wp_id, post_id, url, alt_text, mime_type)
        VALUES (
            {item['id']}, 
            {post_id_sql}, 
            {escape(item['source_url'])}, 
            {escape(item.get('alt_text', ''))}, 
            {escape(item.get('mime_type', ''))}
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements



def transform_authors(authors):
    """Convert authors JSON to SQL INSERT statements."""
    sql_statements = []
    for author in authors:
        sql = f"""
        INSERT INTO authors (wp_id, name, username, email, bio)
        VALUES (
            {author['id']}, 
            {escape(author['name'])}, 
            {escape(author['slug'])}, 
            {escape(author.get('email', ''))}, 
            {escape(author.get('description', ''))}
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def transform_comments(comments):
    """Convert comments JSON to SQL INSERT statements."""
    sql_statements = []
    for comment in comments:
        sql = f"""
        INSERT INTO comments (wp_id, post_id, author_name, author_email, content, created_at)
        VALUES (
            {comment['id']}, 
            {comment.get('post', 'NULL')}, 
            {escape(comment.get('author_name', ''))}, 
            {escape(comment.get('author_email', ''))}, 
            {escape(comment.get('content', {}).get('rendered', ''))}, 
            {escape(comment['date'])}
        ) ON CONFLICT (wp_id) DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def transform_custom_fields(custom_fields):
    """Convert custom fields JSON to SQL INSERT statements."""
    sql_statements = []
    for field in custom_fields:
        sql = f"""
        INSERT INTO custom_fields (post_id, field_name, field_value)
        VALUES (
            {field.get('post', 'NULL')}, 
            {escape(field['key'])}, 
            {escape(field['value'])}
        ) ON CONFLICT DO NOTHING;
        """
        sql_statements.append(sql.strip())

    return sql_statements


def transform_redirects(redirects):
    """Convert redirects JSON to SQL INSERT statements."""
    sql_statements = []
    for redirect in redirects:
        sql = f"""
        INSERT INTO redirects (wp_id, source_url, target_url, http_code)
        VALUES (
            {redirect['id']}, 
            {escape(redirect['source'])}, 
            {escape(redirect['target'])}, 
            {redirect.get('code', 301)}
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
    seo_data = load_json("seo_data.json")
    categories = load_json("categories.json")
    tags = load_json("tags.json")
    media = load_json("media.json")
    authors = load_json("authors.json")
    comments = load_json("comments.json")
    custom_fields = load_json("custom_fields.json")
    redirects = load_json("redirects.json")

    print("Transforming data...")
    post_sql = transform_posts(posts)

    # Fetch existing post IDs before inserting SEO data and media
    existing_post_ids = {post['id'] for post in posts}  # Extract all post wp_ids

    seo_sql = transform_seo(seo_data, existing_post_ids)  # Pass existing_post_ids
    media_sql = transform_media(media, existing_post_ids)  # Pass existing_post_ids

    category_sql = transform_categories(categories)
    tag_sql = transform_tags(tags)
    author_sql = transform_authors(authors)
    comment_sql = transform_comments(comments)
    custom_field_sql = transform_custom_fields(custom_fields)
    redirect_sql = transform_redirects(redirects)

    print("Saving SQL files...")
    save_sql(post_sql, "posts.sql")
    save_sql(seo_sql, "seo_data.sql")
    save_sql(category_sql, "categories.sql")
    save_sql(tag_sql, "tags.sql")
    save_sql(media_sql, "media.sql")
    save_sql(author_sql, "authors.sql")
    save_sql(comment_sql, "comments.sql")
    save_sql(custom_field_sql, "custom_fields.sql")
    save_sql(redirect_sql, "redirects.sql")

    print("Data transformation complete!")


if __name__ == "__main__":
    main()
