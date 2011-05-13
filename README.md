It's convert your snipplr snipt to files. You need to api key from snipplr. You can get from http://www.snipplr.com/settings/ . I'm writting this code for Snippets application in Mac OSX. So, I didn't add so many language. I only add some language that I use.

How to use
----------
In snipplr.py , change Your API Key to your api key that get from settings page.

	snipplr.setup("Your API Key")

After saving, you can run like following from terminal

	$python snipplr.py

after converting , you will see all the file in output folder. Now, it's not support all the language. You can add your langauge in

	def get_ext(language):

Special Thank
-------------
I'm using SnipplrPy.py from http://code.google.com/p/geditsnipplr/