from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from wiki.models import *
from myghtyboard.models import *


Page.objects.all().delete()
p = Page(title='Diamanda Wiki Main Page', slug='index', description='A description :)', text='''[rk:h id="1"]Diamanda Wiki SVN[/rk:h]
[toc]<br /><br />

Diamanda (wiki, forum and other apps) is released under GPL License<br />
<b>Author</b>: Piotr Malinski - riklaunim@gmail.com | <a href="http://www.rkblog.rk.edu.pl">English support</a> | <a href="http://www.python.rk.edu.pl">Polskie Wsparcie</a><br />

<div class="box">This applications is in developement and currently is in Quasi-Stable stage.</div>
<br />
[rk:h id="2"]Features[/rk:h]
- Engines and themes (engine - set of X/HTML templates, themes - sets of CSS stylesheets)<br />
- multilingual interface (pl/en currently)<br /><br />
<b>WIKI</b>
<blockquote>
- add, Edit Pages with permission controll<br />
- full history support<br />
- diffs between all versions of a wikiPage<br />
- safe HTML markup and plugable ContentBBcode tags<br />
- google sitemap generation<br />
- PDF export with htmldoc<br />
</blockquote><br />
<b>MyghtyBoard Forum</b>
<blockquote>
- Add Topic/Post<br />
- Edit my posts<br />
- Permission controll, user cant post a new post after his post<br />
- IP saved<br />
- Nice themes :)<br />
- Lock/Open topics, sticky/global topics<br />
- Topics with my posts, My Topics, Last active Topics lists<br />
- Move Topics
</blockquote>
<b>OTHER APPS</b>
<blockquote>
- Task Manager: manage site tasks and helps coordinate users work<br />
- News: simple news system with keywords<br />
- Stats: Unique entries and referer stats and charts<br />
- User Panel: User Profile, users list, sending messages (emails), login and register with Captcha<br />
- Site Statistics (under /stats/ for admins): unique entries, referers, keywords from google
</blockquote>

<div class="box"><b>NOTE!</b><br />
- All applications can be rather easily used alone (requires some small changes) See support site for more details.</div><br />

[rk:h id="2"]Requirements:[/rk:h]
- install <b>strip-o-gram</b> from <a href="http://www.zope.org/Members/chrisw/StripOGram" target="_blank">here</a> - its a safe HTML filter which is used in Diamanda WikiPages and forums.
<div class="box">python setup.py install</div>
will install it.<br />
- <b>pygments</b>: for code highlighting.<br />
- <b>pyGoogle</b>: optional, if you want to use Google Search API as an extra site search<br />
- <b>matplotlib</b>: optional for Site Statistics unique entries chart<br />
- <b>PIL - Python Imaging Library</b>: makes thumbs and Captcha<br /><br />

[rk:h id="2"]Instalation:[/rk:h]
- edit urls.py and change the site_media path /home/piotr/diamanda/media to that on your computer:
<div class="box">(r^site_media/(.*)$, django.views.static.serve, {document_root: /path/here}),</div>

- create tables (sqlite3 by default):
<div class="box">python manage.py syncdb<br />
python install.py</div>
- create a superuser when creating tables!<br />

- run the dev server: 
<div class="box">python manage.py runserver 8080</div>
<br />

<div class="box">Debug is set to True by default!</div>
<br /><br />

[rk:h id="2"]MyghtyBoard[/rk:h]
MyghtyBoard is the name of the forum script  - it doesn't require myghty (the template framework) but I very old times "MyghtyBoard" was a mygty based forum skeleton app ;) so I've kept the name.<br />
Categories and Forums are managed by the Django Admin Panel. Staff members and superusers are forum moderators.
<br /><br />

[rk:h id="2"]Extra settings in settings.py[/rk:h]
There is some extra settings variables in <b>settings.py</b>.<br />
- RSS settings are used when generating RSS Feeds.<br />
- Anonymous Permissions: True/False<br /><br />

[rk:h id="2"]Logged in users - Permissions[/rk:h]
- add, edit perms are used on Wiki Pages to check if user can add or edit pages. There are also two extra options:<br />
"Can view Page" - can see pages<br />
"Can set Page as current" - can set edited page as current<br /><br />

[rk:h id="3"]CAN_SET_CURENT and Edit Proposals[/rk:h]
If someone cant set edited page as current it will be saved as a one of older versions of that Wiki Page but it will be market as Edit Proposal 
and on the history list will be highlighted in green. Staff members can "unpropose" it (becomes normal "old version") or anyone who CAN_SET_CURENT and edit can
restore it / and if needed - edit it.<br />
- A list of all Edit Proposals can be found on /wiki/proposals/<br /><br />

[rk:h id="2"]RSS Feeds[/rk:h]
<div class="box">http://localhost:8080/wiki/feeds/latestpages/ - latest pages</div>
<br />

[rk:h id="2"]ContentBBCode[/rk:h]
Wiki CBC Descriptions module in the Admin Panel is designed to keep descriptions of all CBC plugins you have. ContentBBcode is a pluggable 
tags system (CBC for short). A CBC plugin can be a JS widget wrapper or perform other dynamic operations like display latest changes on the wiki.<br /><br />


[rk:h id="1"]TODO[/rk:h]
- Themes/Engines improvements and fixes<br />
- Polish all the features<br />
- If full history will get diffs and will be finished and merged to django + the same for full text search then those contribs could be used<br />
- ReST support ? :)<br />
- Suggestions welcomed...
''', changes='Page Creation', creation_date='2006-09-04 15:42:46', modification_date='2006-09-04 15:42:46', modification_user='piotr', modification_ip='666.69.69.69')
p.save()

Category.objects.all().delete()
mc = Category(cat_name='First Category', cat_order='0')
mc.save()
mc = Category(cat_name='Second Category', cat_order='1')
mc.save()

Forum.objects.all().delete()
mf = Forum(forum_category = Category.objects.get(id=1), forum_name = 'First Forum', forum_description ='A Forum', forum_order='0', forum_posts='4', forum_lastpost = 'piotr<br />2006-09-04 15:56:29<br /><a href="/forum/topic/1/2/">Frugalware Topic</a>')
mf.save()
mf = Forum(forum_category = Category.objects.get(id=1), forum_name = 'Second Forum', forum_description ='A description', forum_order='1')
mf.save()
mf = Forum(forum_category = Category.objects.get(id=2), forum_name = 'Bla bla bla', forum_description ='Extra Forum', forum_order='0')
mf.save()

Topic.objects.all().delete()
mt = Topic(topic_forum = Forum.objects.get(id=1), topic_name = 'A Test Topic', topic_author = 'piotr', topic_posts = '2', topic_lastpost = 'piotr<br />2006-09-04 15:55:11', topic_modification_date = '2006-09-04 15:55:11')
mt.save()
mt = Topic(topic_forum = Forum.objects.get(id=1), topic_name = 'Frugalware Topic', topic_author = 'piotr', topic_posts = '2', topic_lastpost = 'piotr<br />2006-09-04 15:56:29', topic_modification_date = '2006-09-04 15:56:29')
mt.save()

Post.objects.all().delete()
mp = Post(post_topic = Topic.objects.get(id=1), post_text = 'This is a test topic\r\n\r\n:twisted::grin:', post_author = 'piotr', post_date = '2006-09-04 15:55:00', post_ip = '127.0.0.1')
mp.save()
mp = Post(post_topic = Topic.objects.get(id=1), post_text = 'and a test reply', post_author = 'piotr', post_date = '2006-09-04 15:55:11', post_ip = '1.2.3.4')
mp.save()
mp = Post(post_topic = Topic.objects.get(id=2), post_text = 'Miklos Vajna has announced the second release candidate of Frugalware Linux 0.5, the last development build before the stable release, expected at the end of September: "The Frugalware Developer Team is pleased to announce the immediate availability of Frugalware 0.5rc2, the second release candidate of the upcoming 0.5 stable release. A short and incomplete list of changes since 0.5rc1: updated GNOME to 2.16 Release Candidate (2.15.92); ~300 bugfixes; updated KDE and GRUB artwork; more than 30 new packages: ntfs-3g, avifile, gnome-sharp and many more!" Here is the brief release announcement. Download (SHA1): frugalware-0.5rc2-i686-dvd1.iso (4,264MB).', post_author = 'piotr', post_date = '2006-09-04 15:56:12', post_ip = '1.2.3.4')
mp.save()
mp = Post(post_topic = Topic.objects.get(id=2), post_text = '<blockquote><b>piotr wrote:</b><br /><cite>Mikos Vajna has announced the second release candidate of Frugalware Linux 0.5, the last development build before the stable release, expected at the end of September: "The Frugalware Developer Team is pleased to announce the immediate availability of Frugalware 0.5rc2, the second release candidate of the upcoming 0.5 stable release. A short and incomplete list of changes since 0.5rc1: updated GNOME to 2.16 Release Candidate (2.15.92); ~300 bugfixes; updated KDE and GRUB artwork; more than 30 new packages: ntfs-3g, avifile, gnome-sharp and many more!" Here is the brief release announcement. Download (SHA1): frugalware-0.5rc2-i686-dvd1.iso (4,264MB).</cite></blockquote>\r\nTollef Fog Heen has announced the second alpha release (also known as "Knot") of Ubuntu 6.10, code name "Edgy Eft": "Welcome to Edgy Eft Knot 2, which will in time become Ubuntu 6.10. The primary changes from Knot 1 have been implementations of feature goals as listed on this page. Common to all variants, we have upgraded X.Org to the 7.1 release. In Ubuntu, GNOME has been updated to 2.16.0 Release Candidate 1. Other notable changes are listed here. KDE has been updated to 3.5.4. Other notable Kubuntu changes are listed here." Read the full release announcement for further information and a list of up-to-date download mirrors. As always, the full range of live and installation CDs for various architectures is available for download from the project''s main server; here is a quick link to the i386 Desktop CD: edgy-desktop-i386.iso (666MB, MD5). Kubuntu 6.10 Knot 2 CDs have also been released.', post_author = 'piotr', post_date = '2006-09-04 15:56:29', post_ip = '1.2.3.4')
mp.save()

from django.contrib.auth.models import Group, Permission
Group.objects.all().delete()
g = Group(name='users')
g.save()
#a = Permission.objects.all()
#for i in a:
	#print str(i.name) + ' - ' + str(i.codename)
g.permissions.add(Permission.objects.get(codename='can_view'), Permission.objects.get(codename='can_set_current'), Permission.objects.get(codename='add_page'), Permission.objects.get(codename='add_taskcomment'), Permission.objects.get(codename='change_page'), Permission.objects.get(codename='add_topic'), Permission.objects.get(codename='add_post'))
