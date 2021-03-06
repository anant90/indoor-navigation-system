package pip;

import java.io.File;
import java.io.IOException;
import org.xml.sax.SAXException;

import com.keithpower.gekmlib.Configuration;
import com.keithpower.gekmlib.KMLParser;
import com.keithpower.gekmlib.Kml;

/**
 * Simple example showing how to load a KML file, modify it
 * and get the KML UpdateKML
 * @author Keith Power March 2007
 * @version 0.03
 */

public class LoadAndModifyExample
{
    public static void main(String[] args)
    {
	KMLParser parser = new KMLParser();
	try
	{
	    /**
	     * You probably don't want IDs auto-generated when you're loading
	     * a document. You can always turn it back on later.
	     * NOTE: KML updates will only work for objects that have
	     * an ID (either autogenerated or assigned).
	     */
	    Configuration.properties.setProperty(Configuration.GENERATE_IDS, Configuration.OFF);

	    Kml ge = parser.parse(new File("whale_shark.kml"));
	    /**
	     * A path identifying a KML document. Any updates produced
	     * will refer to this URL.
	     */
	    ge.setHref("http://someserver.com/somepath");
	    /**
	     * Note: should call it once immediately, unless you want
	     * to produce an update from a blank document (you usually
	     * don't).
	     */
	    ge.toUpdateKML();

	    // Now, change a lookAt deep in the document
	    ge.getFolder().getFolders()[0].getPlacemarks()[0].getLookAt().setAltitude(666.0);

	    // Now, get the KML to produce the update and print it
	    System.out.println(ge.toUpdateKML());
	} catch (IOException e)
	{
	    // Just fail
	    System.err.println("Error reading file "+e);
	} catch (SAXException e)
	{
	    // Just fail
	    System.err.println("Error parsing "+e);
	}
    }
    
}
