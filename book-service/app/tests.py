from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Publisher, Author, Book, BookAuthor, BookInventory, BookMedia


class BookServiceAPITests(APITestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="O'Reilly", address="1005 Gravenstein Hwy N")
        self.author = Author.objects.create(name="Jane Doe", bio="Tech author")
        self.book = Book.objects.create(
            sku="BK-001",
            title="Python Microservices",
            description="Build microservices with Django",
            isbn="9783161484100",
            language="en",
            publisher=self.publisher,
        )
        self.book_author = BookAuthor.objects.create(book=self.book, author=self.author)
        self.inventory = BookInventory.objects.create(book=self.book, stock_qty=50, reserved_qty=0, low_stock_threshold=5)
        self.media = BookMedia.objects.create(book=self.book, file_url="http://example.com/book.pdf", type="ebook")

    def test_health_check(self):
        url = reverse('book_health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('service', response.json())

    def test_publisher_crud(self):
        list_url = reverse('publisher-list-create')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        create_resp = self.client.post(list_url, {'name': 'Packt', 'address': '123 Publishing Lane', 'contact': 'support@packt.com'})
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        publisher_id = create_resp.data['id']

        detail_url = reverse('publisher-detail', kwargs={'pk': publisher_id})
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)

        patch_resp = self.client.patch(detail_url, {'contact': 'hello@packt.com'}, format='json')
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)

        delete_resp = self.client.delete(detail_url)
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_author_crud(self):
        list_url = reverse('author-list-create')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        create_resp = self.client.post(list_url, {'name': 'John Smith', 'bio': 'Author bio'})
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        author_id = create_resp.data['id']

        detail_url = reverse('author-detail', kwargs={'pk': author_id})
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)

    def test_book_crud_and_query(self):
        list_url = reverse('book-list-create')
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        create_resp = self.client.post(list_url, {
            'sku': 'BK-002',
            'title': 'Django for Professionals',
            'description': 'Advanced Django patterns',
            'isbn': '1234567890123',
            'publisher': self.publisher.id,
            'language': 'en',
        })
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        book_id = create_resp.data['id']

        detail_url = reverse('book-detail', kwargs={'pk': book_id})
        book_resp = self.client.get(detail_url)
        self.assertEqual(book_resp.status_code, status.HTTP_200_OK)

        filter_resp = self.client.get(list_url, {'search': 'Django'})
        self.assertEqual(filter_resp.status_code, status.HTTP_200_OK)

    def test_inventory_kits(self):
        list_url = reverse('inventory-list-create')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        create_resp = self.client.post(list_url, {'book': self.book.id, 'stock_qty': 30, 'reserved_qty': 2, 'low_stock_threshold': 5})
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        inv_id = create_resp.data['id']

        detail_url = reverse('inventory-detail', kwargs={'pk': inv_id})
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)

    def test_media_crud(self):
        list_url = reverse('bookmedia-list-create')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        create_resp = self.client.post(list_url, {'book': self.book.id, 'file_url': 'http://example.com/cover.jpg', 'type': 'cover', 'caption': 'Front cover'})
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        media_id = create_resp.data['id']

        detail_url = reverse('bookmedia-detail', kwargs={'pk': media_id})
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
