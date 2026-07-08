# Scrapling | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/research/research-scrapling](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/research/research-scrapling)

本页总览

使用 Scrapling 进行网页抓取——HTTP 获取、隐身浏览器自动化、Cloudflare 绕过及通过 CLI 和 Python 进行爬虫抓取。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选——使用 `hermes skills install official/research/scrapling` 安装 |
| 路径 | `optional-skills/research/scrapling` |
| 版本 | `1.0.0` |
| 作者 | FEUAZUR |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `Web Scraping`, `Browser`, `Cloudflare`, `Stealth`, `Crawling`, `Spider` |
| 相关 skill | [`duckduckgo-search`](/docs/zh-Hans/user-guide/skills/optional/research/research-duckduckgo-search), [`domain-intel`](/docs/zh-Hans/user-guide/skills/optional/research/research-domain-intel) |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# Scrapling

[Scrapling](https://github.com/D4Vinci/Scrapling) 是一个具备反机器人绕过、隐身浏览器自动化和爬虫框架的网页抓取框架。它提供三种获取策略（HTTP、动态 JS、隐身/Cloudflare）以及完整的 CLI。

**本 skill 仅供教育和研究目的使用。** 用户必须遵守当地及国际数据抓取法律，并尊重网站服务条款。

## 使用场景[​](#使用场景 "使用场景的直接链接")

* 抓取静态 HTML 页面（比浏览器工具更快）
* 抓取需要真实浏览器的 JS 渲染页面
* 绕过 Cloudflare Turnstile 或机器人检测
* 使用爬虫抓取多个页面
* 当内置 `web_extract` 工具无法返回所需数据时

## 安装[​](#安装 "安装的直接链接")

```
pip install "scrapling[all]"  
scrapling install
```

最小安装（仅 HTTP，无浏览器）：

```
pip install scrapling
```

仅含浏览器自动化：

```
pip install "scrapling[fetchers]"  
scrapling install
```

## 快速参考[​](#快速参考 "快速参考的直接链接")

| 方式 | 类 | 使用场景 |
| --- | --- | --- |
| HTTP | `Fetcher` / `FetcherSession` | 静态页面、API、快速批量请求 |
| 动态 | `DynamicFetcher` / `DynamicSession` | JS 渲染内容、SPA |
| 隐身 | `StealthyFetcher` / `StealthySession` | Cloudflare、反机器人保护站点 |
| 爬虫 | `Spider` | 跟随链接的多页面抓取 |

## CLI 用法[​](#cli-用法 "CLI 用法的直接链接")

### 提取静态页面[​](#提取静态页面 "提取静态页面的直接链接")

```
scrapling extract get 'https://example.com' output.md
```

使用 CSS 选择器和浏览器模拟：

```
scrapling extract get 'https://example.com' output.md \  
  --css-selector '.content' \  
  --impersonate 'chrome'
```

### 提取 JS 渲染页面[​](#提取-js-渲染页面 "提取 JS 渲染页面的直接链接")

```
scrapling extract fetch 'https://example.com' output.md \  
  --css-selector '.dynamic-content' \  
  --disable-resources \  
  --network-idle
```

### 提取 Cloudflare 保护页面[​](#提取-cloudflare-保护页面 "提取 Cloudflare 保护页面的直接链接")

```
scrapling extract stealthy-fetch 'https://protected-site.com' output.html \  
  --solve-cloudflare \  
  --block-webrtc \  
  --hide-canvas
```

### POST 请求[​](#post-请求 "POST 请求的直接链接")

```
scrapling extract post 'https://example.com/api' output.json \  
  --json '{"query": "search term"}'
```

### 输出格式[​](#输出格式 "输出格式的直接链接")

输出格式由文件扩展名决定：

* `.html` —— 原始 HTML
* `.md` —— 转换为 Markdown
* `.txt` —— 纯文本
* `.json` / `.jsonl` —— JSON

## Python：HTTP 抓取[​](#pythonhttp-抓取 "Python：HTTP 抓取的直接链接")

### 单次请求[​](#单次请求 "单次请求的直接链接")

```
from scrapling.fetchers import Fetcher  
  
page = Fetcher.get('https://quotes.toscrape.com/')  
quotes = page.css('.quote .text::text').getall()  
for q in quotes:  
    print(q)
```

### Session（持久化 Cookie）[​](#session持久化-cookie "Session（持久化 Cookie）的直接链接")

```
from scrapling.fetchers import FetcherSession  
  
with FetcherSession(impersonate='chrome') as session:  
    page = session.get('https://example.com/', stealthy_headers=True)  
    links = page.css('a::attr(href)').getall()  
    for link in links[:5]:  
        sub = session.get(link)  
        print(sub.css('h1::text').get())
```

### POST / PUT / DELETE[​](#post--put--delete "POST / PUT / DELETE的直接链接")

```
page = Fetcher.post('https://api.example.com/data', json={"key": "value"})  
page = Fetcher.put('https://api.example.com/item/1', data={"name": "updated"})  
page = Fetcher.delete('https://api.example.com/item/1')
```

### 使用代理[​](#使用代理 "使用代理的直接链接")

```
page = Fetcher.get('https://example.com', proxy='http://user:pass@proxy:8080')
```

## Python：动态页面（JS 渲染）[​](#python动态页面js-渲染 "Python：动态页面（JS 渲染）的直接链接")

适用于需要执行 JavaScript 的页面（SPA、懒加载内容）：

```
from scrapling.fetchers import DynamicFetcher  
  
page = DynamicFetcher.fetch('https://example.com', headless=True)  
data = page.css('.js-loaded-content::text').getall()
```

### 等待特定元素[​](#等待特定元素 "等待特定元素的直接链接")

```
page = DynamicFetcher.fetch(  
    'https://example.com',  
    wait_selector=('.results', 'visible'),  
    network_idle=True,  
)
```

### 禁用资源以提升速度[​](#禁用资源以提升速度 "禁用资源以提升速度的直接链接")

阻止字体、图片、媒体、样式表（速度提升约 25%）：

```
from scrapling.fetchers import DynamicSession  
  
with DynamicSession(headless=True, disable_resources=True, network_idle=True) as session:  
    page = session.fetch('https://example.com')  
    items = page.css('.item::text').getall()
```

### 自定义页面自动化[​](#自定义页面自动化 "自定义页面自动化的直接链接")

```
from playwright.sync_api import Page  
from scrapling.fetchers import DynamicFetcher  
  
def scroll_and_click(page: Page):  
    page.mouse.wheel(0, 3000)  
    page.wait_for_timeout(1000)  
    page.click('button.load-more')  
    page.wait_for_selector('.extra-results')  
  
page = DynamicFetcher.fetch('https://example.com', page_action=scroll_and_click)  
results = page.css('.extra-results .item::text').getall()
```

## Python：隐身模式（反机器人绕过）[​](#python隐身模式反机器人绕过 "Python：隐身模式（反机器人绕过）的直接链接")

适用于 Cloudflare 保护或高度指纹识别的站点：

```
from scrapling.fetchers import StealthyFetcher  
  
page = StealthyFetcher.fetch(  
    'https://protected-site.com',  
    headless=True,  
    solve_cloudflare=True,  
    block_webrtc=True,  
    hide_canvas=True,  
)  
content = page.css('.protected-content::text').getall()
```

### 隐身 Session[​](#隐身-session "隐身 Session的直接链接")

```
from scrapling.fetchers import StealthySession  
  
with StealthySession(headless=True, solve_cloudflare=True) as session:  
    page1 = session.fetch('https://protected-site.com/page1')  
    page2 = session.fetch('https://protected-site.com/page2')
```

## 元素选择[​](#元素选择 "元素选择的直接链接")

所有 fetcher 均返回一个 `Selector` 对象，包含以下方法：

### CSS 选择器[​](#css-选择器 "CSS 选择器的直接链接")

```
page.css('h1::text').get()              # 第一个 h1 文本  
page.css('a::attr(href)').getall()      # 所有链接 href  
page.css('.quote .text::text').getall() # 嵌套选择
```

### XPath[​](#xpath "XPath的直接链接")

```
page.xpath('//div[@class="content"]/text()').getall()  
page.xpath('//a/@href').getall()
```

### Find 方法[​](#find-方法 "Find 方法的直接链接")

```
page.find_all('div', class_='quote')       # 按标签 + 属性查找  
page.find_by_text('Read more', tag='a')    # 按文本内容查找  
page.find_by_regex(r'\$\d+\.\d{2}')       # 按正则表达式查找
```

### 相似元素[​](#相似元素 "相似元素的直接链接")

查找具有相似结构的元素（适用于商品列表等）：

```
first_product = page.css('.product')[0]  
all_similar = first_product.find_similar()
```

### 导航[​](#导航 "导航的直接链接")

```
el = page.css('.target')[0]  
el.parent                # 父元素  
el.children              # 子元素  
el.next_sibling          # 下一个兄弟元素  
el.prev_sibling          # 上一个兄弟元素
```

## Python：爬虫框架[​](#python爬虫框架 "Python：爬虫框架的直接链接")

适用于跟随链接的多页面抓取：

```
from scrapling.spiders import Spider, Request, Response  
  
class QuotesSpider(Spider):  
    name = "quotes"  
    start_urls = ["https://quotes.toscrape.com/"]  
    concurrent_requests = 10  
    download_delay = 1  
  
    async def parse(self, response: Response):  
        for quote in response.css('.quote'):  
            yield {  
                "text": quote.css('.text::text').get(),  
                "author": quote.css('.author::text').get(),  
                "tags": quote.css('.tag::text').getall(),  
            }  
  
        next_page = response.css('.next a::attr(href)').get()  
        if next_page:  
            yield response.follow(next_page)  
  
result = QuotesSpider().start()  
print(f"Scraped {len(result.items)} quotes")  
result.items.to_json("quotes.json")
```

### 多 Session 爬虫[​](#多-session-爬虫 "多 Session 爬虫的直接链接")

将请求路由到不同的 fetcher 类型：

```
from scrapling.fetchers import FetcherSession, AsyncStealthySession  
  
class SmartSpider(Spider):  
    name = "smart"  
    start_urls = ["https://example.com/"]  
  
    def configure_sessions(self, manager):  
        manager.add("fast", FetcherSession(impersonate="chrome"))  
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)  
  
    async def parse(self, response: Response):  
        for link in response.css('a::attr(href)').getall():  
            if "protected" in link:  
                yield Request(link, sid="stealth")  
            else:  
                yield Request(link, sid="fast", callback=self.parse)
```

### 暂停/恢复抓取[​](#暂停恢复抓取 "暂停/恢复抓取的直接链接")

```
spider = QuotesSpider(crawldir="./crawl_checkpoint")  
spider.start()  # 按 Ctrl+C 暂停，重新运行以从检查点恢复
```

## 注意事项[​](#注意事项 "注意事项的直接链接")

* **需要安装浏览器**：pip 安装后运行 `scrapling install`——否则 `DynamicFetcher` 和 `StealthyFetcher` 将无法使用
* **超时**：DynamicFetcher/StealthyFetcher 的超时单位为**毫秒**（默认 30000），Fetcher 的超时单位为**秒**
* **Cloudflare 绕过**：`solve_cloudflare=True` 会增加 5-15 秒的获取时间——仅在必要时启用
* **资源占用**：StealthyFetcher 运行真实浏览器——限制并发使用量
* **法律合规**：抓取前务必检查 robots.txt 和网站服务条款。本库仅供教育和研究目的使用
* **Python 版本**：需要 Python 3.10+

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [使用场景](#使用场景)
* [安装](#安装)
* [快速参考](#快速参考)
* [CLI 用法](#cli-用法)
  + [提取静态页面](#提取静态页面)
  + [提取 JS 渲染页面](#提取-js-渲染页面)
  + [提取 Cloudflare 保护页面](#提取-cloudflare-保护页面)
  + [POST 请求](#post-请求)
  + [输出格式](#输出格式)
* [Python：HTTP 抓取](#pythonhttp-抓取)
  + [单次请求](#单次请求)
  + [Session（持久化 Cookie）](#session持久化-cookie)
  + [POST / PUT / DELETE](#post--put--delete)
  + [使用代理](#使用代理)
* [Python：动态页面（JS 渲染）](#python动态页面js-渲染)
  + [等待特定元素](#等待特定元素)
  + [禁用资源以提升速度](#禁用资源以提升速度)
  + [自定义页面自动化](#自定义页面自动化)
* [Python：隐身模式（反机器人绕过）](#python隐身模式反机器人绕过)
  + [隐身 Session](#隐身-session)
* [元素选择](#元素选择)
  + [CSS 选择器](#css-选择器)
  + [XPath](#xpath)
  + [Find 方法](#find-方法)
  + [相似元素](#相似元素)
  + [导航](#导航)
* [Python：爬虫框架](#python爬虫框架)
  + [多 Session 爬虫](#多-session-爬虫)
  + [暂停/恢复抓取](#暂停恢复抓取)
* [注意事项](#注意事项)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/research/research-domain-intel](./docs-zh-Hans-user-guide-skills-optional-research-research-domain-intel.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/research/research-duckduckgo-search](./docs-zh-Hans-user-guide-skills-optional-research-research-duckduckgo-search.md)
