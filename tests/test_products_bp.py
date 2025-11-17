import unittest
from app import app

class ProductsBPTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        # Перевіряємо, що продукти присутні
        self.assertIn("Ноутбук", response_text)
        self.assertIn("Смартфон", response_text)
        self.assertIn("Монітор", response_text)
        # Перевіряємо, що посилання на деталі продуктів правильні
        self.assertIn("/products/1", response_text)
        self.assertIn("/products/2", response_text)
        self.assertIn("/products/3", response_text)

    def test_product_detail_page_existing(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        self.assertIn("Ноутбук X1", response_text)
        self.assertIn("Потужний ігровий ноутбук", response_text)

        response2 = self.client.get("/products/2")
        self.assertEqual(response2.status_code, 200)
        response2_text = response2.data.decode("utf-8")
        self.assertIn("Смартфон Pro", response2_text)
        self.assertIn("Флагманський смартфон з 5G", response2_text)

    def test_product_detail_page_non_existing(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        self.assertIn("Продукт не знайдено", response_text)

if __name__ == "__main__":
    unittest.main()
