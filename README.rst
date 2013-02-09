===============
Pyclass Twitter
===============

Introduction
============

For todays assignment, I have several co-conspirators that helped me think of a fantastic exercise to flex your python skills. At the sprint, we are tracking tweets with a hashtag "#emeraldsprint". Because we are self-aggrandizing programmers who don't trust twitter to properly archive our tweets, we are requesting that by the end of the weekend we can run a script which sends a multi-part html email with all of the tweets with that hashtag, including images, which must be embedded in the email (not linked) which will then be run and sent to all of the Plone developers as a "sprint report" Monday night.

To complete this, please break into 3 teams and divide up the task: 

- Team 1 will work with the twitter API to get the tweets and put them into a standard data format. Use the api and don't scrape! We have already looked at the twitter api before so I'm not going to give you any hints on where to start this time!
- Team 2 will mock up the html to be emailed given input from Team 1. You *could* use a template library if you are feeling saucy. You could not. Your call. Test the output in a browser for starters.
- Team 3 will take the output from team 2 and send the email, with multi-part attached images. Please take time to investigate what that means (if you aren't sure). We have dealt a little bit with this api before so most of it should be familiar.

The main function signature should be:

.. code-block:: python

	def send_hashtag_report(hashtag, email_to)

Despite working on 3 different teams depending on input, you should be working on your different parts at the same time. 

HINTS
-----

- Set up and work from a github repo where everyone has write access. Kellan - please don't set this up for them this time :) Put each teams work in a separate file to avoid merge conflicts. 
- Put any test cases in a submodule called tests, with a different test file for each module. They should be runnable with nose. It's up to you how many you write - do whats useful for your own and others development first and if time add test cases for correctness.
- Before breaking up, you might want to decide on method signatures and datatypes for integration.
- Since you are working with functions that haven't been written yet, writing your own test cases to make sure things work right will help a LOT.
- Throughout the day, we will be trolling you with tweets to try and break your stuff. Muahaha...

Good luck and may the force be with you!
