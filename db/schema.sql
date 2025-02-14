DROP TABLE IF EXISTS authors, categories, comments, custom_fields, media, post_categories, post_tags, posts, redirects, seo_data, tags CASCADE;

-- Create the posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, 
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    excerpt TEXT,
    status TEXT,
    author_id INT,
    featured_media INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a trigger function to update `updated_at`
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to posts table
CREATE TRIGGER trigger_update_timestamp
BEFORE UPDATE ON posts
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    slug TEXT NOT NULL,
    status TEXT,
    author_id INT,
    parent_id INT,
    menu_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a trigger function to update `updated_at`
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to pages table
CREATE TRIGGER trigger_update_timestamp
BEFORE UPDATE ON pages
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Create the SEO metadata table
CREATE TABLE seo_data (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(wp_id) ON DELETE CASCADE UNIQUE,  -- Add UNIQUE constraint
    title TEXT,
    meta_description TEXT,
    canonical_url TEXT,
    og_title TEXT,
    og_description TEXT,
    og_image TEXT,
    twitter_card TEXT,
    schema JSONB -- Store structured schema data in JSONB format
);


-- Create the categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, -- WordPress category ID
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    description TEXT
);

-- Create the tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, -- WordPress tag ID
    name TEXT NOT NULL,
    slug TEXT NOT NULL
);

-- Create the media table
CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, -- WordPress media ID
    post_id INT REFERENCES posts(wp_id) ON DELETE SET NULL,
    url TEXT NOT NULL,
    alt_text TEXT,
    mime_type TEXT
);

-- Create the authors table
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, -- WordPress author ID
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    bio TEXT
);


-- Create the comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, -- WordPress comment ID
    post_id INT REFERENCES posts(wp_id) ON DELETE CASCADE,
    author_name TEXT,
    author_email TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the custom fields table
CREATE TABLE custom_fields (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(wp_id) ON DELETE CASCADE,
    field_name TEXT NOT NULL,
    field_value TEXT
);

-- Create the redirects table (if using Redirection plugin)
CREATE TABLE redirects (
    id SERIAL PRIMARY KEY,
    wp_id INT UNIQUE NOT NULL, -- WordPress redirect ID
    source_url TEXT NOT NULL,
    target_url TEXT NOT NULL,
    http_code INT DEFAULT 301
);

-- Create many-to-many relationships for categories & tags
CREATE TABLE post_categories (
    post_id INT REFERENCES posts(wp_id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(wp_id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, category_id)
);

CREATE TABLE post_tags (
    post_id INT REFERENCES posts(wp_id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(wp_id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
