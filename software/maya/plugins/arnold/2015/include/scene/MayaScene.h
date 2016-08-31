#pragma once

#include "platform/Platform.h"
#include "render/RenderSession.h"
#include "session/ArnoldSession.h"

#include <ai_nodes.h>

#include <maya/MStatus.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MItDag.h>
#include <maya/MMatrix.h>
#include <maya/MObjectArray.h>
#include <maya/MSelectionList.h>
#include <maya/MFnCamera.h>
#include <maya/MVectorArray.h>
#include <maya/MMessage.h>
#include <maya/MPlug.h>
#include <maya/MCommonRenderSettingsData.h>


#include <vector>
#include <set>
#include <map>
#include <string>



/// Translates the current state of all or part of an open Maya scene into the active Arnold universe.

/// In IPR mode, the resulting instance allows the scene to be quickly and incrementally retranslated
/// as changes occur to previously translated Maya objects.
///
/// Once CMayaScene::ExportToArnold() is called, the DAG hierarchy is traversed and CDagTranslators
/// are found and exported for all relevant Maya nodes.  Those translators in turn call
/// and CMayaScene::ExportShader() as they require, which triggers dependency graph evaluation and the
/// generation of CNodeTranslators.

class DLLEXPORT CMayaScene
{

public:

   CMayaScene();

   ~CMayaScene();

   // Currently there can be only one export and render session
   // but when it changes, CMayaScene will manage them

   /// Return the instance of the export session.
   static CArnoldSession* GetArnoldSession();
   /// Return the instance of the render session.
   static CRenderSession* GetRenderSession();

   static bool IsActive(ArnoldSessionMode mode=MTOA_SESSION_ANY);

   static ArnoldSessionMode GetSessionMode();
   static bool IsExportingMotion();

   static MStatus Begin(ArnoldSessionMode mode);
   static MStatus End();
   static MStatus Restart();

   static bool IsArnoldLight(const MObject & object);
   static MObject GetSceneArnoldRenderOptionsNode();
   /// Must be called between Begin and End
   static MStatus Export(MSelectionList* selected = NULL);
   /// Must be called between Begin and End, after Export
   static MStatus Render();

   /// Do an export and render in the given mode
   static MStatus ExportAndRenderFrame(ArnoldSessionMode mode, MSelectionList* selected = NULL);
   static MStatus ExportAndRenderSequence(ArnoldSessionMode mode, MSelectionList* selected = NULL);

   static MStatus ExecuteScript(const MString &str, bool echo=false, bool idle=false);

   static MStatus UpdateIPR();

   static void Init();
   static void DeInit();

   static void UpdateSceneChanges();

private:

   static MStatus SetupIPRCallbacks();
   static void ClearIPRCallbacks();

   static void IPRNewNodeCallback(MObject & node, void *);
   static void IPRIdleCallback(void *);
   static void QuitApplicationCallback(void *);
   static void FileOpenCallback(void *);


   static std::vector< CNodeTranslator * > s_translatorsToIPRUpdate;
   static MCallbackId s_IPRIdleCallbackId;
   static MCallbackId s_NewNodeCallbackId;
   static MCallbackId s_QuitApplicationCallbackId;
   static MCallbackId s_FileOpenCallbackId;

   
   // Currently there can be only one export and render session
   // but when it changes, CMayaScene will manage them
   static CRenderSession* s_renderSession;
   static CArnoldSession* s_arnoldSession;

   static double s_currentFrame;

   static AtCritSec s_lock;
   static bool s_active;
};  // class CMayaScene
