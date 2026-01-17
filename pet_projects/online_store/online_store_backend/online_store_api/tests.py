# Тести не встиг доробити

# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.contrib.auth import get_user_model
#
# from online_store_app.models import Product, Category
#
# User = get_user_model()
#
#
# class RecommendationAPITest(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#
#         self.user = User.objects.create_user(
#             email="test@test.com",
#             password="123456"
#         )
#
#         category = Category.objects.create(
#             name="Test",
#             slug="test"
#         )
#
#         self.product1 = Product.objects.create(
#             title="Product 1",
#             description="Desc",
#             category=category
#         )
#
#         self.product2 = Product.objects.create(
#             title="Product 2",
#             description="Desc",
#             category=category
#         )
#
#         self.client.force_authenticate(user=self.user)
#
#     def test_recommendations_returns_products(self):
#         response = self.client.get("/recommendations/")
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 2)
