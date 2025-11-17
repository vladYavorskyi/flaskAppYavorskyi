import unittest
from app import create_app

class ProductsBPTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_product_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        self.assertIn("Ноутбук", response_text)
        self.assertIn("Смартфон", response_text)
        self.assertIn("Монітор", response_text)
        self.assertIn("/products/1", response_text)
        self.assertIn("/products/2", response_text)
        self.assertIn("/products/3", response_text)

    def test_product_detail_page_existing(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        self.assertIn("Ноутбук Hewlett-Packard", response_text)
        self.assertIn("Потужний ігровий ноутбук Hewlett-Packard", response_text)

    def test_product_detail_page_non_existing(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)
        response_text = response.data.decode("utf-8")
        self.assertIn("Продукт не знайдено", response_text)

if __name__ == "__main__":
    unittest.main()
