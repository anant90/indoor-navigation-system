package com.keithpower.gekmlib;

import java.util.Iterator;
import java.util.List;

/**
 * Class for converting some awkward classes to their KML
 * String representation.
 * 
 * @author power
 *
 */
public class SpecialCaseFormatter
{
    public static String toKMLString(java.awt.Color color)
    {
	return Integer.toHexString(color.getRGB());
    }

    public static String toKMLString(java.util.Date date)
    {
	return date.toString();
    }

    // Treating String as a special case allows
    // me to reduce error checking code
    // It is a special case in that it's a built in
    // but non-primitive
    public static String toKMLString(String str)
    {
	return str;
    }

    public static String toKMLString(LongDate aDate)
    {
	return aDate.toString();
    }


    /**
     * @return list delimited with space
     */
    public static String toKMLString(List values)
    {
	return toKMLString(values, " ");
    }
    
    /**
     * Return the KML String for a list of values.
     * 
     * @param values List of values
     * @param delimiter String to write between values
     * @return delimited String representing values
     */
    public static String toKMLString(List values, String delimiter)
    {
	String kml="";
	for (Iterator iter = values.iterator(); iter.hasNext();)
	{
	    Object curVal = iter.next();
	    // Only String required as far as I can tell.
	    if(curVal instanceof String)
	    {
		kml+=SpecialCaseFormatter.toKMLString((String)curVal);
	    }
	    if(iter.hasNext())
	    {
		kml+=delimiter;
	    }
	}
	return kml;
    }
}
