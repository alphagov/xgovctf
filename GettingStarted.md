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
