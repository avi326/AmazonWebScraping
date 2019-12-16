# pip install mediawiki
"""
    this class get data from Wikipedia api.
"""

# import packages
from mediawiki import MediaWiki


class WikiAPI:
    def __init__(self):
        self.wikipedia = MediaWiki()

    def get_player_data(self, player_name):
        player_data = self.wikipedia.page(player_name)
        images = player_data.images
        categories = player_data.categories

        return images, categories
