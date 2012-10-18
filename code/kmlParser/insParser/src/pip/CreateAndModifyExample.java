package pip;

import com.keithpower.gekmlib.Folder;
import com.keithpower.gekmlib.Kml;
import com.keithpower.gekmlib.LineString;
import com.keithpower.gekmlib.Placemark;
import com.keithpower.gekmlib.Point;


/**
 * This is a first bash, there's still much to be done.
 * Including catching the CloneNotSupportedException  
 * 
 * @author Keith Power March 2007
 * @version 0.03
 */

public class CreateAndModifyExample
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
	    
	// call toUpdateKML so these creates are not part of next update
	doc.toUpdateKML();
	
	// Copy first placemark, change coordinates and add to folder
	Placemark mark2 = new Placemark();
	LineString line = new LineString();
	line.setCoordinates("1, 2, 3 4, 5, 6");
	mark2.addLineString(line);
	container.addPlacemark(mark2);
	// also change named of first placemark
	mark1.setName("Placemark 1");
	System.out.println(doc.toUpdateKML());
	    
	// Now delete the first placemark
	container.removeFeature(mark1);
	System.out.println(doc.toUpdateKML());
    }    
}
