#pragma once

#include "translators/DagTranslator.h"

/// A translator for auto-exporting DAG nodes.
/// This is the default translator for cameras and shapes.  It's like ShaderTranslator
/// but for DAG nodes.
class DLLEXPORT CAutoDagTranslator
   :  public CDagTranslator
{
public:
   static void* creator()
   {
      return new CAutoDagTranslator();
   }
   virtual AtNode* CreateArnoldNodes();
   virtual bool RequiresMotionData();
};
