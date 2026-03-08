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


async def _update_product_price_async(product_id):
    """非同步核心邏輯，負責實際的爬蟲與 DB 更新。"""
    db: Session = SessionLocal()
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            return

        print(f"Checking price for: {product.url}")
        details = await crawler.fetch_product_details(product.url)

        if details:
            print(f"Fetched details: {details}")
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
        else:
            print(f"Failed to fetch details for {product.url}")

    except Exception as e:
        print(f"Error updating product {product_id}: {e}")
    finally:
        db.close()


async def check_all_prices():
    """排程任務：更新所有商品的價格。"""
    print("Running scheduled price check...")
    db: Session = SessionLocal()
    try:
        products = db.query(models.Product).all()
        # 排程是在 Uvicorn 的 main event loop 執行，在 Windows 可能無法開啟 subprocess
        # 因此透過 asyncio.to_thread 將任務丟到背景執行緒執行，
        # 藉此使用 update_product_price 裡面建立 ProactorEventLoop 的機制
        for product in products:
            await asyncio.to_thread(update_product_price, product.id)
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(check_all_prices, 'interval', hours=24)
    scheduler.start()
