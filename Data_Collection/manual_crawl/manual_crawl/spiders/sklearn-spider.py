import scrapy
from manual_crawl.items import SklearnItem

class SklearnSpider(scrapy.Spider):
    name = "sklearn"
    allowed_domains = ["scikit-learn.org"]
    start_urls = ["https://scikit-learn.org/stable/modules/classes.html"]

    def parse(self, response):
        # Find all API links in the classes index page
        # Scikit-learn usually uses `table.autosummary a.reference.internal` or similar 
        # Here we look for all links that contain 'modules/generated/sklearn'
        api_links = response.css('a.reference.internal::attr(href)').extract()
        for link in api_links:
            if 'generated/sklearn' in link:
                yield response.follow(link, self.parse_api_page)
                
    def parse_api_page(self, response):
        item = SklearnItem()
        item['url'] = response.url
        
        # 1. Main Component Name
        # e.g., class sklearn.linear_model.LinearRegression
        component_class = response.css('dl.py.class > dt.sig.sig-object.py, dl.py.function > dt.sig.sig-object.py')
        if not component_class:
            component_class = response.css('dl.class > dt.sig.sig-object, dl.function > dt.sig.sig-object')

        if component_class:
            descclassname = component_class.css('span.sig-prename.descclassname::text').get(default='')
            descname = component_class.css('span.sig-name.descname::text').get(default='')
            item['component_name'] = f"{descclassname}{descname}".strip()
        else:
            item['component_name'] = response.css('h1::text').get(default='').strip()

        # 2. Parameters & Descriptions
        # Look for the Parameters section which is usually inside a <dl class="field-list simple">
        parameters = []
        param_dts = response.xpath('//dl[contains(@class, "field-list")]/dt[contains(., "Parameters") or contains(., "Returns")]/following-sibling::dd[1]/dl/dt | //dl[contains(@class, "field-list")]/dt[contains(., "Parameters") or contains(., "Returns")]/following-sibling::dd[1]/ul/li')
        
        if not param_dts:
            # Fallback for some other formats
            param_dts = response.xpath('//p[strong[contains(text(), "Parameters")]]/following-sibling::dl[1]/dt')
            
        for dt in param_dts:
            # The parameter name is usually inside a <strong> tag or it's just the text of the dt/li
            param_name = ''.join(dt.css('strong::text').getall()).strip()
            if  not list(dt.css('strong::text').getall()) and ':' in dt.xpath('string(.)').get(default=''):
                param_name = dt.xpath('string(.)').get().strip().split(':')[0]

            if not param_name:
                continue

            if dt.root.tag == 'dt':
                param_desc_dd = dt.xpath('following-sibling::dd[1]')
                param_desc = ' '.join(param_desc_dd.xpath('string(.)').getall()).strip()
            else:
                total_text = dt.xpath('string(.)').get(default='').strip()
                param_desc = total_text.replace(param_name, '', 1).lstrip(' :').strip()

            parameters.append({
                'parameter': param_name,
                'description': param_desc
            })
            
        item['parameters'] = parameters

        # 3. Code Examples
        # Examples are usually in pre blocks inside div.highlight
        examples_section = response.css('div.highlight-python pre, div.highlight-default pre')
        examples_text = []
        for ex in examples_section:
            code = ex.xpath('string(.)').get()
            if code:
                examples_text.append(code.strip())
                
        item['examples'] = "\n\n".join(examples_text)
        
        # Extract the core text section without global headers, footers, or navigational menus
        main_block = response.css('div.section, main, article').xpath('string(.)').get()
        item['structured_body'] = main_block.strip() if main_block else ""

        yield item
