#!/usr/bin/env python

import sys
import os
import math

# Minimum requirement for Arnold Python bindings is Python 2.6.0,
# due to use of the 'ctypes' module and 'c_bool'
if sys.hexversion < 0x02060000:
   print('Arnold needs Python 2.6.0 or greater (found Python %d.%d.%d)' % (sys.version_info[0], sys.version_info[1], sys.version_info[2]))
   sys.exit(1)

# Add parent directory of 'pykick' to the search path for modules, so we don't need
# to specify an environment variable PYTHONPATH to find Arnold python bindings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

from arnold import *
from command_line import *
from common import *

# Main render loop
#
def RenderLoop():
   result = AiRender(AI_RENDER_MODE_CAMERA)

   return result

# Creates all AOVs needed for rendering 
#
def CreateAOVs(filterType, width, name, driver):
   # First create filter node from given type, or default
   filter = None
   if filterType:
      filter = AiNode(filterType)
      if filter is None:
         print("Unrecognized filter: %s  (defaulting to %s)" % (filterType, K_DEFAULT_FILTER))
   
   if filter is None:
      filter = AiNode(K_DEFAULT_FILTER)

   if width != 0.0:
      if AiNodeEntryLookUpParameter(filter.base_node, "width"):
         AiNodeSetFlt(filter, "width", width)
   
   AiNodeSetStr(filter, "name", name)

   # Build the output string and return it
   aov_decl_str = "RGBA RGBA  %s %s" % (name, driver)
   aov_decl = create_string_buffer(aov_decl_str)
   
   return AiArray(1, 1, AI_TYPE_STRING, aov_decl)
   
# Creates a sets up a file output driver from output file name if none exists 
#
def CreateOutputDriver():
   # First try to get output driver type from the output file name 
   driver = None
   if GC.outputFileName != '':
      name, ext = os.path.splitext(GC.outputFileName)
      if ext:
         GC.driverType = AiFindDriverType(ext[1:])
         driver = AiNodeLookUpByName(K_DRIVER_NAME)

   if not driver:
      if GC.driverType:
         # Create a driver from the given type
         driver = AiNode(AiNodeEntryGetName(GC.driverType))
      else:
         if GC.outputFileName:
            Error('Format of output file "%s" not recognized' % GC.outputFileName)
         else:
            Warning("No output file provided")

      # Set Output Gamma value unless it is the null driver
      if GC.gamma != 1.0:
         AiNodeSetFlt(driver, "gamma", GC.gamma)

      AiNodeSetStr(driver, "name", K_DRIVER_NAME)
      GC.driverNode = driver

   # Set output file name in driver
   if driver:
      AiNodeSetStr(GC.driverNode, "filename", GC.outputFileName)

   AiNodeSetArray(AiUniverseGetOptions(), "outputs", CreateAOVs(GC.filterTypeName, GC.filterWidth, K_FILTER_NAME, K_DRIVER_NAME))

# Process error code returned by AiRender() 
#
def ProcessRenderError(error):
   if GC.verbosity == 0:
      if error == AI_ERROR_WRONG_OUTPUT:
         sys.stderr.write("Can't open output file: %s\n" % AiNodeGetStr(AiUniverseGetOptions(), "output_file_name"))
      elif error == AI_ERROR_NO_CAMERA:
         sys.stderr.write("No camera!\n")
      else:
         sys.stderr.write("Error during rendering\n")

# Render <GC.turns> frames rotating the camera around the look_at point
#
def DoTurntable():
   fileName, fileExt = os.path.splitext(GC.outputFileName)
   camera = cast(AiNodeGetPtr(AiUniverseGetOptions(), "camera"), POINTER(AtNode))
   previous_pos = AiNodeGetPnt(camera, "position")
   lookat = AiNodeGetPnt(camera, "look_at")
   up = AiNodeGetVec(camera, "up")
   lookat_array = AiArrayAllocate(1, 2, AI_TYPE_POINT)
   up_array = AiArrayAllocate(1, 2, AI_TYPE_VECTOR)
   AiArraySetPnt(lookat_array, 0, lookat)
   AiArraySetPnt(lookat_array, 1, lookat)
   AiArraySetVec(up_array, 0, up)
   AiArraySetVec(up_array, 1, up)
   AiNodeSetArray(camera, "look_at", lookat_array)
   AiNodeSetArray(camera, "up", up_array)
   
   # Calculate reference vectors for turntable rendering
   #   v    = pos - lookat
   #   z    = up / |up|
   #   vp   = dot(v, z) * z
   #   x    = v - vp
   #   y    = z ^ x
   #   pos' = lookat + vp + x * cos (angle) + y * sin (angle)
   v = previous_pos - lookat
   z = up.Normalize()
   vp = z * DotProduct(v, z)
   x = v - vp
   y = CrossProduct(z, x)
   vp += lookat

   result = AI_SUCCESS
   
   for n in range(GC.turns):
      if GC.turns > 1:
         GC.outputFileName = "%s.%04d%s" % (fileName, n, fileExt)
         angle = 2.0 * AI_PI * (n + 1) / GC.turns
         new_pos = vp + x * math.cos(angle) + y * math.sin(angle)
         pos_array = AiArrayAllocate(1, 2, AI_TYPE_POINT)
         AiArraySetPnt(pos_array, 0, previous_pos)
         AiArraySetPnt(pos_array, 1, new_pos)
         AiNodeSetArray(camera, "position", pos_array)
         previous_pos = new_pos
         AiNodeSetInt(AiUniverseGetOptions(), "AA_seed", n)

      if GC.driverNode:
         AiNodeSetStr(GC.driverNode, "filename", GC.outputFileName)

      if GC.resave:
         AiASSWrite(GC.resaveFileName, AI_NODE_ALL, GC.openProcedurals)
      else:
         result = RenderLoop()

   return result

# Main render code block
#
def DoRender(argv, count):
   exit_code = K_SUCCESS

   AiBegin()
   SetLogOptions(True)

   AiMsgInfo("[pykick] command: %s", " ".join(argv));

   # Load plugin libraries, possibly from multiple paths
   # (but do it only once if using -repeat)
   if count == 0:
      for path in GC.libPaths:
         AiLoadPlugins(path)
   
   # Must set the ignore list before actually loading the scene
   if GC.ignoreList:
      array = AiArrayAllocate(len(GC.ignoreList), 1, AI_TYPE_STRING)

      for i in range(len(GC.ignoreList)):
         AiArraySetStr(array, i, GC.ignoreList[i])

      AiNodeSetArray(AiUniverseGetOptions(), "ignore_list", array)

   # Open all input files (including stdin if needed)
   for file in GC.inputFileNames:
      if file == K_STDIN_STRING and GC.ignoreStdin:
         continue
      error = AiASSLoad(file, AI_NODE_ALL)
      if error:
         Error("Can't read input file: %s" % file)

   # Do a second pass on the command line parameters, to apply params depending on scene data
   ParseCommandLine2(argv)

   # If no output string set in the input scene, create it now
   if AiNodeGetArray(AiUniverseGetOptions(), "outputs").contents.nelements == 0 and not GC.resave:
      CreateOutputDriver()

   if GC.resave:
      GC.renderWindow = False
      GC.progressive = False

   # Override camera settings
   if GC.shutterStart >= 0:
      AiNodeSetFlt(AiUniverseGetCamera(), "shutter_start", GC.shutterStart)
      AiNodeSetFlt(AiUniverseGetCamera(), "shutter_end", GC.shutterEnd)
   if GC.fov >= 0:
      fovArray = AiNodeGetArray(AiUniverseGetCamera(), "fov")
      if fovArray:
         for i in range(fovArray.contents.nelements * fovArray.contents.nkeys):
            AiArraySetFlt(fovArray, i, GC.fov)
   if GC.camera_exposure != 0:
      AiNodeSetFlt(AiUniverseGetCamera(), "exposure", GC.camera_exposure);

   # Apply attributes set in the command line (via -set parameter)
   ApplyAttributes()

   result = AI_SUCCESS
   
   # If turn is on, render N frames changing the camera and output file
   if GC.turns > 1:
      result = DoTurntable()
   else:
      if GC.resave:
         AiASSWrite(GC.resaveFileName, AI_NODE_ALL, GC.openProcedurals)
      else:   
         result = RenderLoop()

   AiEnd()
   
   if result != AI_SUCCESS:
      ProcessRenderError(result)
      exit_code = K_ERROR
         
   return exit_code

# Program entry point 
#
def main(argv = None):
   if argv is None:
      argv = sys.argv

   if len(argv) == 1 and sys.stdin.isatty():
      DisplayVersion()
      Error("No arguments. Try pykick --help for a command summary")

   if not sys.stdin.isatty():
      GC.inputFileNames.append('-')
      
   ParseCommandLine1(argv)

   SetupPluginSearchPath()
   
   if GC.infoMode == InfoMode.K_INFO_NODES:
      PrintNodes(GC.infoSort)
      return K_SUCCESS
   elif GC.infoMode == InfoMode.K_INFO_NODE:
      PrintNodeInfo(GC.infoData, GC.infoSort)
      return K_SUCCESS
   elif GC.infoMode == InfoMode.K_INFO_LIST_OUTPUT_DRIVERS:
      PrintDriverExtensions()
      return K_SUCCESS
   elif GC.infoMode == InfoMode.K_INFO_LICENSE:
      PrintLicenseInfo()
      return K_SUCCESS

   if len(GC.inputFileNames) == 0 or (len(GC.inputFileNames) == 1 and not sys.stdin.isatty() and GC.ignoreStdin):
      Error("No input files. Try pykick --help for a command summary")

   for count in range(GC.repetitions):
      exit_code = DoRender(argv, count)
      if GC.repetitions > 1:
         print("[pykick] render %d finished" % (count + 1))

   return exit_code

if __name__ == "__main__":
   main()
