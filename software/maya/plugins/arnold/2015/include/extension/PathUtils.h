#pragma once

#define PLUGIN_SEARCH "$ARNOLD_PLUGIN_PATH"
#define EXTENSION_SEARCH "$MTOA_EXTENSIONS_PATH"

#ifdef WIN32
#define PATH_SEPARATOR ";"
#else
#define PATH_SEPARATOR ":"
#endif
