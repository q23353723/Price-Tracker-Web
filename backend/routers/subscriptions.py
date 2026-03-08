from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import database, models, schemas, auth, scheduler

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

@router.get("/", response_model=List[schemas.SubscriptionResponse])
def read_subscriptions(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return current_user.subscriptions

@router.post("/", response_model=schemas.SubscriptionResponse)
def create_subscription(
    subscription: schemas.SubscriptionCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.url == subscription.product_url).first()
    
    if not product:
        # 商品不存在，建立暫存資訊（爬蟲後會更新）
        product = models.Product(
            url=subscription.product_url,
            name="資料更新中...",
            website_source="unknown"
        )
        db.add(product)
        db.commit()
        db.refresh(product)
    
    # Check if subscription already exists for this user and product
    existing_sub = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id,
        models.Subscription.product_id == product.id
    ).first()
    
    if existing_sub:
        raise HTTPException(status_code=400, detail="Already subscribed to this product")

    new_subscription = models.Subscription(
        user_id=current_user.id,
        product_id=product.id,
        target_price=subscription.target_price,
        notify_method=subscription.notify_method
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    # 訂閱成功後，無論商品新舊都立即觸發一次爬蟲更新資料
    background_tasks.add_task(scheduler.update_product_price, product.id)

    return new_subscription

@router.put("/{subscription_id}", response_model=schemas.SubscriptionResponse)
def update_subscription(
    subscription_id: str,
    update: schemas.SubscriptionUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """更新訂閱項目的目標價格或通知方式"""
    subscription = db.query(models.Subscription).filter(
        models.Subscription.id == subscription_id,
        models.Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if update.target_price is not None:
        subscription.target_price = update.target_price
    if update.notify_method is not None:
        subscription.notify_method = update.notify_method

    db.commit()
    db.refresh(subscription)
    return subscription

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(
    subscription_id: str, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.id == subscription_id,
        models.Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
