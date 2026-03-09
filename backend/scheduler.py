import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
import models, crawler, notifier

scheduler = AsyncIOScheduler()


def update_product_price(product_id):
    """
    同步版本的爬蟲更新函式，供 FastAPI BackgroundTasks 使用。
    在 Windows 上，BackgroundTasks 在執行緒中執行，無法直接使用現有的
    async event loop 執行 Playwright（需要 subprocess 支援）。
    因此在 Windows 環境下，我們獨立建立一個專屬此 thread 的 ProactorEventLoop，
    避免修改全域的 event loop policy 而干擾 Uvicorn 的運行。
    """
    import sys
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_update_product_price_async(product_id))
        finally:
            loop.close()
    else:
        asyncio.run(_update_product_price_async(product_id))


def _handle_product_price_update(db: Session, product: models.Product, details: dict):
    if details['current_price'] is not None:
        product.current_price = details['current_price']
    if details['name']:
        product.name = details['name']
    if details['image_url']:
        product.image_url = details['image_url']

    product.last_checked_at = datetime.utcnow()
    db.commit()

    # 檢查是否有需要通知的訂閱
    subscriptions = product.subscriptions
    for sub in subscriptions:
        if sub.is_active and product.current_price and product.current_price <= sub.target_price:
            message = f"Price Alert! {product.name} is now ${product.current_price} (Target: ${sub.target_price}). Check it out: {product.url}"
            print(f"Notify user {sub.user_id} via {sub.notify_method}!")

            if sub.notify_method in ["EMAIL", "BOTH"]:
                notifier.send_email(sub.user.email, "Price Alert", message)

            if sub.notify_method in ["LINE", "BOTH"] and sub.user.line_token:
                # line_token 欄位現儲存使用者的 Line User ID（Line Messaging API）
                notifier.send_line_message(sub.user.line_token, message)


async def _update_product_price_async(product_id):
    """非同步核心邏輯，負責實際的爬蟲與 DB 更新（單筆更新用）。"""
    db: Session = SessionLocal()
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            return

        print(f"Checking price for: {product.url}")
        details = await crawler.fetch_product_details(product.url)

        if details:
            print(f"Fetched details: {details}")
            _handle_product_price_update(db, product, details)
        else:
            print(f"Failed to fetch details for {product.url}")

    except Exception as e:
        print(f"Error updating product {product_id}: {e}")
    finally:
        db.close()


async def _batch_update_all_prices_async():
    """使用共用的 Browser 實批次更新所有商品價格"""
    from playwright.async_api import async_playwright
    db: Session = SessionLocal()
    try:
        products = db.query(models.Product).all()
        if not products:
            return
            
        print(f"Starting batch price check for {len(products)} products...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-extensions", "--single-process"]
            )
            page = await browser.new_page()
            
            for product in products:
                print(f"Batch checking price for: {product.url}")
                details = await crawler.fetch_product_details(product.url, shared_page=page)
                if details:
                    print(f"Batch fetched details: {details}")
                    _handle_product_price_update(db, product, details)
                else:
                    print(f"Batch failed to fetch details for {product.url}")
                    
                # 休眠一下避免短時間過於頻繁的請求被阻擋
                await asyncio.sleep(3)
                
            await browser.close()
    except Exception as e:
        print(f"Error in batch price check: {e}")
    finally:
        db.close()


def run_batch_check_sync():
    import sys
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_batch_update_all_prices_async())
        finally:
            loop.close()
    else:
        asyncio.run(_batch_update_all_prices_async())


async def check_all_prices():
    """排程任務：更新所有商品的價格。"""
    print("Running scheduled price check using shared browser...")
    await asyncio.to_thread(run_batch_check_sync)


def start_scheduler():
    scheduler.add_job(check_all_prices, 'interval', hours=24)
    scheduler.start()
