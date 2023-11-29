import random
import streamlit as st 
from yt_extractor import get_youtube_video_info
from database_service import HandleDb
from database_service import VideoHandler

COLLECTION = "tutorials"
COLLECTION_TODAY = "tutorial_today"

def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text

def show_video(collection):
    db_handler = HandleDb(collection)
    all_vids_id = []
    for doc in db_handler.get_data():
        vids = doc.to_dict()
        url = "https://youtu.be/" + vids["video_id"]
        st.markdown(f"#### {vids['title']}")
        st.video(url)
        st.text(f"{vids['channel']} - {get_duration_text(vids['duration'])}")
        del_stat = st.button('Delete Tutorial', key = vids["video_id"])
        if del_stat:
            db_handler.delete_tutorial(vids["video_id"])
            st.experimental_rerun()
        all_vids_id.append(vids["video_id"])
    return all_vids_id
 
def update_todays(collection, collection_today):
    main_db = HandleDb(collection)
    # Get all documents from the main collection
    all_docs = main_db.get_data()
    # Check if there are any documents in the collection
    if not all_docs:
        print("Error: No documents found in the main collection.")
        return
    # Get a random index
    idx = random.randint(0, len(all_docs) - 1)
    # Get the random document
    rand_doc = all_docs[idx]
    # Get the document ID (assuming the document ID is used as the rand_doc_name)
    rand_doc_name = rand_doc.id
    # Update the tutorial today with data from the random document
    db_handler_today = HandleDb(COLLECTION_TODAY, rand_doc_name)
    db_handler_today.update_tutorial_today(collection, insert=False)
           
st.title("Tutorials APP")

menu_options = ("Today's tutorial", "All tutorials", "Add tutorial", "Register")

selection = st.sidebar.selectbox("Menu", menu_options)

if selection == "All tutorials":
    st.markdown(f"## All tutorials")
    show_video(COLLECTION)

 
elif selection == "Add tutorial":
    st.markdown(f"## Add tutorial")
    video_url = st.text_input('Please enter the video url')
    if video_url:
        video_handler = VideoHandler(video_url)
        video_handler.process_video_info()
        
elif selection == "Register":
    st.markdown(f'Register for getting updates and motivations')
    name = st.text_input('Enter your full name:')
    mail = st.text_input('Enter your email address:')
    
    # this will continue...
    
else:
    st.markdown(f"## Today's tutorial")
    x = show_video(COLLECTION_TODAY)
    update_stat = st.button('Get Random Tutorial', key = x)
    if update_stat:
        update_todays(COLLECTION, COLLECTION_TODAY)
            

    
    
    
    
    # n = len()
    # db_handler_today = HandleDb(COLLECTION_TODAY, 'vusUfPBsggw')
    # db_handler_today.update_tutorial_today(COLLECTION, insert=False)
    # show_video(COLLECTION_TODAY)
    
