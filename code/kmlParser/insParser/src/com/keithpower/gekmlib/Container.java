package com.keithpower.gekmlib;
/**
 * AutoGenerated.
 *
 */

import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
abstract public class Container extends Feature
{


    public Container()
    {
        super();
    }

    public Container(Node parent)
    {
        super(parent);
    }



    public Object clone() throws CloneNotSupportedException
    {
        Container result = (Container)super.clone();
        return result;
    }
    public void setRecursiveNotDirty()
    {
        super.setRecursiveNotDirty();
    }
}
