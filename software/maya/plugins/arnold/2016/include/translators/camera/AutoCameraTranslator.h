#pragma once

#include "CameraTranslator.h"

class DLLEXPORT CAutoCameraTranslator : public CCameraTranslator{
public:
   CAutoCameraTranslator()
   {
      m_exportFOV = false;
      m_fovAnimated = false;
   }
   static void* creator()
   {
      return new CAutoCameraTranslator();
   }
   virtual AtNode* CreateArnoldNodes();
   
   virtual void Export(AtNode* camera);
   virtual void ExportMotion(AtNode* camera, unsigned int step);
protected:
   float GetFOV(AtNode* camera);
   bool m_exportFOV;
   bool m_fovAnimated;
};
