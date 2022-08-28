import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase/secrets/kavovy-srovnavac-firebase-adminsdk-3xhos-b8ce22cc67.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
coffee_ref = db.collection(u"coffee")


def upload_to_firestore(data: list[dict], uid: str, collection_ref) -> list:
	ret = []
	for d in data:
		ret.append(collection_ref.document(d[uid]).set(d))
	return ret