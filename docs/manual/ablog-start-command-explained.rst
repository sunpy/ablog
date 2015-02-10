.. _workflow:



ABlog Start Command Explained
=============================

.. post:: Feb 9, 2015
   :tags: config, start,
   :author: Mehmet
   :category: Manual
   :location: SF

This is a simple walk through of the "`ablog start`" flow, intended to explain the options you're presented when
running the command to start your blog.

The start command will ask you to enter the following:

Basic Information:
^^^^^^^^^^^^^^^^^^
1. **Blog root folder:**
    This is where your configuration file and the rest of your projects files and folders will be created.
    The default is [.] the current working folder.
#. **Title of your blog:**
	Title of your blog. It will appear on various locations on your blog depending 
	on your choice of themes. 
#. **Author Name:**
	Name of the blog owner (person, project, organization, etc.)
	It will be the actual display 'title' of the blog.
#. **Blog URL:**
	The URL pointing to your intended publishing address of your blog. 
	It will be used for feed generation. (e.g. Atom, RSS etc.)

Optional Features:
^^^^^^^^^^^^^^^^^^
**Alabaster Sphinx theme opt-in:**
If you happen to have Alabaster Sphinx theme installed on your system,
you will be asked whether you'd like to enable it. 
The default value is [y] and you'll only be asked, if you have alabaster installed
on your system.
If you don't see this prompt and wan't to install alabaster on your system, you can 
do so by using the following command:

    >>>pip install alabaster
	
Please see `Alabaster GitHub home`_ for more information.

.. _`Alabaster GitHub home`: https://github.com/bitprophet/alabaster 
    
**This is the end, if you're not using 'Alabaster'.**

	
Alabaster Options:
^^^^^^^^^^^^^^^^^^

	1. **Google Analytics ID:**
	Google Analytics ID for the blog to track traffic. 
	The default is blank. Leave blank to disable.

	2. **Alabaster GitHub Options:**
	Enables GitHub options for Alabaster and will lead to a few more
	questions. 

**This is the end, if you're not using GitHub options for `Alabaster`**
		
Alabaster GitHub Options:
^^^^^^^^^^^^^^^^^^^^^^^^^

		1. **GitHub Project Name:**
		The name of the GitHub project, just the project name.
		e.g. `http://www.github.com/abakan/ablog` --> `ablog`

		#. **GitHub User Name:**
			The user name of the GitHub project owner.
			e.g. `http://www.github.com/abakan/ablog` --> `abakan`

		#. **GitHub Project Description:**
			A single line (short line) description for the GitHhub project.

		#. **GitHub Project Logo:**
			Path to the GitHub project logo. 
			Relative to project root or external (http, etc.).
			Default is blank and you can leave blank to disable.

		#. **Travis-CI Button Opt-In:**
			If your project is linked to Travis-CI you can enable the
			Travis-CI button/build badge, if you like.
			Default is [n].


Sample "`ablog start`" Flow:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

    myComp:home user$ ablog start
    Welcome to the ABlog 0.4 start utility.
    
    Please enter values for the following settings (just press Enter to
    accept a default value, if one is given in brackets).
    
    Enter the root path for your blog.
    > Root path for your blog [.]: myBlog
    
    The blog project title will occur in several places in the blog.
    > Blog project title: MyBlog
    > Author name(s): Tyler Durden       
    
    Please enter the base URL for your blog. This URL will be used for feed 
    generation.
    > Please enter the base URL for your blog. : www.blogs.com/myblog
    
    You have the Alabaster Sphinx theme install on your system, would you
    like to enable it for your blog? 
    > Enable Alabaster Sphinx theme? (y/n) [y]: y
    
    Please enter your Google Analytics ID to your blog for tracking? Leave blank for disabling.
    > Please enter your Google Analytics ID: 
    
    Would you like to enable Alabaster options for GitHub projects on your blog? 
    > Enable Alabaster GitHub features? (y/n) [n]: y
    
    Please enter the name for the GitHub project.
    > Please enter the project name. : myProject    
    
    Please enter the user name for the GitHub project.
    > Please enter GitHub user name. : myusername
    
    Please enter a short description for the GitHub project.
    > Please enter GitHub project description. : my fun project
    
    Please enter the path for the GitHub project logo. (png, jpg, etc.)
    > Please enter logo path. : mylogo.png
    
    If you happen to have the github project linked to Travis CI, you may want
    to enable the Travis-CI button in your blog.
    > Enable the Travis CI button in your blog? (y/n) [n]: y
    
    Creating file myBlog/conf.py.
    Creating file myBlog/index.rst.
    Finished: An initial directory structure has been created.