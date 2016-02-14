from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ClientContextFactory


class MyClientContextFactory(ClientContextFactory):
    def __init__(self):
        self.method = SSL.SSLv3_METHOD  # or SSL.SSLv23_METHOD