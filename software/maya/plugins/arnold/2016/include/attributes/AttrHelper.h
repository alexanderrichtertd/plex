#pragma once

#include "platform/Platform.h"
#include <ai_node_entry.h>
#include <ai_params.h>
#include <ai_metadata.h>
#include <ai_msg.h>

#include <maya/MPxNode.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MObject.h>
#include <maya/MStatus.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MRampAttribute.h>
#include <maya/MStringArray.h>

#include <maya/MTypes.h>
#include <maya/MNodeClass.h>

#include <string>
#include <map>
#include <vector>

#define OUT_NAME MString("outValue")
#define OUT_COLOR_NAME MString("outColor")
#define OUT_ALPHA_NAME MString("outAlpha")
// #define OUT_NODE_NAME MString("outNode")
// #define OUT_MATRIX_NAME MString("outMatrix")
#define OUT_SHORTNAME MString("out")

MString toMayaStyle(MString s);

MString toMayaStyle(MString s);

/// Structure for holding attribute properties
struct CAttrData
{
   MString      name;
   MString      shortName;
   MString      stringDefault;
   AtParamValue defaultValue;
   bool         isArray;
   int          type;
   bool         hasMin;
   AtParamValue min;
   bool         hasMax;
   AtParamValue max;
   bool         hasSoftMin;
   AtParamValue softMin;
   bool         hasSoftMax;
   AtParamValue softMax;
   bool         keyable;
   MStringArray enums;
   bool         linkable;
   bool         channelBox;
   CAttrData() :  name(""),
                  shortName(""),
                  stringDefault(""),
                  isArray(false),
                  type(AI_TYPE_UNDEFINED),
                  hasMin(false),
                  hasMax(false),
                  hasSoftMin(false),
                  hasSoftMax(false),
                  keyable(true),
                  linkable(true),
                  channelBox(false)   {}
};

struct CCompoundAttrData
{
   CAttrData data;
   std::vector<CAttrData> children;
};

typedef MStatus  (*AddAttributeFunction)(const MObject &attr);

// CBaseAttrHelper
//
/// Abstract base class for all attribute creation helper classes.
///
/// the attribute helper classes simplify the act of creating maya attributes from arnold node parameters,
/// by examining parameter properties and metadata from the passed arnold node type.
///
/// below is a list of recognized metadata
///
/// - <B>description</B>:     in maya, used as the annotation for the attribute in the Attribute Editor
/// - <B>min</B>:             minimum value allowed
/// - <B>max</B>:             maximum value allowed
/// - <B>softmin</B>:         overridable lower limit used in GUI
/// - <B>softmax</B>:         overridable upper limit used in GUI
/// - <B>maya.shortname</B>:  attribute short name
/// - <B>maya.name</B>:       alternate name to use for the attribute
/// - <B>maya.hide</B>:       don't generate the attribute (default: false)
/// - <B>maya.keyable</B>:    whether the maya attribute should be keyable (default: true)
///
/// CStaticAttrHelper is used within the initialize method of a custom MPxNode to generate static attributes.
///
/// CDynamicAttrHelper adds dynamic attributes to an existing Maya node.
///
/// CExtensionAttrHelper registers dynamic attributes for a node class, such that the attributes are
/// automatically added to all current and future node instances. Extension attribute helpers are used within a
/// translator's NodeInitializer function. Their primary use case is writing a translator for a built-in Maya
/// node type that requires additional Arnold-specific parameters. For example:
///
/// @code
///   CExtensionAttrHelper helper(nodeClassName, "polymesh");
///   helper.MakeInput("subdiv_type");
/// @endcode
///
/// metadata is used to determine all the qualities of the resulting maya attribute: name, keyability, default, min,
/// max, softmin, softmax, etc. (note that the node factory uses CStaticAttrHelper internally, so the same metadata
/// applies for automatically generated custom nodes, and is actually the most common use case). metadata can be
/// created in the shader's C++ source, or in a plain-text mtd file. values in the plain text file take precedence.
///
/// Attributes that do not have an Arnold equivalent can currently only be created from within a NodeInitializer.
/// For example:
/// @code
///   CAttrData data;
///   data.defaultValue.BOOL = false;
///   data.name = "aiExportTangents";
///   data.shortName = "ai_exptan";
///   helper.MakeInputBoolean(data);
/// @endcode
///
/// Any call to any CBaseAttrHelper.MakeInput variants that does not explicitly provide a name will convert the Arnold
/// style "parameter_name" to maya style "parameterName".

class DLLEXPORT CBaseAttrHelper
{

public:
   CBaseAttrHelper(const AtNodeEntry* arnoldNodeEntry=NULL, const MString& prefix="") :
      m_nodeEntry(arnoldNodeEntry),
      m_attrNum(0),
      m_prefix(prefix)
   {
      ReadPrefixMetadata();
   }
   CBaseAttrHelper(const MString& arnoldNodeEntryName, const MString& prefix="") :
      m_nodeEntry(AiNodeEntryLookUp(arnoldNodeEntryName.asChar())),
      m_attrNum(0),
      m_prefix(prefix)
   {
      if (arnoldNodeEntryName.length() && m_nodeEntry == NULL)
         AiMsgWarning("[mtoa.attr] CBaseAttrHelper passed unknown Arnold node type \"%s\"",
                      arnoldNodeEntryName.asChar());
      ReadPrefixMetadata();
   }
   virtual ~CBaseAttrHelper() {};
   bool GetAttrData(const char* paramName, CAttrData& data);

   virtual void MakeInputByte(MObject& attrib, const char* paramName);
   virtual void MakeInputByte(CAttrData& data);
   virtual void MakeInputInt(MObject& attrib, const char* paramName);
   virtual void MakeInputInt(CAttrData& data);
   virtual void MakeInputBoolean(MObject& attrib, const char* paramName);
   virtual void MakeInputBoolean(CAttrData& data);
   virtual void MakeInputFloat(MObject& attrib, const char* paramName);
   virtual void MakeInputFloat(CAttrData& data);
   virtual void MakeInputRGB(MObject& attrib, const char* paramName);
   virtual void MakeInputRGB(CAttrData& data);
   virtual void MakeInputRGBA(MObject& attrib, MObject& attribA, const char* paramName);
   virtual void MakeInputRGBA(CAttrData& data);
   virtual void MakeInputVector(MObject& attrib, const char* paramName);
   virtual void MakeInputVector(CAttrData& data);
   virtual void MakeInputPoint(MObject& attrib, const char* paramName);
   virtual void MakeInputPoint(CAttrData& data);
   virtual void MakeInputPoint2(MObject& attrib, MObject& attribX, MObject& attribY, const char* paramName);
   virtual void MakeInputPoint2(CAttrData& data);
   virtual void MakeInputString(MObject& attrib, const char* paramName);
   virtual void MakeInputString(CAttrData& data);
   virtual void MakeInputMatrix(MObject& attrib, const char* paramName);
   virtual void MakeInputMatrix(CAttrData& data);
   virtual void MakeInputEnum(MObject& attrib, const char* paramName);
   virtual void MakeInputEnum(CAttrData& data);
   virtual void MakeInputNode(MObject& attrib, const char* paramName);
   virtual void MakeInputNode(CAttrData& data);
   /*virtual void MakeInputCurveRamp(MObject& attrib, const char* paramName);
   virtual void MakeInputCurveRamp(CAttrData& data);
   virtual void MakeInputColorRamp(MObject& attrib, const char* paramName);
   virtual void MakeInputColorRamp(CAttrData& data);*/

   virtual void MakeInputCompound(CAttrData& data, std::vector<CAttrData>& children);
   virtual void MakeInputCompound(MObject& attrib, CAttrData& data, std::vector<CAttrData>& children);

   virtual MObject MakeInput(const char* paramName);
   virtual MObject MakeInput(CAttrData& attrData);

   void MakeOutputInt(MObject& attrib, CAttrData& data);
   void MakeOutputBoolean(MObject& attrib, CAttrData& data);
   void MakeOutputFloat(MObject& attrib, CAttrData& data);
   void MakeOutputRGB(MObject& attrib, CAttrData& data);
   void MakeOutputRGBA(MObject& attrib, MObject& attribA, CAttrData& data);
   void MakeOutputVector(MObject& attrib, CAttrData& data);
   void MakeOutputPoint(MObject& attrib, CAttrData& data);
   void MakeOutputPoint2(MObject& attrib, MObject& attribX, MObject& attribY, CAttrData& data);
   void MakeOutputString(MObject& attrib, CAttrData& data);
   void MakeOutputMatrix(MObject& attrib, CAttrData& data);
   void MakeOutputEnum(MObject& attrib, CAttrData& data);
   void MakeOutputNode(MObject& attrib, CAttrData& data);

   MObject MakeOutput();

   void SetNode(const char* arnoldNodeName);
   void GetMObject(const char* attrName) const;

   void SetPrefix(const MString& prefix) { m_prefix = prefix;}

   // helpers
   bool IsHidden(const char* paramName) const;
   virtual MString GetMayaAttrName(const char* paramName) const;
   virtual MString GetMayaAttrShortName(const char* paramName) const;
   // default methods, can't always get the information
   virtual MString GetMayaNodeTypeName() const {return "";}
   virtual MTypeId GetMayaNodeTypeId() const {return MTypeId(MFn::kBase);}

protected:
   void ReadPrefixMetadata();

   virtual void MakeInputInt(MObject& attrib, CAttrData& data);
   virtual void MakeInputByte(MObject& attrib, CAttrData& data);
   virtual void MakeInputBoolean(MObject& attrib, CAttrData& data);
   virtual void MakeInputFloat(MObject& attrib, CAttrData& data);
   virtual void MakeInputRGB(MObject& attrib, CAttrData& data);
   virtual void MakeInputRGBA(MObject& attrib, MObject& attribA, CAttrData& data);
   virtual void MakeInputVector(MObject& attrib,CAttrData& data);
   virtual void MakeInputPoint(MObject& attrib, CAttrData& data);
   virtual void MakeInputPoint2(MObject& attrib, MObject& attribX, MObject& attribY, CAttrData& data);
   virtual void MakeInputString(MObject& attrib, CAttrData& data);
   virtual void MakeInputMatrix(MObject& attrib, CAttrData& data);
   virtual void MakeInputEnum(MObject& attrib, CAttrData& data);
   virtual void MakeInputNode(MObject& attrib, CAttrData& data);
   /*virtual void MakeInputCurveRamp(MObject& attrib, CAttrData& data);
   virtual void MakeInputColorRamp(MObject& attrib, CAttrData& data);*/
   virtual void MakeInput(MObject& input, CAttrData& attrData);

   const AtNodeEntry* m_nodeEntry;
   int m_attrNum;
   MString m_prefix;
   std::map<std::string, MObject> m_attributes;
   virtual MStatus addAttribute(MObject& attrib){return MStatus::kFailure;};

};

// CStaticAttrHelper
//
/// Attribute helper for creating static attributes during Maya node initialization
///
class DLLEXPORT CStaticAttrHelper : public CBaseAttrHelper
{

public:
   /// @param addFunc  function to call to add a dynamic attribute: should be YourMPxSubClass::addAttribute
   /// @param arnoldNodeEntry  arnold node entry to use when checking parameter metadata
   CStaticAttrHelper(AddAttributeFunction addFunc, const AtNodeEntry* arnoldNodeEntry=NULL, const MString& prefix="") :
      CBaseAttrHelper(arnoldNodeEntry, prefix),
      m_addFunc(addFunc)
   {}
   /// @param addFunc  function to call to add a dynamic attribute: should be YourMPxSubClass::addAttribute
   /// @param arnoldNodeEntryName  arnold node entry to use when checking parameter metadata
   CStaticAttrHelper(AddAttributeFunction addFunc, const char* arnoldNodeEntryName, const MString& prefix="") :
      CBaseAttrHelper(arnoldNodeEntryName, prefix),
      m_addFunc(addFunc)
   {
      if (m_nodeEntry == NULL)
      {
         AiMsgWarning("[mtoa.attr] CStaticAttrHelper passed unknown Arnold node type \"%s\"",
                      arnoldNodeEntryName);
      }
   }

protected:
   AddAttributeFunction m_addFunc;

protected:
   virtual MStatus addAttribute(MObject& attrib);
};

// CDynamicAttrHelper
//
/// Attribute helper for creating dynamic attributes on existing Maya nodes
///
class DLLEXPORT CDynamicAttrHelper : public CBaseAttrHelper
{

public:
   /// @param obj  maya node to add attributes to
   /// @param arnoldNodeEntry  arnold node entry to use when checking parameter metadata
   CDynamicAttrHelper(MObject& obj, const AtNodeEntry* arnoldNodeEntry=NULL, const MString& prefix="ai_") :
      CBaseAttrHelper(arnoldNodeEntry, prefix),
      m_instance(obj)
   {}
   /// @param obj  maya node to add attributes to
   /// @param arnoldNodeEntryName  arnold node entry to use when checking parameter metadata
   CDynamicAttrHelper(MObject& obj, const MString& arnoldNodeEntryName, const MString& prefix="ai_") :
      CBaseAttrHelper(arnoldNodeEntryName, prefix),
      m_instance(obj)
   {
      if (m_nodeEntry == NULL)
      {
         AiMsgWarning("[mtoa.attr] CDynamicAttrHelper passed unknown Arnold node type \"%s\" for Maya node type \"%s\"",
                      arnoldNodeEntryName.asChar(), MFnDependencyNode(m_instance).typeName().asChar());
      }
   }

   MString GetMayaNodeTypeName() const {return m_instance.apiTypeStr();}
   MTypeId GetMayaNodeTypeId() const {return MTypeId(m_instance.apiType());}

protected:
   MObject m_instance;

protected:
   virtual MStatus addAttribute(MObject& attrib);
};

// CExtensionAttrHelper
//
/// Attribute helper for adding extension attributes to Maya node classes
///
/// Extension attributes are like a cross between a static and a dynamic attribute. Like static
/// attributes they are added at the class level, but like a dynamic attribute they can be added after
/// the node class has been initialized.
///
/// Extension attributes are added in Maya 2012 via the new MNodeClass. MtoA provides a rough
/// equivalent of this class for versions prior to 2012

class DLLEXPORT CExtensionAttrHelper : public CBaseAttrHelper
{

public:
   /// @param mayaNodeClassName  name of maya class to add attributes to
   /// @param arnoldNodeEntry  arnold node entry to use when checking parameter metadata
   CExtensionAttrHelper(MString mayaNodeClassName, const AtNodeEntry* arnoldNodeEntry = NULL, const MString& prefix = "ai_", 
      bool addCommonAttributes = true) :
      CBaseAttrHelper(arnoldNodeEntry, prefix),
      m_class(mayaNodeClassName)
   {
      if (MTypeId(MFn::kInvalid) == m_class.typeId())
      {
         AiMsgWarning("[mtoa.attr] CExtensionAttrHelper was passed an unknown Maya node type \"%s\"",
                      mayaNodeClassName.asChar());
      }      
      if (addCommonAttributes)
         AddCommonAttributes();
   }
   /// @param mayaNodeClassName  name of maya class to add attributes to
   /// @param arnoldNodeEntryName  arnold node entry to use when checking parameter metadata
   CExtensionAttrHelper(MString mayaNodeClassName, const MString& arnoldNodeEntryName, const MString& prefix = "ai_", 
      bool addCommonAttributes = true) :
      CBaseAttrHelper(arnoldNodeEntryName, prefix),
      m_class(mayaNodeClassName)
   {
      if (MTypeId(MFn::kInvalid) == m_class.typeId())
      {
         AiMsgWarning("[mtoa.attr] CExtensionAttrHelper was passed an unknown Maya node type \"%s\"",
                      mayaNodeClassName.asChar());
      }
      if (m_nodeEntry == NULL)
      {
         AiMsgWarning("[mtoa.attr] CExtensionAttrHelper was passed an unknown Arnold node type \"%s\" for Maya node type \"%s\"",
                      arnoldNodeEntryName.asChar(), mayaNodeClassName.asChar());
      }
      if (addCommonAttributes)
         AddCommonAttributes();
   }

   MString GetMayaNodeTypeName() const {return m_class.typeName();}

protected:   
   MStatus virtual addAttribute(MObject& attrib);

protected:
   void AddCommonAttributes();
   MNodeClass m_class;

};
