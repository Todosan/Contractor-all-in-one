from dotenv import load_dotenv
import os
from prisma import Prisma

db = Prisma()

load_dotenv()  # Load variables from .env


