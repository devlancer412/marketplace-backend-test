from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    creator = Column(String(42), index=True)
    collection = Column(String(42), index=True)
    token_id = Column(Integer)
    payment_token = Column(String(42), index=True)
    bidder_sig = Column(String(132), default=None)
    amount = Column(BigInteger, default=None)