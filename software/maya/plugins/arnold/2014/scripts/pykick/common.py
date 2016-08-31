
import sys
import platform
import os.path
from arnold import *

# Global constant definition
K_SUCCESS = 0
K_ERROR = 256

K_SEARCH_PATH = "KICK_SEARCHPATH"
K_STDIN_STRING = "-"

K_DRIVER_NAME = "kick_driver"
K_FILTER_NAME = "kick_filter"
K_DEFAULT_FILTER = "gaussian_filter"

class InfoMode:
   K_INFO_NONE = 0
   K_INFO_NODES = 1
   K_INFO_NODE = 2
   K_INFO_LIST_OUTPUT_DRIVERS = 3
   K_INFO_LICENSE = 4
   
# Global context
class GC:
   verbosity = 1             # Log verbosity level
   inputFileNames = []       # Input .ass files
   outputFileName = ''       # Output image file
   logFileName = ''          # Output log file
   renderWindow = True       # Toggles render window display
   progressive = True        # Toggles progressive rendering
   maxWarnings = 200         # Max number of warnings allowed in the log
   writeLog = False          # Toggles log generation
   libPaths = []             # Additional paths for plugins      
   repetitions = 1           # Number of times the scene will be rendered (for debugging purposes) 
   turns = 1                 # Number of different shots to be rendered around the scene 
   resave = False            # Rewrite the scene to a new .ass file 
   openProcedurals = False   # Rewrite the scene to a new .ass file, opening procedurals
   resaveFileName = ''       # File the scene will be rewritten to
   shutterStart = -1         # Camera parameter override
   shutterEnd = -1           # Camera parameter override
   fov = -1                  # Camera parameter override
   camera_exposure = 0       # Camera parameter override
   gamma = 1.0               # Output gamma 
   flatAll = False           # Set all shaders to a flat color
   driverType = None         # Output driver type
   driverNode = None         # Output driver node
   filterTypeName = ''       # Output filter name
   filterWidth = 0.0         # Output filter width 
   attributes = []           # List of attributes to be set before rendering
   ignoreStdin = False       # Toggles use of the stdin as an input file
   ignoreList = []           # List of node (or parameters) to be ignored when rendering
   infoMode =  InfoMode.K_INFO_NONE
   infoSort = 0
   infoData = ''

# Convert verbosity level into a flags bitmask for Arnold
def ComputeLogFlags(verbosity):
   if (verbosity == 0):
      return 0
   if (verbosity == 5):
      return AI_LOG_ALL & ~AI_LOG_DEBUG
   if (verbosity == 6):
      return AI_LOG_ALL

   if (verbosity >= 1):
      flags = AI_LOG_INFO      | AI_LOG_WARNINGS  | AI_LOG_ERRORS | \
              AI_LOG_TIMESTAMP | AI_LOG_BACKTRACE | AI_LOG_MEMORY | \
              AI_LOG_COLOR
      if (verbosity >= 2):
         flags |= AI_LOG_PROGRESS
         if (verbosity >= 3):
            flags |= AI_LOG_STATS
            if (verbosity >= 4):
               flags |= AI_LOG_PLUGINS

   return flags

def SetLogOptions(info):
   flags = ComputeLogFlags(GC.verbosity)

   if not info:
      flags &= ~AI_LOG_INFO
      flags &= ~AI_LOG_TIMESTAMP
      flags &= ~AI_LOG_MEMORY

   AiMsgSetMaxWarnings(GC.maxWarnings)

   # this one is for the console output
   AiMsgSetConsoleFlags(flags)

   # and this one is for the file output
   if GC.writeLog:
      if GC.logFileName != '':
         logname = GC.logFileName
      elif GC.outputFileName == '':
         logname = 'arnold.log'
      else:
         logname = GC.outputFileName + '.log'
      AiMsgSetLogFileName(logname)
      AiMsgSetLogFileFlags(flags)

def SetupPluginSearchPath():
   if K_SEARCH_PATH in os.environ:
      GC.libPaths = os.environ[K_SEARCH_PATH].split(os.pathsep)
   if len(GC.libPaths) == 0:
      GC.libPaths.append(os.curdir)

def Error(message):
   if AiUniverseIsActive():
      AiMsgError("[pykick] %s", message)
      AiEnd()
   else:
      sys.stderr.write(message + "\n")
   sys.exit(K_ERROR) 

def Warning(message):
   if AiUniverseIsActive():
      AiMsgWarning("[pykick] %s", message)
   else:
      sys.stderr.write(message + "\n")

def DisplayVersion():
   print(AiGetVersionInfo())

def DisplayHelp():
   DisplayVersion()
   
   print("\nUsage:\n  pykick [option] [option] [option] ...")
   print("\nOptions:")
   print("  -i <s>          Input .ass file")
   print("  -o <s>          Output filename")
   print("  -of <s>         Output format (none jpg tiff8 tiff16 tiff32)")
   print("  -r <n n>        Image resolution")
   print("  -sr <f>         Scale resolution <f> times in each dimension")
   print("  -rg <n n n n>   Render region (minx miny maxx maxy)")
   print("  -as <n>         Anti-aliasing samples")
   print("  -af <s> <f>     Anti-aliasing filter and width (box disk gaussian ...)")
   print("  -asc <f>        Anti-aliasing sample clamp")
   print("  -c <s>          Active camera")
   print("  -sh <f f>       Motion blur shutter (start end)")
   print("  -fov <f>        Camera FOV")
   print("  -e <f>          Camera Exposure")
   print("  -ar <f>         Aspect ratio")
   print("  -g <f>          Output gamma")
   print("  -tg <f>         Texture gamma")
   print("  -lg <f>         Light source gamma")
   print("  -sg <f>         Shader gamma")
   print("  -t <n>          Threads")
   if platform.system().lower() == 'windows':
      print("  -tp <n>         Thread priority (0..3)")
   print("  -bs <n>         Bucket size")
   print("  -bc <s>         Bucket scanning (top bottom left right random woven spiral hilbert)")
   print("  -td <n>         Total ray depth")
   print("  -rfl <n>        Reflection depth")
   print("  -rfr <n>        Refraction depth")
   print("  -dif <n>        Diffuse depth")
   print("  -glo <n>        Glossy depth")
   print("  -ds <n>         Diffuse samples")
   print("  -gs <n>         Glossy samples")
   print("  -d <s.s>        Disable (ignore) a specific node or node.parameter")
   print("  -it             Ignore texture maps")
   print("  -is             Ignore shaders")
   print("  -ib             Ignore background shaders")
   print("  -ia             Ignore atmosphere shaders")
   print("  -il             Ignore lights")
   print("  -id             Ignore shadows")
   print("  -isd            Ignore mesh subdivision")
   print("  -idisp          Ignore displacement")
   print("  -ibump          Ignore bump-mapping")
   print("  -imb            Ignore motion blur")
   print("  -idof           Ignore depth of field")
   print("  -isss           Ignore sub-surface scattering")
   print("  -idirect        Ignore direct lighting")
   print("  -flat           Flat shading")
   print("  -sd <n>         Max subdivisions")
   print("  -v <n>          Verbose level (0..6)")
   print("  -nw <n>         Maximum number of warnings")
   print("  -log            Enable log file")
   print("  -logfile <s>    Enable log file and write to the specified file path")
   print("  -dw             Disable render window (recommended for batch rendering)")
   print("  -dp             Disable progressive rendering (recommended for batch rendering)")
   print("  -l <s>          Add search path for plugin libraries")
   print("  -nodes [n|t]    List all installed nodes, sorted by Name or Type")
   print("  -info [n|u] <s> List information for a given node, sorted by Name or Unsorted")
   print("  -tree <s>       Print the shading tree for a given node")
   print("  -repeat <n>     Repeat the render n times (useful for debugging)")
   print("  -turn <n>       Render n frames rotating the camera around the lookat point")
   print("  -resave <s>     Re-save .ass scene to filename")
   print("  -db             Disable binary encoding when re-saving .ass files")
   print("  -forceexpand    Force single-threaded expansion of procedural geometry before rendering or re-saving")
   print("  -nstdin         Ignore input from stdin")
   print("  -set <s.s> <s>  Set the value of a node parameter (-set name.parameter value)")
   print("  -cm <s>         Set the value of ai_default_reflection_shader.color_mode (use with -is)")
   print("  -sm <s>         Set the value of ai_default_reflection_shader.shade_mode (use with -is)")
   print("  -om <s>         Set the value of ai_default_reflection_shader.overlay_mode (use with -is)")
   print("  -utest          Run unit tests")
   print("  -av             Print Arnold version number")
   print("  -sl             Skip license check (assume license is not available)")
   print("  -licensecheck   Check the connection with the license servers and list installed licenses")
   print("  -h, --help      Show this help message")
  
   print("")
   print("where <n>=integer, <f>=float, <s>=string")
   print("")
   print("Example:")
   print("  pykick -i teapot.ass -r 640 480 -g 2.2 -o teapot.tif")
   print("")

   print("(c) 2001-2009 Marcos Fajardo and (c) 2009-2014 Solid Angle SL, www.solidangle.com")
   print("Acknowledgements: armengol ben brian cliff colman erco francisco quarkx rene scot sergio xray yiotis")

def PrintDriverExtensions():
   AiBegin()
   SetLogOptions(False)
   SetupPluginSearchPath()
   
   for path in GC.libPaths:
      AiLoadPlugins(path)

   driver_types = []
   it = AiUniverseGetNodeEntryIterator(AI_NODE_DRIVER)
   while not AiNodeEntryIteratorFinished(it):
      nentry     = AiNodeEntryIteratorGetNext(it)
      extensions = AiDriverExtension(nentry)
      if extensions:
         driver_types.append(extensions.contents.value)
   AiNodeEntryIteratorDestroy(it)

   print("Installed drivers:", " ".join(driver_types))
   
   AiEnd()

def ApplyAttributes():
   if not GC.attributes:
      return
      
   AiMsgInfo("applying %d attr value overrides", len(GC.attributes))

   for (attrib, value) in GC.attributes:
      if not attrib or not value:
         AiMsgWarning("bad attr value override for -set")
         continue

      (node_name, sep, param) = attrib.rpartition('.')
      
      node = AiNodeLookUpByName(node_name)
      
      if node:
         pentry = AiNodeEntryLookUpParameter(AiNodeGetNodeEntry(node), param)

         if pentry:
            type = AiParamGetType(pentry)
            if type == AI_TYPE_ARRAY:
               type = AiParamGetDefault(pentry).contents.ARRAY.contents.type
         else:
            upentry = AiNodeLookUpUserParameter(node, param)
            
            if upentry:
               type = AiUserParamGetType(upentry)
               if type == AI_TYPE_ARRAY:
                  type = AiUserParamGetArrayType(upentry)
                  
         if type != AI_TYPE_UNDEFINED:
            if type == AI_TYPE_BYTE:
               AiNodeSetByte(node, param, AtByte(int(value)))
            elif type == AI_TYPE_INT:
               AiNodeSetInt(node, param, AtInt(int(value)))
            elif type == AI_TYPE_UINT:
               AiNodeSetUInt(node, param, AtUInt(int(value)))
            elif type == AI_TYPE_BOOLEAN:
               AiNodeSetBool(node, param, value in ["yes", "on", "true", "1"])
            elif type == AI_TYPE_FLOAT:
               AiNodeSetFlt(node, param, AtFloat(float(value)))
            elif type == AI_TYPE_STRING:
               AiNodeSetStr(node, param, value)
            elif type == AI_TYPE_ENUM:
               AiNodeSetInt(node, param, AiEnumGetValue(AiParamGetEnum(pentry), value))
            elif type == AI_TYPE_POINTER:
               AiNodeSetPtr(node, param, AiNodeLookUpByName(value))
            elif type == AI_TYPE_RGB:
               rgb = [float(v) for v in value.split(" ")]
               if len(rgb) == 3:
                  AiNodeSetRGB(node, param, rgb[0], rgb[1], rgb[2])
               else:
                  AiMsgWarning("couldn't parse '%s' for %s", value, param);
            elif type == AI_TYPE_RGBA:
               rgba = [float(v) for v in value.split(" ")]
               if len(rgba) == 4:
                  AiNodeSetRGBA(node, param, rgba[0], rgba[1], rgba[2], rgba[3])
               else:
                  AiMsgWarning("couldn't parse '%s' for %s", value, param);
            elif type == AI_TYPE_VECTOR:
               vec = [float(v) for v in value.split(" ")]
               if len(vec) == 3:
                  AiNodeSetVec(node, param, vec[0], vec[1], vec[2])
               else:
                  AiMsgWarning("couldn't parse '%s' for %s", value, param);
            elif type == AI_TYPE_POINT:
               pnt = [float(v) for v in value.split(" ")]
               if len(pnt) == 3:
                  AiNodeSetPnt(node, param, pnt[0], pnt[1], pnt[2])
               else:
                  AiMsgWarning("couldn't parse '%s' for %s", value, param);
            elif type == AI_TYPE_POINT2:
               pnt = [float(v) for v in value.split(" ")]
               if len(pnt) == 2:
                  AiNodeSetPnt2(node, param, pnt[0], pnt[1])
               else:
                  AiMsgWarning("couldn't parse '%s' for %s", value, param);
            else:
               AiMsgWarning("unsupported type for -set: %s", param);
         else:
            AiMsgWarning("couldn't find parameter named '%s' for -set", param)
      else:
         AiMsgWarning("couldn't find node named '%s' for -set", node_name)
