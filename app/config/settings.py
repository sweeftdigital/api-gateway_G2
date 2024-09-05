import os

MICROSERVICES = {
    "accounts": f"{os.getenv('ACCOUNTS_API_HOST')}:{os.getenv('ACCOUNTS_API_PORT')}",
}
