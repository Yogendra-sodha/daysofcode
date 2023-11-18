from dotenv import load_dotenv

load_dotenv()
import os

print(os.environ.get('FK'))
print(os.environ.get('DATABASE_URI'))
