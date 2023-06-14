import streamlit as st
import requests
import json
import time
# Function to convert image to base64
def get_image_b64_string(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


CSS = """
body {
    color: white;
}
.stApp {
    background-image:  url(https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kaka[…]Fdn%2FoyTFx%2FbtsjZ9JShbN%2F0sDGTMi0lMEJCvVk7FxVA0%2Fimg.png),url(https://images.unsplash.com/photo-1474552226712-ac0f0961a954?ixlib=rb-4.0.3&ixid=M3wxM[…]dlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1742&q=80);
    background-size: 335px, cover;
    background-repeat: no-repeat, no-repeat;
    background-position: right bottom, left top;
    }
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


# st.title('Suicidality Detector')
st.markdown(f"<div style='font-size: 60px; color: White; '><strong>Suicidality Detector</strong></div>", unsafe_allow_html=True)
#WALLPAPER CODE ENDS
# color sequence
color_sequence = ['#AFEEEE', '#48D1CC', '#40E0D0', '#00CED1', '#20B2AA']
# text input cell for users
user_post = st.text_input("Enter Text:")
def classifier(max_val):
    if max_val == 4:
        return {'max_val' : 'Supportive', 'probability' : max_val_p, 'explanation' : 'The author of this text shows empathy toward another person regarding suicidality and offers help or advice',
                'recommendation' : ''}
    elif max_val == 2:
        return {'max_val' : 'Ideation',
                'probability' : max_val_p,
                'explanation' : 'This text contains thoughts about suicide, ranging from passing considerations to detailed plans',
                'recommendation' : 'There is some risk that the author of this text may commit suicide. If you have the opportunity to contact this person, please offer help and refer to local emergency calls or ambulances.'}
    elif max_val == 1:
        return {'max_val' : 'Behavior',
                'probability' : max_val_p,
                'explanation' : 'This text reports actions that are related to suicide but do not constitute an actual attempt, such as preparing to commit suicide.', 'recommendation' : 'The risk that the author of this text will commit suicide is considered high. If you have the opportunity to contact this person, please offer help and refer to local emergency calls or ambulances.'}
    elif max_val == 0:
        return {'max_val' : 'Attempt',
                'probability' : max_val_p,
                'explanation' : 'This text reports a suicide attempt, that is, a specific act with the intention of dying in the process.',
                'recommendation' : 'The risk that the author of this text will commit suicide is considered high. If you have the opportunity to contact this person, please offer help and refer to local emergency calls or ambulances.'}
    elif max_val == 3:
        return {'max_val' : 'Indicator',
                'probability' : max_val_p,
                'explanation' : 'This text indicates a potential suicide risk without specifically mentioning suicide.',
                'recommendation' : 'There is some risk that the author of this text may commit suicide. If you have the opportunity to contact this person, please offer help and refer to local emergency calls or ambulances.'}
    else:
        return {'max_val' : 'error', 'probability' : 'error', 'explanation' : 'error'}
# button uses the fast_predict function to get a prediction
if st.button("Analyze"):
    #st.markdown(user_post)
     # This will add a message "Please wait..."
    with st.empty():
        with st.spinner('Analyzing...'):
            time.sleep(5)
            url = 'https://suicidalitydetectorfast-vgublbx6qq-ew.a.run.app/predict'  # uvicorn web server url
            params= {'post': user_post}
            response = requests.get(url, params=params)
            results = response.json()[0]
            max_val = int(results['max_val'])
            max_val_p = float(results['max_val_p'])
            st.success('Analysis complete')
            #st.experimental_rerun() # This will clear the "Please wait..." message.
            prediction = classifier(max_val)
    st.markdown(f"<h2 style='font-size: 50px; text-align: center; color: red;'><strong>{prediction['max_val']}</strong></h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # space
    st.markdown(f"<div style='font-size: 20px; color: black; '><strong>{prediction['explanation']}</strong></div>", unsafe_allow_html=True)
    if prediction['recommendation']:
        if prediction['max_val'] in ['Ideation', 'Indicator']:
            st.markdown("<br>", unsafe_allow_html=True)  # space
            st.markdown("<br>", unsafe_allow_html=True)  # space
            st.markdown(f"<div style='font-size: 20px; color: black;'><strong>{prediction['recommendation']}</strong></div>", unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True)  # space
            st.markdown("<br>", unsafe_allow_html=True)  # space
            st.markdown(f"<div style='font-size: 20px; color: red;'><strong>{prediction['recommendation']}</strong></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # space
    st.markdown("<br>", unsafe_allow_html=True)  # space
    st.markdown("<div style='font-size: 20px; color: black;'><strong><em>This assessment is based on an AI analysis and can not replace a psychiatric or psychological evaluation.</em></strong></div>", unsafe_allow_html=True)
