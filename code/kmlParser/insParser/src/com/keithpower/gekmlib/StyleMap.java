package com.keithpower.gekmlib;
/**
 * AutoGenerated.
 *
 */

import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
public class StyleMap extends StyleSelector
{
    protected List pair = new ArrayList();


    public StyleMap()
    {
        super();
    }

    public StyleMap(Node parent)
    {
        super(parent);
    }

    public StyleMapPair [] getPairs()
    {
        StyleMapPair [] array = new StyleMapPair[this.pair.size()];
        return (StyleMapPair [])this.pair.toArray(array);
    }

    public void removePair(StyleMapPair value)
    {
        if(value!=null)
        {
            markDeletedNode(value);
            this.pair.remove(value);
        }
    }

    public void addPair(StyleMapPair value)
    {
        if(value!=null)
        {
            value.setParent(this);
            markCreatedNode(value);
            this.pair.add(value);
        }
    }



    public String toKML()
    {
        return toKML(false);
    }
    public String toKML(boolean suppressEnclosingTags)
    {
        String kml="";
        if(!suppressEnclosingTags)
        {
        kml+="<StyleMap";
        if(this.id!=null)
        {
            kml+=" id=\""+this.getId()+"\"";
        }
        if(this.targetId!=null)
        {
            kml+=" targetId=\""+this.getTargetId()+"\"";
        }
        kml+=">\n";
        }
        kml+=super.toKML(true);
        for (Iterator iter = this.pair.iterator(); iter.hasNext();)
        {
            StyleMapPair cur = (StyleMapPair)iter.next();
            kml+=cur.toKML();
        }
        if(!suppressEnclosingTags)
        {
            kml+="</StyleMap>\n";
        }
        return kml;
    }
    public String toUpdateKML()
    {
        return toUpdateKML(false);
    }
    public String toUpdateKML(boolean suppressEnclosingTags)
    {
        if(!isDirty())
        {
            return "";
        }
        String change = "";
        boolean isPrimDirty = isPrimitiveDirty(); // need to track it after object is setNotDirty
        if(isPrimDirty && !suppressEnclosingTags)
        {
        change+="<StyleMap";
        if(this.id!=null)
        {
            change+=" id=\""+this.getId()+"\"";
        }
        if(this.targetId!=null)
        {
            change+=" targetId=\""+this.getTargetId()+"\"";
        }
        change+=">\n";
        }
        change+=super.toUpdateKML(true);
        for (Iterator iter = this.pair.iterator(); iter.hasNext();)
        {
            StyleMapPair cur = (StyleMapPair)iter.next();
            if(cur.isDirty())
            {
                change+=cur.toUpdateKML();
            }
        }
        if(isPrimDirty && !suppressEnclosingTags)
        {
        change+="</StyleMap>\n";
        }
        setNotDirty();
        return change;
    }
    public Object clone() throws CloneNotSupportedException
    {
        StyleMap result = (StyleMap)super.clone();
      if(result.pair!=null)
      {
        result.pair = new ArrayList();
        for (Iterator iter = this.pair.iterator(); iter.hasNext();)
        {
            StyleMapPair element = (StyleMapPair)iter.next();
            StyleMapPair elementClone = (StyleMapPair)element.clone();
            elementClone.setParent(result);
        result.pair.add(elementClone);
        }
      }
        return result;
    }
    public void setRecursiveNotDirty()
    {
        super.setRecursiveNotDirty();
        for (Iterator iter = this.pair.iterator(); iter.hasNext();)
        {
            StyleMapPair cur = (StyleMapPair)iter.next();
            cur.setRecursiveNotDirty();
        }
    }
}