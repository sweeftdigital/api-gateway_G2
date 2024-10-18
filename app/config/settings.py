import os

MICROSERVICES = {
    "accounts": f"{os.getenv('ACCOUNT_SERVICE_HOST')}:{os.getenv('ACCOUNT_SERVICE_PORT')}",
    "auctions": f"{os.getenv('AUCTION_SERVICE_HOST')}:{os.getenv('AUCTION_SERVICE_PORT')}",
}
