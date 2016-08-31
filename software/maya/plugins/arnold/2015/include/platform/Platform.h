#pragma once

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#define DLLEXPORT __declspec(dllexport)
#ifdef _MSC_VER
#pragma warning(disable:4251)
#pragma warning(disable:4267)
#include "platform/win32/Debug.h"
#endif // _MSC_VER
#include "platform/win32/Event.h"
#include <platform/win32/dirent.h>
#define PATHSEP ';'
#define DIRSEP "/"
#define LIBEXT ".dll"

#else // _WIN32

#include <sys/types.h>
#include <dirent.h>
#include <dlfcn.h>

#define PATHSEP ':'
#define DIRSEP "/"

#ifdef _LINUX
#define DLLEXPORT __attribute__ ((visibility("default")))
#define DEBUG_NEW new
#include "platform/linux/Event.h"
#define LIBEXT ".so"
#endif // _LINUX

#ifdef _DARWIN
#define DLLEXPORT __attribute__ ((visibility("default")))
#define DEBUG_NEW new
#include "platform/darwin/Event.h"
#define LIBEXT ".dylib"
#endif // _DARWIN

#endif // #else _WIN32
