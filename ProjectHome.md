Jython Console is a Jython Interactive Interpreter that adds Code Completion.

![http://jythonconsole.googlecode.com/svn/trunk/jythonconsole.png](http://jythonconsole.googlecode.com/svn/trunk/jythonconsole.png)

Check out the [screenshots](http://don.freeshell.org/jython/screenshots.html).

**Jythonconsole-0.0.7 works with Jython 2.5**

Requirements
  * [Java](http://java.sun.com)
  * [Jython](http://www.jython.org)

Installation
  * [Download](http://jythonconsole.googlecode.com/files/jythonconsole-0.0.7.zip) jythonconsole-0.0.7.zip
  * Unzip the archive
  * Open a terminal or cmd prompt
  * cd jythonconsole-0.0.7
  * jython console.py

Hints
  * 

&lt;TAB&gt;

 and 

&lt;ENTER&gt;

 choose method completion
  * remember to use the keyboard not the mouse
  * 

&lt;ESC&gt;

 makes the popup go away

0.0.7
  * **works with Jython 2.5**
  * Fixes [Issue 17](https://code.google.com/p/jythonconsole/issues/detail?id=17), [Issue 18](https://code.google.com/p/jythonconsole/issues/detail?id=18) and [Issue 21](https://code.google.com/p/jythonconsole/issues/detail?id=21)

0.0.6
  * This release should work on Windows
  * Fixes [Issue 7](https://code.google.com/p/jythonconsole/issues/detail?id=7), [Issue 8](https://code.google.com/p/jythonconsole/issues/detail?id=8) and [Issue 10](https://code.google.com/p/jythonconsole/issues/detail?id=10)

0.0.5
  * beautify call tips - remove 'java.lang.', translate [to byte[](B.md), [to char[](C.md), etc.
  * don't show static methods when completing methods for an object instance
  * show properties for accessors when completing methods e.g. foo for getFoo()
  * fix [Issue 3](https://code.google.com/p/jythonconsole/issues/detail?id=3) sends KeyboardInterrupt on CTRL+C or CTRL+BREAK
  * fix [Issue 4](https://code.google.com/p/jythonconsole/issues/detail?id=4) patch submitted by andeol
  * fix [Issue 5](https://code.google.com/p/jythonconsole/issues/detail?id=5) Page Up and Down in popup pgupdown - patch submitted by andeol
  * remove dis.py since it's no longer used
  * modify jintrospect since inspect.py from jython 2.2 does not have isbuiltin()

0.0.4
  * change code since os.path missing from Jython 2.2a0
  * remove stack trace when completion fails

0.0.3
  * code cleanup
  * more unit tests
  * Emacs style keybindings C-a, C-e, C-k, C-y
  * hide special and private python methods by default
  * new implemention of jintrospect.ispython for Jython2.2 changes
  * add Console.main(namespace) to make embedding in Java easier
  * history ignores duplicates
  * backspace won't overwrite the prompt
  * too many backspaces in popup will now close the popup
  * convert stray tabs to spaces

0.0.2
  * '(' and ')' now insert at the caret rather than at the end of the line
  * Duplicates are removed from the method completion list for Java classes (Patch from Harry Fuecks)
  * Added auto complete for imports
  * Added auto complete for static methods and static field on java classes
  * Fix StackOverflow in introspect.py with Jython 2.2b1

Credits
  * This project uses code from Patrick O'Brien's [PyCrust](http://sourceforge.net/projects/pycrust/) as well as [inspect.py](http://www.python.org/doc/current/lib/module-inspect.html) from [Python](http://www.python.org) 2.2.2 for Python completion.
  * The UI uses code from Carlos Quiroz's [Jython Interpreter for JEdit](http://www.jedit.org)

This project moved here from the [old site](http://don.freeshell.org/jython/).
