#pragma once

#include "NodeTranslator.h"

// Abstract base class for Dag node translators
//
typedef std::map<MObjectHandle, MDagPath, MObjectCompare> ObjectHandleToDagMap;

class DLLEXPORT CDagTranslator : public CNodeTranslator
{

public:
   virtual AtNode* Init(CArnoldSession* session, MDagPath& dagPath, MString outputAttr="")
   {
      m_dagPath = dagPath;
      // must call this after member initialization to ensure they are available to virtual functions like SetArnoldNodeName
      AtNode * tmpRet = CNodeTranslator::Init(session, CNodeAttrHandle(dagPath, outputAttr));      
      return tmpRet;
   }

   virtual AtNode* Init(CArnoldSession* session, MObject& object, MString outputAttr="")
   {
      MDagPath dagPath;
      MDagPath::getAPathTo(object, dagPath);
      return Init(session, dagPath, outputAttr);
   }

   virtual MDagPath GetMayaDagPath() const { return m_dagPath; }
   virtual MString GetMayaPartialPathName() const { return m_dagPath.partialPathName(); }
   virtual bool IsMayaTypeDag() {return true;}
   virtual bool IsMayaTypeRenderable() {return true;}

   virtual void AddUpdateCallbacks();
   // for initializer callbacks:
   static void MakeMayaVisibilityFlags(CBaseAttrHelper& helper);
   // for initializer callbacks:
   static void MakeArnoldVisibilityFlags(CBaseAttrHelper& helper);

protected:
   CDagTranslator() : CNodeTranslator(){}
   virtual void Export(AtNode* atNode);
   virtual void ExportMotion(AtNode* atNode, unsigned int step);
   virtual MStatus GetOverrideSets(MDagPath path, MObjectArray &overrideSets);
   virtual MStatus ExportOverrideSets();

   virtual bool IsMasterInstance();
   virtual bool DoIsMasterInstance(const MDagPath& dagPath, MDagPath &masterDag);
   virtual MDagPath& GetMasterInstance();

   void GetRotationMatrix(AtMatrix& matrix);
   static void GetMatrix(AtMatrix& matrix, const MDagPath& path, CArnoldSession* session = 0);
   virtual void GetMatrix(AtMatrix& matrix);
   void ExportMatrix(AtNode* node, unsigned int step);
   // for computing a path different from m_dagPath
   AtByte ComputeVisibility(const MDagPath& path);
   AtByte ComputeVisibility();   

   virtual void Delete();
   void AddHierarchyCallbacks(const MDagPath & path);
   void SetArnoldNodeName(AtNode* arnoldNode, const char* tag="");

protected:
   MDagPath m_dagPath;
private:
   MDagPath m_masterDag;
   bool m_isMasterDag;
};
