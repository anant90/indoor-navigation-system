package pip;

/**
 * A simple example showing how to create a Kml document from
 * scratch.
 *  
 * @author Keith Power March 2007
 * @version 0.03
 */

import com.keithpower.gekmlib.Folder;
import com.keithpower.gekmlib.Kml;
import com.keithpower.gekmlib.Placemark;
import com.keithpower.gekmlib.Point;

public class CreateExample
{
    public static void main(String[] args)
    {
	// Start with a blank Kml object, give it a URL
	Kml doc = new Kml();
	doc.setHref("http://localhost/random");

	// create and add root folder
	Folder root = new Folder();
	root.setName("Root Folder");
	root.setDescription("This is the root folder");
	doc.addFolder(root);
	
	// create and add another folder to root
	Folder container = new Folder();
	container.setName("First Sub Folder");
	container.setDescription("This is the a folder contained by the root");
	root.addFolder(container);
	
	// create and add a Placemark containing a Point
	Placemark mark1 = new Placemark();
	Point point1 = new Point();
	point1.setCoordinates("1, 2, NA");	// NA will go to 0.0
	mark1.addPoint(point1);
	container.addPlacemark(mark1);
	System.out.println(doc.toKML()+"\n\n");
    }    
}
