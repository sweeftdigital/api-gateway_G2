import os

MICROSERVICES = {
    "accounts": f"{os.getenv('ACCOUNT_SERVICE_HOST')}:{os.getenv('ACCOUNT_SERVICE_PORT')}",
}
