package com.keithpower.gekmlib;

import java.awt.Color;

/**
 * Utility class to provide basic functionality used in the classes
 *
 * @author power
 *
 */
public class Utility
{
    ////////////////////// Public methods  ///////////////////////////////
    
    /**
     * This method takes a 32-bit hex String and parses it into
     * a Color with alpha value.
     * Color.decode only supports 24 bit for some reason.
     * 
     * Alpha is 1st 2 chars, r, g, b next pairs.
     * @param String with hexValue to make into Color (no 0x in String)
     * @return Color representing hexCode
     */
    public static Color createColor(String hexValue)
    {
        if(hexValue.length()!=8)
        {
             return null;
        }
        int alpha = Integer.valueOf(hexValue.substring(0, 2), 16).intValue();
        int r = Integer.valueOf(hexValue.substring(2, 4), 16).intValue();
        int g = Integer.valueOf(hexValue.substring(4, 6), 16).intValue();
        int b = Integer.valueOf(hexValue.substring(6, 8), 16).intValue();
        
        Color newCol = new java.awt.Color(r, g, b, alpha);
        return newCol;
    }
}
