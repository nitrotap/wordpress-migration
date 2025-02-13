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
