import streamlit as st
import speech_recognition as sr
from collections import OrderedDict
import SessionState
import os
import openai
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from PIL import Image



st.set_page_config(page_title='QuickDoc', page_icon = ":heart:", layout = 'wide', initial_sidebar_state = 'auto')



openai.api_key = "empty"
 
doctors = {
    "mike" : "empty",
    "harvey" : "empty",
    "charlie" : "empty",
    "bob" : "empty",
    "ava" :"empty",
    "zoe" : "empty"
}


def takeName():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please state your first and last name")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            #st.write("Your name is :",text)
        except:
            st.write("Please say again ..")
            return ""
        return text
        
def takeDoctor():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please state your doctors last name")
        audio=r.listen(source)
        doctor_name=""
        try:
            text=r.recognize_google(audio)
            text=text.lower()
            for key in doctors:
                if key in text:
                    doctor_name = key
            if doctor_name is "":
                st.write("This Doctor does not work at this hospital")
                st.write("Please say again ..")
                return ""
            #st.write("Your doctor is :",doctor_name.upper())
        except:
            st.write("Please say again ..")
            return ""
        return doctor_name
    
def takeSymptoms():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please explain what you would like to discuss with your doctor")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
           # st.write("You  said :",text)
        except:
            st.write("Please say again ..")
            return ""
        return text

def takeEmail():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please state your email address")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
           # st.write("You  said :",text)
        except:
            st.write("Please say again ..")
            return ""
        return text
        
def send_mail(name, doctor, purpose, email):
    sender_email = "empty"
    receiver_email = email
    password = "empty"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Appointment for "+name
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
    Patient Name: """ + name +"""
    
    Email: """ + email + """
    
    Doctor: """ + doctor +"""
    
    Purpose of Appointment: """+ purpose
    
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a>
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    #part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    #message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    

if __name__ =="__main__":
    st.markdown("<p style = 'font-size:80px; color: red;font-family: Monospace; background-color:powderblue;'> <center>&#10084 <b>The eDoctor</b></center> </p>", unsafe_allow_html=True)
    
    st.header("")
    
    col1,col2 = st.beta_columns(2)
    col1.markdown("<p style = 'font-size: 30px; color: black; font-family: Monospace;'> Easily connect with your doctor</p> <p><i>We at Hospital XYZ are commited to ensuring our patients get the best care during these difficult times. Filling out the fields below will help expediate your experience at the hospital, limiting your contact with others. <i></p>", unsafe_allow_html=True)
    
    #og = Image.open("./doctorimage.jpg")
    #col2.image(og, use_column_width = True)
    col2.markdown("<center><img src='https://i.pinimg.com/originals/2c/ea/fb/2ceafb64a5dae55d2a61ef5e12be6e5f.gif' alt='Computer man' style='width:230px;height:350px;'></center>",unsafe_allow_html = True)
    
    st.write("")
    st.markdown( "<p style = 'font-size: 50px; color: #F80000; font-family: Monospace; background-color: lightblue;'> <center> Contact your Doctor </center> </p>", unsafe_allow_html=True)
    
    st. markdown("<p style = 'font-size: 20px; color: black;'> Fill out the following fields by either clicking the record buttons to state the required information or typing in the content in the fields.</p>", unsafe_allow_html=True)
    
    st.write("")
    
    patient_input = st.text_input("Please type in your name or record your name below")
    if st.button("Record your Name"):
        patient = takeName()
        if patient is not "":
            patient_name=open('./patient_name.txt','w')
            patient_name.write(patient)
            patient_name.close()
    elif patient_input is not "":
        patient_name=open('./patient_name.txt','w')
        patient_name.write(patient_input)
        patient_name.close()
        
    st.write("")
    email_input = st.text_input("Please type in your email or record it below")
    if st.button("Record your Email"):
        email = takeEmail()
        if email is not "":
            email_name=open('./email_name.txt','w')
            email_name.write(email)
            email_name.close()
    elif email_input is not "":
        email_name=open('./email_name.txt','w')
        email_name.write(email_input)
        email_name.close()
        
    st.write("")
    doctor_input = st.text_input("Please type in the name of your doctor or record their name below")
    if  st.button("Record Doctor's Name"):
        doctor=takeDoctor()
        if doctor is not "":
            doctor_name=open('./doctor_name.txt','w')
            doctor_name.write(doctor)
            doctor_name.close()
    elif doctor_input is not "":
        doctor_last_name=""
        for key in doctors:
            if key in doctor_input.lower():
                doctor_last_name = key
        if doctor_last_name is "":
            st.write("This Doctor does not work at this hospital")
            st.write("Please try again ..")
        else:
            doctor_name=open('./doctor_name.txt','w')
            doctor_name.write(doctor_last_name)
            doctor_name.close()

    st.write("")
    purpose_input = st.text_area("Please type in or record the purpose for which you want to schedule your appointment. Please include any symptoms or any conerns you might have")
    if st.button("Record Purpose of Visit"):
        purpose = takeSymptoms()
        if purpose is not "" :
            purpose_of_visit=open('./purpose.txt','w')
            purpose_of_visit.write(purpose)
            purpose_of_visit.close()
    elif purpose_input is not "" :
        purpose_of_visit=open('./purpose.txt','w')
        purpose_of_visit.write(purpose_input)
        purpose_of_visit.close()
    
    email=""
    patient = ""
    doctor =""
    purpose=""
    st.write("")
    
    st.markdown( "<p style = 'font-size: 40px; color: #F80000; font-family: Monospace; background-color: lightblue;'> <center> Content being sent <center></p>", unsafe_allow_html=True)
    col1, col2,col3,col4 = st.beta_columns(4)
    col1.subheader('Patient')
    col2.subheader('Email')
    col3.subheader('Doctor')
    col4.subheader("Purpose")
    
    
   
    try:
        remember= open('./patient_name.txt', 'r')
        patient=remember.read().upper()
        col1.write(patient)
        patient = "Given the following prompt answer the question:\n\n\"\"\"\n" + patient +"\n\"\"\"\n\nQ:What is the patients name?\n\nA:"
    except:
            col1.write("Patient Name: N/A")
    
    try:
        remember= open('./email_name.txt', 'r')
        email=remember.read().lower()
        email = email.replace('at', '@')
        email = email.replace(' ','')
        col2.write(email)
    except:
        col2.write("Email Name: N/A")

    try:
        remember= open('./doctor_name.txt', 'r')
        doctor=remember.read().upper()
        col3.write(doctor)
        doctor = "Given the following prompt answer the question:\n\n\"\"\"\n" + doctor +"\n\"\"\"\n\nQ:What is the doctors name?\n\nA:"
    except:
        col3.write("Doctor Name: N/A")

    
    try:
        remember= open('./purpose.txt', 'r')
        purpose=remember.read()
        col4.write(purpose)
        purpose = purpose+"\n\ntl;dr:"
    except:
        col4.write("Purpose of Visit: N/A")
        
    
    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "
    
    if patient is not "":
        response = openai.Completion.create(
          engine="davinci",
          prompt=patient,
          temperature=0,
          max_tokens=4,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=["\n"]
        )
    
        final_patient_details = response["choices"][0]["text"]
    
    if doctor is not "":
        response = openai.Completion.create(
          engine="davinci",
          prompt=doctor,
          temperature=0,
          max_tokens=4,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=["\n"]
        )
        
        #st.write(response["choices"][0]["text"])
        final_doctor_details = response["choices"][0]["text"]
    
    if purpose is not "":
        response = openai.Completion.create(
          engine="davinci",
          prompt=purpose,
          temperature=0.3,
          max_tokens=64,
          top_p=1,
          frequency_penalty=1.0,
          presence_penalty=0,
          stop=["\n"]
        )
        
        send_info = response["choices"][0]["text"]
        
    if st.button("Send info to doctor"):
        if patient == "" or doctor =="" or purpose=="" or email =="":
            st.write("Not all fields are complete, please complete all fields before emailing")
        else:
            with st.spinner('Sending...'):
                for key in doctors:
                    if key in doctor.lower():
                        email = doctors[key]
                send_mail(final_patient_details, final_doctor_details, send_info,email)
            st.success('Email sent!')
            st.balloons()
    st.write("")
    
    st.markdown( "<p style = 'font-size: 50px; color: #F80000; font-family: Monospace; background-color: lightblue;'> <center> FAQ <center></p>", unsafe_allow_html=True)
    col1,col2 = st.beta_columns(2)
    col1.header("Ask questions here!")
    question = col1.text_area("Fill in the box and click submit to see the answer to your question")
    response =""
    prompt ="Based on the following prompt, answer the question:\n\n\"\"\"\nThis Hospital's name is Hospital XYZ. The hospital's address is 1234 Random Richardson, TX 75080. The hospital has 400 doctors and nurses. There is a 24-hour emergency room. Our goal is to provide excellent patient service and outstanding quality of care.\n\"\"\"\n\nQ: "+question+"?\nA:"
    if col1.button("Ask"):
        response = openai.Completion.create(
          engine="davinci",
          prompt=prompt,
          temperature=0,
          max_tokens=15,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=["\n"]
        )
    if response is not "":
        col2.markdown("<p style = 'font-size:30px; color: black;font-family: Monospace;'><center><i>"+response["choices"][0]["text"]+"</i></center></p>", unsafe_allow_html=True)
    else:
        col2.markdown("<p style = 'font-size:30px; color: black;'><center>Nothing yet!</center></p>", unsafe_allow_html=True)
    
    
    
        
    
    

   

        
        
        
    
            
    
   
        
    
