#pragma once

#include "extension/PxUtils.h"
#include "extension/PathUtils.h"
#include "translators/NodeTranslator.h"
#include "utils/Version.h"

#include <maya/MTypeId.h>
#include <maya/MPxNode.h>

#include <algorithm>

#define BUILTIN "<built-in>"

#define EXPORT_API_VERSION DLLEXPORT const char* getAPIVersion(){return MTOA_VERSION;}

class CAbMayaNode;

// To track loaded Arnold plugins
class PluginStore: public std::vector<std::string>
{
public:
   iterator find(const std::string& item)
   {
      return std::find(begin(), end(), item);
   }

   void insert(const std::string& item)
   {
      push_back(item);
   }
   void erase(const std::string& item)
   {
      iterator it = find(item);
      std::vector<std::string>::erase(it);
   }
};


typedef PluginStore LoadedArnoldPluginsSet;
// To track required  Maya plugins
typedef std::set<std::string> RequiredMayaPluginsSet;

// class CExtension

/// Class to represent and manipulate Arnold extensions.
///
/// This class is used in the initializeExtensions and deinitializeExtension functions
/// of a MtoA extension to respectively register and deregister the extension services
/// (nodes, translators) with MtoA and Maya.RT CExtension
///
class DLLEXPORT CExtension
{
   friend class CExtensionsManager;

public:
   CExtension(const MString &file);
   virtual ~CExtension() {}
   void Requires(const MString &plugin);
   MStringArray Required();
   MString GetExtensionName() const {return m_extensionName;}
   MString GetExtensionFile() const {return m_extensionFile;}
   MString GetApiVersion() const {return m_apiVersion;}
   unsigned int RegisteredNodesCount() const {return m_registeredMayaNodes.size();}
   unsigned int TranslatedNodesCount() const {return m_registeredTranslators.size();}
   unsigned int TranslatorCount() const;
   bool IsRegistered() const {return m_registered;}
   bool IsDeferred() const {return m_deferred;}

   // Arnold Plugin loading
   MString LoadArnoldPlugin(const MString &file,
                            const MString &path=PLUGIN_SEARCH,
                            MStatus *returnStatus=NULL);
   // Get list of Arnold plugins this extension loads
   MStringArray GetOwnLoadedArnoldPlugins();

   // Can be called directly to register new Maya nodes
   MStatus RegisterNode(const MString &mayaTypeName,
                        const MTypeId &mayaTypeId,
                        MCreatorFunction creatorFunction,
                        MInitializeFunction initFunction,
                        MPxNode::Type type=MPxNode::kDependNode,
                        const MString &classification="");

   // To register a translator for a given Maya node
   // gives no access to metadata (all info needs to be set explicitely)
   MStatus RegisterTranslator(const MString &mayaTypeName,
                              const MString &translatorName,
                              TCreatorFunction creatorFunction,
                              TNodeInitFunction nodeInitFunction=NULL);

   // Register Maya nodes for all Arnold nodes declared with
   // the given plugin, using metadata info
   MStatus RegisterPluginNodesAndTranslators(const MString &plugin="");

   MStatus RegisterAOV(const MString &nodeType,
                       const MString &aovName,
                       int dataType,
                       const MString &aovAttr);

   static bool IsArnoldPluginLoaded(const MString &path);
   static MStringArray GetAllLoadedArnoldPlugins();

protected :
   MStatus setFile(const MString &file);

   MStatus UnloadArnoldPlugins();
   MStatus UnloadArnoldPlugin(const MString &resolved);
   MStatus DoUnloadArnoldPlugin(const MString &resolved);
   MStatus NewArnoldPlugin(const MString &file);
   MStatus DeleteArnoldPlugin(const MString &file);

   // Register the Maya node for a givem Arnold node, using the node metadata
   MStatus RegisterNode(CPxMayaNode &mayaNode,
                        const CPxArnoldNode &arnoldNode);

   // Register a translator from the metadata associated with the Arnold node name or entry
   MStatus RegisterTranslator(const CPxTranslator &translator,
                              CPxMayaNode &mayaNode,
                              const CPxArnoldNode &arnoldNode);

   MStatus NewMappedMayaNode(CPxMayaNode mayaNode,
                             const CPxArnoldNode &arnoldNode);
   MStatus NewMayaNode(const CPxMayaNode &mayaNode);
   MStatus MapMayaNode(const CPxMayaNode &mayaNode,
                       const CPxArnoldNode &arnoldNode);
   MStatus NewTranslator(const CPxTranslator &translator,
                         const CPxMayaNode &mayaNode);

   const CPxMayaNode* FindRegisteredMayaNode(const CPxMayaNode &mayaNode);
   const TranslatorsSet* FindRegisteredTranslators(const CPxMayaNode &mayaNode);

   static MString FindFileInPath(const MString &file,
                                 const MString &path,
                                 MStatus *returnStatus=NULL);
   static MStringArray FindLibraries(const MString &path,
                                     MStatus *returnStatus=NULL);


protected:
   MString m_extensionFile;
   MString m_extensionName;
   MString m_apiVersion;
   void* m_library;
   bool m_registered;
   bool m_deferred;
   // LoadedArnoldPluginsSet m_ownArnoldPlugins;
   // only the new maya nodes registered by this Extension
   MayaNodesSet m_registeredMayaNodes;
   // new maya nodes as well as existing associated to arnold nodes
   // FIXME can probably remove it
   ArnoldNodeToMayaNodeMap m_arnoldToMayaNodes;
   // translators registered by this extension, indexed by Maya node
   MayaNodeToTranslatorsMap m_registeredTranslators;
   // Arnold plugins loaded by this extension
   LoadedArnoldPluginsSet m_ownLoadedArnoldPlugins;
   // Maya plugins required by this extension
   RequiredMayaPluginsSet m_requiredMayaPlugins;

   // Static info for all extensions
   static unsigned int s_autoNodeId;
   static LoadedArnoldPluginsSet s_allLoadedArnoldPlugins;
};
