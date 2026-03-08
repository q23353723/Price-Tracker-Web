from playwright.async_api import async_playwright
import re


async def _get_meta_content(page, property_name: str) -> str | None:
    """
    安全地取得 meta tag 的 content，找不到直接回傳 None（不等待、不 timeout）。
    使用 query_selector 而非 locator，避免「元素不存在時等到 timeout」的問題。
    """
    el = await page.query_selector(f'meta[property="{property_name}"]')
    if el:
        return await el.get_attribute("content")
    return None


async def _extract_price_momo(page) -> float | None:
    """
    momo 購物網專屬價格解析。
    頁面上可能有多個帶有 price 屬性的元素，取最後一個的 price 屬性值作為商品價格。
    """
    price_str = await page.evaluate("""
        () => {
            const elements = document.querySelectorAll('[price]');
            if (!elements || elements.length === 0) return null;
            const last = elements[elements.length - 1];
            return last.getAttribute('price');
        }
    """)
    if price_str:
        try:
            return float(str(price_str).replace(",", ""))
        except ValueError:
            pass
    return None


async def _extract_price_generic(page) -> float | None:
    """通用價格解析：優先 og:price:amount meta，再嘗試常見 CSS 選擇器。"""
    # 1. og:price:amount meta（需用 query_selector，locator 找不到會 timeout）
    og_price = await _get_meta_content(page, "og:price:amount")
    if og_price:
        try:
            return float(og_price.replace(",", ""))
        except ValueError:
            pass

    # 2. 常見電商 CSS 選擇器
    selectors = [
        '[itemprop="price"]',
        '.price',
        '.product-price',
        '.sale-price',
        '#price',
    ]
    for sel in selectors:
        el = await page.query_selector(sel)
        if el:
            text = await el.inner_text()
            digits = re.sub(r"[^\d.]", "", text.replace(",", ""))
            if digits:
                try:
                    return float(digits)
                except ValueError:
                    continue

    return None


async def fetch_product_details(url: str):
    """
    爬取商品頁面，回傳 name、image_url、current_price。
    支援 momo 購物網的專屬選擇器，並以通用邏輯作為後備。
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # 1. 圖片（og:image meta）
            image_url = await _get_meta_content(page, "og:image")

            # 2. 商品名稱
            name = await page.title()
            og_title = await _get_meta_content(page, "og:title")
            if og_title:
                name = og_title

            # 3. 價格：依據網域選擇策略
            price = None
            if "momoshop.com.tw" in url:
                price = await _extract_price_momo(page)

            # 若網站專屬策略失敗，fallback 到通用邏輯
            if price is None:
                price = await _extract_price_generic(page)

            return {
                "name": name,
                "image_url": image_url,
                "current_price": price,
            }

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        finally:
            await browser.close()
