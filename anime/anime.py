from typing import Counter
from discord.embeds import Embed
import requests
import urllib.parse


class Anime:

    TOKEN: str = 'X6nbfeLPhNdGZ8_uWn7PSSXFh4xkwxeT2P_igZUNjmo'

    filter_title: str
    prev_page: int
    next_page: int
    total_count: int
    output_embed: Embed

    def __init__(self, filter_title):
        self.filter_title = filter_title
    
    def get_anime(self, page=1):
        query = {
                'access_token': self.TOKEN,
                'filter_title': self.filter_title,
                'per_page': 1,
                'page': page,
                'sort_season': 'asc'
                }
        query = urllib.parse.urlencode(query)
        response = requests.get('https://api.annict.com/v1/works?' + query)
        json = response.json()
        if json['total_count'] == 0:
            self.output_embed = Embed(title='作品が見つからなかったよ', color=0xff0000)
            return False
        
        work = json['works'][0]
        title = work.get('title') or ''
        title_en = work.get('title_en') or ''
        media_text = work.get('media_text') or ''
        official_site_url = work.get('official_site_url') or ''
        wikipedia_url = work.get('wikipedia_url') or ''
        twitter_username = work.get('twitter_username') or ''
        recommended_url = work.get('images').get('recommended_url') or ''
        episodes_count = work.get('episodes_count') or ''
        season_name_text = work.get('season_name_text') or ''
        self.total_count = json.get('total_count') or ''
        self.prev_page = json.get('prev_page')
        self.next_page = json.get('next_page')

        embed: Embed = Embed(title=title, description=title_en, color=0x00ff00)
        if official_site_url:
            embed.add_field(name='公式サイト', value='[こちら]({0})'.format(official_site_url), inline=True)
        if wikipedia_url:
            embed.add_field(name='Wikipedia', value='[こちら]({0})'.format(wikipedia_url), inline=True)
        if twitter_username:
            embed.add_field(name='Twitter', value='[@{0}](https://twitter.com/{0})'.format(twitter_username), inline=True)
        if episodes_count:
            embed.add_field(name='エピソード数', value='全{0}話'.format(episodes_count), inline=True)
        if season_name_text:
            embed.add_field(name='シーズン', value=season_name_text, inline=True)
        if media_text:
            embed.add_field(name='種別', value=media_text, inline=True)
        if recommended_url:
            embed.set_image(url=recommended_url)
        if self.total_count:
            embed.set_footer(text='Current page {0} of {1}'.format(page, self.total_count))
        
        self.output_embed = embed
        return True
