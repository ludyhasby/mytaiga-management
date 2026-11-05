import os 
from dotenv import load_dotenv

def LoadEnv():
    load_dotenv()
    secretKey = os.getenv("SECRET_KEY")
    maxAttempts = os.getenv("MAX_ATTEMPTS")
    lockoutSeconds = os.getenv("LOCKOUT_SECONDS")
    return {
        "secretKey" : secretKey, 
        "maxAttempts" : maxAttempts, 
        "lockoutSeconds": lockoutSeconds
    }