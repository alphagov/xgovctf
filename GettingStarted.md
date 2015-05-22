# Getting Started with the picoCTF Platform 2#

## Setting up a Development Environment ##

In order to facilitate development by different users with different systems, the picoCTF Platform uses [Vagrant](http://vagrantup.com "Vagrant") to create an identical Linux setup across platforms. Vagrant works on top of any number of different virtualization [providers](https://docs.vagrantup.com/v2/providers/ "providers"), though we recommend [VirtualBox](https://www.virtualbox.org/ "VirtualBox"), since this is the one we have tested the most. 

After installing VirtualBox and Vagrant, follow these steps to get your development environment up and running:

1. Clone the `picoCTF-Platform-2` repository.
2. Inside the repository, run `vagrant up`. This will download an Ubuntu 14.04 image, create a new VM, then execute a set of setup scripts inside that VM that install the necessary dependencies for the picoCTF Platform. Note that this process can take a long time (about 30 minutes from scratch).
3. Once the setup is completed, run `vagrant ssh` to connect to the development VM.

There are many other useful [Vagrant commands](http://docs.vagrantup.com/v2/cli/ "Vagrant commands") that it will be useful to be familiar with, such as `vagrant suspend` to suspend your development VM and `vagrant reload` to restart it.


### What if I don't want to use Vagrant?
You do not need to use either Vagrant or VirtualBox to run the picoCTF Platform. This is purely to ease development. You can always run the picoCTF Platform directly on Ubuntu 14.04 or a similar Linux distribution by running the `scripts/vagrant_setup.sh` directly on the target machine (as root). This is the recommended approach for setting up the picoCTF Platform on a production server.


## Starting the picoCTF Platform ##

Once inside your development VM, you can launch the picoCTF Platform by running the `devploy` command. This will deploy the latest version of your code to be served by the web server, then restart both the web server and the picoCTF API.

You should now be able to visit the deployed site in a browser at `127.0.0.1:8080` on the host machine (or `127.0.0.1` directly on the VM). Note that going to `localhost` will display the site, but will **not** handle cookies correctly.

## Competition Quick Start

Assuming you have already created and added your problems (see next section), these steps will prepare your competition to go live:  

1. Change the value of `api.app.secret_key` in `api/api/config.py` to a new secret value.
- Change the value of `api.app.session_cookie_domain` in `api/api/config.py` to the domain you will be using to host your competition.
- Change the value of `start_time` and `end_time` in `api/api/config.py` to the start and end dates of your competition.
- (Optional) Add SMTP information in `api/api/config.py` to enable recovery of lost passwords
- Edit `scripts/devploy` to replace the line `tmux new-session -s picoapi -d "cd /home/vagrant/api && python3 run.py"` with `cd /home/vagrant/api && ./gunicorn_start.sh &`. This will switch to using [Gunicorn](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/) to run the API.
- Run `devploy` to copy the static files to the server directory and launch the API.
- Start the scoreboard with `python3 daemon_manager.py -i 300 cache_stats` in the `api` folder. Change 300 seconds, which represents how frequently the scoreboard graphs refresh, to whatever interval you prefer. It is recommended that you run this command under `tmux` or `screen`.

## Problems

### Creating Problems
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

The "threshold" and "weightmap" fields are used to manage problem unlocking. If you would like a problem to always be available, set "threshold" to 0 and "weightmap" to `{}`. Suppose we have four problems "A", "B", "C", and "D". If we want to make "D" unlock if any 2 of "A", "B", or "C" are solved, we set the "weightmap" to `{"A": 1, "B": 1, "C": 1}` since all these problems are weighted equally and "threshold" to 2, since we want to unlock the problem when any two problems are solved.

Some problems need to provide additional files for the user to view or download (binaries, encrypted messages, images, etc.). To add static files to your problem, add a *static* folder in the directory for that problem (`/problems/misc/myproblem/static/`, for example) and place any files in that directory that you want to serve statically. Then, in your problem description (or hint), you can link to this file using the URL `/problem-static/[path to problem in problems directory]/[file name]`. Look at the example problem `Sdrawkcab` to see this in action.

### Autogen Problems

Automatically generated (autogen) problems allow different teams to receive different versions of the same challenge. For example, the picoCTF 2014 problem `Substitution` (a substitution chipher problem) uses different letter mappings and Disney song lyrics for different problem instances. This has numerous advantages, including the prevention and detection of flag sharing between teams. 

Before deploying a competition, you need to generate some number of autogen problem instances per problem which will serve as the pool of possible version of the problem that a team can get. During the competition, teams will randomly be assigned an autogen instance from the pool of available instances.

Where as basic problems have just a *grader* script, autogen problems have both a *grader* and a *generator*. The *generator* contains code for producing all of the content needed for a given problem isntance. The *grader*, as in basic problems, is used to determine whether an flag submitted by a user for a given problem instance is correct. 

The `Hidden Message` problem under `example_problems` contains example code for creating an autogen problem. We will use this as a working example of how to develop an autogen problem.

*Generators* implement the following function signature: `generate(random, pid, autogen_tools, n)`, where each argument is as follows:
 
- *random*: A Python [`random`](https://docs.python.org/3.4/library/random.html) instance, which should be the only source of randomness used to generate the problem. This allows autogen problems to be random, but deterministic, such that regenerating a set of problems will always create identical instances.
- *pid*: The problem id for the autogen problem
- *autogen_tools*: An object supporting the autogen-related functions defined in `api/api/autogen_tools.py`
- *n*: The instance number for the current problem instance being generated

The `generate` function should return a dictionary with three fields: "resource_files" (per-instance files that can be seen by players solving the problem), "static files" (per-instance files hidden from players), and "problem_updates" (what fields in the original `problem.json` object need to be altered for this particular problem instance). Take a look at `example_problems/web/hidden-message/grader/generator.py` for an example simple generator that produces a custom problem description for each problem instance.

*Graders* must implement the following function signature: `grade(autogen, key)`, where each argument is as follows:

- *autogen*: An instance of the `GraderProblemInstance` class defined in `api/api/autogen`. Notably it has the field `instance` which gives you the instance number (same as `n` in the generator). 
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
### Loading Problems

Problems are loaded into the database and set up for deployment using the `api_manager.py` script. To load your problems, run the following command in `~/api`:

`python3 api_manager.py problems load [your problems directory] graders/ ../problem_static`

Note that this will create the `graders` and `problem_static` folder if they do not exists. At present you cannot trivially move the locations of the `graders` and `problem_static` directory since they are explicitly referenced elsewhere.

As always, you must run `devploy` to see your new problems appear.

In addition to loading problems, you must also generate instances for any autogen problems (see previous section) that you may have. To generate 100 problem instances for each autogen problem, you would run the following command:

`python3 api_manager.py autogen build 100`

Note that this command is idempotent. Assuming your autogen instances use only the provided source of randomness, repeatedly running this command will regenerate the exact same set of 100 problem instances.

### Updating and Deleting Problems 

In order to update problems, you must first remove the old version of the problems from the database. Currently, this is done by connecting to the database and deleting the problems as follows:

1. Run `mongo pico`
2. Enter `db.problems.remove()` in the MongoDB terminal

Once you have removed the problems, you can load in the new versions as described in the previous section. If any autogen problems have been deleted, you will also need to rebuild the autogen instances.

## Customizing the Site

### Jekyll and Static Templates

Web pages for the picoCTF Platform are built using static [Jekyll](http://jekyllrb.com/ "Jekyll") templates. When `devploy` is run, the Jekyll templates are compiled into static HTML pages, which are then served directly by Nginx. 

The main layout file for the entire site is stored in `web/_layouts/default.html`, which includes other additional important files, such as `web/_includes/header.html` (the navbar), `/web/_includes/head.html` (the contents of `<head>`, including the various CSS and JS files that need to be loaded), and `web/_includes/footer.html`. Editing these files will affect all of the pages on the site.

The file `web/_config.yml` contains global settings related to Jekyll templates. For example, in this file the name of the site can be changed from "picoCTF Platform 2" to whatever name you would like the title of your competition to be.

The `web/_posts` folder is a special folder used to store posts to be displayed on the "News" page. Placing markdown files here will automatically add them to both the News page and the site RSS feed. Check out the ["Jekyll Documentation"](http://jekyllrb.com/docs/posts/ "Jekyll Documentation") for more information.

### Creating a New Page

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

You may want to make it so that you do not have to include ".html" in the URL for your new page. `web/about.html`, for example, is served from `127.0.0.1:8080/about`. In order to add an alias for your page go to `config/ctf.nginx` and add the name of your page to the list of existing pages with rewrite rules:

	    location ~ ^/(problems|login|chat|logout|compete|...|contact|mynewpage)$
        {
            default_type text/html;
            alias /srv/http/ctf/$1.html;
        }

This will cause `127.0.0.1:8080/mynewpage` to serve content from `web/mynewpage.html`.

### Configuring Site Options

Most configuration settings for the picoCTF Platform are specified in `api/api/config.py`. Useful setting values include:

- The hostname or IP of the server hosting the platform (used for cookies)
- The name of the competition (as used by the API)
- Optional features, such as teacher accounts, problem feedback, and achievements
- Database settings
- The competition start and end date
- Emails to contact in cases of critical errors (requires setting up an SMTP server)

Changing these settings is as easy as editing the relevant Python assignments. Note that you will need to run `devploy` in order for any changes to setting to take effect.

### CoffeeScript

All of the client-side code for the picoCTF Platform is written in [CoffeeScript](http://coffeescript.org/). When `devploy` is used to deploy the site, all CoffeeScript files in `web/coffee` are compiled to JavaScript and stored in `web/js` before being copied to the server directory. This means that any edits to the client-side code should occur in the relevant `.coffee` file NOT the `.js` file.

### Adding Google Analytics

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

## Security

### Setting the Passphrase

The picoCTF Platform uses encrypted cookies to store session information without the need to store session state server side. In order to prevent session hijacking, you MUST change the application secret key. To change the key, edit the `api.app.secret_key` value in `api/api/config.py`. Be sure to use an unpredictable and reasonably long value for the key.

### Note on the Team Password

Passwords for individual users are stored in the database as salted hashes. *Team Passphrases*, however, are stored in plaintext so that they can be displayed back to users on the *Team* page. This allowed us to avoid creating a separate mechanism for forgotten team passphrases, at the risk that a database leak would allow a user to join a team with which they are not affiliated. 

### Protecting the Database

The default MongoDB configuration used by the picoCTF Platform blocks all non-local connections and therefore does not use password authentication for local users. This means that if you use the server with the database to also host CTF problems that give shell access to users, you MUST [take steps to control access to the database](http://docs.mongodb.org/manual/tutorial/enable-authentication/).

### CSRF Defenses

For design reasons, the picoCTF Platform does not use tokens embedded in `<form>` tags in order to prevent CSRF attacks. Instead, it uses the [Double Submit Cookies](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29_Prevention_Cheat_Sheet#Double_Submit_Cookies) method in which a token is read from a cookie and submitted with requests that need to be protected. This happens transparently client-side, as long as a request goes through the `apiCall` function (see `web/coffee/dependencies.coffee`). Server-side, API requests that need CSRF protection should use the `@check_csrf` annotation to indicate that checking the value of the submitted cookie is required.
