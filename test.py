from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
vbee_api_key = os.getenv("VBEE_API_KEY")

print("API Key:", vbee_api_key)
