# Getting Started with the picoCTF Platform 2#

1. [Setting Up a Development Environment](#devenv)
	- [What if I don't want to use Vagrant?](#devenv-novagrant)
- [Starting the picoCTF Platform](#starting)
- [Competition Quick Start](#quickstart)
	- [Ending the Competition](#quickstart-ending)
- [Problems](#problems)
	- [Creating Problems](#problems-creating)
	- [Autogen Problems](#problems-autogen)
	- [Problem Categories](#problems-categories)
	- [Loading Problems](#problems-loading)
	- [Updating and Deleting Problems](#problems-updating)
- [Customizing the Site](#customizingsite)
	- [Jekyll and Static Templates](#customizingsite-jekyll)
	- [Creating a New Page](#customizingsite-newpage)
	- [Adjusting the Links in the Navbar](#customizingsite-navbar)
	- [Configuring Site Options](#customizingsite-options)
	- [CoffeeScript](#customizingsite-coffeescript)
	- [Adding Google Analytics](#customizingsite-analytics)
	- [Adding a favicon](#customizingsite-favicon)
- [Achievements](#achievements)
	- [Creating a Processor Script](#achievements-script)
	- [Loading Achievements](#achievements-loading)
	- [Removing Achievements](#achievements-removing)
- [Working with Competition Data](#competitiondata)
	- [Running API Commands Directly](#competitiondata-api)
	- [Getting Statistics](#competitiondata-stats)
	- [Getting Review Data Directly](#competitiondata-reviews)
	- [Disabling Accounts](#competitiondata-disabling)
	- [Disqualifying Teams](#competitiondata-disqualifying)
- [Eligibility](#eligibility)
	- [Other Cases](#eligibility-other)
	- [Updating Eligibility](#eligibility-updating)
- [Security](#security)
	- [Setting the Passphrase](#security-passphrase)
	- [Note on the Team Password](#security-password)
	- [Protecting the Database](#security-database)
	- [CSRF Defenses](#security-csrf)

## <a name="devenv"></a> Setting up a Development Environment ##

In order to facilitate development by different users with different systems, the picoCTF Platform uses [Vagrant](http://vagrantup.com "Vagrant") to create an identical Linux setup across platforms. Vagrant works on top of any number of different virtualization [providers](https://docs.vagrantup.com/v2/providers/ "providers"), though we recommend [VirtualBox](https://www.virtualbox.org/ "VirtualBox"), since this is the one we have used with the most success.

After installing VirtualBox and Vagrant, follow these steps to get your development environment up and running:

1. Clone the `picoCTF-Platform-2` repository.
2. Inside the repository, run `vagrant up`. This will download an Ubuntu 14.04 image, create a new VM, then execute a set of setup scripts inside that VM that install the necessary dependencies for the picoCTF Platform. Note that this process can take a long time (about 30 minutes from scratch).
3. Once the setup is completed, run `vagrant ssh` to connect to the development VM.

There are many other useful [Vagrant commands](http://docs.vagrantup.com/v2/cli/ "Vagrant commands") that it will be useful to be familiar with, such as `vagrant suspend` to suspend your development VM and `vagrant reload` to restart it.


###<a name="devenv-novagrant"></a>  What if I don't want to use Vagrant?
You do not need to use either Vagrant or VirtualBox to run the picoCTF Platform. This is purely to ease development. You can always run the picoCTF Platform directly on Ubuntu 14.04 or a similar Linux distribution by running the `scripts/vagrant_setup.sh` directly on the target machine (as root). This is the recommended approach for setting up the picoCTF Platform on a production server.


## <a name="starting"></a> Starting the picoCTF Platform ##

Once inside your development VM, you can launch the picoCTF Platform by running the `devploy` command. This will deploy the latest version of your code to be served by the web server, then restart both the web server and the picoCTF API.

You should now be able to visit the deployed site in a browser at `127.0.0.1:8080` on the host machine (or `127.0.0.1` directly on the VM). Note that going to `localhost` will display the site, but will **not** handle cookies correctly.

## <a name="quickstart"></a> Competition Quick Start

Assuming you have already created and added your problems (see next section), these steps will prepare your competition to go live:  

1. Change the value of `api.app.secret_key` in `api/api/config.py` to a new secret value.
- Change the value of `api.app.session_cookie_domain` in `api/api/config.py` to the domain you will be using to host your competition.
- Change the value of `start_time` and `end_time` in `api/api/config.py` to the start and end dates of your competition.
- (Optional) Add SMTP information in `api/api/config.py` to enable recovery of lost passwords
- Edit `scripts/devploy` to replace the line `tmux new-session -s picoapi -d "cd /home/vagrant/api && python3 run.py"` with `cd /home/vagrant/api && ./gunicorn_start.sh &`. This will cause the picoCTF platform to use [Gunicorn](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/) to run the API.
- Run `devploy` to copy the static files to the server directory and launch the API.
- Start the scoreboard with `python3 daemon_manager.py -i 300 cache_stats` in the `api` folder. Change 300, which represents how the number of seconds between scoreboard refreshes, to whatever interval you prefer. It is recommended that you run this command under `tmux` or `screen`.

### <a name="quickstart-ending"></a> Ending the Competition

Once the competition end date (as specified in `api/api/config.py`) is reached, submissions will no longer be accepted. This may or may not be what you want to have happen at the end of your competition. For picoCTF, we leave the competition online, but fix the *scoreboard* at the end of the competition. To accomplish this, we initially set the end date to the end of the competition to ensure that the scoreboard could not be changed after the competition. We then copied the scoreboard itself as raw HTML and replaced the contents of `web/scoreboard.html` with the scoreboard dump. Finally, we moved the competition end date to an indefinite future date to re-allow submissions, knowing that they would not affect the final (now static) scoreboard.

## <a name="problems"></a> Problems

### <a name="problems-creating"></a> Creating Problems
There are two types of problems supported by this framework: *basic* problems, and *auto-generated* problems. Auto-generated problems allow for different users to receive different versions of the same problem. Basic problems have only one version. In this section we will discuss adding basic problems. Several example problems are included under the *example_problems* directory.

Every basic problem needs two components: a *problem.json* file and a *grader* directory containing a grading script. A *problem.json* file should look like this:

```json
    {"name": "Problem Name",
     "score": 10,
     "category": "Category Name",
     "grader": "misc/myproblem/grader.py",
     "description": "Problem text. HTML can be used here.",
     "threshold": 0,
     "weightmap": {},
     "hint": "Hint text. HTML can be used here"}
```

A grading script, written in Python, should look like this:

```python
    def grade(arg, key):
        if "this_is_the_flag" in key:
            return True, "Correct"
        else:
            return False, "Incorrect"
``` 

Note that the problem loading script (`api_manager.py problems load`) makes a number of assumptions about the folder structure used to hold your problems. Suppose you want to create a new problem *My Problem* and you are storing all of your problems in ~/problems. First we make a directory for our problem, such as `/problems/misc/myproblem`. Now we place our *problem.json* file at `/problems/misc/myproblem/problem.json` and our grading script at `/problems/misc/myproblem/grader/grader.py`. Now we double check that our "grader" path in *problem.json* points to the grader. Note that this path is NOT an absolute path. It instead has the following format: if our grader is at `[problem directory]/[path to problem in problem directory]/grader/[grader name]`, then the "grader" path should be set to `[path to problem in problem directory]/[grader name]`. Thus, for `/problems/misc/myproblem/grader/grader.py`, we use `misc/myproblem/grader.py`.

The "threshold" and "weightmap" fields are used to manage problem unlocking. If you would like a problem to always be available, set "threshold" to 0 and "weightmap" to `{}`. Suppose we have four problems "A", "B", "C", and "D". If we want to make "D" unlock if any 2 of "A", "B", or "C" are solved, we set the "weightmap" to `{"A": 1, "B": 1, "C": 1}`, since all these problems are weighted equally, and "threshold" to 2, since we want to unlock the problem when any two problems are solved.

Some problems need to provide additional files for the user to view or download (binaries, encrypted messages, images, etc.). To add static files to your problem, add a *static* folder in the directory for that problem (`/problems/misc/myproblem/static/`, for example) and place any files in that directory that you want to serve statically. Then, in your problem description (or hint), you can link to this file using the URL `/problem-static/[path to problem in problems directory]/[file name]`. Look at the example problem `Sdrawkcab` to see this in action.

### <a name="problems-autogen"></a> Autogen Problems

Automatically generated (autogen) problems allow different teams to receive different versions of the same challenge. For example, the picoCTF 2014 problem `Substitution` (a substitution cipher problem) uses different letter mappings and Disney song lyrics for different problem instances. This has numerous advantages, including the prevention and detection of flag sharing between teams.

Before deploying a competition, you need to generate some number of autogen problem instances per autogen problem. These instances will serve as a pool of possible versions of the problem. During the competition, teams will randomly be assigned one autogen instance from the pool of available instances.

Whereas basic problems have just a *grader* script, autogen problems have both a *grader* and a *generator* script. The *generator* contains code for producing all of the content needed for a given problem instance. The *grader*, as with basic problems, is used to determine whether an flag submitted by a user for a given problem instance is correct.

The `Hidden Message` problem under `example_problems` contains example code for creating an autogen problem. We will use this as a working example of how to develop an autogen problem.

*Generators* implement the following function signature: `generate(random, pid, autogen_tools, n)`, where each argument is as follows:
 
- *random*: A Python [`random`](https://docs.python.org/3.4/library/random.html) instance, which should be the only source of randomness used to generate the problem. This allows autogen problems to be random, but deterministic, such that regenerating a set of problems will always create identical instances.
- *pid*: The problem id for the autogen problem
- *autogen_tools*: An object supporting the autogen-related functions defined in `api/api/autogen_tools.py`
- *n*: The instance number for the current problem instance being generated

The `generate` function should return a dictionary with three fields: "resource_files" (per-instance files that can be seen by players solving the problem), "static files" (per-instance files hidden from players), and "problem_updates" (what fields in the original `problem.json` object need to be altered for this particular problem instance). Take a look at `example_problems/web/hidden-message/grader/generator.py` for an example simple generator that produces a custom problem description for each problem instance.

*Graders* must implement the following function signature: `grade(autogen, key)`, where each argument is as follows:

- *autogen*: An instance of the `GraderProblemInstance` class defined in `api/api/autogen.py`. Notably it has the field `instance` which gives you the instance number (same as `n` in the generator).
- *key*: The flag submitted by the user to be checked for correctness
 
Graders return a boolean, string pair as with basic problems.

It is very likely that both the problem *generator* and *grader* need to know the value of the flag for the given problem instance. There are two possible methods to share a common flag between the two scripts:

1. Generate the flag in the *generator*, then save it in a static file that is read in by the *grader*.
2. Make the flag deterministic based on the problem instance. 

The example problem `Hidden Message` uses the latter strategy. In the generator, it calculates the flag with the following code:

```python 
    key = "my_key_here"
    flag = "flag_" + sha1((str(n) + key).encode('utf-8')).hexdigest()
```

The grader then performs a similar calculation:

```python
    secretkey = "my_key_here"
    n = autogen.instance
    flag = sha1((str(n) + secretkey).encode('utf-8')).hexdigest()
```

Note that autogen problems must set two additional fields in the `problem.json` file. In addition to "grader", there needs to be a "generator" field pointing to the generator script. Also, the "autogen" field must be set to `true`. See `example_problems/web/hidden-message/problem.json` for an example.

### <a name="problems-categories"></a> Problem Categories

The category of a problem is specified in the "category" field of the `problem.json` file. Note that there is not a fixed set of categories; you may use any free-form category name. Many features, such as the code to generate problem statistics, will group problems by category name. Thus, it is useful to make sure that you are consistent in your spelling and formatting for each category name.

If you plan on using the existing achievements from picoCTF, you will need to edit the "Category Completion" and "Category Solved 5" achievements based on your new category names.

### <a name="problems-loading"></a> Loading Problems

Problems are loaded into the database and set up for deployment using the `api_manager.py` script. To load your problems, run the following command in `~/api`:

`python3 api_manager.py problems load [your problems directory] graders/ ../problem_static`

Note that this will create the `graders` and `problem_static` folder if they do not exists. At present you cannot trivially move the locations of the `graders` and `problem_static` directory since they are explicitly referenced elsewhere.

As always, you must run `devploy` to see your new problems appear.

In addition to loading problems, you must also generate instances for any autogen problems (see previous section) that you may have. To generate 100 problem instances for each autogen problem, you would run the following command:

`python3 api_manager.py autogen build 100`

Note that this command is idempotent. Assuming your autogen instances use only the provided source of randomness, repeatedly running this command will regenerate the exact same set of 100 problem instances.

### <a name="problems-updating"></a> Updating and Deleting Problems 

In order to update problems, you must first remove the old version of the problems from the database. Currently, this is done by connecting to the database and deleting the problems as follows:

1. Run `mongo pico`
2. Enter `db.problems.remove()` in the MongoDB terminal
3. Enter `db.submissions.remove()` in the MongoDB terminal (deletes all problem submissions)

Once you have removed the problems, you can load in the new versions as described in the previous section. If any autogen problems have been deleted, you will also need to rebuild the autogen instances.

**Note on updating problems during the live competition**: During the competition, you may want to update problems without clearing out all submissions (step three above). Existing submissions will be correctly associated with an updated problem if both the new and old problem share *exactly the same name*. Thus, if you want to update a problem, but not its name, you need not delete existing submissions. If you change the problem name, you **must** delete existing submissions, or users will receive errors on the "Problems" page. Note that if you change a problem's *grader* and keep existing submissions they will not be reevaluated using the new grader. In other words, if you keep existing submissions to a problem, all correct submissions will always remain correct for the new version of the problem.

## <a name="customizingsite"></a> Customizing the Site

### <a name="customizingsite-jekyll"></a> Jekyll and Static Templates

Web pages for the picoCTF Platform are built using static [Jekyll](http://jekyllrb.com/ "Jekyll") templates. When `devploy` is run, the Jekyll templates are compiled into static HTML pages, which are then served directly by Nginx. 

The main layout file for the entire site is stored in `web/_layouts/default.html`, which includes other additional important files, such as `web/_includes/header.html` (the navbar), `/web/_includes/head.html` (the contents of `<head>`, including the various CSS and JS files that need to be loaded), and `web/_includes/footer.html`. Editing these files will affect all of the pages on the site.

The file `web/_config.yml` contains global settings related to Jekyll templates. For example, in this file the name of the site can be changed from "picoCTF Platform 2" to whatever name you would like the title of your competition to be.

The `web/_posts` folder is a special folder used to store posts to be displayed on the "News" page. Placing markdown files here will automatically add them to both the News page and the site RSS feed. Check out the ["Jekyll Documentation"](http://jekyllrb.com/docs/posts/ "Jekyll Documentation") for more information.

### <a name="customizingsite-newpage"></a> Creating a New Page

In order to add a new page to the site, create a new HTML document under `web` with the following format:

	---
	layout: default
	title: My New Page
	post_scripts:
	 - js/script_i_want_to_run.js
	startup_functions:
	 - functionToRunOnStart()
	---
	[HTML content for the page]

Note that both the `post_scripts` field and the `startup_functions` field can be omitted altogether. Check out `web/about.html` and `web/shell.html` for good examples of simple pages.

You may want to make it so that you do not have to include ".html" in the URL for your new page. `web/about.html`, for example, is served from `127.0.0.1:8080/about` as well as `127.0.0.1:8080/about.html`. In order to add an alias for your page, go to `config/ctf.nginx` and add the name of your page to the list of existing pages with rewrite rules:

	    location ~ ^/(problems|login|chat|logout|compete|...|contact|mynewpage)$
        {
            default_type text/html;
            alias /srv/http/ctf/$1.html;
        }

This will cause `127.0.0.1:8080/mynewpage` to serve content from `web/mynewpage.html`.

### <a name="customizingsite-navbar"></a> Adjusting the Links in the Navbar

The links displayed on the navbar (the menu bar at the top of every page) are not defined in a template, but instead set in JavaScript. This allows the navbar to change based on whether the competition is active and whether or not the user is currently logged in.

All of the links displayed in different contexts are defined in the CoffeeScript file `web/coffee/navbar.coffee`. Consider the following menu definition:

	teacherLoggedInNoCompetition =
	  Classroom: "/classroom"
	  About: "/about"
	  News: "/news"
	  Account:
	    Manage: "/account"
	    Logout: "#"

This defines the navbar that will be displayed for a teacher account that is logged in outside of the competition dates (defined in `api/api/config.py`). The dictionary "keys" dictate the text that appears on the navbar buttons, while the "values" serve as the link targets. Note that you can nest these definitions (as with "Account") to create navbar items with dropdown menus. Generated navbar buttons have predictable names ("navbar-item-" + lower case button text with spaces replaced with underscores) if you want to bind JavaScript functions to them (as is done with "Logout").

### <a name="customizingsite-options"></a> Configuring Site Options

Most configuration settings for the picoCTF Platform are specified in `api/api/config.py`. Useful setting values include:

- The hostname or IP of the server hosting the platform (used for cookies)
- The name of the competition (as used by the API)
- Optional features, such as teacher accounts, problem feedback, and achievements
- Database settings
- The competition start and end date
- Emails to contact in cases of critical errors (requires setting up an SMTP server)

Changing these settings is as easy as editing the relevant Python assignments. Note that you will need to run `devploy` in order for any changes to setting to take effect.

### <a name="customizingsite-coffeescript"></a> CoffeeScript

All of the client-side code for the picoCTF Platform is written in [CoffeeScript](http://coffeescript.org/). When `devploy` is used to deploy the site, all CoffeeScript files in `web/coffee` are compiled to JavaScript and stored in `web/js` before being copied to the server directory. This means that any edits to the client-side code should occur in the relevant `.coffee` file NOT the `.js` file.

### <a name="customizingsite-analytics"></a> Adding Google Analytics

Client-side events can be recorded for use with [Google Analytics](http://www.google.com/analytics). In order to enable analytics, first create a new file `web/_includes/analytics.html` and fill it with your Analytics tracking code. It should look something like this:

	<script>
	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
	  ga('create', '[your id here]', 'auto');
	  ga('require', 'displayfeatures');
	  ga('send', 'pageview');
	</script>

Then change `mode: development` to `mode: production` in `_config.yml` to enable Analytics. Note that we currently only support the ["Universal Analytics"](https://support.google.com/analytics/answer/2790010?hl=en) method and not the "Classic" method of Google Analytics.

### <a name="customizingsite-favicon"></a> Adding a favicon

Simplest way is to add a `<link rel="icon" href="/path/to/favicon.ico" />` in `/web/_includes/head.html`. This is included in the default layout and will be used for all the pages.

## <a name="achievements"></a> Achievements 

Achievements are small awards given to teams as they complete challenges or perform special actions in the competition. Note that the achievement system is completely divorced from the scoring system; there currently is no way to make achievements impact competition performance. They are designed to be purely for fun.

Achievements are only earned by *teams*. There is no notion of an individual *user* having an achievement, even though a single user may be responsible for unlocking the achievement. A given achievement can only be earned by a team once (except for *multi-achievements* described below). 

Like problems, achievements are defined as *json* files that are imported into the database that refer to a specific script containing each achievement's implementation. The following example achievement is included in the file `api/achievements/categorycompletion.json`:  

	{"name": "Category Completion",
	 "description": "You team has solved every 'x' problem.",
	 "event": "submit",
	 "multiple": true,
	 "hidden": false,
	 "score": 300,
	 "processor": "categorycompletion/categorycompletion.py",
	 "image": "/img/achievements/silver.png",
	 "smallimage": "/img/achievements/silver_unlock.png"}

These fields mean the following:

- *name*: The name of the achievement displayed to the user
- *description*: The description of how the achievement was earned
- *image*: The image displayed alongside the achievement (Recommended dimensions: 233px x 200px)
- *score*: Unrelated to the score of a team on the scoreboard. This is used to prioritize the order in which achievements are displayed. Achievements with a higher score are displayed higher in the list.
- *event*: Achievements are unlocked in response to events. When the event type specified here occurs, the *processor* script is called to check whether or not the achievement has been earned. Possible events are:
	- "review": A problem has just been reviewed
	- "submit": A **correct** answer to problem has just been submitted
- *processor*: The script used to tell whether the achievement has been earned in response to the trigger event. Similar to a problem *grader*.
- *multiple*: Achievements come in two types: normal achievements and *multi-achievements*. This distinction is similar to the basic/autogen problem division. A normal achievement can be earned once per team and contains exactly the name and description in the *.json* file. A multi-achievement can be earned multiple times, each potentially with a different name or description. This is how the "Category Completion" achievement actually serves as multiple different achievements (one for each category) and has a different name for each one. 

The *hidden* and *smallimage* fields are deprecated.

### <a name="achievements-script"></a> Creating a Processor Script ###

An achievement *processor* script is expected to implement the following interface: `process(api, data)` where `api` is an imported version of the top level picoCTF API library and `data` contains extra information based on the achievement's `event` type.

The `data` dictionary has the following values based on the event:

- "review": "uid" (user id of the reviewer), "tid" (team id of that user), "pid" (problem id of the reviewed problem)
- "submit": "uid" (user id of the problem solver), "tid" (team id of that user), "pid" (problem id of the problem just solved correctly)

Processor scripts are expected to return a pair where the first value is a boolean indicating whether or not the achievement has been earned, and the second is a dictionary with values to change in the achievement (for multi-achievements). 

Consider the following simple processor that awards an achievement when a team gets more than 100 points:

```python
	def process(api, data):
	    return api.stats.get_score(tid=data["tid"]) > 100, {}
```
 
This script checks the score of the team that submitted the problem correctly and returns True if the score is over 100. The second argument is an empty dictionary since it is not a multi-achievement. Since non-multi-achievements can earned only once, there is no need to check if the team already has the achievement. If a teams solves a series of problems, they will receive the achievement as soon as they achieve 100 points and will not earn it again for solving subsequent problems.

Now consider the processor for the multi-achievement `Category Completion`:

```python

	def process(api, data):
	    pid = data["pid"]
	    pid_map = api.stats.get_pid_categories()
	    category = pid_map[pid]
	    category_pids = api.stats.get_pids_by_category()[category]
	    solved_pids = api.problem.get_solved_pids(tid=data['tid'])

	    earned = True
	    for pid in category_pids:
	        if pid not in solved_pids:
	            earned = False
	
	    name = "Category Master"
	    if category == "Cryptography":
	        name = "Cryptography Experts"
	    elif category == "Reverse Engineering":
	        name = "Reversing Champions"
	    ...
	
	    description = "Solved every '%s' challenge" % category
	    return earned, {"name": name, "description": description}
```

The first half of this processor checks if all problems in a given category have successfully been completed. In the second half, it produces the correct version of the achievement to return based on the category. If, for example, a user solves every problem in the "Cryptography" category, then it will set the name of the achievement to "Cryptography Experts" and the description to "Solved every 'Cryptography' challenge.

Note that unlike normal achievements, multi-achievements have no checks for repetition. For example, in the multi-achievement `Category Solved 5`, where a team gets an achievement if they solve 5 problems in a category, we must check for *exactly* 5 submissions. If we checked for 5 or more submissions (as in the earlier 100 points example), we could earn the same achievement multiple times.   

### <a name="achievements-loading"></a> Loading Achievements

Like problems, achievements are loaded via the `api_manager.py` script. In the `api` folder, run the following command:

	python3 api_manager.py -v achievements load achievements/*.json

This assumes that you store all of your achievements in the `api/achievements` folder. As always, you will need to run `devploy` for your changes to take effect.

### <a name="achievements-removing"></a> Removing Achievements

Achievements must be removed directly from the database. To remove all of the achievements, perform the following steps:

1. Run `mongo pico`
2. In the MongoDB terminal, run `db.achievements.remove()`
3. In the MongoDB terminal, run `db.earned_acheivements.remove()`

## <a name="competitiondata"></a> Working with Competition Data

There is currently no web interface for competition organizers. This means that in order to access non-public data about the competition, you will need to directly call the relevant API endpoint in Python or communicate with the MongoDB database directly.

### <a name="competitiondata-api"></a> Running API Commands Directly

The Python API is designed to run out of the `api` folder (not to be confused with the `api/api` folder). Thus, the easiest way to run API commands directly is to switch to the `api` directory, run `python3`, then import the relevant portion of the API using commands such as `import api.stats`.

### <a name="competitiondata-stats"></a> Getting Statistics

The `api/api/stats.py` file provides a number of useful statistics-gathering functions for the picoCTF Platform. You can obtain most of the interesting statistics by running the function `get_stats()`.

Note that with the exception of the scoreboard functionality, the functions in `api/api/stats.py` are designed to be run by an administrator in the background and are likely too slow to be served directly to users.  

### <a name="competitiondata-reviews"></a> Getting Review Data Directly

The picoCTF Platform allows users to provide feedback on whether or not they found a problem interesting, educational, etc. This information is then stored in the MongoDB collection `problem_feedback`. Based on how you want to use the review data, you may want to query the database directly. Running the command `db.problem_feedback.find({}, {"pid": true, "feedback.comment": true})` in the MongoDB terminal, for example, will yield all of the text comments provided in problem reviews.

The `get_review_stats` and `print_review_comments` functions in `api/api/stats.py` are also useful for easily accessing data from problem reviews.

### <a name="competitiondata-disabling"></a> Disabling Accounts

As a competition organizer, you may want to disable specific user accounts. Disabled users cannot log in and do not count towards the team limit. Note that disabling a user does not allow another user to create a new user with the same name. Users can voluntarily disable their accounts on the "Account->Manage" page. You can also manually disable a user's account with the following command in the MongoDB terminal:

	db.users.update({"username": "[enter username here]"}, {$set: {"disabled": true}})

You can re-enable a user with a similar command. Note, however, that doing so may allow a team to have more members than allowed by the team limit.

We strongly recommend against removing a user from the database altogether, as submission and achievement logs reference specific users in the database and may behave incorrectly if the relevant users are not present in the database.

### <a name="competitiondata-disqualifying"></a> Disqualifying Teams

Rather than disabling accounts, you may simply want to mark a team as *ineligible* (not on the public scoreboard). To mark a team as disqualified, use the following command in the MongoDB terminal:

	db.teams.update({"team_name": "[enter team name here]"}, {$set: {"disqualified": true}})

Note that to actually mark the team as ineligible, you will need to run the `determine_eligibility` function with the `tid` for the given team after marking it as disqualified (see next section).

## <a name="eligibility"></a> Eligibility

The picoCTF Platform supports the notion of teams that are *eligible* and teams that are *ineligible*. The key difference between these two team types is that ineligible teams do not show up on the main scoreboard. Ineligible teams may, however, show up on Classroom scoreboards. Some of the included achievements also rely on eligibility. The "Breakthrough" achievement, for example, is earned by the first *eligible* team that solves a given challenge.

A team is *eligible* if every member of the team meets a certain set of criteria. For picoCTF, the requirement is that each team member must be a middle or high school student from the United States. For the picoCTF Platform, there is no requirement by default. To adjust the eligibility criteria, you will need to modify the code in several places.

First, edit the `eligible = True` line in the `create_user_request` function in `api/api/user.py`. picoCTF 2014, for example, has the following line instead:

	eligible = params['country'] == "US" and params['background'] in ['student_el', 'student_ms', 'student_hs', 'student_home']

Whenever the members of team change, the function `determine_eligibility` in `/api/api/team.py` is called to determine if the team is still eligible. In order to add eligibility restrictions, you will need to edit this function as well. Some example code is included as comments in this function. Note that the `determine_eligibility`   also returns a set of 'justifications'. These are displayed to the user on the "Team" page to explain why a team is not considered eligible.

### <a name="eligibility-other"></a> Other Cases

Teacher Accounts are special accounts that can create Class Groups and cannot join teams. In order to allow Teacher Accounts to play through the competition, each Teacher Account is associated with a unique hidden team with the prefix "TEACHER-". These Teacher Account teams are always marked as ineligible and are not designed to ever show up on any scoreboard.

If all members of a team disable their accounts, then a team will be marked as ineligible.

If a team is marked as "disqualified" (see previous section), then they will always be considered ineligible.

### <a name="eligibility-updating"></a> Updating Eligibility

Team eligibility is recalculated every time a new member joins or leaves a team *via the web interface*. If you as the competition organizer manually modify a team, you will need to manually trigger the eligibility update by calling the `determine_eligibility` function in `api.team` with the appropriate `tid` (team id).

## <a name="security"></a> Security

### <a name="security-passphrase"></a> Setting the Passphrase

The picoCTF Platform uses encrypted cookies to store session information without the need to store session state server side. In order to prevent session hijacking, you MUST change the application secret key. To change the key, edit the `api.app.secret_key` value in `api/api/config.py`. Be sure to use an unpredictable and reasonably long value for the key.

### <a name="security-password"></a> Note on the Team Password

Passwords for individual users are stored in the database as salted hashes. *Team Passphrases*, however, are stored in plaintext so that they can be displayed back to users on the *Team* page. This allowed us to avoid creating a separate mechanism for forgotten team passphrases, at the risk that a database leak would allow a user to join a team with which they are not affiliated. 

### <a name="security-database"></a> Protecting the Database

The default MongoDB configuration used by the picoCTF Platform blocks all non-local connections and therefore does not use password authentication for local users. This means that if you use the server with the database to also host CTF problems that give shell access to users, you MUST [take steps to control access to the database](http://docs.mongodb.org/manual/tutorial/enable-authentication/).

### <a name="security-csrf"></a> CSRF Defenses

For design reasons, the picoCTF Platform does not use tokens embedded in `<form>` tags in order to prevent CSRF attacks. Instead, it uses the [Double Submit Cookies](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29_Prevention_Cheat_Sheet#Double_Submit_Cookies) method in which a token is read from a cookie and submitted with requests that need to be protected. This happens transparently client-side, as long as a request goes through the `apiCall` function (see `web/coffee/dependencies.coffee`). Server-side, API requests that need CSRF protection should use the `@check_csrf` annotation to indicate that checking the value of the submitted cookie is required.
