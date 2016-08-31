#pragma once

#include "translators/DagTranslator.h"

class DLLEXPORT CLightTranslator
   :   public CDagTranslator
{
public:

   virtual AtNode* Init(CArnoldSession* session, MDagPath& dagPath, MString outputAttr="")
   {
      CDagTranslator::Init(session, dagPath, outputAttr);
      return m_atNode;
   }
   virtual bool RequiresMotionData()
   {
      return m_session->IsMotionBlurEnabled(MTOA_MBLUR_LIGHT);
   }
   static AtRGB ConvertKelvinToRGB(float kelvin);
protected:
   virtual bool IsMayaTypeLight() { return true; }
   virtual void Export(AtNode* light);
   virtual void ExportMotion(AtNode* light, unsigned int step);
   virtual void Delete();
   virtual bool IsFinite() const { return true; } // to decide if scaling is required or not
   static void MakeCommonAttributes(CBaseAttrHelper& helper);   
};
