=== PERMISSIONS TEST GUIDE ===

Test Users Created:
1. viewer / viewer123 (Viewers group)
2. editor / editor123 (Editors group)  
3. admin / admin123 (Admins group)

What each user can do:

VIEWER (viewer/viewer123):
- Can view book list
- Can view book details
- CANNOT: Add, Edit, or Delete books

EDITOR (editor/editor123):
- Can view book list
- Can view book details
- CAN: Add new books
- CAN: Edit existing books
- CANNOT: Delete books

ADMIN (admin/admin123):
- Can do everything: View, Add, Edit, Delete

Test URLs:
1. Book Management: http://127.0.0.1:8000/bookshelf/
2. Admin Panel: http://127.0.0.1:8000/admin/

To stop server: Press Ctrl+C in terminal where server is running
