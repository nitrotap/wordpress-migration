# pip install requests
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


def extract_seo_data(item):
    """
    Extracts relevant SEO metadata from a post or page.
    """
    seo = item.get("yoast_head_json", {})

    # Handle og_image field, which might be a list
    og_image = seo.get("og_image", [])
    if isinstance(og_image, list) and len(og_image) > 0:
        og_image_url = og_image[0].get("url", "")
    elif isinstance(og_image, dict):
        og_image_url = og_image.get("url", "")
    else:
        og_image_url = ""

    return {
        "post_id": item["id"],
        "slug": item["slug"],
        "title": seo.get("title", item["title"]["rendered"]),
        "meta_description": seo.get("description", ""),
        "canonical_url": seo.get("canonical", ""),
        "og_title": seo.get("og_title", ""),
        "og_description": seo.get("og_description", ""),
        "og_image": og_image_url,
        "twitter_card": seo.get("twitter_card", ""),
        "schema": seo.get("schema", {}),
    }


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

    print("Extracting SEO data from posts and pages...")
    seo_data = [extract_seo_data(post) for post in posts] + [
        extract_seo_data(page) for page in pages
    ]
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
