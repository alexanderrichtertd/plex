#pragma once

#include <maya/MPxNode.h>

// A Maya node class abstract
// Hold the information necessary to customize base Maya node classes
// for different Arnold nodes

// Extend as it becomes necessary

class CAbMayaNode
{
   friend class CPxMayaNode;
public:
   CAbMayaNode(const MString &mayaClassName = "",
               const MString &arnoldClassName = "",
               const MString &classif = "",
               const MString &providerName = "")
   : name(mayaClassName),
     arnold(arnoldClassName),
     classification(classif),
     provider(providerName)
   {}

   MString name;
   MString arnold;
   MString classification;
   MString provider;
};
