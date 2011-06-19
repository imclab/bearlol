#!/usr/bin/python

__author__ = "seshadri"
__doc__ = """
A bunny1 server for frequently used Berkeley websites and web services. Forked
from ccheever/bunny1 on Github.
"""
__version__ = "1.1"

CURRENT_SEMESTER = 'FL'
SEMESTER_MAP = {
    'sp':'SP',
    'spring':'SP',
    'summer':'SU',
    'sumer':'SU',
    'smr':'SU',
    'fa':'FL',
    'fl':'FL',
    'fall':'FL'
    }

import urlparse
import subprocess

import bunny1
from bunny1 import cherrypy
from bunny1 import Content
from bunny1 import q
from bunny1 import qp
from bunny1 import expose
from bunny1 import dont_expose
from bunny1 import escape

def is_int(x):
    """tells whether something can be turned into an int or not"""
    try:
        int(x)
        return True
    except ValueError:
        return False

class BearCommands(bunny1.Bunny1Commands):

    # UC Berkeley-specific commands come in before others, in alphabetical order.
    def asuc(self, arg):
        """Associated Students of the University of California (student government) website"""
        return "http://asuc.org/"

    def bandwidth(self, arg):
        """See how much bandwidth you have left"""
        return 'https://www.rescomp.berkeley.edu/cgi-bin/pub/online-helpdesk/index.pl'
    bw = bandwidth

    def bf(self, arg):
        """Bear Facts - Student Information Systems"""
        return "https://bearfacts.berkeley.edu"

    def blu(self, arg):
        """UC Berkeley Employment Portal"""
        return "http://blu.berkeley.edu"

    def bs(self, arg):
        """bSpace"""
        return "https://bspace.berkeley.edu/"

    def cll(self, arg):
        """Campus Life & Leadership"""
        return "http://campuslife.berkeley.edu/cll"

    def calmail(self, arg):
        """calmail, your @berkeley.edu email address"""
        return "http://calmail.berkeley.edu"
    email = calmail
    mail = calmail

    def decal(self, arg):
        """visit the DeCal website. decal course to search for student run courses"""
        return "http://www.decal.org/" \
            if not arg else \
            "http://www.google.com/cse?cx=008782446105542804781%3A-dpyvf3t2by&ie=UTF-8&sa=Go&siteurl=www.decal.org%2F&q=" + q(arg)

    def events(self, arg):
        """List of upcoming (official) campus events"""
        return "http://events.berkeley.edu/"

    def food(self, arg):
        """Residential Dining Menus for today. food latenight for late night menus."""
        if not arg:
            return "http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp"
        elif arg == 'latenight':
            return "http://caldining.berkeley.edu/menus_late_night.html"

    @bunny1.unlisted
    def hkn(self, arg):
        """visit the hkn website"""
        return "https://hkn.eecs.berkeley.edu"        

    def map(self, arg):
        """Campus map."""
        return "https://berkeley.edu/map"

    def sc(self, arg):
        """Search the class schedule: 'sc Chemistry', 'sc CS 61A', 'sc Fall Math 110' etc."""
        if not arg:
            return 'http://schedule.berkeley.edu'
        else:
            terms = arg.split()
            if len(terms) == 1:
                terms = [CURRENT_SEMESTER] + terms + ['']
            elif len(terms) == 2:
                terms = [CURRENT_SEMESTER] + terms
            elif len(terms) == 3:
                terms[0] = SEMESTER_MAP.get(terms[0].lower(), CURRENT_SEMESTER)
            else:
                raise HTML('could not understand your query.' + \
                               ' See the command <a href="?list">list</a> for examples')

            semester, dept, courseNum = terms
            return "http://osoc.berkeley.edu/OSOC/osoc?p_term=%s&p_dept=%s&p_course=%s" % \
                (semester, dept, courseNum)

    def sg(self, arg):
        """List all student groups. <b>sg name</b> search campus student groups by name"""
        if not arg:
            return "http://students.berkeley.edu/osl/studentgroups/public/index.asp?todo=listgroups"
        else:
            return "http://students.berkeley.edu/osl/studentgroups/public/index.asp?todo=searchgroups&keyword=" + q(arg)

    def tb(self, arg):
        """Tele-BEARS Enrollment System"""
        return "https://telebears.berkeley.edu/telebears/home"

    # General commands go here

    # an example of a redirect that goes to a non-HTTP URL
    # also, an example of a command that requires an argument
    def aim(self, arg):
        """use AOL Instant Messenger to IM a given screenname"""
        return "aim:goim?screenname=%s" % qp(arg)

    def bugcongress(self, arg):
        """looks up your senator or congressperson based on a zip code you give it"""
        # similar to the ubiquity command found here:
        # http://people.mozilla.com/~jdicarlo/ubiquity-tutorial-1.mov
        if arg:
            return "http://www.congress.org/congressorg/officials/congress/?lvl=C&azip=%s" % arg
        else:
            return "http://www.congress.org/congressorg/officials/congress/"

    def fb(self, arg):
        """search www.facebook.com or go there"""
        if arg:
            return "http://www.facebook.com/s.php?q=%s&init=q" % qp(arg)
        else:
            return "http://www.facebook.com/"
    f = fb

    def fbapp(self, arg):
        """go to a particular Facebook app's default canvas page"""
        return "http://apps.facebook.com/%s" % arg

    # an example involving slightly more complciated logic
    def fbappabout(self, arg):
        """go to the about page for an app given a canvas name, app id, or api key"""
        if is_int(arg):
            return "http://www.facebook.com/apps/application.php?id=%s" % qp(arg)
        else:
            try:
                # check to see if this is a valid API key
                if len(arg) == 32:
                    int(arg, 16)
                    return "http://www.facebook.com/apps/application.php?api_key=%s" % qp(arg)
            except ValueError:
                pass
            return "http://www.facebook.com/app_about.php?app_name=%s" % qp(arg)

    def fbdevforum(self, arg):
        """goes to the developers discussion forum.  still need to add search to this :/"""
        return "http://forum.developers.facebook.com/"

    def fblucky(self, arg):
        """facebook i'm feeling lucky search, i.e. go directly to a person's profile"""
        return "http://www.facebook.com/s.php?jtf&q=" + q(arg)
    fbs = fblucky

    def gcal(self, arg):
        """Google Calendar"""
        return 'https://www.google.com/calendar'

    def gimg(self, arg):
        """Google Image Search"""
        return 'http://images.google.com/images?q=' + q(arg)

    def gmail(self, arg):
        """Google Mail"""
        return 'https://mail.google.com/mail'
        
    def gmap(self, arg):
        """Google Maps Search"""
        return 'http://maps.google.com/maps?q=' + q(arg)
    gmaps = gmap

    def gnews(self, arg):
        """Google News"""
        return 'https://news.google.com/'

    def gtalk(self, arg):
        """Google Talk"""
        return 'https://talkgadget.google.com/talkgadget/popout'

    def gtrans(self, arg):
        """Google Translate"""
        return "http://translate.google.com/#auto|en|" + q(arg)

    def lol(self, arg):
        """a random lolcat"""
        return "http://icanhascheezburger.com/?random"

    def p(self, arg):
        """Piazzza. Doesn't search, yet.."""
        return "https://www.piazzza.com"
    piaza = piazza = piazzza = p

    @bunny1.unlisted
    def piazzzza(self, arg):
        """easter egg"""
        raise HTML('Om nom nom nom nom nom http://lavals.com')

    def qu(self, arg):
        """Quora search"""
        return 'http://www.quora.com/?q=' + q(arg)

    # an example of showing content instead of redirecting and also
    # using content from the filesystem
    def readme(self, arg):
        """shows the contents of the README file for this software"""
        raise bunny1.PRE(bunny1.bunny1_file("README"))

    def rickroll(self, arg):
        """You Just Got Rick Roll'd!"""
        return "http://tinyurl.com/djddqw"

    def yt(self, arg):
        """Searches YouTube or goes to it"""
        if arg:
            return "http://www.youtube.com/results?search_query=%s&search_type=&aq=-1&oq=" % qp(arg)
        else:
            return "http://www.youtube.com/"

    def yts(self, arg):
        """goes to your YouTube subscription center"""
        return "http://www.youtube.com/subscription_center"

    def ytd(self, arg):
        """Searches YouTube by date added instead of by relevance, or goes to youtube.com"""
        if arg:
            return "http://www.youtube.com/results?search_query=%s&search_sort=video_date_uploaded" % qp(arg)
        else:
            return "http://www.youtube.com/"

    def time(self, arg):
        """shows the current time in US time zones"""
        return "http://tycho.usno.navy.mil/cgi-bin/timer.pl"

    def ya(self, arg):
        """searches Yahoo! Answers for an answer to your question"""
        if arg:
            return "http://answers.yahoo.com/search/search_result?p=%s" % qp(arg)
        else:
            return "http://answers.yahoo.com/"

    def _author(self, arg):
        """goes to the maintainer's homepage"""
        return "https://www.twitter.com/seshness"

    @dont_expose
    def _help_html(self, examples=None, name="lolbear"):
        """the help page that gets shown if no command or 'help' is entered"""
        import random
        def bookmarklet(name):
            return """<a href="javascript:bunny1_url='""" + self._base_url() + """?';cmd=prompt('bunny1.  type &quot;help&quot; to get help or &quot;list&quot; to see commands you can use.',window.location);if(cmd){window.location=bunny1_url+escape(cmd);}else{void(0);}">""" + name + """</a>"""

        if not examples:
            examples = [
                    "g berkeley",
                    "f Seshadri",
                    "ya why are Berkeley students awesome?",
                    "list",
                    "fb mark zuckerberg",
                    "gmaps 285 Hamilton Ave, Palo Alto, CA 94301",
                    "gimg bisu",
                    "rickroll",
                    "yt i'm cool sushi654 yeah",
                    "y osteria palo alto",
                    ]

        return """
<html>
<head>
<title>lolbear</title>
""" + self._opensearch_link() + """
<style>
body {
    font-family: Sans-serif;
    width: 800px;
}

code {
    color: darkgreen;
}

A {
    color: #3B5998;
}

small {
    width: 800px;
    text-align: center;
}

.header {
    position: absolute;
    top: 0px;
    left: 0px;
}

.test-query-input {
    width: 487px;
    font-size: 20px;
}

.header-placeholder {
    height: 45px;
}

</style>
</head>
<body>
<h1 class="header-placeholder"><img class="header" src="header.gif" /></h1>

<p>""" + name + """ is a tool that lets you write smart bookmarks in python and then share them across all your browsers and with a group of people or the whole world.  It was developed at <a href="http://www.facebook.com/">Facebook</a> and is widely used there.</p>

<form method="GET">
<p style="width: 820px; text-align: center;"><input class="test-query-input" id="b1cmd" type="text" name="___" value=""" + '"' + escape(random.choice(examples)) + '"' + """/> <input type="submit" value=" try me "/></p>

<p>Type something like """ + " or ".join(["""<a href="#" onclick="return false;"><code onclick="document.getElementById('b1cmd').value = this.innerHTML; return true;">""" + x + "</code></a>" for x in examples]) + """.</p>

<p>Or you can see <a href="?list">a list of shortcuts you can use</a> with this example server.</p>

<h3>What if I want command X to do Y?</h3>
<ul>Check out the <a href="http://github.com/seshness/bearlol/">source code</a> for the project and submit a pull request, or create an "issue".</ul>
<ul>This project was forked from <a href="http://github.com/ccheever/bunny1/">ccheever/bunny1</a>.</ul>

<h3>Installing on Google Chrome</h3>
<ul>Choose <code>Preferences</code> from the wrench menu to the right of the location bar in Chrome, then under the section <code>Default Search</code>, click the <code>Manage</code> button.</ul>
<ul>Click the <code>Add</code> button and then fill in the fields name, keyword, and URL with <code>""" + name + """</code>, <code>bl</code>, and <code>""" + self._base_url() + """?%s</code>.</ul>
<ul>Hit <code>OK</code> and then select """ + name + """ from the list of search engines and hit the <code>Make Default</code> button to make """ + name + """ your default search engine.</ul>
<ul>Type <code>list</code> into your location bar to see a list of commands you can use.</ul>

<h3>Installing on Firefox</h3>
<ul>Type <code>about:config</code> into your location bar in Firefox.</ul>
<ul>Set the value of keyword.URL to be <code>""" + self._base_url() + """?</code></ul>
<ul>Make sure you include the <code>http://</code> at the beginning and the <code>?</code> at the end.</ul>
<ul>Also, if you are a Firefox user and find bunny1 useful, you should check out <a href="http://labs.mozilla.com/projects/ubiquity/">Ubiquity</a>.</ul>

<h3>Installing on Safari</h3>
<ul>Drag this bookmarklet [""" + bookmarklet(name) + """] to your bookmarks bar.</ul>
<ul>Now, visit the bookmarklet, and in the box that pops up, type <code>list</code> or <code>g facebook comments widget video</code> and hit enter.</ul>
<ul>In Safari, one thing you can do is make the bookmarklet the leftmost bookmark in your bookmarks bar, and then use <code>Command-1</code> to get to it.</ul>
<ul>Alternatively, you can get the location bar behavior of Firefox in Safari 3 by using the <a href="http://purefiction.net/keywurl/">keywurl</a> extension.</ul>

<h3>Installing on Internet Explorer</h3>
<ul>There aren't any great solutions for installing """ + name + """ on IE, but two OK solutions are:</ul>
<ul>You can use this bookmarklet [""" + bookmarklet(name) + """] by dragging into your bookmarks bar and then clicking on it when you want to use """ + name + """.</ul>
<ul>Or, in IE7+, you can click the down arrow on the search bar to the right of your location bar and choose the starred """ + name + """ option there.  This will install the bunny OpenSearch plugin in your search bar.</ul>

<br />

<div id="fb-root"></div><script src="http://connect.facebook.net/en_US/all.js#appId=135569583186732&amp;xfbml=1"></script><fb:like href="https://hkn.eecs.berkeley.edu/~seshadri/lolbear.cgi" send="true" width="450" show_faces="true" font=""></fb:like>

<hr />
<small>bunny1 was originally written by <a href="http://www.facebook.com/people/Charlie-Cheever/1160">Charlie Cheever</a> at <a href="http://developers.facebook.com/opensource.php">Facebook</a> and is maintained by him, <a href="http://www.facebook.com/people/David-Reiss/626221207">David Reiss</a>, Eugene Letuchy, and <a href="http://www.facebook.com/people/Daniel-Corson/708561">Dan Corson</a>. Julie Zhuo drew the bunny logo.
<br />
lolbear was forked and is maintained by <a href="https://twitter.com/seshness">Seshadri Mahalingam</a></small>


</body>
</html>
        """

    # fallback is special method that is called if a command isn't found
    # by default, bunny1 falls back to yubnub.org which has a pretty good
    # database of commands that you would want to use, but you can configure
    # it to point anywhere you'd like.  ex. you could run a personal instance
    # of bunny1 that falls back to a company-wide instance of bunny1 which
    # falls back to yubnub or some other global redirector.  yubnub similarly
    # falls back to doing a google search, which is often what a user wants.

    @dont_expose
    def fallback(self, raw, *a, **k):

        # this code makes it so that if you put a command in angle brackets
        # (so it looks like an HTML tag), then the command will get executed.
        # doing something like this is useful when there is a server on your
        # LAN with the same name as a command that you want to use without
        # any arguments.  ex. at facebook, there is an 'svn' command and
        # the svn(.facebook.com) server, so if you type 'svn' into the
        # location bar of a browser, it goes to the server first even though
        # that's not usually what you want.  this provides a workaround for
        # that problem.
        if raw.startswith("<") and raw.endswith(">"):
            return self._b1.do_command(raw[1:-1])

        # meta-fallback
        return bunny1.Bunny1Commands.fallback(self, raw, *a, **k)


def rewrite_tld(url, new_tld):
    """changes the last thing after the dot in the netloc in a URL"""
    (scheme, netloc, path, query, fragment) = urlparse.urlsplit(url)
    domain = netloc.split(".")

    # this is just an example so we naievely assume the TLD doesn't
    # include any dots (so this breaks if you try to rewrite .co.jp
    # URLs for example)...
    domain[-1] = new_tld
    new_domain = ".".join(domain)
    return urlparse.urlunsplit((scheme, new_domain, path, query, fragment))

def tld_rewriter(new_tld):
    """returns a function that rewrites the TLD of a URL to be new_tld"""
    return expose(lambda url: rewrite_tld(url, new_tld))


class BearDecorators(bunny1.Bunny1Decorators):
    """decorators that show switching between TLDs"""

    # we don't really need to hardcode these since they should get handled
    # by the default case below, but we'll include them just as examples.
    com = tld_rewriter("com")
    net = tld_rewriter("net")
    org = tld_rewriter("org")
    edu = tld_rewriter("edu")

    # make it so that you can do @co.uk -- the default decorator rewrites the TLD
    def __getattr__(self, attr):
        return tld_rewriter(attr)

    @expose
    def archive(self, url):
        """shows a list of older versions of the page using the wayback machine at archive.org"""
        return "http://web.archive.org/web/*/%s" % url

    @expose
    def identity(self, url):
        """a no-op decorator"""
        return url

    @expose
    def tinyurl(self, url):
        """creates a tinyurl of the URL"""
        # we need to leave url raw here since tinyurl will actually
        # break if we send it a quoted url
        return "http://tinyurl.com/create.php?url=%s" % url

class BearBunny(bunny1.Bunny1):
    """An example"""
    def __init__(self):
        bunny1.Bunny1.__init__(self, BearCommands(), BearDecorators())

    # an example showing how you can handle URLs that happen before
    # the querystring by adding methods to the Bunny class instead of
    # the commands class
    @cherrypy.expose
    def header_gif(self):
        """the banner GIF for the bunny1 homepage"""
        cherrypy.response.headers["Content-Type"] = "image/gif"
        return bunny1.bunny1_file("header.gif")


if __name__ == "__main__":
    bunny1.main_cgi(BearBunny())
