#pragma once

#include "platform/Platform.h"

#include <stdio.h>
#include <stdarg.h>
#include <cstring>

#include <ai_msg.h>

#if defined ARNOLD_DEBUG || !defined NDEBUG
#define DEFAULT_LOG_FLAGS AI_LOG_ALL
#else
#define DEFAULT_LOG_FLAGS (AI_LOG_ERRORS | AI_LOG_WARNINGS | AI_LOG_TIMESTAMP | AI_LOG_BACKTRACE)
#endif

DLLEXPORT int GetFlagsFromVerbosityLevel(unsigned int level);

DLLEXPORT void MtoaLogCallback(int logmask, int severity, const char *msg_string, int tabs);

DLLEXPORT void MtoaSetupLogging(int logflags = DEFAULT_LOG_FLAGS);
