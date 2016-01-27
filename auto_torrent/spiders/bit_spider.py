import scrapy
import re
import transmissionrpc
import pdb

from auto_torrent.items import PirateItem


class PirateSpider(scrapy.Spider):
  name = 'pirate'

  def __init__(self, base_url='https://thepiratebay.se/search/',
               search_term='modern family', season='', episode=''):
    self.base_url = base_url
    self.season = season
    self.episode = episode
    self.search_term = search_term
    self.start_urls = [self.base_url + self.search_term + ' ' + self.format_search_term(self.episode, self.season)]

  def parse(self, response):
    for sel, sel2 in zip(response.xpath('//tr/td[2]'), response.xpath('//tr/td[3]')):
      item = PirateItem()

      # get magnet link
      try:
        magnet_link = [x.encode('utf-8') for x in sel.xpath('a/@href').extract() if re.match('magnet', x)]
      except AttributeError:
        pass

      if magnet_link:
         item['magnet_link'] = str(magnet_link[0])
      else:
         item['magnet_link'] = ''

      # get title
      title = [x.encode('utf-8') for x in sel.xpath('div/a/@title').extract()]
      if title:
        item['title'] = str(title[0])
      else:
        item['title'] = ''

      #get season
      try:
        season_abr = re.search('E(\d.*?)\D', str(item['title'])).group(1)
        season_complete = re.search('Season.*?(\d.*?)\D', str(item['title'])).group(1)
      except AttributeError:
        pass

      if season_abr:
        item['season'] = season_abr
      elif season_complete:
        item['season'] = season_complete
      else:
        item['season'] = ''

      #get episode
      try:
        episode = re.search('E(\d.*?)\D', str(item['title'])).group(1)
      except AttributeError:
        pass

      if episode:
        item['episode'] = episode
      else:
        item['episode'] = ''

      #get source
      try:
        source = [re.search('user{0}(.*?){0}'.format(r"/"), x.encode('utf-8')).group(1) for x in sel.xpath('font/a/@href').extract()]
      except AttributeError:
        pass

      if source:
        item['source'] = str(source[0])
      else:
        item['source'] = ''

      #get seeders
      try:
        seeders = re.search('"right">(\d.*?)<', sel2.extract()).group(1)
      except AttributeError:
        pass

      if seeders:
        item['seeders'] = seeders
      else:
        item['seeders'] = ''

      yield item

    # download torrent
    # self.download_torrent(magnet_links[1])


  def download_torrent(self, magnet_link):
    tc = transmissionrpc.Client('localhost', port=9091) # connect to transmission daemon

    tc.add_torrent(magnet_link)


    def filter_magnet_links(self, links):
      pass


  def remove_torrent(self, torrent):
    pass


  def move_torrent(self, file):
    pass


  def format_search_term(self, season, episode):
    if (season and episode) == '':
      return ''
    else:
      try:
        season = str(0) + re.search('([1-9])', season).group(1)
      except AttributeError:
        pass

      try:
        episode = str(0) + re.search('([1-9])', episode).group(1)
      except AttributeError:
        pass

      return 'S' + season + 'E' + episode
