#pragma once

#include "platform/Platform.h"
#include <ai.h>

DLLEXPORT bool AiNodeDeclareConstant(AtNode* node, const char* name, unsigned int type);
DLLEXPORT bool AiNodeDeclareConstantArray(AtNode* node, const char* name, unsigned int type);
DLLEXPORT bool AiNodeDeclareUniform(AtNode* node, const char* name, unsigned int type);
DLLEXPORT bool AiNodeDeclareVarying(AtNode* node, const char* name, unsigned int type);
