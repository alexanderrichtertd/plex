#pragma once

#include "platform/Platform.h"
#include "AOV.h"

#include <ai_types.h>

#include <maya/MString.h>
#include <maya/MCommonRenderSettingsData.h>
#include <maya/MFnDagNode.h>
#include <maya/MDagPath.h>

#include <vector>
#include <set>
#include <map>
#include <string>

class CMayaScene;

enum RenderType
{
   MTOA_RENDER_INTERACTIVE,
   MTOA_RENDER_EXPORTASS,
   MTOA_RENDER_EXPORTASS_AND_KICK
};

enum LogVerbosity
{
   MTOA_LOG_ERRORS,
   MTOA_LOG_WANINGS_INFO,
   MTOA_LOG_DEBUG
};

class DLLEXPORT CRenderOptions
{
   friend class CRenderSession;

public:

   CRenderOptions();

   AtUInt32 minX() const
   {
      return m_minx;
   }

   AtUInt32 minY() const
   {
      return m_miny;
   }

   AtUInt32 maxX() const
   {
      return m_maxx;
   }

   AtUInt32 maxY() const
   {
      return m_maxy;
   }

   AtUInt32 width() const
   {
      return m_width;
   }

   AtUInt32 height() const
   {
      return m_height;
   }

   float pixelAspectRatio() const
   {
      return m_pixelAspectRatio;
   }

   bool useRenderRegion() const
   {
      return m_useRenderRegion;
   }

   bool clearBeforeRender() const
   {
      return m_clearBeforeRender;
   }

   bool useBinaryEncoding() const
   {
      return m_useBinaryEncoding;
   }
   
   bool sceneUpdateBeforeIPRRender() const
   {
      return m_forceSceneUpdateBeforeIPRRefresh;
   }
   
   bool useExistingTiledTextures() const 
   { 
     return m_use_existing_tiled_textures; 
   }

   MString outputAssFile() const
   {
      return m_outputAssFile;
   }

   unsigned int outputAssMask() const
   {
      return m_outputAssMask;
   }
   
   bool expandProcedurals() const
   {
      return m_expandProcedurals;
   }

   void SetOutputAssMask(unsigned int mask)
   {
      m_outputAssMask = mask;
   }
   
   void SetExpandProcedurals(bool expand_procedurals)
   {
      m_expandProcedurals = expand_procedurals;
   }

   void SetUseBinaryEncoding(bool ube)
   {
      m_useBinaryEncoding = ube;
   }

   void SetCamera(MDagPath& camera);

   void SetRenderViewPanelName(const MString &panel)
   {
      m_panel = panel;
   }

   void SetWidth(unsigned int width)
   {
      m_width = width;

      UpdateImageDimensions();
   }

   void SetHeight(unsigned int height)
   {
      m_height = height;

      UpdateImageDimensions();
   }

   void SetRegion(const unsigned int left, const unsigned int right, const unsigned int bottom, const unsigned int top)
   {
      m_useRenderRegion = true;

      m_minx = left;
      m_miny = bottom;
      m_maxx = right;
      m_maxy = top;

      UpdateImageDimensions();
   }

   MDagPath GetCamera() const
   {
      return m_camera;
   }

   MString GetCameraName() const
   {
      return MFnDagNode(m_camera).name();
   }

   MString GetRenderViewPanelName() const
   {
      return m_panel;
   }

   bool MultiCameraRender() const
   {
      return m_multiCameraRender;
   }

   bool isProgressive() const
   {
      return m_progressive_rendering;
   }

   int progressiveInitialLevel() const
   {
      return m_progressive_initial_level;
   }

   void SetProgressive(const bool is_progressive)
   {
      m_progressive_rendering = is_progressive;
   }

   bool forceTranslateShadingEngines() const
   {
      return m_force_translate_shading_engines;
   }

   void SetForceTranslateShadingEngines(const bool force_translate_shading_engines)
   {
      m_force_translate_shading_engines = force_translate_shading_engines;
   }

   MStatus GetFromMaya();

   void SetupLog() const;
   
   MString GetFileExtension(const MString& imageRenderFormat) const;
   void UpdateImageFilename();
   void UpdateImageOptions();
   void UpdateImageDimensions();
   inline const MObject& GetArnoldRenderOptions() const { return m_options; }
   inline void SetArnoldRenderOptions(const MObject& options) { m_options = options; }

   MString GetShaderSearchPath() const { return m_shader_searchpath; }

private:

   MStatus ProcessCommonRenderOptions();
   MStatus ProcessArnoldRenderOptions();

   void SetupImageOptions() const;
   void SetupImageFilter() const;

private:
   MCommonRenderSettingsData m_defaultRenderGlobalsData;

   MDagPath m_camera;

   MObject m_options;

   MString m_arnoldRenderImageFormat;
   MString m_plugins_path;
   MString m_outputAssFile;
   MString m_log_filename;
   MString m_renderDriver;
   MString m_imageFileExtension;
   MString m_imageFilename;
   MString m_panel;
   MString m_shader_searchpath;

   float m_pixelAspectRatio;
   float m_startFrame;
   float m_endFrame;
   float m_byFrameStep;
   float m_AA_sample_clamp;
   float m_AA_sample_clamp_AOVs;

   AtUInt32 m_minx, m_miny, m_maxx, m_maxy;
   AtUInt32 m_width, m_height;
   AtUInt32 m_extensionPadding;

   unsigned int m_log_max_warnings;
   unsigned int m_log_verbosity;
   unsigned int m_AA_samples;
   unsigned int m_GI_diffuse_samples;
   unsigned int m_GI_glossy_samples;
   unsigned int m_outputAssMask;
   unsigned int m_progressive_initial_level;
   unsigned int m_threads;

   bool m_useRenderRegion;
   bool m_clearBeforeRender; 
   bool m_forceSceneUpdateBeforeIPRRefresh;
   bool m_forceTextureCacheFlushAfterRender;
   bool m_useBinaryEncoding;
   bool m_log_to_file;
   bool m_log_to_console;
   bool m_expandProcedurals;
   bool m_force_translate_shading_engines;
   bool m_lock_sampling_noise;
   bool m_use_existing_tiled_textures;
   bool m_outputAssBoundingBox;
   bool m_progressive_rendering;
   bool m_isAnimated;
   bool m_multiCameraRender;  
};
