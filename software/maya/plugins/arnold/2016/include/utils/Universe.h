#pragma once

#include "MtoaLog.h"

#include <maya/MString.h>
#include <maya/MStatus.h>

DLLEXPORT void SetMetafile(MString metafile);

DLLEXPORT MStatus ReadMetafile();

DLLEXPORT void InstallNodes();
DLLEXPORT void LoadPlugins();

// return true if the universe had to be initialized (and thus should be uninitialized), false if it was already active
DLLEXPORT bool ArnoldUniverseBegin(int logFlags = DEFAULT_LOG_FLAGS);
DLLEXPORT bool ArnoldUniverseOnlyBegin();
DLLEXPORT void ArnoldUniverseLoadPluginsAndMetadata();
DLLEXPORT void ArnoldUniverseEnd();
DLLEXPORT void ArnoldUniverseEndAndFlush(int cache_flags);
