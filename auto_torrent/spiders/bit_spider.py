import scrapy
import re
import transmissionrpc
import pdb
from auto_torrent.items import PirateItem



class PirateSpider(scrapy.Spider):
    name = 'pirate'

    def __init__(self, base_url='https://kat.cr/usearch/',
               search_term='family guy', season='14', episode='13'):
        self.base_url = base_url
        self.season = season
        self.episode = episode
        self.search_term = search_term
        self.start_urls = [self.base_url + self.search_term + ' ' + self.format_search_term(self.season, self.episode)]

    def parse(self, response):
        header = True
        for sel in response.xpath('//tr'):

            # skip header
            if header:
                header = False
                continue
            # create new item
            item = PirateItem()

            # get magnet link
            icons = sel.xpath('.//a[@class="icon16"]//@href').extract()
            magnet_link = ''
            for link in icons:
                if re.match('magnet', link):
                    magnet_link = link
            if magnet_link:
                item['magnet_link'] = str(magnet_link)

            # get title
            title = sel.xpath('.//a[@class="cellMainLink"]//@href').extract()
            if title:
                item['title'] = str(title)

            # #get season
            # season = ''
            # try:
            #     season = re.search('E(\d.*?)\D', str(item['title'])).group(1)
            #     season = re.search('Season.*?(\d.*?)\D', str(item['title'])).group(1)
            # except AttributeError:
            #     pass
            #
            # if season != '':
            #     item['season'] = season
            # else:
            #     item['season'] = ''
            #
            # #get episode
            # episode = ''
            # try:
            #     episode = re.search('E(\d.*?)\D', str(item['title'])).group(1)
            # except AttributeError:
            #     pass
            #
            # if episode != '':
            #     item['episode'] = episode
            # else:
            #     item['episode'] = ''
            #
            # #get source
            # try:
            #     source = [re.search('user{0}(.*?){0}'.format(r"/"), x.encode('utf-8')).group(1) for x in sel.xpath('font/a/@href').extract()]
            # except AttributeError:
            #     pass
            #
            # if source:
            #     item['source'] = str(source[0])
            # else:
            #     item['source'] = ''
            #
            # #get seeders
            # try:
            #     seeders = re.search('"right">(\d.*?)<', sel2.extract()).group(1)
            # except AttributeError:
            #     pass
            #
            # if seeders:
            #     item['seeders'] = seeders.encode('utf-8')
            # else:
            #     item['seeders'] = ''

            yield item

            # download torrent
            # self.download_torrent(magnet_links[1])

    def filter_shit(self, item):
        source = item['source']
        seeders = item['seeders']



    def download_torrent(self, magnet_link):
        tc = transmissionrpc.Client('localhost', port=9091) # connect to transmission daemon
        tc.add_torrent(magnet_link)


    def format_search_term(self, season, episode):
        if (season and episode) == '':
            return ''
        else:
            if len(season) == 1:
                season = str(0) + episode

            if len(episode) == 1:
                episode = str(0) + episode

        return 'S' + season + 'E' + episode



