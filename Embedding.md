# Introduction #

Here's one way to embed Jython Console into a Java application

# Details #

```
import org.python.core.PySystemState;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

/**
 * Simple Java Wrapper around JythonConsole Code (written in Jython).
 * <p/>
 * This should enable JythonConsole to be embedded in a Java application. 
 */
public class EmbedExample {

    public EmbedExample() {

        PySystemState.initialize();
        PythonInterpreter pyi = new PythonInterpreter();   
        pyi.exec("import sys");    
        // you can pass the python.path to java to avoid hardcoding this
        // java -Dpython.path=/path/to/jythonconsole-0.0.6 EmbedExample
        pyi.exec("sys.path.append(r'/path/to/jythonconsole-0.0.6/')");
        pyi.exec("from console import main");
        PyObject main = pyi.get("main");

        // stuff some objects into the namespace
        // this will probably be objects from your application
        pyi.set("embed_example", this);
        pyi.set("foo", "bar");
        pyi.set("n", 17);
        main.__call__(pyi.getLocals());
    }

    public static void main(String[] args) {
        new EmbedExample();
    }

}

```