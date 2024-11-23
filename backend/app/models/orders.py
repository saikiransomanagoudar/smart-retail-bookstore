from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from backend.app.database.database import Base, SessionLocal
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, List
import uuid

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)  # Added to group items from same order
    user_id = Column(String, ForeignKey('user_preferences.user_id'))
    title = Column(String)
    price = Column(Float)
    total_quantity = Column(Integer, default=1)

    # Address fields
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    # Payment fields
    card_number = Column(String)  # Store last 4 digits only
    expiry_date = Column(String)

    # Dates
    purchase_date = Column(DateTime, default=datetime.utcnow)
    expected_shipping_date = Column(DateTime)

    @classmethod
    def create_order(cls, cart_items: List[Dict[str, Any]], order_data: Dict[str, Any]) -> tuple[bool, str]:
        try:
            db = SessionLocal()
            # Generate a single order_id for all items in this order
            order_id = str(uuid.uuid4())
            purchase_time = datetime.utcnow()
            expected_delivery = purchase_time + timedelta(days=5)

            # Create an order item for each cart item with the same order_id
            for item in cart_items:
                new_order = cls(
                    order_id=order_id,  # Same order_id for all items in this order
                    user_id=order_data.get('user_id'),
                    title=item.get('title'),
                    price=float(item.get('Price', 0)),
                    total_quantity=int(item.get('quantity', 1)),
                    street=order_data.get('street'),
                    city=order_data.get('city'),
                    state=order_data.get('state'),
                    zip_code=order_data.get('zip_code'),
                    card_number=f"****{order_data.get('card_number')[-4:]}",
                    expiry_date=order_data.get('expiry_date'),
                    purchase_date=purchase_time,
                    expected_shipping_date=expected_delivery
                )
                db.add(new_order)

            db.commit()
            db.close()
            return True, order_id

        except Exception as e:
            logging.error(f"Error creating orders: {str(e)}")
            if 'db' in locals():
                db.rollback()
                db.close()
            return False, str(e)