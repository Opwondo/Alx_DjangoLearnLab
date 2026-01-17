# Django Admin Integration for Book Model

1. Imported the `Book` model into `bookshelf/admin.py`.
2. Registered the model using `@admin.register(Book)` decorator.
3. Customized the admin interface with:
    - `list_display` to show `title`, `author`, and `publication_year`
    - `list_filter` for quick filtering by `author` and `publication_year`
    - `search_fields` for searching by `title` and `author`
4. Created a superuser with `python3 manage.py createsuperuser`.
5. Accessed the admin interface at `http://127.0.0.1:8000/admin/` to verify.
