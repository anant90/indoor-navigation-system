/*
 Author:	Anant Jain
 Dated:		October 2010
 Email:		anant90@gmail.com
 */


//package pip;

import java.io.*;
import org.xml.sax.SAXException;

import com.keithpower.gekmlib.Configuration;
import com.keithpower.gekmlib.KMLParser;
import com.keithpower.gekmlib.Kml;
import com.keithpower.gekmlib.Placemark;
import com.keithpower.gekmlib.Feature;
import com.keithpower.gekmlib.Geometry;
import com.keithpower.gekmlib.Point;
import com.keithpower.gekmlib.LineString;
import com.keithpower.gekmlib.Document;

import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;



public class parse
{
	static int ARRAY_SIZE = 100;
	static insNode[] insNodeArray = new insNode[ARRAY_SIZE]; // Start of the graph
	
    public static class insNode {
		
		double latitude;
		double longitude;
		int n, s, e, w, ne, nw, se, sw;
		int id;
		int priorityOrder;
		boolean isPublicUtility;
		String publicUtilityType;
		String nodeName;
		
		public insNode() {
			id = -1;
			nodeName = null;
			latitude = 0;
			longitude = 0;
			n = -1;
			e = -1;
			w = -1;
			s = -1;
			ne = -1;
			nw = -1;
			se = -1;
			sw = -1;
			id = -1;
			priorityOrder = 1;
			isPublicUtility = false;
			publicUtilityType = null;
		}
		
		public insNode(int idNo, double lati, double longi) {
			
			nodeName = null;
			id = idNo;
			latitude = lati;
			longitude = longi;
			
			n = -1;
			e = -1;
			w = -1;
			s = -1;
			ne = -1;
			nw = -1;
			se = -1;
			sw = -1;
			
			priorityOrder = 1;
			isPublicUtility = false;
			publicUtilityType = null;
			
		}
		
		public double getLatitude() {
			return latitude;
		}
		
		public double getLongitude() {
			return longitude;
		}
		
		public void setName(String n) {
			nodeName = n;
		}
		
		public String getName() {
			return nodeName;
		}
		
		public void setN(int i) {
			n = i;
		}
		
		public void setE(int i) {
			e = i;
		}
		
		public void setW(int i) {
			w = i;
		}
		
		public void setS(int i) {
			s = i;
		}
		
		public void setNE(int i) {
			ne = i;
		}
		
		public void setNW(int i) {
			nw = i;
		}
		
		public void setSE(int i) {
			se = i;
		}
		
		public void setSW(int i) {
			sw = i;
		}
		
		public int getN() { return n; }
		public int getNE() { return ne; }
		public int getE() { return e; }
		public int getSE() { return se; }
		public int getS() { return s; }
		public int getSW() { return sw; }
		public int getW() { return w; }
		public int getNW() { return nw; }
		
		public String description() {
			String desc = "";
			desc += id; desc += ",";
			desc += longitude; desc += ",";
			desc += latitude; desc += ",";
			
			if(isPublicUtility)
				desc += "True,";
			else 
				desc += "False,";
			
			if(publicUtilityType==null) desc+="\"\"";
			else desc += publicUtilityType; desc += ",";
			desc += nodeName; desc += ",";
			desc += priorityOrder; desc += ",";
			desc += n; desc += ",";
			if(n==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[n].getLongitude(), insNodeArray[n].getLatitude()); desc+=","; }
			desc += ne; desc += ",";
			if(ne==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[ne].getLongitude(), insNodeArray[ne].getLatitude()); desc+=","; }
			desc += e; desc += ",";
			if(e==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[e].getLongitude(), insNodeArray[e].getLatitude()); desc+=","; }
			desc += se; desc += ",";
			if(se==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[se].getLongitude(), insNodeArray[se].getLatitude()); desc+=","; }
			desc += s; desc += ",";
			if(s==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[s].getLongitude(), insNodeArray[s].getLatitude()); desc+=","; }
			desc += sw; desc += ",";
			if(sw==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[sw].getLongitude(), insNodeArray[sw].getLatitude()); desc+=","; }
			desc += w; desc += ",";
			if(w==-1) desc+="-1,"; else { desc+= distance(longitude, latitude, insNodeArray[w].getLongitude(), insNodeArray[w].getLatitude()); desc+=","; }
			desc += nw;	desc+=",";
			if(nw==-1) desc+="-1"; else { desc+= distance(longitude, latitude, insNodeArray[nw].getLongitude(), insNodeArray[nw].getLatitude()); }
			desc +=";";
			return desc;
		}
	}
	
	public static double distance(double long_1, double lat_1, double long_2, double lat_2) {
		
		double latDiff = lat_1-lat_2;
		double longDiff = long_1-long_2;
		
		// convert latDiff and longDiff to metres:
		latDiff *= 110828.28; // hard coded for 28.545 deg N; Replace with appropriate formula
		longDiff *= 97862.52; // hard coded for 28.545 deg N; Replace with appropriate formula
		
		return Math.sqrt(latDiff*latDiff + longDiff*longDiff);
	}
	
	public static int heading(double longFrom, double latFrom, double longTo, double latTo) {
		
		double latDiff = latTo - latFrom;
		double longDiff = longTo - longFrom;
		
		// convert latDiff and longDiff to metres:
		latDiff *= 110828.28; // hard coded for 28.545 deg N; Replace with appropriate formula
		longDiff *= 97862.52; // hard coded for 28.545 deg N; Replace with appropriate formula
		double angle;
		int quadrant;
		if(longDiff==0) angle = 0;
		else {
			if (latDiff<0 && longDiff<0) quadrant = 3;
			else if(latDiff<0 && longDiff>0) quadrant = 2;
			else if(latDiff>=0 && longDiff<0) quadrant = 4;
			else quadrant = 1;
			latDiff = Math.abs(latDiff);
			longDiff = Math.abs(longDiff);
			angle = Math.atan(latDiff/longDiff);
			angle *= 180/(Math.PI);
			//System.out.println(angle);
			switch(quadrant) {
				case 1:
					angle = 90-angle;
					break;
				case 2:
					angle = 90+angle;
					break;
				case 3:
					angle = 270 - angle;
					break;
				case 4:
					angle = 270+angle;
					break;
			}
		}
		return (int)angle;
	}
	
	public static double distance(Point p1, Point p2) {
		
		double [] array1 = p1.getNumericalCoordinates();
		double [] array2 = p2.getNumericalCoordinates();
		
		double long_1 = array1[0];
		double lat_1 = array1[1];
		double long_2 = array2[0];
		double lat_2 = array2[1];
		
		//System.out.println("\n\nListing: "+lat_1+" "+long_1+" "+lat_2);
		return distance(long_1, lat_1, long_2, lat_2);
		
	}
	public static void main(String[] args)
    {
	KMLParser parser = new KMLParser();
	try
	{
		//Auto-ID setting:
		Configuration.properties.setProperty(Configuration.GENERATE_IDS, Configuration.OFF);
		BufferedWriter printer = new BufferedWriter(new FileWriter(args[0]+".map"));
		BufferedWriter kmlPrinter = new BufferedWriter(new FileWriter("processed"+args[0]));
		
		Kml doc = parser.parse(new File(args[0])); 
		Kml processedKml = new Kml();
		Document processedDoc = new Document();
		
		
		// Get a list of the placemarks
		List placemarks = doc.getDocument().getPlacemarks();
		
		int noOfNodes = 0;
		int orientation = 0;
		
		// Iterator for all the LineStrings:
		boolean firstTime = true; // for setting the orientation;
		
		for(Iterator iter = placemarks.iterator(); iter.hasNext();)
		{
            Placemark cur = (Placemark)iter.next();
            if(cur.getGeometry() instanceof LineString)
            {
				// Do something with the LineStrings here
				LineString a = cur.getLineString();
				double[] coordinates = a.getNumericalCoordinates();
				int lastVertex = -1;
				for (int i = 0; i<coordinates.length; i++) {
					double thisLongitude = coordinates[i++];
					double thisLatitude = coordinates[i++];
					
					// Addition of the new coordinate to the graph;
					int alreadyPresent = -1;
					// Check if already in the graph
					for (int j=0; j<noOfNodes; j++) {
						
						if(distance(insNodeArray[j].getLongitude(), insNodeArray[j].getLatitude(), thisLongitude, thisLatitude)<0.5) {
							alreadyPresent = j;
						}
						
					}
					
					if(alreadyPresent == -1) {
						insNode newNode = new insNode( noOfNodes, thisLatitude, thisLongitude );
						insNodeArray[noOfNodes++] = newNode;
						alreadyPresent = noOfNodes-1;
					}
					
				
					if (lastVertex==-1) {
						// this was the first vertex, set lastVertex:
						lastVertex = alreadyPresent;
					}
					else {
						// this isn't the first vertex: link it up with the last vertex;
						
						// find heading between lastVertex and this one
						int head = heading(insNodeArray[lastVertex].getLongitude(), insNodeArray[lastVertex].getLatitude(), thisLongitude, thisLatitude );
						if(firstTime == true) {
							firstTime = false;
							orientation = head;
						}
						head -= orientation; // Get the heading to local orientation
						
						if (head>337 || head <= 23) {
							insNodeArray[lastVertex].setN(alreadyPresent);
							insNodeArray[alreadyPresent].setS(lastVertex);
						}
						else if (head>23 && head <= 67) {
							insNodeArray[lastVertex].setNE(alreadyPresent);
							insNodeArray[alreadyPresent].setSW(lastVertex);
						}
						else if (head>67 && head <= 112) {
							insNodeArray[lastVertex].setE(alreadyPresent);
							insNodeArray[alreadyPresent].setW(lastVertex);
						}
						else if (head>112 && head <= 157) {
							insNodeArray[lastVertex].setSE(alreadyPresent);
							insNodeArray[alreadyPresent].setNW(lastVertex);
						}
						else if (head>157 && head <= 202) {
							insNodeArray[lastVertex].setS(alreadyPresent);
							insNodeArray[alreadyPresent].setN(lastVertex);
						}
						else if (head>202 && head <= 247) {
							insNodeArray[lastVertex].setSW(alreadyPresent);
							insNodeArray[alreadyPresent].setNE(lastVertex);
						}
						else if (head>247 && head <= 292) {
							insNodeArray[lastVertex].setW(alreadyPresent);
							insNodeArray[alreadyPresent].setE(lastVertex);
						}
						else if (head>292 && head <= 337) {
							insNodeArray[lastVertex].setNW(alreadyPresent);
							insNodeArray[alreadyPresent].setSE(lastVertex);
						}
						
						// Finally set the lastVertex:
						lastVertex = alreadyPresent;
					}
				}
				
				// System.out.println(a.toKML());
            }
        }
		
		// Iterator for all the Points:
		for(Iterator iter = placemarks.iterator(); iter.hasNext();)
		{
            Placemark cur = (Placemark)iter.next();
            if(cur.getGeometry() instanceof Point)
            {
				// Do something with the Points here

				Point a = cur.getPoint();
				double coordinates[] = a.getNumericalCoordinates();
				
				double minDist = -1;
				int minDistNode = -1;
				for (int i=0; i<noOfNodes; i++) {
					double thisDist = distance(coordinates[0], coordinates[1], insNodeArray[i].getLongitude(), insNodeArray[i].getLatitude());
					if(thisDist<minDist || minDistNode == -1) {
						minDist = thisDist;
						minDistNode = i;
					}
				}
				
				insNodeArray[minDistNode].setName(cur.getName());
				
				// Remove this later:
				// System.out.println(a.toKML());
            }
        }
		
		
		//printer.write(doc.toKML());	
		String mapFile = "";
		mapFile+= orientation; mapFile+=";";
		mapFile+= insNodeArray[0].getLongitude();
		mapFile+= ",";
		mapFile+= insNodeArray[0].getLatitude();
		mapFile+=";";
		for (int i=0; i<noOfNodes; i++) {
			mapFile = mapFile + insNodeArray[i].description();
			//System.out.println(insNodeArray[i].description());
		}
		
		printer.write(mapFile);
		printer.close();
		
		// Now make the processed document
		
		for(int i=0;i<noOfNodes;i++) {
			Point a = new Point();
			a.setCoordinates(insNodeArray[i].getLongitude()+","+insNodeArray[i].getLatitude()+",0.0");
			Placemark temp = new Placemark();
			temp.addGeometry(a);
			temp.setName(insNodeArray[i].getName());
			processedDoc.addPlacemark(temp);
			
			for(int j=i+1;j<noOfNodes;j++) {
				if(insNodeArray[j].getN()==i || insNodeArray[j].getNE()==i || insNodeArray[j].getE()==i || insNodeArray[j].getSE()==i || insNodeArray[j].getS()==i || insNodeArray[j].getSW()==i || insNodeArray[j].getW()==i || insNodeArray[j].getNW()==i ) {
						// there's a line string from insNodeArray[j] and insNodeArray[i]
					LineString aLineString = new LineString();
					aLineString.setCoordinates(insNodeArray[i].getLongitude()+","+insNodeArray[i].getLatitude()+",0.0 "+insNodeArray[j].getLongitude()+","+insNodeArray[j].getLatitude()+",0.0");
					Placemark ls = new Placemark();
					ls.addGeometry(aLineString);
					processedDoc.addPlacemark(ls);
				}
			}
		}
		
		
		processedKml.addDocument(processedDoc);
		kmlPrinter.write(processedKml.toKML());
		kmlPrinter.close();
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
