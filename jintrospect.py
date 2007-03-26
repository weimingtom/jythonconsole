"""Extend introspect.py for Java based Jython classes."""

from org.python.core import PyJavaClass
from java.lang import Class
from java.lang.reflect import Modifier
from java.util.logging import Logger
from introspect import *
import string
import re
import types

__author__ = "Don Coleman <dcoleman@chariotsolutions.com>"

_re_import_package = re.compile('import\s+(.+)\.') # import package
# TODO need to check for a trailing '.'  example: "from java import lang." don't autocomplete on trailing '.'
_re_from_package_import = re.compile('from\s+(\w+(?:\.\w+)*)\.?(?:\s*import\s*)?') # from package import class 

# TODO replace this with something better!
def debug(name, value=None):
    if value == None:
        print >> sys.stderr, name
    else:
        print >> sys.stderr, "%s = %s" % (name, value)

def completePackageName(target):
    """ Get a package object given the full name."""      
    targetComponents = target.split('.')
    base = targetComponents[0]
    baseModule = __import__(base, globals(), locals())
    module = baseModule    

    for component in targetComponents[1:]:
        module = getattr(module, component)

    list = dir(module)
    list.remove('__name__')
    list.append('*')
    return list
  
def getPackageName(command):    
        
    match = _re_import_package.match(command)
    if not match:
        #try the other re
        match = _re_from_package_import.match(command)
            
    return match.groups()[0]

def unique(methods):
    """
    Return a unique list of methods
    """
    umethods = []
    
    u = {}
    for method in methods:
        if not u.has_key(method.__name__):
            u[method.__name__] = 1
            umethods.append(method)
    
    return umethods

def getAutoCompleteList(command='', locals=None, includeMagic=1, 
                        includeSingle=1, includeDouble=1):
    """Return list of auto-completion options for command.
    
    The list of options will be based on the locals namespace."""
    debug("getAutoCompleteList '%s'" % command) 

    # Temp KLUDGE here rather than in console.py
    command += "."

    attributes = []
    # Get the proper chunk of code from the command.
    root = getRoot(command, terminator='.')
    
    # check to see if the user is attempting to import a package
    # this may need to adjust this so that it doesn't pollute the namespace
    if command.startswith('import ') or command.startswith('from '):
        target = getPackageName(command)
        return completePackageName(target)
    
    try:
        if locals is not None:
            object = eval(root, locals)
        else:
            object = eval(root)
    except:
        return attributes
    
    if ispython(object):
        # use existing code
        attributes = getAttributeNames(object, includeMagic, includeSingle, includeDouble)
    else:
        if type(object) == PyJavaClass:
            attributes = staticMethodNames(object)
            attributes.extend(staticFieldNames(object))
        else:
            # TODO hide static methods
            methods = unique(methodsOf(object.__class__))
            attributes = [eachMethod.__name__ for eachMethod in methods]
        
    return attributes

def staticMethodNames(clazz):
    """return a list of static method name for a class"""
    # TODO get static methods from base classes
    static_methods = {}
    declared_methods = Class.getDeclaredMethods(clazz)
    for method in declared_methods:
        if Modifier.isStatic(method.getModifiers()) and Modifier.isPublic(method.getModifiers()):
            static_methods[method.name] = method
    methods = static_methods.keys()
    
    for eachBase in clazz.__bases__:
        methods.extend(staticMethodNames(eachBase)) 
    
    return methods
    
def staticFieldNames(clazz):
    """return a list of static field names for class"""
    # TODO get static fields from base classes
    static_fields = {}
    declared_fields = Class.getDeclaredFields(clazz)
    for field in declared_fields:
        if Modifier.isStatic(field.getModifiers()) and Modifier.isPublic(field.getModifiers()):
            static_fields[field.name] = field
    fields = static_fields.keys()   
    
    for eachBase in clazz.__bases__:
         fields.extend(staticFieldNames(eachBase)) 

    return fields        

def methodsOf(clazz):
    """return a list of all the methods in a class"""
    classMembers = vars(clazz).values()
    methods = [eachMember for eachMember in classMembers if callable(eachMember)]
    for eachBase in clazz.__bases__:
        methods.extend(methodsOf(eachBase))
    return methods

def getCallTipJava(command='', locals=None):
    """For a command, return a tuple of object name, argspec, tip text.

    The call tip information will be based on the locals namespace."""

    calltip = ('', '', '')  # object name, argspec, tip text.

    # Get the proper chunk of code from the command.
    root = getRoot(command, terminator='(')

    try:
        if locals is not None:
            object = eval(root, locals)
        else:
            object = eval(root)
    except:
        return calltip

    if ispython(object):
        # Patrick's code handles python code
        # TODO fix in future because getCallTip runs eval() again
        return getCallTip(command, locals)

    name = ''
    try:
        name = object.__name__
    except AttributeError:
        pass
    
    tipList = []
    argspec = '' # not using argspec for Java
    
    if inspect.isbuiltin(object):
        # inspect.isbuiltin() fails for Jython
        # Can we get the argspec for Jython builtins?  We can't in Python.
        pass
    elif inspect.isclass(object):
        # get the constructor(s)
        # TODO consider getting modifiers since jython can access private methods
        constructors = object.getConstructors()
        for constructor in constructors:
            paramList = []
            paramTypes = constructor.getParameterTypes()
            # paramTypes is an array of classes, we need Strings
            # TODO consider list comprehension
            for param in paramTypes:
                # TODO translate [B to byte[], [C to char[] etc
                paramList.append(param.__name__)
            paramString = string.join(paramList,', ')
            tip = "%s(%s)" % (constructor.name, paramString)
            tipList.append(tip)
             
    elif inspect.ismethod(object):
        method = object
        object = method.im_class

        # java allows overloading so we may have more than one method
        methodArray = object.getMethods()

        for eachMethod in methodArray:
            if eachMethod.name == method.__name__:
                paramList = []
                for eachParam in eachMethod.parameterTypes:
                    paramList.append(eachParam.__name__)
                 
                paramString = string.join(paramList,', ')

                # create a python style string a la PyCrust
                # we're showing the parameter type rather than the parameter name, since that's all I can get
                # we need to show multiple methods for overloading
                # TODO improve message format
                # do we want to show the method visibility
                # how about exceptions?
                # note: name, return type and exceptions same for EVERY overload method

                tip = "%s(%s) -> %s" % (eachMethod.name, paramString, eachMethod.returnType)
                tipList.append(tip)
            
#    else:
#        print "Not a java class :("

    calltip = (name, argspec, string.join(tipList,"\n"))
    return calltip
                                      
def ispython(object):
    """
    Figure out if this is Python code or Java Code

    """
    pyclass = 0
    pycode = 0
    pyinstance = 0
    
    if inspect.isclass(object):
        try:
            object.__doc__
            pyclass = 1
        except AttributeError:
            pyclass = 0

    elif inspect.ismethod(object):
        try:
            object.__dict__
            pycode = 1
        except AttributeError:
            pycode = 0
    else: # I guess an instance of an object falls here
        try:
            object.__dict__
            pyinstance = 1
        except AttributeError:
            pyinstance = 0

#    print "object", object, "pyclass", pyclass, "pycode", pycode, "returning", pyclass | pycode
    
    return pyclass | pycode | pyinstance

