#pragma once

#include "PxMayaNode.h"
#include "PxArnoldNode.h"
#include "PxTranslator.h"

#include <string>
#include <list>
#include <set>
#include <map>


// Set of Maya node proxies
typedef std::set<CPxMayaNode> MayaNodesSet;
// Maya node to Arnold node multimap
/// key: maya node name. value: arnold node name and maya node id
typedef std::multimap<CPxMayaNode, CPxArnoldNode> MayaNodeToArnoldNodeMap;
// Arnold node to Maya node multimap
/// key: arnold node name. value: maya node name
typedef std::multimap<CPxArnoldNode, CPxMayaNode> ArnoldNodeToMayaNodeMap;
// Set of Translator proxies
typedef std::set<CPxTranslator> TranslatorsSet;
// Maya node to Translator map
typedef std::map<CPxMayaNode, TranslatorsSet> MayaNodeToTranslatorsMap;
// Storing the default translator value
typedef std::map<std::string, MString> DefaultTranslatorMap;
