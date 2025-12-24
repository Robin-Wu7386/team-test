#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中药材知识图谱爬虫 - 最终优化版
直接运行: python zhongyaocai_spider.py
"""
from scrapy.exceptions import CloseSpider  # <--- 新增这行
import pandas as pd
import scrapy
import re
import os
import json
import hashlib
import requests
import time
from urllib.parse import urljoin, urlparse
from scrapy.crawler import CrawlerProcess

# 如果系统支持 uvloop，可以加速异步循环（Linux/Mac有效，Windows忽略）
try:
    import uvloop
    import asyncio

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class ZhongyaocaiSpider(scrapy.Spider):
    """中药材爬虫 - 适配 zysj.com.cn"""

    name = 'zhongyaocai'
    allowed_domains = ['zysj.com.cn']

    # 🚀 优化配置：加速与重试
    custom_settings = {
        # === 并发设置 (加速关键) ===
        'CONCURRENT_REQUESTS': 32,  # 增加全局并发数
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,  # 针对该域名的并发
        'DOWNLOAD_DELAY': 0.2,  # 降低延迟 (对方反爬不严的话可设低)
        'AUTOTHROTTLE_ENABLED': True,  # 自动限速，防止封IP
        'AUTOTHROTTLE_START_DELAY': 0.2,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10.0,

        # === 重试设置 (爬取失败重试) ===
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,  # 网页请求失败重试3次
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],

        # === 其他设置 ===
        'LOG_LEVEL': 'INFO',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # 标准字段列表
    STANDARD_FIELDS = [
        '拼音', '拼音注音', '英文名', '别名', '来源', '原形态', '生境分布',
        '栽培', '性状', '化学成分', '药理作用', '鉴别', '炮制', '性味',
        '归经', '功能主治', '用法用量', '注意', '附方', '各家论述',
        '摘录', '出处', '复方', '临床应用', '制剂', '备注', '毒性'
    ]

    def __init__(self, max_count=20000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'https://www.zysj.com.cn'
        self.max_count = int(max_count)

        # 数据存储
        self.summary_data = []
        self.details_data = []
        self.processed_urls = set()
        self.medicine_counter = 0

        # 创建目录
        os.makedirs('images', exist_ok=True)
        os.makedirs('output', exist_ok=True)

        # 加载断点
        self._load_checkpoint()

    def _load_checkpoint(self):
        """加载断点"""
        if os.path.exists('processed_urls.txt'):
            try:
                with open('processed_urls.txt', 'r', encoding='utf-8') as f:
                    self.processed_urls = set(line.strip() for line in f if line.strip())
                self.logger.info(f"已加载 {len(self.processed_urls)} 个已处理URL")
            except Exception:
                pass

    def _save_checkpoint(self, url):
        """保存断点"""
        try:
            with open('processed_urls.txt', 'a', encoding='utf-8') as f:
                f.write(url + '\n')
            self.processed_urls.add(url)
        except Exception:
            pass

    def start_requests(self):
        """起始请求"""
        self.logger.info(f"🚀 开始爬取，最大数量: {self.max_count}")

        urls = [f'{self.base_url}/zhongyaocai/index.html']
        # 扩大范围以覆盖所有索引页
        urls += [f'{self.base_url}/zhongyaocai/index_{i}.html' for i in range(1, 6)]
        urls += [f'{self.base_url}/zhongyaocai/index__{i}.html' for i in range(1, 40)]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_list, errback=self.errback)

    def parse_list(self, response):
        """解析列表页"""
        # ⚡️ 检查点 1：如果数量够了，直接抛出异常强制停止
        if self.medicine_counter >= self.max_count:
            raise CloseSpider(f"已达到目标数量: {self.max_count}")

        # 提取药材链接
        links = response.css('a[href*="/zhongyaocai/"][href$="/index.html"]')

        for link in links:
            # ⚡️ 检查点 2：循环内也要检查，防止一页提取太多
            if self.medicine_counter >= self.max_count:
                raise CloseSpider(f"已达到目标数量: {self.max_count}")

            href = link.css('::attr(href)').get()
            title = link.css('::attr(title)').get() or link.css('::text').get()

            if not href or '/zhongyaocai/index' in href:
                continue
            if href.count('/') < 2:
                continue

            detail_url = response.urljoin(href)

            if detail_url in self.processed_urls:
                continue

            title = self._clean_text(title) if title else ''
            medicine_id = self._extract_medicine_id(detail_url)

            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={'medicine_id': medicine_id, 'title': title},
                errback=self.errback
            )

    def parse_detail(self, response):
        """解析详情页"""
        # ⚡️ 检查点 3：进来先检查
        if self.medicine_counter >= self.max_count:
            # 先保存再停止
            self._save_final_files()
            raise CloseSpider(f"已达到目标数量: {self.max_count}")

        medicine_id = response.meta.get('medicine_id')
        title = response.meta.get('title', '')

        # 验证有效性
        content = response.css('div#content').get()
        if not content:
            self.logger.warning(f"页面结构异常，跳过: {response.url}")
            return

        self.medicine_counter += 1
        if self.medicine_counter % 10 == 0:
            print(f"\r🌿 进度: {self.medicine_counter}/{self.max_count} | 当前: {title[:10]}", end='', flush=True)

        # 1. 下载图片 (带重试)
        image_urls, local_paths = self._extract_images(response, medicine_id)
        downloaded_paths = self._download_images(image_urls, medicine_id)

        # 2. 提取数据 (核心修改: 使用摘录作为来源)
        all_source_data = self._extract_all_sources(response)

        # 3. 兜底处理
        if not all_source_data:
            all_source_data = [{'source': '未知来源', 'data': {'备注': '页面结构异常，未能提取数据'}}]

        # 4. 汇总所有来源名称
        source_names = [s['source'] for s in all_source_data if s['source'] != '未知来源']
        source_list_str = ';'.join(source_names) if source_names else '未知来源'

        # 5. 构建主表
        summary_item = {
            '药材ID': medicine_id,
            '药材名称': title or medicine_id,
            '拼音注音': self._get_first_field(all_source_data, '拼音注音'),
            '别名': self._get_first_field(all_source_data, '别名'),
            '图片本地路径': ','.join(downloaded_paths),
            '图片原始URL': ','.join(image_urls),
            '来源页面URL': response.url,
            '来源数量': len(all_source_data),
            '来源列表': source_list_str,
            '采集时间': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 6. 构建副表
        detail_items = []
        for source_data in all_source_data:
            source_name = source_data['source']
            for field_name, field_value in source_data['data'].items():
                if field_value:
                    detail_items.append({
                        '药材ID': medicine_id,
                        '药材名称': title or medicine_id,
                        '来源': source_name,
                        '属性名称': field_name,
                        '属性值': field_value,
                    })

        self.summary_data.append(summary_item)
        self.details_data.extend(detail_items)
        self._save_checkpoint(response.url)

        if self.medicine_counter % 50 == 0:
            self._save_progress()
        # ⚡️ 检查点 4：处理完当前这条后，再次检查是否达标
        if self.medicine_counter >= self.max_count:
            self.logger.info(f"🛑 数量已达标 ({self.medicine_counter})，正在停止...")
            raise CloseSpider(f"已达到目标数量: {self.max_count}")

    def _extract_all_sources(self, response):
        """
        提取所有来源数据
        逻辑：遍历 div.section -> 提取所有键值对 -> 查找'摘录'字段 -> 用'摘录'的值作为该section的来源名
        """
        all_source_data = []

        # 1. 查找所有 section
        sections = response.css('div#content div.section')

        if not sections:
            # 备用：通用提取
            fields = self._extract_fields_universal(response)
            if fields:
                source_name = fields.get('摘录', '未知来源')
                # 清理摘录中的书名号等
                source_name = self._clean_source_name(source_name)
                all_source_data.append({'source': source_name, 'data': fields})
            return all_source_data

        for section in sections:
            fields = {}
            items = section.css('div.item')

            # 提取该 section 下所有属性
            for item in items:
                key = item.css('div.item-name').xpath('string(.)').get(default='').strip()
                value = item.css('div.item-content').xpath('string(.)').get(default='').strip()
                value = re.sub(r'\s+', ' ', value)  # 压缩空白

                if key and value:
                    fields[self._normalize_field_name(key)] = value

            if fields:
                # === 核心修改 ===
                # 优先使用该段落内的 '摘录' 字段作为来源名
                if '摘录' in fields:
                    raw_source = fields['摘录']
                    source_name = self._clean_source_name(raw_source)
                else:
                    # 如果没有摘录字段，尝试从 section 标题提取 (兼容旧逻辑)
                    raw_title = section.css('h2').xpath('string(.)').get(default='').strip()
                    source_name = self._clean_source_name(raw_title)
                    if not source_name:
                        source_name = '未知来源'

                all_source_data.append({
                    'source': source_name,
                    'data': fields
                })

        return all_source_data

    def _clean_source_name(self, text):
        """清理来源名称：提取书名或清理标点"""
        if not text:
            return ''

        # 1. 如果包含书名号，提取书名号内容
        if '《' in text and '》' in text:
            match = re.search(r'《([^》]+)》', text)
            if match:
                return f"《{match.group(1)}》"

        # 2. 如果是 '来源：XXX' 格式
        if '：' in text:
            text = text.split('：')[0]
        if ':' in text:
            text = text.split(':')[0]

        # 3. 去除多余空格
        text = text.strip()

        # 4. 补充书名号（如果看起来像书名但没书名号）
        known_books = ['全国中草药汇编', '中药大辞典', '中华本草', '本草纲目', '图经本草']
        if text in known_books:
            return f"《{text}》"

        return text

    def _extract_fields_universal(self, response):
        """[备用] 通用字段提取"""
        fields = {}
        content_area = response.css('div#content')
        all_texts = content_area.xpath('.//text()').getall()

        for text in all_texts:
            text = text.strip()
            # 匹配 "字段名：内容"
            match = re.match(r'^([^：:]{2,10})[：:](.+)$', text)
            if match:
                key = match.group(1).strip()
                val = match.group(2).strip()
                if self._is_valid_field(key):
                    fields[self._normalize_field_name(key)] = val
        return fields

    def _normalize_field_name(self, name):
        """标准化字段名"""
        name = name.strip()
        name = re.sub(r'[【】\[\]（）()：:]', '', name)
        mapping = {
            '拼音': '拼音注音',
            '注意事项': '注意',
            '主治': '功能主治',
            '功效': '功能主治',
        }
        return mapping.get(name, name)

    def _is_valid_field(self, name):
        """验证字段名有效性"""
        for std in self.STANDARD_FIELDS:
            if name == std or name.startswith(std):
                return True
        return False

    def _get_first_field(self, all_source_data, field_name):
        """获取第一个非空字段值"""
        for src in all_source_data:
            if field_name in src['data'] and src['data'][field_name]:
                return src['data'][field_name]
        return ''

    def _extract_images(self, response, medicine_id):
        """提取图片URL"""
        image_urls = set()
        selectors = ['img::attr(data-original)', 'img::attr(data-src)', 'img::attr(src)']

        for selector in selectors:
            for url in response.css(selector).getall():
                if not url or url.startswith('data:'): continue
                full_url = response.urljoin(url)
                if '/zhongyaocai/' in full_url and not any(x in full_url for x in ['logo', 'icon']):
                    image_urls.add(full_url)

        image_urls = list(image_urls)[:5]
        local_paths = []
        for i, url in enumerate(image_urls, 1):
            ext = os.path.splitext(urlparse(url).path)[1] or '.jpg'
            local_paths.append(f"images/{medicine_id}_{i}{ext}")
        return image_urls, local_paths

    def _download_images(self, image_urls, medicine_id):
        """图片下载（带3次重试）"""
        downloaded = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        for i, url in enumerate(image_urls, 1):
            ext = os.path.splitext(urlparse(url).path)[1] or '.jpg'
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                ext = '.jpg'
            filename = f"images/{medicine_id}_{i}{ext}"

            if os.path.exists(filename):
                downloaded.append(filename)
                continue

            # 🔄 重试循环
            for attempt in range(3):
                try:
                    resp = requests.get(url, headers=headers, timeout=10)
                    if resp.status_code == 200 and len(resp.content) > 500:
                        with open(filename, 'wb') as f:
                            f.write(resp.content)
                        downloaded.append(filename)
                        break  # 成功，跳出循环
                except Exception:
                    if attempt < 2: time.sleep(1)  # 失败等待

        return downloaded

    def _extract_medicine_id(self, url):
        """从URL提取ID"""
        path = urlparse(url).path
        parts = path.strip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'zhongyaocai':
            return parts[1].lower()
        return hashlib.md5(url.encode()).hexdigest()[:10]

    def _clean_text(self, text):
        return re.sub(r'\s+', ' ', str(text).strip())

    def _save_progress(self):
        """保存临时进度文件（防止意外中断）"""
        try:
            if self.summary_data:
                # 保存到临时文件（快，只用于恢复）
                pd.DataFrame(self.summary_data).to_csv('output/medicines_summary_temp.csv', index=False,
                                                       encoding='utf-8-sig')
                pd.DataFrame(self.details_data).to_csv('output/medicines_details_temp.csv', index=False,
                                                       encoding='utf-8-sig')

                # 每500条保存一次Excel（因为Excel保存慢）
                if self.medicine_counter % 500 == 0:
                    pd.DataFrame(self.summary_data).to_excel('output/medicines_summary_temp.xlsx', index=False)
                    pd.DataFrame(self.details_data).to_excel('output/medicines_details_temp.xlsx', index=False)

                if self.medicine_counter % 100 == 0:
                    self.logger.info(f"💾 已保存临时文件（{self.medicine_counter}条）")
        except Exception as e:
            self.logger.error(f"保存临时文件失败: {e}")

    def errback(self, failure):
        self.logger.error(f"❌ 请求失败: {failure.request.url}")

    def closed(self, reason):
        """爬虫结束时保存最终文件"""
        print(f"\n✅ 爬取结束! 共处理 {self.medicine_counter} 条数据")

        if not self.summary_data:
            print("⚠️  没有数据可保存")
            return

        try:
            # 1. 先保存CSV（快速，保证数据不丢）
            summary_df = pd.DataFrame(self.summary_data)
            details_df = pd.DataFrame(self.details_data)

            csv_success = False
            excel_success = False

            # 先保存CSV
            csv_paths = [
                'output/medicines_summary.csv',
                'output/medicines_details.csv'
            ]
            summary_df.to_csv(csv_paths[0], index=False, encoding='utf-8-sig')
            details_df.to_csv(csv_paths[1], index=False, encoding='utf-8-sig')
            csv_success = True
            print(f"📊 CSV已保存: {len(summary_df)}条摘要, {len(details_df)}条详情")

            # 2. 再保存Excel
            excel_paths = [
                'output/medicines_summary.xlsx',
                'output/medicines_details.xlsx'
            ]
            if len(summary_df) <= 1000000:
                summary_df.to_excel(excel_paths[0], index=False)
                details_df.to_excel(excel_paths[1], index=False)
                excel_success = True
                print("✅ Excel文件已保存")
            else:
                print("⚠️  数据量过大，建议使用CSV文件")
                excel_success = True  # 不算失败，只是没保存Excel

            # 3. 确认文件已成功保存后再删除临时文件
            if csv_success:
                temp_files = [
                    'output/medicines_summary_temp.csv',
                    'output/medicines_details_temp.csv',
                    'output/medicines_summary_temp.xlsx',
                    'output/medicines_details_temp.xlsx'
                ]

                deleted_count = 0
                for temp_file in temp_files:
                    try:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                            deleted_count += 1
                    except:
                        pass

                if deleted_count > 0:
                    print(f"🧹 已清理 {deleted_count} 个临时文件")

        except Exception as e:
            print(f"❌ 保存失败: {e}")
            print("⚠️  临时文件保留以便恢复数据")


# ========== 运行入口 ==========

def main():
    print("=" * 60)
    print("🚀 中药材全量爬虫")
    print("=" * 60)

    settings = {
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'crawl.log',
    }

    # max_count 设置一个大数以爬取全部
    process = CrawlerProcess(settings)
    process.crawl(ZhongyaocaiSpider, max_count=20000)
    process.start()


if __name__ == '__main__':
    main()