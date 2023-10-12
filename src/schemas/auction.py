from pydantic import BaseModel, Field


class AuctionBase(BaseModel):
    creator: str = Field(title="Creator address of auction", len=42, pattern="(0x[a-fA-F0-9]{40})")
    collection: str = Field(title="Collection address of NFT", len=42, pattern="(0x[a-fA-F0-9]{40})")
    token_id: int = Field(title="Token id of NFT")
    payment_token: str = Field(title="Payment token address", len=42, pattern="(0x[a-fA-F0-9]{40})")
