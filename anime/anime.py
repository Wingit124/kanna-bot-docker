import requests
import discord
import urllib.parse
from discord import embeds


class Anime:

    TOKEN = 'X6nbfeLPhNdGZ8_uWn7PSSXFh4xkwxeT2P_igZUNjmo'
    json = ''

    def get_anime_by_title(self, title):
        query = {
                'access_token': self.TOKEN,
                'filter_title': title
                }
        query = urllib.parse.urlencode(query)
        response = requests.get('https://api.annict.com/v1/works?' + query)
        self.json = response.json()
        work = self.json['works'][0]
        title = work['title'] or ''
        title_en = work['title_en'] or ''
        media_text = work['media_text'] or ''
        official_site_url = work['official_site_url'] or ''
        wikipedia_url = work['wikipedia_url'] or ''
        twitter_username = work['twitter_username'] or ''
        recommended_url = work['images']['recommended_url'] or ''
        episodes_count = work['episodes_count'] or ''
        season_name_text = work['season_name_text'] or ''

        embed = discord.Embed(title=title, description=title_en)
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
        
        return embed
