#pragma once

#include "translators/DagTranslator.h"
#include <maya/MPlugArray.h>


class DLLEXPORT CShapeTranslator : public CDagTranslator
{
public:
   virtual AtNode* Init(CArnoldSession* session, MDagPath& dagPath, MString outputAttr="")
   {
      m_atNode       = CDagTranslator::Init(session, dagPath, outputAttr);
      m_motion       = IsMotionBlurEnabled(MTOA_MBLUR_OBJECT);
      m_motionDeform = IsMotionBlurEnabled(MTOA_MBLUR_DEFORM);
      return m_atNode;
   }
   virtual bool RequiresMotionData()
   {
      return ((m_motion || m_motionDeform) && IsLocalMotionBlurEnabled());
   }

protected:
   virtual void ProcessRenderFlags(AtNode* node);
   virtual void ExportTraceSets(AtNode* node, const MPlug& traceSetsPlug);
   void ExportLightLinking(AtNode* polymesh);
   // for initializer callbacks:
   static void MakeCommonAttributes(CBaseAttrHelper& helper);

   virtual AtNode* ExportRootShader(const MPlug& plug, CNodeTranslator** outTranslator = 0);
   virtual AtNode* ExportRootShader(AtNode *rootShader);
   AtNode* CreateShadingGroupShader(AtNode *rootShader, std::vector<AtNode*> &aovShaders);
   MPlug GetNodeShadingGroup(MObject dagNode, int instanceNum);

protected:
   bool m_motion;
   bool m_motionDeform;


};
