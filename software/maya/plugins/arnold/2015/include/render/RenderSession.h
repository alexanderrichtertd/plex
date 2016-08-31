#pragma once

#include "render/RenderOptions.h"

#include <maya/MGlobal.h>

#include <ai_nodes.h>
#include <ai_universe.h>
#include <ai_bbox.h>

#include <maya/MMessage.h> // for MCallbackId
#include <maya/MThreadAsync.h>
#include <maya/MComputation.h>

class MImage;
class CRenderView;
/** CRenderSession handles the management of Arnold and rendering.
 * 
 * This is an important class. It handles rendering as well
 * loading plugins to Arnold, exporting ASS files and swatch
 * rendering.
 */

class DLLEXPORT CCritSec{
private:
   AtCritSec m_critSec;
   friend class CScopedLock;
public:
   CCritSec() {AiCritSecInitRecursive(&m_critSec);}
   ~CCritSec() {AiCritSecClose(&m_critSec);}

   void lock() {AiCritSecEnter(&m_critSec);}
   void unlock() {AiCritSecLeave(&m_critSec);}

   class CScopedLock{
   private:
      CCritSec& m_critSec;
   public:
      CScopedLock(CCritSec& critSec) : m_critSec(critSec) { m_critSec.lock(); }

      ~CScopedLock() { m_critSec.unlock(); }
   };
};

class DLLEXPORT CRenderSession
{
   friend class CMayaScene;

public:

   /// Initialize the Arnold universe, it will be ready for translation and render
   MStatus Begin(const CRenderOptions &options);
   /// Terminate a render. This will shutdown the Arnold universe.
   MStatus End();

   void SetRendering(bool renderState);
   // This provide an alternative to AiRendering that returns true between progressive
   // render levels. It should be used instead of AiRendering to prevent false
   // detection of rendering done.
   bool IsRendering();

   typedef void (*RenderCallbackType) (void);   
   static void SetCallback(RenderCallbackType callback);
   static void ClearCallback();
   static RenderCallbackType GetCallback();

   static void DeleteRenderView();
   

   // Render Methods.
   /// Render into the Render View, not IPR.
   void DoInteractiveRender(const MString& postRenderMel="");
   /// Render in the background of Maya.
   int DoBatchRender();

   /// Get a valid ass name
   MString GetAssName(const MString& customName,
                      const MCommonRenderSettingsData& renderGlobals,
                      double frameNumber,
                      const MString &sceneName,
                      const MString &cameraName,
                      const MString &fileFormat,
                      const MObject layer,
                      const bool createDirectory=true,
                      const bool isSequence=false,
                      const bool subFrames=false,
                      const bool isBatch=false,
                      MStatus *ReturnStatus=NULL) const;
   /// Export and ass file.
   /// \param customFileName file to export too.
   void DoAssWrite(MString customFileName, const bool compressed=false);
   /// Get the translated scene bounding box.
   AtBBox GetBoundingBox();
   MStatus WriteAsstoc(const MString& filename, const AtBBox& bBox);

   /// For interactive render, watch for interrupt, render end and process method
   ///   provided to CRenderSession::SetCallback() in the driver.
   static void InteractiveRenderCallback(float, float, void* data);

   /// Stop a render, leaving Arnold univierse active.
   void InterruptRender(bool waitFinished = false);

   void RunRenderView();
   /// Start and IPR render.
   void DoIPRRender();
   void StopIPR();
   /// Pause IPR, callbacks will still fire and Arnold will get the changes.
   void PauseIPR();
   /// Start off rendering again.
   void UnPauseIPR();

   void StartRenderView();
   void UpdateRenderView();

   void ObjectNameChanged(MObject& node, const MString& str);


   /// Get memory usage from Arnold.
   /// \return memory used in MB.
   AtUInt64 GetUsedMemory();

   // Swatch Rendering methods
   /// Start a swatch render.
   /// \param resolution the resolution of the swatch, it must be square.
   void DoSwatchRender(MImage & image, const int resolution);

   /// Set the ass output mask
   inline void SetOutputAssMask(unsigned int mask) { m_renderOptions.SetOutputAssMask(mask); }
   
   /// Set Expand Procedurals
   inline void SetExpandProcedurals(bool expand_procedurals) { m_renderOptions.SetExpandProcedurals(expand_procedurals); }
   inline void SetUseBinaryEncoding(bool ube) { m_renderOptions.SetUseBinaryEncoding(ube); }
   inline void SetForceTranslateShadingEngines(bool ftsh) { m_renderOptions.SetForceTranslateShadingEngines(ftsh); }

   /// Set the resolution of the render.
   /// \param width width in pixels.
   /// \param height height in pixels.
   void SetResolution(const int width, const int height);
   /// Get the camera used to render
   MDagPath GetCamera() const;
   /// Get the render view panel name for interactive render
   MString GetRenderViewPanelName() const;

   /// Set the camera to use for render.
   void SetCamera(MDagPath cameraNode);
   /// Set the render view panel name to render in
   void SetRenderViewPanelName(const MString &panel);
   /// Set progressive mode
   void SetProgressive(bool is_progressive);
   /// Set render region
   void SetRegion(const unsigned int left,const unsigned int right,
                  const unsigned int bottom, const unsigned int top);

   /// Return a pointer to the render options.
   /// \see CRenderOptions
   inline CRenderOptions* RenderOptions() { return &m_renderOptions; }

   /// Returns the state of rendering.
   /// This is different from if Arnold is active. After tuning in IPR
   /// this will return true, because the RenderSession is busy. Even
   /// though Arnold is not currently rendering.
   /// \return if we're active.
   inline bool IsActive() const { return m_is_active; }

   static void ClearIdleRenderViewCallback();
   
   static void sleep(AtUInt64 usecs);


private:

   CRenderSession()
      : m_paused_ipr(false)
      , m_is_active(false)
      , m_render_thread(NULL)
      , m_rendering(0)
      //, m_renderView(NULL)
   {
   }

   ~CRenderSession() { End(); };

   /// The idle callback is used to update the
   /// render view when rendering IPR.
   void AddIdleRenderViewCallback(const MString& postRenderMel);
   static void DoAddIdleRenderViewCallback(void* data);   

   /// This is the static method for performing a progressive render.
   /// data should be a CRenderSession pointer.
   static unsigned int ProgressiveRenderThread(void* data);

   /// This is the static method for performing an interactive render.
   /// data should be a CRenderSession pointer.
   static unsigned int InteractiveRenderThread(void* data);



private:

   CRenderOptions m_renderOptions;
   bool           m_paused_ipr;  ///< True when IPR is paused.
   bool           m_is_active;   ///< True when after a Init() and before a Finish().

   /// This is a special callback installed to update the render view while Arnold is rendering in IPR.
   /// \see AddIdleRenderViewCallback
   /// \see ClearIdleRenderViewCallback
   static MCallbackId    s_idle_cb;

   /// This is a pointer to the thread which is running RenderThread.
   void*           m_render_thread;
   static CCritSec m_render_lock;
   volatile int    m_rendering;
   
   static RenderCallbackType   m_renderCallback;
   
   static MComputation*   s_comp;
   MString        m_postRenderMel;

   //CRenderView  *m_renderView;
   
}; // class CRenderSession
