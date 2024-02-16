from django.test import TestCase
from django.urls import reverse

class RecipeURLsTest(TestCase):
    def test_recipe_category_url_is_correct():
        url = reverse('recipes:category', kwargs={'category_id':1})
        self.assertEqual(url, '/recipes/category/1/')


    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
        self.fail(url)

# RED - GREEN - REFACTOR