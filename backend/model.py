from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    CHAR,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# Application User Model
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100))


# ---------------------------------------------------------
# Olist E-Commerce Dataset Models
# ---------------------------------------------------------
class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    customer_id: Mapped[str] = mapped_column(CHAR(32), primary_key=True)
    customer_unique_id: Mapped[str] = mapped_column(CHAR(32), index=True)
    customer_zip_code_prefix: Mapped[str] = mapped_column(String(10))
    customer_city: Mapped[str] = mapped_column(String(100))
    customer_state: Mapped[str] = mapped_column(String(10))

    # Relationships
    orders: Mapped[List["Order"]] = relationship(back_populates="customer")


# Alias for backwards compatibility
Customers = Customer


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    order_id: Mapped[str] = mapped_column(CHAR(32), primary_key=True)
    customer_id: Mapped[str] = mapped_column(
        CHAR(32),
        ForeignKey("customers.customer_id"),
        index=True,
        comment="Link to customers.customer_id",
    )
    order_status: Mapped[str] = mapped_column(String(50))
    order_purchase_timestamp: Mapped[datetime] = mapped_column(DateTime)
    order_approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    order_delivered_carrier_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    order_delivered_customer_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    order_estimated_delivery_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
    payments: Mapped[List["OrderPayment"]] = relationship(back_populates="order")
    reviews: Mapped[List["OrderReview"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    order_id: Mapped[str] = mapped_column(
        CHAR(32),
        ForeignKey("orders.order_id"),
        primary_key=True,
    )
    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[str] = mapped_column(
        CHAR(32),
        ForeignKey("products.product_id"),
        index=True,
    )
    seller_id: Mapped[str] = mapped_column(
        CHAR(32),
        ForeignKey("sellers.seller_id"),
        index=True,
    )
    shipping_limit_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    freight_value: Mapped[float] = mapped_column(Float)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped[Optional["Product"]] = relationship(back_populates="order_items")
    seller: Mapped[Optional["Seller"]] = relationship(back_populates="order_items")


class OrderPayment(Base):
    __tablename__ = "order_payments"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    order_id: Mapped[str] = mapped_column(
        CHAR(32),
        ForeignKey("orders.order_id"),
        primary_key=True,
    )
    payment_sequential: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_type: Mapped[str] = mapped_column(String(50))
    payment_installments: Mapped[int] = mapped_column(Integer)
    payment_value: Mapped[float] = mapped_column(Float)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="payments")


class OrderReview(Base):
    __tablename__ = "order_reviews"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    review_id: Mapped[str] = mapped_column(CHAR(32), primary_key=True)
    order_id: Mapped[str] = mapped_column(
        CHAR(32),
        ForeignKey("orders.order_id"),
        primary_key=True,
        index=True,
    )
    review_score: Mapped[int] = mapped_column(Integer)
    review_comment_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    review_comment_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    review_creation_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    review_answer_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="reviews")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    product_id: Mapped[str] = mapped_column(CHAR(32), primary_key=True)
    product_category_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    product_name_lenght: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    product_description_lenght: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    product_photos_qty: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    product_weight_g: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    product_length_cm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    product_height_cm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    product_width_cm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")


class Seller(Base):
    __tablename__ = "sellers"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    seller_id: Mapped[str] = mapped_column(CHAR(32), primary_key=True)
    seller_zip_code_prefix: Mapped[str] = mapped_column(String(10))
    seller_city: Mapped[str] = mapped_column(String(100))
    seller_state: Mapped[str] = mapped_column(String(10))

    # Relationships
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="seller")


class Geolocation(Base):
    __tablename__ = "geolocation"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    geolocation_zip_code_prefix: Mapped[str] = mapped_column(String(10), index=True)
    geolocation_lat: Mapped[float] = mapped_column(Float)
    geolocation_lng: Mapped[float] = mapped_column(Float)
    geolocation_city: Mapped[str] = mapped_column(String(100))
    geolocation_state: Mapped[str] = mapped_column(String(10))


class ProductCategoryTranslation(Base):
    __tablename__ = "product_category_name_translation"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
    }

    product_category_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    product_category_name_english: Mapped[str] = mapped_column(String(100), nullable=False)
