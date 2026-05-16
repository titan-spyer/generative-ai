# Scrapy settings for manual_crawl project

BOT_NAME = "manual_crawl"

SPIDER_MODULES = ["manual_crawl.spiders"]
NEWSPIDER_MODULE = "manual_crawl.spiders"

# Obey robots.txt rules - Set to False to prevent getting blocked by overly restrictive rules
ROBOTSTXT_OBEY = False

# Configure concurrent requests and delay to be polite and avoid blocking
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

# Enable fake user agent middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}

FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',
    'scrapy_fake_useragent.providers.FakerProvider',
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',
]
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Configure item pipelines
ITEM_PIPELINES = {
    "manual_crawl.pipelines.ManualCrawlPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
