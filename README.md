fbxapitool
==========

Warning : this package deals with documented API functions, where some are unstables meaning these can change in the future ; moreover some others are not documented (OpenVPN Client & VM management), then they are more unstables

This package is an evolution of "freepybox", available here : https://github.com/fstercq/freepybox. In addition of many modifications, it brings new functions to missing API calls. But the Freebox API is not fully covered. Some features has not been tested, as they refers to options that I've not subscribed. It was developed with Python 3 with Delta S box, and tested under Linux (Debian & Ubuntu). I think it can be used under macOS, not yet tested on my side. I've no idea of the effort required to used it on Windows 10, and I'll not do it. Last but not least, it'll only work with last version of the API in end of 2020, which mean version 8.

Install
-------

Manually download and install the last version from github
```bash
$ git clone https://github.com/corwin-31/fbxapitool.git
$ python setup.py install
```

Get started
-----------
```python
# Import fbxapitool package
from fbxapitool import Freebox

# Instantiate the Freebox class
# Be ready to authorize the app on the box
fbx = Freebox()

# Connect, open a session to the freebox
fbx.open('mafreebox.freebox.fr',443)

# Do something usefull, rebooting the box for example
fbx.system.reboot()

# Close the session.
fbx.close()
```
Have a look on the [fbx-status.py] (https://github.com/corwin-31/fbxapitool/blob/master/fbx-status.py) for a more complete overview

Resources
---------
Freebox OS API documentation : http://dev.freebox.fr/sdk/os/ or http://mafreebox.freebox.fr/doc/index.html#

