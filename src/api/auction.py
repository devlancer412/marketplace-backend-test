from __future__ import annotations
from typing import Callable, List, Annotated
from app.__internal import Function
from fastapi import (
    FastAPI,
    APIRouter,
    status,
    HTTPException,
    Depends,
    Query,
    Path
)
from sqlalchemy.orm import Session
from operator import and_


from src.schemas.auction import AuctionBase
from src.models import Auction
from src.deps.database import get_db_session

from src.utils.web3 import check_nft_ownable, check_nft_approvement, check_bidder_sig, check_token_allowance


class AuctionAPI(Function):
    def __init__(self, error: Callable):
        self.log.info("auction apis")

    def Bootstrap(self, app: FastAPI):
        router = APIRouter(
            prefix="/auction",
            tags=["auction"],
            responses={404: {"description": "Not found"}},
        )

        @router.get("/list", summary="get all auctions")
        async def get_all_auctions(
            offset: int = Query(
                default=0, description="offset for pagination"),
            limit: int = Query(
                default=10, description="limit for pagination"),
            session: Session = Depends(get_db_session),
        ):
            auctions: List[Auction] = (
                session.query(Auction).offset(offset).limit(limit).all()
            )

            return auctions
        
        @router.get("/{id}", summary="get an auction")
        async def get_auction(
            id: int = Annotated[int, Path(title="The ID of the auction to get", ge=1)],
            session: Session = Depends(get_db_session),
        ):
            auction: Auction = (
                session.query(Auction).filter(Auction.id == id).first()
            )

            if auction is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Can't find such auction")

            return auction

        @router.post("/", summary="create an auction")
        async def create_auction(
            data: AuctionBase,
            session: Session = Depends(get_db_session),
        ):
            auction = (
                session.query(Auction)
                .filter(
                    and_(
                        and_(
                            Auction.collection == data.collection, 
                            Auction.token_id == data.token_id
                        ), 
                        Auction.creator == data.creator
                    )
                )
                .first()
            )
            if auction is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Auction with this NFT already exist",
                )
            
            if check_nft_ownable(data.collection, data.token_id, data.creator) is False:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Creator is not owner of this NFT",
                )
        
            if check_nft_approvement(data.collection, data.token_id, data.creator) is False:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Creator should approve NFT to create auction",
                )
        
            auction = Auction()
            auction.creator = data.creator
            auction.collection = data.collection
            auction.token_id = data.token_id
            auction.payment_token = data.payment_token

            session.add(auction)
            session.flush()
            session.commit()
            session.refresh(auction, attribute_names=["id"])

            return auction

        @router.put("/{id}", summary="bid to auction")
        async def bid(
            id: int = Annotated[int, Path(title="The ID of auction", ge=1)],
            amount: int = Query(title="Bid amount"),
            bidder_sig: str = Query(title="Signature of bidder", regex="(0x[a-fA-F0-9]{130})"),
            session: Session = Depends(get_db_session),
        ):
            auction: Auction = (
                session.query(Auction)
                .filter(Auction.id == int(id))
                .first()
            )

            if auction is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Can't find such auction")

            if auction.amount is not None:
                if auction.amount >= amount:
                    raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                        detail="Underpriced amount")
                
            if check_nft_ownable(auction.collection, auction.token_id, auction.creator) is False or check_nft_approvement(auction.collection, auction.token_id, auction.creator) is False:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Auction already finished")
            
            bidder: str;
            try:
                bidder = check_bidder_sig(auction.collection, auction.payment_token, auction.token_id, amount, bidder_sig)
            except Exception:
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid parameter")
            
            if check_token_allowance(auction.payment_token, amount, bidder) is False:
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid signature or insufficient payment token allowance")

            
            auction.bidder_sig = bidder_sig
            auction.amount = amount

            session.commit()
            session.refresh(auction)

            return auction
            

        app.include_router(router)