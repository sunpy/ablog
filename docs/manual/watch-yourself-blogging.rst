
Watch Yourself Blogging
=======================

.. post:: Apr 19, 2015
   :tags: commands, tips
   :category: Manual
   :author: Ahmet
   :location: SF
   :language: en

Wouldn't you like your blog being rebuilt and served to you automatically as you are blogging on a sunny Sunday afternoon?
It's now possible with the improved ``ablog serve`` command.

First, you need to install Watchdog_ Python package, e.g. `pip install watchdog`.
Then, you need to run ``ablog serve -r``.
Regardless of the weather being sunny or the day of the week, your project will be rebuilt when you change a page or add a new one.
This won't refresh your browser page though.
Unless you want to hit refresh once in a while, you can easily find an auto refresher extension for you browser.

.. _Watchdog: https://github.com/gorakhargosh/watchdog
