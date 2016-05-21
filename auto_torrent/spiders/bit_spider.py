import re
import scrapy
import transmissionrpc
from auto_torrent.items import PirateItem
import pdb


class PirateSpider(scrapy.Spider):
    name = 'pirate'

    def __init__(self, search_term='family guy', season='', episode=''):
        self.base_url = 'https://kat.cr/usearch/'
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
            for link in icons:
                if re.match('magnet', link):
                    magnet_link = link
                    item['magnet_link'] = str(magnet_link)

            #get title, season, and episode
            title = ''
            try:
                title = sel.xpath('.//a[@class="cellMainLink"]//@href').extract()[0]
                item['title'] = str(title)
            except Exception as e:
                print 'Error! could not extract title \n {0}'.format(e)

            if title:
                #get season (title contains season & episode
                season = ''
                try:
                    season = re.search('E(\d.*?)\D', str(item['title']), re.IGNORECASE).group(1)
                except AttributeError:
                     print 'Error! could not extract title \n {0}'.format(e)

                try:
                    season = re.search('Season.*?(\d.*?)\D', str(item['title']), re.IGNORECASE).group(1)
                except AttributeError:
                    print 'Error! could not extract title \n {0}'.format(e)

                if season:
                    item['season'] = season

                #get episode
                episode = ''
                try:
                    episode = re.search('E(\d.*?)\D', str(item['title']), re.IGNORECASE).group(1)
                except AttributeError:
                    print 'Error! could not extract episode \n {0}'.format(e)

                try:
                    episode = re.search('Episode(\d.*?)\D', str(item['title']), re.IGNORECASE).group(1)
                except AttributeError:
                    print 'Error! could not extract episode \n {0}'.format(e)

                if episode:
                    item['episode'] = episode

            # get source
            try:
                source = sel.xpath('.//a[@class="plain"]//@href').extract()[0]
                source = re.search('user/(.*)/', str(source)).group(1)
                item['source'] = source
            except Exception as e:
                print 'Error! could not extract source \n {0}'.format(e)

            # get size
            try:
                size = sel.xpath('.//td[@class="nobr center"]//text()').extract()
                item['size'] = ''.join(size)
            except:
                 print 'Error! could not extract size \n {0}'.format(e)

            # get seeders
            try:
                seeders = sel.xpath('.//td[@class="green center"]//text()').extract()[0]
                item['seeders'] = seeders
            except:
                 print 'Error! could not extract size \n {0}'.format(e)

            yield item

            # download torrent
            # self.download_torrent(magnet_links[1])

    # # connect to transmission daemon and download torrent
    def download_torrent(self, magnet_link):
        tc = transmissionrpc.Client('localhost', port=9091)
        tc.add_torrent(magnet_link)

    # format season and episode number - prefixes '0' if only one digit entered
    def format_search_term(self, season, episode):
        if (season and episode) == '':
            return ''
        else:
            if len(season) == 1:
                season = str(0) + episode

            if len(episode) == 1:
                episode = str(0) + episode

        return 'S' + season + 'E' + episode


