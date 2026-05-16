import scrapy

class SklearnItem(scrapy.Item):
    url = scrapy.Field()
    component_name = scrapy.Field()
    parameters = scrapy.Field()
    examples = scrapy.Field()
