The GDS CTF Platform
==============

The Government Digital Service ran a CTF for security enthusiasts from across Government (The Cross Government CTF, or X-GOV-CTF).  We wanted a platform on which to host the questions, and so this platform was born.

Much of this platform is based on the picoCTF platform, which was designed to be easily adapted to other CTF or programming competitions.

Setting Up
------------
1. Download VirtualBox (easiest, though others can work)
2. Download Vagrant (vagrantup.com)
3. `vagrant up` inside the repo
4. Wait until completion
5. `vagrant ssh` to connect to the VM
6. Run `devploy` to deploy the development version of the site
7. Go to port 8080 on the Host Machine

The Website
-----------

We ran the platform on AWS, on an Ubuntu 16.10 server.  

Note that we ran the event inside our building, with a server that was only accessible to people present.  We therefore modified the platform from the original in the following ways (which might be unsafe if you run this on the public internet):

The X-GOV-CTF needed to look like a GDS themed website if possible.  The security team had little expertise in CoffeeScript, which the picoCTF website was written in, and so @bruntonspall decided to write a frontend in Python and Flask.

Due to the extremely short timelines, and for what seemed like a good idea at the time, the new web frontend was run separately to the old python flask API.

It seemed sensible to maintain running the API as unaltered, and to simply front the API with a static website.  With hindsight, we probably should have written the website in the existing Flask python application, and removed the public API work.

The website asks for registration details, covering name and email address only.  We weren't running this publicly or remotely on the web, and as such many of the other fields are unnecessary.

We made a few modifications to the vagrant setup and devploy scripts, to update to a new version of rails and eventually to remove all the coffee script website requirements.  The vagrant setup still contains some code that needs cleaning up.

You should be able to setup the server as below, and access the frontend web through the normal means.  You can also access the undocumented URL /apis/<path> to direct a request to the backend API (mostly for debugging).

API Authentication
------------------

This was an interesting problem to solve in a hurry.  In the original coffeescript version, the users browser did the login and authentication directly against the API, not against the server.  When our frontend proxied the login, we discovered that we couldn't make requests to the backend API as expected.

This turned out to be a combination of cookies, the token cookie, and the flask session cookie, both of which are necessary to make a request to the API.

This web frontend simply stores both the API flask session cookie and the token in the web frontend's flask session cookie, and then on each request, gets them back out and uses them to make the API call on the users behalf.

Cache
-----

The original API was clearly directly accessible and was intended to be web hosted, and as such many of the calls were wrapped in cache decorators that cached the results, sometimes forever and sometimes for just a period of time.

Because we weren't implementing every user journey or feature of the original, the caches didn't work as expected, so for the purpose of the CTF, we simply removed all the caches.

If we were going to setup a public facing version of this service, we would have to re-address this problem, and put caches in the right place.

Loading the Example Problems (In the vagrant VM)
------------
*note*: We modified the devploy script to regenerate these problems every time.  This is because for the majority of the time we were adjusting the problems

1. Run `cd ~/api`
2. Run `python3 api_manager.py -v problems load /vagrant/example_problems/ graders/ ../problem_static/`
3. Run `python3 api_manager.py autogen build 100`
4. Run `devploy`

Getting Started
---------------

A detailed explanation of the basics of the picoCTF Platform 2 can be found in our [Getting Started Guide](GettingStarted.md).

We haven't modified this at all, and we found it helpful when writing our own problems.

Contributing and TODO's
------------

We don't know if we'll need to run another CTF, so while contributions are welcome, this isn't under active development.

There should be some issues that need addressing:

1. The scoreboard doesn't add up both achievements and scores for teams.
2. The system is entirely uncached and unprotected, so attack the CTF platform itself is probably trivial
3. The vagrantfile and the setup instructions are not ideal.  A simpler, smaller vagrant machine would be ideal, and some form of config management for setting up the server would be sensible.
4. The web site and the API should be the same server.  There's a lot of things you can't do easily in the web site that would be easier if you could use the internal API rather than the public API
5. An admin page would be ideal, showing progression, which teams have unlocked which problems and so forth.
6. The hints system and feedback system could do with being properly implemented

There are some issues that are probably with picoCTF itself that could do with fixing, or improving.

1. The grader/generator python file locations and description in the json aren't really very obvious.  It's also very difficult to share code between them, so a shared crypto library or something.
2. The generator updating the description makes sense, but it makes updating the descriptions difficult when some are in json and some in generator.py
3. The weightmap and threshold features are really cool and powerful, but if you just want incrementing puzzles in a category are overkill, and can create bugs
4. Running the autogen by hand rather than dynamically seems odd.  A system that generates a new instance on demand, as teams get access to the problem seems more sensible, unless generation is going to be long and slow for 1 instance.
5. Running a daemon or file that should be compiled by Makefile appears to have code to support it in the API code, but it's unclear where you would call it from.
6. It would be really neat if the hint system could deduct points as hints are given, and have increasing numbers of hints.  Especially for the binary problems, we would have liked to give a few hints, and then a binary compiled with debugging symbols, which might have reduced the points earned. (although first completer achievement needs to not outweigh this)

Contact
------------

Massive thanks to the original picoCTF team, we were able to go from concept of running a CTF, to having one up and running in a couple of months, as well as having a full time job.  Thats something we could only have done with the help of this tool.

Authors: Michael Brunton-Spall, David King, David Stent, Ruben Arakelyan

Original picoCTF Credits: Jonathan Burket, Tim Becker, Chris Ganas, David Brumley, Peter Chapman

Email: security-engineering@digital.cabinet-office.gov.uk
