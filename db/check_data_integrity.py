import json
import os
from collections import Counter

# Directory containing extracted JSON data
DATA_DIR = "wordpress_data"


def load_json(filename):
    """Load JSON data from a file."""
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as file:
        return json.load(file)


# Load extracted data
authors = load_json("authors.json")
posts = load_json("posts.json")
pages = load_json("pages.json")
categories = load_json("categories.json")
tags = load_json("tags.json")
comments = load_json("comments.json")
redirects = load_json("redirects.json")


# Function to check for duplicates in a list of values
def find_duplicates(values):
    return [item for item, count in Counter(values).items() if count > 1]


# Check for duplicate or missing author emails
print("\nChecking Authors...")
emails = [author.get("email", None) for author in authors if author.get("email")]
duplicates = find_duplicates(emails)
if duplicates:
    print(f"⚠️  Duplicate emails found: {duplicates}")
else:
    print("✅ No duplicate emails.")

# Check for duplicate post and page slugs
print("\nChecking Posts and Pages...")
post_slugs = [post["slug"] for post in posts]
page_slugs = [page["slug"] for page in pages]
all_slugs = post_slugs + page_slugs
duplicates = find_duplicates(all_slugs)
if duplicates:
    print(f"⚠️  Duplicate slugs found: {duplicates}")
else:
    print("✅ No duplicate slugs.")

# Check for duplicate category and tag slugs
print("\nChecking Categories and Tags...")
category_slugs = [cat["slug"] for cat in categories]
tag_slugs = [tag["slug"] for tag in tags]
duplicates = find_duplicates(category_slugs + tag_slugs)
if duplicates:
    print(f"⚠️  Duplicate category/tag slugs found: {duplicates}")
else:
    print("✅ No duplicate category/tag slugs.")

# Check for comments linked to non-existent posts
print("\nChecking Comments...")
post_ids = {post["id"] for post in posts}  # Set for quick lookup
orphaned_comments = [
    comment["id"] for comment in comments if comment["post"] not in post_ids
]
if orphaned_comments:
    print(f"⚠️  Comments linked to missing posts: {orphaned_comments}")
else:
    print("✅ No orphaned comments.")

# Check for duplicate redirects
print("\nChecking Redirects...")
old_urls = [redirect["source"] for redirect in redirects]
duplicates = find_duplicates(old_urls)
if duplicates:
    print(f"⚠️  Duplicate redirects found for old URLs: {duplicates}")
else:
    print("✅ No duplicate redirects.")

print("\n✅ Data Integrity Check Complete!")
