import os

MICROSERVICES = {
    "accounts": f"accounts-g2-dev-ud32gcxh6a-uc.a.run.app:{os.environ.get('ACCOUNT_SERVICE_PORT')}",
}
