#pragma once

#include <ai_node_entry.h>

#include <cstring>

#include <maya/MString.h>

// An Arnold node entry proxy
class CPxArnoldNode
{
   friend class CExtension;
   friend class CExtensionsManager;

public:
   // in 2012 we can determine the node Id from the node name
   CPxArnoldNode(const MString &nodeName);
   CPxArnoldNode(const AtNodeEntry* nodeEntry=NULL);
   ~CPxArnoldNode() {};

   inline bool operator==(const CPxArnoldNode& other) const { return name == other.name; }
   inline bool operator!=(const CPxArnoldNode& other) const { return name != other.name; }
   inline bool operator<(const CPxArnoldNode& other) const { return strcmp(name.asChar(), other.name.asChar()) < 0; }

   inline bool IsNull() const {return (NULL == entry);}
   void Set(const CPxArnoldNode& other);

private:
   MString name;
   const AtNodeEntry* entry;
   MString provider;
   MString file;
};
