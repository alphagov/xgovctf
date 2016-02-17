picoCTF-Platform 2
==============

The picoCTF Platform 2 is the infrastructure on which picoCTF runs. The 
platform is designed to be easily adapted to other CTF or programming 
competitions.

picoCTF Platform 2 targets Ubuntu 14.04 LTS but should work on just about 
any "standard" Linux distribution. It would probably even work on 
Windows. MongoDB must be installed; all default configurations should 
work.

Setting Up
------------
1. Download VirtualBox (easiest, though others can work)
2. Download Vagrant (vagrantup.com)
3. `vagrant up` inside the repo
4. Wait 20 minutes
5. `vagrant ssh` to connect to the VM
6. Run `devploy` to deploy the development version of the site
7. Go to port 8080 on the Host Machine
8. Remember to always use 127.0.0.1:8080 not localhost:8080

*Note*: The competition has two modes: competition active and competition inactive. In inactive mode, there are no problems and only registration is available. To change what mode the competition is in, edit api/api/config.py and change the competition dates such that the current date is either inside or outside the range of the competition dates.


Loading the Example Problems (In the vagrant VM)
------------
1. Run `cd ~/api`
2. Run `python3 api_manager.py -v problems load /vagrant/example_problems/ graders/ ../problem_static/`
3. Run `python3 api_manager.py autogen build 100`
4. Run `devploy`


Running the Regression Tests
----------------------------

The platform comes with a series of regression tests that should be run before any change is committed to the API.
To run the tests:

1. `vagrant ssh` into your virtual machine.
2. Run `devploy` to bring up an instance from your latest code.
3. To be able to import the API, `cd api` and run the tests with `./run_tests.sh`
 
All tests should pass with your changes.


Getting Started
---------------

A detailed explanation of the basics of the picoCTF Platform 2 can be found in our [Getting Started Guide](GettingStarted.md).


Contact
------------

We are happy to help but no support is guaranteed.

Authors: Jonathan Burket, Tim Becker, Chris Ganas

Copyright: Carnegie Mellon University

License: MIT

Maintainers: Roy Ragsdale

Credits: David Brumley, Tim Becker, Chris Ganas, Peter Chapman, Jonathan Burket

Email: rragsdale@cmu.edu

