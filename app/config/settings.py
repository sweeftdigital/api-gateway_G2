import os

MICROSERVICES = {
    "accounts": f"accounts:{os.environ.get('ACCOUNT_SERVICE_PORT')}",
}
