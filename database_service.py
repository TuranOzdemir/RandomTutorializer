import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



COLLECTION = "tutorials"
COLLECTION_TODAY = "tutorial_today"

if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()
""" 
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
 """
class HandleDb():
    def __init__(self, col_name, doc_name = None):
        self.col_name = col_name
        self.doc_name = doc_name
        
    
    def insert_tutorial(self, data):
        db.collection(self.col_name).document(self.doc_name).set(data)
    
    def delete_tutorial(self, selected_doc_name):
        db.collection(self.col_name).document(selected_doc_name).delete()
    
    def update_tutorial_today(self, collection_name, insert=False):
        if '_today' in self.col_name:
            try:
                # Fetch the update data from the 'tutorials' collection
                tutorials_ref = db.collection(collection_name).document(self.doc_name)
                tutorials_doc = tutorials_ref.get()

                if tutorials_doc.exists:
                    # Extract the data from the 'tutorials' document
                    update_data = tutorials_doc.to_dict() 
                    # Update the 'tutorial_today' document
                    doc_ref = db.collection(self.col_name).document('today')
                    doc_ref.set(update_data)
                    # I can use pop up or something else to tell 'updated successfully'
                    '''print(f"Document {'today'} updated successfully with data from 'tutorials'.")'''
                else:
                    raise ValueError(f"Error: Document {'today'} not found in 'tutorials' collection.")

                # Optionally, insert a new document if it doesn't exist
                if not doc_ref.get().exists and insert:
                    doc_ref.set(update_data)
                    print(f"New document {'today'} inserted successfully.")
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            raise ValueError("Error: '_today' not found in col_name.")

    def get_data(self):
        docs = db.collection(self.col_name).get()
        # docs.to_dict()
        return docs
            


class VideoHandler:
    def __init__(self, video_url):
      self.video_url = video_url
      self.video_info = get_youtube_video_info(video_url)
    
    def process_video_info(self):
        if "Error" in self.video_info:
            return False
        else:
            doc_id = self.video_info['video_id']
            data = self.video_info                
            db_handler = HandleDb(COLLECTION, doc_id)
            db_handler.insert_tutorial(data)
            return True
        
    def get_video_id(self):
        return self.video_info['video_id']

from yt_extractor import get_youtube_video_info

# This is an exp about how to add data:    
'''
addMe = HandleDb('persons', 'ytb')
addMe.insert_tutorial(data)
'''

# adding new video to tutorials
'''
video_url = "https://youtu.be/0tM-l_ZsxjU?si=R6xPBawSeQzodwKd"
video_handler = VideoHandler(video_url)
video_handler.process_video_info()
'''
# deleting tutorial from tutorials
'''
db_handler = HandleDb(COLLECTION,'KMkmA4i2FQc')
db_handler.delete_tutorial()
'''
# update tutorial
'''
db_handler_today = HandleDb(COLLECTION_TODAY, 'vusUfPBsggw')
db_handler_today.update_tutorial_today(COLLECTION, insert=False)
'''
# get all data one by one 
""" 
db_handler = HandleDb(COLLECTION)
for doc in db_handler.get_data():
    print(doc.to_dict()['video_id'])
"""