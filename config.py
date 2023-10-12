from app.__internal import ConfigBase


class Configuration(ConfigBase):
    # database config
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"
    DATABASE: str = "marketplace-backend"

    MARKETPLACE_ADDRESS: str = "0x597C9bC3F00a4Df00F85E9334628f6cDf03A1184"
    RPC_URL: str = "https://ethereum-sepolia.publicnode.com"


# --- Do not edit anything below this line, or do it, I'm not your mom ----
defaults = Configuration(autoload=False)
cfg = Configuration()
