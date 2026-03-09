import requests
from bs4 import BeautifulSoup
import re

def _get_meta_content(soup: BeautifulSoup, property_name: str) -> str | None:
    """
    安全地取得 meta tag 的 content。
    """
    meta = soup.find('meta', property=property_name)
    if meta and meta.get('content'):
        return meta.get('content')
    return None

def _extract_price_momo(soup: BeautifulSoup) -> float | None:
    """
    momo 購物網專屬價格解析。
    頁面上可能有多個帶有 price 屬性的元素，取最後一個的 price 屬性值作為商品價格。
    """
    elements = soup.find_all(attrs={"price": True})
    if elements:
        last = elements[-1]
        price_str = last.get('price')
        if price_str:
            try:
                return float(str(price_str).replace(",", ""))
            except ValueError:
                pass
    return None

def _extract_price_generic(soup: BeautifulSoup) -> float | None:
    """通用價格解析：優先 og:price:amount meta，再嘗試常見 CSS 選擇器。"""
    og_price = _get_meta_content(soup, "og:price:amount")
    if og_price:
        try:
            return float(og_price.replace(",", ""))
        except ValueError:
            pass

    # 常見電商 CSS 選擇器
    selectors = [
        '[itemprop="price"]',
        '.price',
        '.product-price',
        '.sale-price',
        '#price',
    ]
    for sel in selectors:
        for el in soup.select(sel):
            text = el.get_text(strip=True)
            digits = re.sub(r"[^\d.]", "", text.replace(",", ""))
            if digits:
                try:
                    return float(digits)
                except ValueError:
                    continue
    return None

async def fetch_product_details(url: str, shared_page=None):
    """
    爬取商品頁面，回傳 name、image_url、current_price。
    原先使用 Playwright，現在為了節省資源改用 requests + BeautifulSoup 在背景執行緒解析。
    (保留 shared_page 參數名稱只是為了與舊版簽名相容可不用)
    """
    import asyncio
    return await asyncio.to_thread(_fetch_product_details_sync, url)

def _fetch_product_details_sync(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, "html.parser")

        # 1. 圖片
        image_url = _get_meta_content(soup, "og:image")

        # 2. 商品名稱
        name = soup.title.string if soup.title else ""
        og_title = _get_meta_content(soup, "og:title")
        if og_title:
            name = og_title

        # 3. 價格
        price = None
        if "momoshop.com.tw" in url:
            price = _extract_price_momo(soup)

        if price is None:
            price = _extract_price_generic(soup)

        return {
            "name": name,
            "image_url": image_url,
            "current_price": price,
        }

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

