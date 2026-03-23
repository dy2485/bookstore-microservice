# Book Service Completion

This service is now fully implemented with REST endpoints and tests.

## Available endpoints (all under `/api/`)
- `GET /api/health/`

Publishers
- `GET /api/publishers/`
- `POST /api/publishers/`
- `GET /api/publishers/{id}/`
- `PUT/PATCH /api/publishers/{id}/`
- `DELETE /api/publishers/{id}/`

Authors
- `GET /api/authors/`
- `POST /api/authors/`
- `GET /api/authors/{id}/`
- `PUT/PATCH /api/authors/{id}/`
- `DELETE /api/authors/{id}/`

Books
- `GET /api/books/` (supports `search`, `ordering`, `publisher`, `author` filters)
- `POST /api/books/`
- `GET /api/books/{id}/`
- `PUT/PATCH /api/books/{id}/`
- `DELETE /api/books/{id}/`

Book authors mapping
- `GET /api/book-authors/`
- `POST /api/book-authors/`
- `GET /api/book-authors/{id}/`
- `DELETE /api/book-authors/{id}/`

Inventory
- `GET /api/inventories/`
- `POST /api/inventories/`
- `GET /api/inventories/{id}/`
- `PUT/PATCH /api/inventories/{id}/`
- `DELETE /api/inventories/{id}/`

Media
- `GET /api/media/`
- `POST /api/media/`
- `GET /api/media/{id}/`
- `PUT/PATCH /api/media/{id}/`
- `DELETE /api/media/{id}/`
