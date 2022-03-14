import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from config import FIREBASE_CRED

cred = credentials.Certificate(FIREBASE_CRED)
firebase_admin.initialize_app(cred)
db = firestore.client()