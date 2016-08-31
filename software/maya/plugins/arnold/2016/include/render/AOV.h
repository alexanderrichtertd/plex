#pragma once

#include "platform/Platform.h"

#include <ai.h>

#include <maya/MString.h>
#include <maya/MPlug.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MStringArray.h>

#include <cstring>
#include <string>
#include <map>
#include <vector>
#include <set>

class CMayaScene;

class CAOV;
typedef std::set<CAOV> AOVSet;

struct CAOVData
{
   MString attribute;
   MString name;
   int type;
};

class CAOV;
typedef std::set<CAOV> AOVSet;

enum AOVMode
{
   AOV_MODE_DISABLED,
   AOV_MODE_ENABLED,
   AOV_MODE_BATCH_ONLY
};

/// Represents a single AOV
class DLLEXPORT CAOV
{
public:
   CAOV();
   CAOV(const CAOV &rhs);
   ~CAOV();

   CAOV& operator=(const CAOV &rhs);

   inline bool operator==(const CAOV& other) const { return m_name == other.GetName(); }
   inline bool operator!=(const CAOV& other) const { return m_name != other.GetName(); }
   inline bool operator<(const CAOV& other) const { // "beauty" AOV will be first
      return (strcmp(other.GetName().asChar(),"beauty") != 0) && ((strcmp(m_name.asChar(),"beauty") == 0) || (strcmp(m_name.asChar(), other.GetName().asChar()) < 0)); }

   inline const MString& GetName() const { return m_name; }
   inline void SetName(const MString &name) { m_name = name; }

   inline MObject GetNode() const { return m_object; }

   inline const MString& GetPrefix() const { return m_prefix; }
   inline int GetDataType() const { return m_type; };

   inline const MStringArray& GetImageFormats() const { return m_extensions; }

   bool IsEnabled() const { return m_enabled; }
   bool FromMaya(MObject &o);

protected:

   void ReturnType(MString &mtype) const;
   void NormalizePath(MString &path) const;
   void Strip(MString &str) const;

protected:

   MString   m_name;
   // enumerator that corresponds to arnold's data type enum
   int       m_type;
   bool      m_enabled;
   MString   m_prefix;
   MString   m_imageformat;
   MObject   m_object;
   MFnDependencyNode m_fnNode;
   std::vector<AtNode*>  m_drivers;
   std::vector<AtNode*>  m_filters;
   MStringArray m_extensions;
};
