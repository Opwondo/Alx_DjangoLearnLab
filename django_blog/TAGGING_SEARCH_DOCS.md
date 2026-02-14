# Django Blog - Tagging and Search Functionality Documentation

## Overview
The tagging and search system enhances blog post discoverability through keyword-based categorization and content search. Users can tag posts with relevant keywords and search through posts using various criteria.

## Features

### 1. Tagging System

#### Adding Tags to Posts
- Tags can be added when creating or editing a post
- Enter tags as comma-separated values (e.g., "python, django, tutorial")
- Tags are automatically created if they don't exist
- Multiple posts can share the same tag

#### Viewing Posts by Tag
- Click on any tag link to see all posts with that tag
- URL pattern: `/tag/<tag_name>/`
- Shows paginated list of posts with the selected tag
- Current tag is highlighted in the tag list

### 2. Search Functionality

#### Search Bar
- Located in the header of every page
- Searches through:
  - Post titles
  - Post content
  - Post tags
- Case-insensitive search using Django Q objects

#### Search Results Page
- URL: `/search/?q=<query>`
- Displays matching posts with pagination
- Shows the search query in the header
- Maintains search query during pagination
- "No results" message with helpful suggestions

### 3. Related Posts
- Automatically shown on post detail pages
- Based on shared tags
- Limited to 5 related posts
- Excludes current post
- Provides content discovery beyond search

## Database Schema Updates

### Post Model Additions
```python
tags = TaggableManager()  # From django-taggit
