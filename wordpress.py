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
    Fetch paginated data from WordPress REST API
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
            print(f"Error fetching {endpoint}: {response.status_code}")
            break

    return all_data


def save_json(data, filename):
    """
    Save JSON data to a file
    """
    with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def fetch_and_save():
    """
    Fetch posts, pages, and SEO metadata and save them
    """
    print("Fetching posts...")
    posts = fetch_data("posts")
    save_json(posts, "posts.json")

    print("Fetching pages...")
    pages = fetch_data("pages")
    save_json(pages, "pages.json")

    print("Fetching SEO data (if using Yoast SEO)...")
    seo_data = fetch_data("yoast_indexable")  # For Yoast SEO
    save_json(seo_data, "seo_data.json")

    print("Data saved successfully!")


if __name__ == "__main__":
    fetch_and_save()
