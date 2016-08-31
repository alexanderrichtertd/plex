#pragma once

#include "common/MObjectCompare.h"
#include "platform/Platform.h"
#include "attributes/AttrHelper.h"
#include "session/ArnoldSession.h"
#include "extension/AbTranslator.h"
#include "render/AOV.h"

#include <ai_nodes.h>

#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MPlug.h>
#include <maya/MGlobal.h>
#include <maya/MMessage.h> // for MCallbackId
#include <maya/MCallbackIdArray.h>

#include <string>
#include <vector>
#include <map>

#define AI_ATT_SEP "."
#define AI_TAG_SEP "@"

#define AI_UPDATE_ONLY 0
#define AI_DELETE_NODE 1
#define AI_RECREATE_NODE 2

MString GetAOVNodeType(int type);

// Abstract base class for all Maya-to-Arnold node translators
//
class DLLEXPORT CNodeTranslator
{
   // protect this class from its subclasses: make methods that should not be
   // called by subclasses private
   friend class CArnoldSession;
   friend class CExtensionsManager;
   friend class CExtension;
   friend class CRenderSwatchGenerator;

private:
   AtNode* DoExport(unsigned int step);
   AtNode* DoUpdate(unsigned int step);
   AtNode* DoCreateArnoldNodes();
   void SetTranslatorName(MString name) {m_abstract.name = MString(name);}
   bool ProcessParameterComponentInputs(AtNode* arnoldNode, const MPlug &plug, const char* arnoldAttrib, int arnoldAttribType);
   AtNode* ProcessParameterInputs(AtNode* arnoldNode, const MPlug &plug, const char* arnoldAttrib, int arnoldAttribType);

public:
   MString GetTranslatorName() {return m_abstract.name;}
   /// for translators that are associated with a specific arnold node
   MString GetArnoldNodeType() {return m_abstract.arnold;};

   virtual ~CNodeTranslator()
   {}
   virtual AtNode* Init(CArnoldSession* session, const MObject& nodeObject, const MString& attrName="")
   {
      return Init(session, CNodeAttrHandle(nodeObject, attrName));
   }
   virtual AtNode* Init(CArnoldSession* session, const MPlug& plug)
   {
      return Init(session, CNodeAttrHandle(plug));
   }

   virtual MObject GetMayaObject() const { return m_handle.object(); }
   virtual MString GetMayaNodeName() const { return MFnDependencyNode(m_handle.object()).name(); }
   virtual MString GetMayaAttributeName() const { return m_handle.attribute(); }
   virtual MString GetMayaNodeTypeName() const { return MFnDependencyNode(m_handle.object()).typeName(); }
   virtual MObject GetMayaObjectAttribute(MString attributeName) const { return MFnDependencyNode(m_handle.object()).attribute(attributeName); }

   virtual AtNode* GetArnoldRootNode();
   virtual AtNode* GetArnoldNode(const char* tag="");
   virtual const char* GetArnoldNodeName(const char* tag="");
   virtual const char* GetArnoldTypeName(const char* tag="");

   virtual MPlug FindMayaObjectPlug(const MString &attrName, MStatus* ReturnStatus=NULL) const;
   virtual MPlug FindMayaOverridePlug(const MString &attrName, MStatus* ReturnStatus=NULL) const;
   virtual MPlug FindMayaPlug(const MString &attrName, MStatus* ReturnStatus=NULL) const;

   // overridable translator properties
   virtual bool IsMayaTypeDag() {return false;}
   virtual bool IsMayaTypeRenderable() {return false;}
   virtual bool IsMayaTypeLight() { return false; }
   virtual bool DependsOnExportCamera() {return false;}
   /// Instead of caching translator exports, allow a Maya node to be exported multiple times, each time generating new arnold nodes
   virtual bool DisableCaching() {return false;}
   virtual bool DependsOnOutputPlug() {return false;} // translator performs different operations depending on the type of output plug

   virtual void TrackAOVs(AOVSet* aovs);
   virtual void TrackShaders(AtNodeSet* nodes) {m_shaders = nodes;};

   // Overide this if you have some special callbacks to install.
   virtual void AddUpdateCallbacks();
   // Remove callbacks installed. This is virtual incase
   // a translator needs to do more than remove the managed
   // callbacks.
   virtual void RemoveUpdateCallbacks();
   // This is a help that tells mtoa to re-export/update the node passed in.
   // Used by the Update callbacks.
   virtual void RequestUpdate(void * clientData = NULL);

   static void NodeInitializer(CAbTranslator context);
   static void ExportUserAttributes(AtNode* anode, MObject object, CNodeTranslator* translator = 0);

protected:
   CNodeTranslator()  :
      m_abstract(CAbTranslator()),
      m_session(NULL),
      m_atNode(NULL),
      m_overrideSets(),
      m_step(0),
      m_localAOVs(),
      m_upstreamAOVs(),
      m_shaders(NULL),
      m_updateMode(AI_UPDATE_ONLY),
      m_handle(CNodeAttrHandle())      
   {}

   virtual MStatus GetOverrideSets(MObject object, MObjectArray &overrideSets);
   virtual MStatus ExportOverrideSets();
   virtual MPlug GetOverridePlug(const MPlug &plug, MStatus* ReturnStatus=NULL) const;

   virtual void ComputeAOVs();
   void AddAOVDefaults(AtNode* shadingEngine, std::vector<AtNode*> &aovShaders);
   void WriteAOVUserAttributes(AtNode* atNode);
   
   AtNode* Init(CArnoldSession* session, const CNodeAttrHandle& object)
   {
      m_session = session;
      m_handle = object;
      ExportOverrideSets();
      return DoCreateArnoldNodes();
   }
   CNodeAttrHandle GetMayaHandle() const { return m_handle; }

   virtual void Export(AtNode* atNode);
   virtual void ExportMotion(AtNode* atNode, unsigned int step){}
   // Update runs during IPR for step==0 (calls Export by default)
   virtual void Update(AtNode* atNode){Export(atNode);}
   // UpdateMotion runs during IPR for step>0 (calls ExportMotion by default)
   virtual void UpdateMotion(AtNode* atNode, unsigned int step){ExportMotion(atNode, step);}
   virtual bool RequiresMotionData() {return false;}
   /// Create nodes using AddArnoldNode(), and return the node which forms the root of the exported network
   virtual AtNode* CreateArnoldNodes() = 0;
   /// Return false if the passed outputAttribute is invalid
   virtual bool ResolveOutputPlug(const MPlug& outputPlug, MPlug &resolvedOutputPlug);
   virtual void Delete() {}

   // Using the translator's MObject m_object and corresponding attrbuteName (default behavior)
   virtual AtNode* ProcessParameter(AtNode* arnoldNode, const char* arnoldParamName, int arnoldParamType);
   // For a specific Maya attribute on the translator Maya node
   virtual AtNode* ProcessParameter(AtNode* arnoldNode, const char* arnoldParamName, int arnoldParamType, const MString& mayaAttrName);
   // For a specific Maya plug
   virtual AtNode* ProcessParameter(AtNode* arnoldNode, const char* arnoldParamName, int arnoldParamType, const MPlug& plug);
   AtArray* InitArrayParameter(unsigned int arnoldParamType, unsigned int size);
   void SetArrayParameter(AtNode* arnoldNode, const char* arnoldParamName, AtArray* array);
   virtual void ProcessArrayParameterElement(AtNode* arnoldNode, AtArray* array, const char* arnoldParamName, const MPlug& elemPlug, unsigned int arnoldParamType, unsigned int pos);
   virtual void ProcessArrayParameter(AtNode* arnoldNode, const char* arnoldParamName, const MPlug& plug);
   void ProcessConstantArrayElement(int type, AtArray* array, unsigned int i, const MPlug& elem);
   void ProcessAnimatedParameter(AtNode* arnoldNode, const char* arnoldParamName, const MPlug& plug, unsigned int step);
   AtNode* ProcessConstantParameter(AtNode* arnoldNode, const char* arnoldParamName, int arnoldParamType, const MPlug& plug);

   void ExportUserAttribute(AtNode *anode);

   // session info
   inline double GetExportFrame() const {return m_session->GetExportFrame();}
   inline bool IsMotionBlurEnabled(int type = MTOA_MBLUR_ANY) const { return m_session->IsMotionBlurEnabled(type); }
   bool IsLocalMotionBlurEnabled() const
   {
      bool local_motion_attr(true);
      MPlug plug = FindMayaPlug("motionBlur");
      if (!plug.isNull())
         local_motion_attr = plug.asBool();
      return local_motion_attr;
   }
   inline unsigned int GetMotionStep() const {return m_step;}
   inline unsigned int GetNumMotionSteps() const {return m_session->GetNumMotionSteps();}
   inline CArnoldSession* GetSession() const {return m_session;}
   inline const CSessionOptions& GetSessionOptions() const  { return m_session->GetSessionOptions(); }
   inline ArnoldSessionMode GetSessionMode() const {return m_session->GetSessionMode();}
   inline const MObject& GetArnoldRenderOptions() const   { return m_session->GetArnoldRenderOptions(); }
   inline double GetMotionByFrame() const {return m_session->GetMotionByFrame(); }

   // session action
   AtNode* ExportNode(const MPlug& outputPlug, bool track=true, CNodeTranslator** outTranslator = 0);
   AtNode* ExportDagPath(MDagPath &dagPath);

   // set the arnold node that this translator is exporting (should only be used after all export steps are complete)
   virtual void SetArnoldRootNode(AtNode* node);
   virtual AtNode* AddArnoldNode(const char* type, const char* tag="");
   virtual void SetArnoldNodeName(AtNode* arnoldNode, const char* tag="");

   // Add a callback to the list to manage.
   void ManageUpdateCallback(const MCallbackId id);

   // Some simple callbacks used by many translators.
   static void NodeDirtyCallback(MObject& node, MPlug& plug, void* clientData);
   static void NameChangedCallback(MObject& node, const MString& str, void* clientData);
   static void NodeDeletedCallback(MObject& node, MDGModifier& modifier, void* clientData);
   static void NodeDestroyedCallback(void* clientData);
   static void ConvertMatrix(AtMatrix& matrix, const MMatrix& mayaMatrix, const CArnoldSession* arnoldSession = 0);

protected:

   CAbTranslator m_abstract;

   CArnoldSession* m_session;

   AtNode* m_atNode;
   std::map<std::string, AtNode*> m_atNodes;

   std::vector<CNodeTranslator*> m_overrideSets;

   unsigned int m_step;

   AOVSet m_localAOVs;
   AOVSet m_upstreamAOVs;
   AtNodeSet* m_shaders;

   // This stores callback IDs for the callbacks this
   // translator creates.
   MCallbackIdArray m_mayaCallbackIDs;
   
   unsigned int m_updateMode;

private:
   
   CNodeAttrHandle m_handle;
};
