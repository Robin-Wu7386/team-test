import pandas as pd
import scrapy


class ZhongyaofangSpider(scrapy.Spider):
    name = 'fangji'
    allowed_domains = ['zysj.com.cn']
    start_urls = [f"https://www.zysj.com.cn/zhongyaofang/index_{i}.html" for i in range(1, 27)]

    def __init__(self, *args, **kwargs):
        self.data = []

    def parse(self, response):
        # 提取包含链接和标题的部分
        for li in response.css('div#list-content ul li'):
            a_tag = li.css('a')
            title = a_tag.css('::attr(title)').get()
            href = a_tag.css('::attr(href)').get()
            if title and href:
                # 构建完整的详情页 URL
                detail_url = response.urljoin(href)
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'title': title})

    # 如果没有这个元素，就设置空就行
    # 处方： div[class="item prescription"]/div[class="item-content"]/p/text
    # 制法： div[ class="item making"]/div[class="item-content"]/p/text
    # 主治： div class="item functional_indications"]/div[class="item-content"]/p/text
    # 用法用量： class="item usage"]/div[class="item-content"]/p/text
    # 注意事项： class="item care"]/div[class="item-content"]/p/text
    # 摘录： class="item excerpt"]/div[class="item-content"]/text
    def parse_detail(self, response):
        title = response.meta['title']

        # 提取各个字段
        prescription = response.css('div.item.prescription div.item-content p::text').get(default='').strip()
        making = response.css('div.item.making div.item-content p::text').get(default='').strip()
        functional_indications = response.css('div.item.functional_indications div.item-content p::text').get(
            default='').strip()
        usage = response.css('div.item.usage div.item-content p::text').get(default='').strip()
        care = response.css('div.item.care div.item-content p::text').get(default='').strip()
        excerpt = response.css('div.item.excerpt div.item-content::text').get(default='').strip()

        item = {
            'title': title,
            'prescription': prescription,
            'making': making,
            'functional_indications': functional_indications,
            'usage': usage,
            'care': care,
            'excerpt': excerpt
        }

        self.data.append(item)

        yield item

    def closed(self, reason):
        # 当爬虫关闭时，保存数据到 Excel 文件
        df = pd.DataFrame(self.data)
        df.to_excel('zhongyaofang_data.xlsx', index=False)

