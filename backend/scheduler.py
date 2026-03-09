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
    """
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
    """批次更新所有商品價格 (使用 requests)"""
    db: Session = SessionLocal()
    try:
        products = db.query(models.Product).all()
        if not products:
            return
            
        print(f"Starting batch price check for {len(products)} products using requests...")
            
        for product in products:
            print(f"Batch checking price for: {product.url}")
            details = await crawler.fetch_product_details(product.url)
            if details:
                print(f"Batch fetched details: {details}")
                _handle_product_price_update(db, product, details)
            else:
                print(f"Batch failed to fetch details for {product.url}")
                
            # 休眠一下避免短時間過於頻繁的請求被阻擋
            await asyncio.sleep(3)
                
    except Exception as e:
        print(f"Error in batch price check: {e}")
    finally:
        db.close()


def run_batch_check_sync():
    """以同步方式呼叫非同步的批次作業 (給 Scheduler 背景執行緒使用)"""
    asyncio.run(_batch_update_all_prices_async())


async def check_all_prices():
    """排程任務：更新所有商品的價格。"""
    print("Running scheduled price check using shared browser...")
    await asyncio.to_thread(run_batch_check_sync)


def start_scheduler():
    scheduler.add_job(check_all_prices, 'interval', hours=24)
    scheduler.start()
