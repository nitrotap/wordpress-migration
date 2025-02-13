import requests



import requests
import json
import os

# WordPress API Base URL
WORDPRESS_SITE = "https://yourdomain.com"
API_BASE = f"{WORDPRESS_SITE}/wp-json/wp/v2"

# Directory to save data
DATA_DIR = "wordpress_data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_data(endpoint, per_page=100):
    """
    Fetch paginated data from WordPress REST API with error handling.
    """
    all_data = []
    page = 1

    while True:
        url = f"{API_BASE}/{endpoint}?per_page={per_page}&page={page}"
        print(f"Fetching: {url}")  # Debugging info
        response = requests.get(url)

        # Check for HTTP errors
        if response.status_code != 200:
            print(f"Error fetching {endpoint}: HTTP {response.status_code} - {response.text}")
            break

        # Handle empty response
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Unable to decode JSON for {endpoint}. Response content: {response.text}")
            break

        if not data:
            print(f"No more data for {endpoint}. Stopping pagination.")
            break

        all_data.extend(data)
        page += 1

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
