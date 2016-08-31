#pragma once

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/time.h>
#endif

#include <sys/timeb.h>

#include <ai_types.h>
#include <ai_nodes.h>
#include <ai_node_entry.h>

#define MAX_NAME_SIZE 65535

inline AtUInt64 MtoaTicks()
{
#ifdef _WIN32
   LARGE_INTEGER PerformanceCount;
   LARGE_INTEGER Frequency;

   QueryPerformanceCounter(&PerformanceCount);
   QueryPerformanceFrequency(&Frequency);

   return PerformanceCount.QuadPart / (Frequency.QuadPart / 1000000);
#else
   // UNIX platforms: Linux and OS X
   struct timeval tp;
   gettimeofday(&tp, NULL);
   return ((AtUInt64) tp.tv_sec * 1000000) + ((AtUInt64) tp.tv_usec);
#endif
}


inline AtUInt32 MtoaTime()
{
#ifdef _WIN32
   struct _timeb timebuffer;

   _ftime(&timebuffer);
   return (AtUInt32) (timebuffer.time * 1000) + timebuffer.millitm;
#else
   // UNIX platforms: Linux and OS X
   struct timeval tp;
   gettimeofday(&tp, NULL);
   return (AtUInt32) ((AtUInt64) (tp.tv_sec * 1000) + (AtUInt64) (tp.tv_usec / 1000));
#endif
}

/*
 * Creates a unique name string with the node type followed
 * by a double time-stamp (current time in milliseconds and
 * process ellapsed time in microseconds). Example:
 *
 *    sphere_34CEAD9B00052F21
 *           \______/\______/
 *           AiTime  AiTicks
 *
 * \param      node    the node we want to give a default name to
 * \param[out] string  pre-allocated buffer for the new name string
 * \return             the new name string (again)
 */
inline char *NodeUniqueName(AtNode *node, char *string)
{
   sprintf(string, "%s_%08X%08llX",
      AiNodeEntryGetName(AiNodeGetNodeEntry(node)), MtoaTime(), MtoaTicks());
   return string;
}

