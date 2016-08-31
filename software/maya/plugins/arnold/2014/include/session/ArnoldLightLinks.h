#pragma once

#include <maya/MFnDependencyNode.h>
#include <maya/MDagPath.h>

#include <ai.h>

#include <map>
#include <vector>
#include <string>

class CArnoldLightLinks{
public:
   CArnoldLightLinks() {}
   ~CArnoldLightLinks() {}
   
   // Building the database from the lightLinker nodes
   void ClearLightLinks();
   void ParseLights();
   // for getting the node name
   // and maybe for a different light linking mode later
   void ExportLightLinking(AtNode* shape, const MDagPath& path);
   void SetLinkingMode(int light, int shadow);
private:
   enum NodeLinkMode{
      MTOA_NODELINK_LINK,
      MTOA_NODELINK_IGNORE
   };
   
   const std::vector<AtNode*>& GetObjectsFromObjectSet(MFnDependencyNode& objectSet);
   void CheckNode(MObject node);
   void AppendNodesToList(MFnDependencyNode& targetNode, std::vector<std::string>& nodeList,  const std::vector<std::string> *existingList = 0);
   void HandleLightLinker(MPlug& conn, bool checkExisting = false);
   bool CheckMessage(MFnDependencyNode& dNode, bool checkExisting = false);
   bool FillLights(const std::vector<std::string> &linkList, const std::vector<std::string> &ignoreList);

   // saving the lights here for faster access
   std::map<std::string, AtNode*> m_arnoldLights;
   std::vector<AtNode *> m_arnoldDefaultLights;
   std::vector<AtNode *> m_arnoldMeshLights;
   std::map<std::string, std::vector<AtNode*> > m_cachedObjectSets;
   size_t m_numArnoldLights;
   
   std::vector<std::string> m_linkedLights;
   std::vector<std::string> m_ignoredLights;
   std::vector<std::string> m_linkedShadows;
   std::vector<std::string> m_ignoredShadows;
   std::vector<AtNode*>     m_groupLights;

   
   int m_lightMode;
   int m_shadowMode;
};
