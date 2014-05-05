from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
	def setUp(self):
		User.objects.create_user(username='bob', email='bob@bob.bob', password='bob')

	def test_user_creation(self):
		"""Tests the existence of created accounts"""
		self.assertEqual(User.objects.filter(username='bob').count(), 1)
		user = User.objects.get(username='bob')
		self.assertIsNotNone(user)


"""
Manual test plan for form validation

- Go to the users/signup page
- Enter random text into the textboxes
- Ensure that only valid input is accepted

- Go to the users/login page
- Enter random text into the textboxes
- Ensure that only valid input is accepted


"""