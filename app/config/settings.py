import os

MICROSERVICES = {
    "accounts": f"accounts:{os.environ.get('ACCOUNT_SERVICE_PORT')}",
    "auctions": f"auctions:{os.environ.get('AUCTION_SERVICE_PORT')}",
}
