#ifndef DEBUG_H
#define DEBUG_H

#ifdef _DEBUG
#include <stdlib.h>
#include <crtdbg.h>
// #include <vld.h>
#ifndef DEBUG_NEW
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#endif // DEBUG_NEW
// Use this at any point in code
// to dump memory leaks info into debugger output window
#ifndef DEBUG_MEMORY
#define DEBUG_MEMORY _CrtDumpMemoryLeaks()
#endif // DEBUG_MEMORY
#else
#ifndef DEBUG_MEMORY
#define DEBUG_MEMORY
#endif // DEBUG_MEMORY
#endif

#endif  // DEBUG_H
