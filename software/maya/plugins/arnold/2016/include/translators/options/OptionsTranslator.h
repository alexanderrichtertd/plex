#pragma once

#include "translators/NodeTranslator.h"

struct CAOVOutput
{
   AtNode* driver;
   AtNode* filter;
   bool mergeAOVs; // whether or not to split AOVs
   bool singleLayer;
   bool raw;
   MString prefix;
};

struct CAOVOutputArray
{
   MString name;
   int type;
   MString tokens;
   std::vector<CAOVOutput> outputs;
};



class DLLEXPORT COptionsTranslator : public CNodeTranslator
{
public:
   static void* creator(){return new COptionsTranslator();}
   virtual void Export(AtNode* options);
   virtual void Update(AtNode *options);
   AtNode* CreateArnoldNodes();
   virtual bool DependsOnExportCamera() {return true;}

   void SetCamera(AtNode *options);
   bool IsActiveAOV(CAOV &aov) const
   {
      if (m_aovs.count(aov))
         return true;
      else
         return false;
   }

   AOVSet GetActiveAOVs() const
   {
      return m_aovs;
   }

   static void AddProjectFoldersToSearchPaths(AtNode* options);
protected:
   COptionsTranslator()  :
      CNodeTranslator(),
      m_aovs(),
      m_aovsEnabled(true),
      m_aovsInUse(false)
   {
      // Just for debug info, translator creates whatever arnold nodes are required
      // through the CreateArnoldNodes method
      m_abstract.arnold = "options";
   }
   void ProcessAOVs();
   void SetImageFilenames(MStringArray &outputs);
   void ExportAOVs();
   void ExportAtmosphere(AtNode* options);
   void CreateFileDirectory(const MString &filename) const;
   unsigned int GetOutputArray(const CAOV& aov,
                                     std::vector<CAOVOutput>& outputs);
   bool GetOutput(const MPlug& driverPlug,
                  const MPlug& filterPlug,
                  CAOVOutput& output);
   AtNode* ExportDriver(const MPlug& driverPlug,
                        MString& prefix,
                        bool& mergeAOVs,
                        bool& singleLayer,
                        bool& raw);
   AtNode* ExportFilter(const MPlug& filterPlug);

   virtual AtNode* ProcessParameter(AtNode* arnoldNode, const char* arnoldParamName, int arnoldParamType, const MPlug& plug);

protected:
   AOVSet m_aovs;
   std::vector<CAOVOutputArray> m_aovData;
   bool m_aovsEnabled;
   bool m_aovsInUse;
   std::map<std::string, AtNode*> m_multiDriverMap;
};
