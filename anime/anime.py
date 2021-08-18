import requests
import discord
from anime.const import Const
from discord import embeds


class Anime:

    TOKEN = 'X6nbfeLPhNdGZ8_uWn7PSSXFh4xkwxeT2P_igZUNjmo'

    def get_anime_by_title(self, title):
        headers = {
        'Authorization': 'bearer {0}'.format(self.TOKEN),
        }
        data = {
        'query': Const.query_by_title % (title)
        }
        response = requests.post('https://api.annict.com/graphql', headers=headers, data=data)
        json = response.json()
        node = json['data']['searchWorks']['edges'][0]['node']
        embed = discord.Embed(title = node['title'], url = node['officialSiteUrl'])
        embed.set_thumbnail(url=node['image']['recommendedImageUrl'] or '')
        for cast in node['casts']['edges']:
            embed.add_field(name=cast['node']['character']['name'], value=cast['node']['name'], inline=True)

        #for anime in json['data']['searchWorks']['edges']:
            #print('タイトル: {0}'.format(anime['node']['title']))
            #print('サイトURL: {0}'.format(anime['node']['officialSiteUrl']))
            #print('画像URL: {0}'.format(anime['node']['image']['recommendedImageUrl'] or ''))
            #for cast in anime['node']['casts']['edges']:
                #print('{0}(CV. {1})'.format(cast['node']['character']['name'], cast['node']['name']))

            #print('\n\n\n')

        return embed
