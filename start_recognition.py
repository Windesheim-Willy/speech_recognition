#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Int32
from std_msgs.msg import String
import speech_recognition as sr
import subprocess
import re
import string
from fuzzywuzzy import fuzz

# define needed hit ratio for the resemblance text hallo willy in ratio_willy
ratio_willy = 60
# define needed hit ratio for the resemblance text of the enquete letters in ratio_letter
ratio_letter = 75
# create list with lower case letters of the alphabet
alphabets=list(string.ascii_lowercase)

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
        heard_text = " "
        print("Google Speech Recognition thinks you said: ")
        heard_text = r.recognize_google(audio, language="nl")
        print(heard_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # heard_text is the clear text that is heard on the microphone
    # because the voice, microphone and the google algorithm isn't always correct,
    # we use fuzzy logic to give a number of correctness to the phrase we are looking for
    # if numer is higer that the resemblance ratio defined in ratio_willy, the match is oke
    # publish "1" on topic /interaction/is_active to state that hallo willy is heard
    # publish heard_text on topic /interaction/clear_text
    if fuzz.ratio(heard_text.lower(), 'hallo willy') > ratio_willy:
        print(" ")
        print("Willy says: Hello!")
        pub03.publish(heard_text)
        time.sleep(.5)
        pub01.publish(1)

    # check if heard_text is a letter, probably used in the enquete
    for a in alphabets:
        if fuzz.ratio(heard_text.lower(), a) > ratio_letter:
            print("Willy says: Thanks for " + a)
            pub03.publish(a)

    # for diagnostics reasins allways publish heard text on topic /interaction/clear_text
    # this can later better be changed to a separate topic
    pub03.publish(heard_text)

    rate.sleep()
