#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
import speech_recognition as sr
import subprocess

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

    print("X")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(" ")
        print("Say something! Say Goodbye to stop")
        audio = r.listen(source)
    print("X")
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        heard_text = " "
        print("Google Speech Recognition thinks you said: ")
        heard_text = r.recognize_google(audio)
        print(heard_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# For demo publish all text on topic
    pub03.publish(heard_text)

    if heard_text == "hello willy":
        print(" ")
        print("Willy says: Hello!")
        pub01.publish(1)
    if heard_text == "a":
        print(" ")
        print("Willy says: Thanks for A")
        pub03.publish("A")
    if heard_text == "b":
        print(" ")
        print("Willy says: Thanks for B")
        pub03.publish("B")
    if heard_text == "c":
        print(" ")
        print("Willy says: Thanks for C")
        pub03.publish("C")
    if heard_text == "d":
        print(" ")
        print("Willy says: Thanks for D")
        pub03.publish("D")
    if heard_text == "goodbye":
        print(" ")
        print("Willy says: Goodbye")
        break
    rate.sleep()
