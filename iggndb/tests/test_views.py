from .base import BaseTest


class MainTest(BaseTest):

    def test_index_page(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'index.html')



