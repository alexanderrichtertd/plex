#pragma once

#include "render/AOV.h"

#include <ai_node_entry.h>


#include <string>

#include <maya/MString.h>
#include <maya/MPxNode.h>

class CAbMayaNode;

#include <vector>

// A Maya node class proxy
class CPxMayaNode
{
   friend class CAbMayaNode;
   friend class CExtension;
   friend class CExtensionsManager;

public:
   // in 2012 we can determine the node Id from the node name
   CPxMayaNode(const MString &typeName = "",
               const MTypeId &typeId = MTypeId(0),
               const MString &providerName = "",
               const MString &providerFile = "",
               MCreatorFunction creatorFunction = NULL,
               MInitializeFunction initFunction = NULL,
               MPxNode::Type typeNode = MPxNode::kDependNode,
               const MString &classif = "");
   ~CPxMayaNode() {};

   inline bool operator==(const CPxMayaNode& other) const { return name == other.name; }
   inline bool operator!=(const CPxMayaNode& other) const { return name != other.name; }
   inline bool operator<(const CPxMayaNode& other) const { return strcmp(name.asChar(), other.name.asChar()) < 0; }

   inline bool IsNull() const {return (name == "");}
   MStatus ReadMetaData(const AtNodeEntry* arnoldNodeEntry);

   void RegisterAOV(const MString &aovName,
                    int dataType,
                    const MString &aovAttr);

private:
   MString name;
   MTypeId id;
   MString provider;
   MString file;
   // MString provider;
   MCreatorFunction creator;
   MInitializeFunction initialize;
   MPxNode::Type type;
   MString classification;
   MString arnold;
   CAbMayaNode *abstract;
   std::vector<CAOVData> m_aovs;
};
