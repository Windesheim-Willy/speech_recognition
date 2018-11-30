#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
import speech_recognition as sr
import subprocess
import re
from fuzzywuzzy import fuzz

# define needed hit ratio for the resemblance text hallo willy in ratio_willy
ratio_willy = 60
# define needed hit ratio for the resemblance text of the enquete letters in ratio_letter
ratio_letter = 75

# To which topic on Willy we will publish
willy_topic_name01 ='/interaction/is_active'
willy_topic_name02 ='/interaction/action'
willy_topic_name03 ='/interaction/clear_text'

rospy.init_node('speech_fetcher')
pub01 = rospy.Publisher(willy_topic_name01, Int32 ,queue_size=25)
pub02 = rospy.Publisher(willy_topic_name02, Int32 ,queue_size=25)
pub03 = rospy.Publisher(willy_topic_name03, String ,queue_size=25)

rate = rospy.Rate(2)
count = 0

while not rospy.is_shutdown():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(" ")
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        heard_text = " "
        print("Google Speech Recognition thinks you said: ")
        heard_text = r.recognize_google(audio, language="nl")
        print(heard_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    pub03.publish(heard_text)

    # heard_text is the clear text that is heard on the microphone
    # because the voice, microphone and the google algorithm isn't always correct,
    # we use fuzzy logic to give a number of correctness to the phrase we are looking for

    if fuzz.ratio(heard_text.lower(), 'hallo willy') > ratio_willy:
        print(" ")
        print("Willy says: Hello!")
        pub01.publish(1)
    if fuzz.ratio(heard_text.lower(), 'a') > ratio_letter:
        print(" ")
        print("Willy says: Thanks for A")
        pub03.publish("A")
    if fuzz.ratio(heard_text.lower(), 'b') > ratio_letter:
        print(" ")
        print("Willy says: Thanks for B")
        pub03.publish("B")
    if fuzz.ratio(heard_text.lower(), 'c') > ratio_letter:
        print(" ")
        print("Willy says: Thanks for C")
        pub03.publish("C")
    if fuzz.ratio(heard_text.lower(), 'd') > ratio_letter:
        print(" ")
        print("Willy says: Thanks for D")
        pub03.publish("D")
    rate.sleep()
