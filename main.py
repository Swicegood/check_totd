#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Load environment variables
load_dotenv()

# Use the loaded environment variable for Firebase authentication
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

def check_firestore():
    # Reference to your collection
    collection_ref = db.collection(u'thought-of-the-days')
    
    # Get the timestamp for 5 days ago
    five_days_ago = datetime.now() - timedelta(days=5)
    
    # Create a query against the collection
    from google.cloud.firestore import Query

    query = collection_ref.where('processed', '>=', five_days_ago).order_by('processed', direction=Query.DESCENDING)
    
    # Retrieve query results
    docs = query.stream()
    for doc in docs:
        doc_dict = doc.to_dict()  # Convert the document to a dictionary
        print(f'{doc.id} => {doc_dict["date"]}')  # Access the 'date' field from the dictionary
        return True
    return False


# Main script logic
if __name__ == "__main__":
    # CHeeck is there is any doc in thought of hte day with date < 5 days ago
    result = check_firestore()
    if result:
        # put into result file /result/result.txt
        with open('./result/result.txt', 'w') as f:
            f.write('"localhost\tThought Of The Day\t0\tOK: There is a thought of the day in the last 5 days."')
        print("OK: There is a thought of the day in the last 5 days.")
        print("Check the result file at /result/result.txt")
    else:    
        with open('./result/result.txt', 'w') as f:
            f.write('"localhost\tThought Of The Day\t2\tCRITICAL: There is no thought of the day in the last 5 days."')
        print("CRITICAL: There is no thought of the day in the last 5 days.")
        print("Check the result file at /result/result.txt")
