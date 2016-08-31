#pragma once

#include <ai_nodes.h>

#include <maya/MStatus.h>
#include <maya/MPlug.h>
#include <maya/MStringArray.h>

namespace // <anonymous>
{
const MStringArray INVALID_COMPONENTS;
const char* rgbComp[3] = {"r", "g", "b"};
const MStringArray RGB_COMPONENTS(rgbComp, 3);
const char* rgbaComp[4] = {"r", "g", "b", "a"};
const MStringArray RGBA_COMPONENTS(rgbaComp, 4);
const char* point2Comp[2] = {"x", "y"};
const MStringArray POINT2_COMPONENTS(point2Comp, 2);
const char* vectorComp[3] = {"x", "y", "z"};
const MStringArray VECTOR_COMPONENTS(vectorComp, 3);
}

enum ComponentType
{
   COMPONENT_TYPE_INVALID,
   COMPONENT_TYPE_NONE,
   COMPONENT_TYPE_NORMAL,
   COMPONENT_TYPE_OUTALPHA
};

const MStringArray& GetComponentNames(int arnoldParamType);
MString GetComponentName(int arnoldParamType, const MPlug &plug);
int GetFloatComponentIndex(const MPlug &plug);
ComponentType ResolveFloatComponent(const MPlug &plug, MPlug &attrResult);
AtNode* InsertConversionNodes(const MPlug &shaderOutputPlug, ComponentType compMode, AtNode* shader);
