from json.decoder import JSONDecoder
import requests


class Anime:

    TOKEN = 'X6nbfeLPhNdGZ8_uWn7PSSXFh4xkwxeT2P_igZUNjmo'

    def get_anime(self):
        headers = {
        'Authorization': 'bearer {0}'.format(self.TOKEN),
        }
        data = {
        'query': '''
        query {
            searchWorks(
                seasons: ["2021-summer"],
                orderBy: { field: WATCHERS_COUNT, direction: DESC }
            )   {
                edges {
                    node {
                        title
                        officialSiteUrl 
                        image {
                            recommendedImageUrl
                        }
                        casts {
                            edges {
                                node {
                                    character {
                                        name
                                    }
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        '''
        }
        response = requests.post('https://api.annict.com/graphql', headers=headers, data=data)
        json = response.json()
        for anime in json['data']['searchWorks']['edges']:
            print('タイトル: {0}'.format(anime['node']['title']))
            print('サイトURL: {0}'.format(anime['node']['officialSiteUrl']))
            print('画像URL: {0}'.format(anime['node']['image']['recommendedImageUrl']))
            for cast in anime['node']['casts']['edges']:
                print('{0}(CV. {1})'.format(cast['node']['character']['name'], cast['node']['name']))

            print('\n\n\n')
        
        print('process finished')



anime = Anime()
anime.get_anime()