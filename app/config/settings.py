import os

MICROSERVICES = {
    "accounts": f"accounts-g2-dev-424868328181.us-central1.run.app:{os.environ.get('ACCOUNT_SERVICE_PORT')}",
}
