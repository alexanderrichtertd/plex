
from arnold import *
from common import *
from info import *

class CommandLineParser:
   def __init__(self, args):
      self.args = args
      self.current = 0
      
   def Finished(self):
      return (self.current == len(self.args))
      
   def CurrentParameter(self):
      return '' if self.Finished() else self.args[self.current]

   def CurrentArguments(self):
      arguments = []
      index = 1
      while (self.current + index < len(self.args)) and not self.IsParameter(self.args[self.current + index]):
         arguments.append(self.args[self.current + index])
         index += 1
      return arguments

   def CheckArgument(self, num):
      if (len(self.CurrentArguments()) < num):
         Error('Wrong number of arguments in parameter "%s"' % self.CurrentParameter());
      else:
         self.current += num

   def IsParameter(self, str):
      # NOTE: Command line parameters are assumed to begin with a lower case letter
      return (len(str) >= 2) and (str[0] == '-') and str[1].islower()

def ParseCommandLine1(argv):
   if len(argv) < 2:
      return False

   parser = CommandLineParser(argv[1:])

   while not parser.Finished():
      param = parser.CurrentParameter()
      arguments = parser.CurrentArguments()
      
      if param == '-i':
         parser.CheckArgument(1)
         if not arguments[0] in GC.inputFileNames:
            GC.inputFileNames.append(arguments[0])
      elif param == '-o':
         parser.CheckArgument(1)
         GC.outputFileName = arguments[0]
      elif param == '-of':
         if parser.current == len(parser.args) - 1:
            GC.infoMode = InfoMode.K_INFO_LIST_OUTPUT_DRIVERS
         else: 
            parser.CheckArgument(1)
      elif param == '-r':
         parser.CheckArgument(2)
      elif param == '-d':
         parser.CheckArgument(1)
         GC.ignoreList.append(arguments[0])
      elif param == '-dw':
         GC.renderWindow = False
      elif param == '-dp':
         GC.progressive = False
      elif param == '-db':
         GC.binary_ass = False
      elif param == '-v':
         if len(arguments) == 0:
            GC.verbosity = 1
         else:
            GC.verbosity = int(arguments[0])
            parser.current += 1
      elif param == '-nw':
         parser.CheckArgument(1)
         GC.maxWarnings = int(arguments[0])               
      elif param == '-log':
         GC.writeLog = True
      elif param == '-logfile':
         parser.CheckArgument(1)
         GC.logFileName = arguments[0]
         GC.writeLog = True
      elif param == '-l':
         parser.CheckArgument(1)
         if not arguments[0] in GC.libPaths:
            GC.libPaths.append(arguments[0])
      elif param == '-repeat':
         parser.CheckArgument(1)
         GC.repetitions = max(1, int(arguments[0]))               
      elif param == '-turn':
         parser.CheckArgument(1)
         GC.turns = max(1, int(arguments[0]))               
      elif param == '-resave':
         parser.CheckArgument(1)
         GC.resave = True
         GC.resaveFileName = arguments[0]
      elif param == '-nstdin':
         GC.ignoreStdin = True
      elif param == '-set':
         parser.CheckArgument(len(arguments))
         attrib = arguments[0]
         value = " ".join(arguments[1:])
         GC.attributes.append((attrib, value))
      elif param == '-cm':
         parser.CheckArgument(1)
         attrib = "ai_default_reflection_shader.color_mode"
         value = arguments[0]
         GC.attributes.append((attrib, value))
      elif param == '-sm':
         parser.CheckArgument(1)
         attrib = "ai_default_reflection_shader.shade_mode"
         value = arguments[0]
         GC.attributes.append((attrib, value))
      elif param == '-om':
         parser.CheckArgument(1)
         attrib = "ai_default_reflection_shader.overlay_mode"
         value = arguments[0]
         GC.attributes.append((attrib, value))
      elif param == '-nodes':
         GC.infoMode = InfoMode.K_INFO_NODES
         if len(arguments) == 0:
            GC.infoSort = 0
         else:
            parser.CheckArgument(1)
            if arguments[0] == 'n':
               GC.infoSort = 0
            elif arguments[0] == 't':
               GC.infoSort = 1
            else:
               Error('Unknown sort type "%s"' % arguments[0])
      elif param == '-info':
         GC.infoMode = InfoMode.K_INFO_NODE
         parser.CheckArgument(1)
         if arguments[0] == 'u':
            parser.CheckArgument(1)
            GC.infoData = arguments[1]
            GC.infoSort = 0
         elif arguments[0] == 'n':
            parser.CheckArgument(1)
            GC.infoData = arguments[1]
            GC.infoSort = 1
         else:
            GC.infoData = arguments[0]
            GC.infoSort = 1
      elif param == '-tree':
         parser.CheckArgument(1)
      elif param == '-utest':
         result = AiTest()
         sys.exit(K_SUCCESS if result else K_ERROR)
      elif param == '-av':
         print(AiGetVersionString())
         sys.exit(K_SUCCESS)
      elif param == '-h' or param == '-help' or param == '--help':
         DisplayHelp()
         sys.exit(K_SUCCESS)
      elif param == '-licensecheck':
         GC.infoMode = InfoMode.K_INFO_LICENSE
      else:
         ext = os.path.splitext(param)[1]
         if ext == '.ass' or ext == '.gz':
            if not param in GC.inputFileNames:
               GC.inputFileNames.append(param)

      parser.current += 1          
      
   return True

def ParseCommandLine2(argv):
   options = AiUniverseGetOptions()
   
   if not options:
      return False
   
   if len(argv) < 2:
      return False

   parser = CommandLineParser(argv[1:])

   while not parser.Finished():
      param = parser.CurrentParameter()
      arguments = parser.CurrentArguments()
      
      if param == '-i':
         parser.CheckArgument(1)
      if param == '-o':
         parser.CheckArgument(1)
      elif param == '-of':
         parser.CheckArgument(1)
         format = arguments[0]
         GC.driverType = AiFindDriverType(format)

         if not GC.driverType:
            Error("Output file format not recognized")
      elif param == '-c':
         parser.CheckArgument(1)
         cam = AiNodeLookUpByName(arguments[0])
         if cam:
            AiNodeSetPtr(options, "camera", cam)
         else:
            Error("Camera %s does not exist", arguments[0])
      elif param == '-sh':
         parser.CheckArgument(2)
         GC.shutterStart = float(arguments[0])
         GC.shutterEnd = float(arguments[1])
      elif param == '-fov':
         parser.CheckArgument(1)
         GC.fov = float(arguments[0])
      elif param == '-e':
         parser.CheckArgument(1)
         GC.camera_exposure = float(arguments[0])
      elif param == '-r':
         parser.CheckArgument(2)
         AiNodeSetInt(options, "xres", int(arguments[0]))
         AiNodeSetInt(options, "yres", int(arguments[1]))
      elif param == '-rg':
         parser.CheckArgument(4)
         AiNodeSetInt(options, "region_min_x", int(arguments[0]))
         AiNodeSetInt(options, "region_min_y", int(arguments[1]))
         AiNodeSetInt(options, "region_max_x", int(arguments[2]))
         AiNodeSetInt(options, "region_max_y", int(arguments[3]))
      elif param == '-sr':
         parser.CheckArgument(1);
         s = float(arguments[0])
         # scale width and height
         AiNodeSetInt(options, "xres", int(float(AiNodeGetInt(options, "xres")) * s)); 
         AiNodeSetInt(options, "yres", int(float(AiNodeGetInt(options, "yres")) * s)); 
         # reset render region 
         AiNodeSetInt(options, "region_min_x", -1); 
         AiNodeSetInt(options, "region_min_y", -1); 
         AiNodeSetInt(options, "region_max_x", -1); 
         AiNodeSetInt(options, "region_max_y", -1); 
      elif param == '-t':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "threads", int(arguments[0]))
      elif param == '-tp' and platform.system().lower() == 'windows':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "thread_priority", int(arguments[0]))
      elif param == '-bs':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "bucket_size", int(arguments[0]))
      elif param == '-bc':
         parser.CheckArgument(1)
         pentry = AiNodeEntryLookUpParameter(AiNodeEntryLookUp("options"), "bucket_scanning")
         enum = AiParamGetEnum(pentry)
         scanType = AiEnumGetValue(enum, arguments[0])
         if scanType != -1:
            AiNodeSetInt(options, "bucket_scanning", scanType)
         else:
            Error('Bucket scanning not recognized')
      elif param == '-as':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "AA_samples", int(arguments[0]))
      elif param == '-af':
         parser.CheckArgument(2)
         if (arguments[0] == 'box' or
             arguments[0] == 'catrom2D' or
             arguments[0] == 'catrom' or
             arguments[0] == 'cone' or
             arguments[0] == 'cook' or
             arguments[0] == 'cubic' or
             arguments[0] == 'disk' or
             arguments[0] == 'gaussian' or
             arguments[0] == 'mitnet' or
             arguments[0] == 'sinc' or
             arguments[0] == 'triangle' or
             arguments[0] == 'video'):
            GC.filterTypeName = "%s_filter" % arguments[0]
            GC.filterWidth = float(arguments[1])
         else:
            Error('Anti-aliasing filter not recognized')
      elif param == '-asc':
         parser.CheckArgument(1)
         AiNodeSetFlt(options, "AA_sample_clamp", float(arguments[0]))
      elif param == '-ar':
         parser.CheckArgument(1)
         AiNodeSetFlt(options, "aspect_ratio", float(arguments[0]))
      elif param == '-g':
         parser.CheckArgument(1)
         GC.gamma = float(arguments[0])
      elif param == '-td':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_total_depth", int(arguments[0]))
      elif param == '-rfl':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_reflection_depth", int(arguments[0]))
      elif param == '-rfr':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_refraction_depth", int(arguments[0]))
      elif param == '-dif':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_diffuse_depth", int(arguments[0]))
      elif param == '-glo':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_glossy_depth", int(arguments[0]))
      elif param == '-ds':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_diffuse_samples", int(arguments[0]))
      elif param == '-gs':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "GI_glossy_samples", int(arguments[0]))
      elif param == '-f':
         GC.flatAll = True      
      elif param == '-tg':
         parser.CheckArgument(1)
         AiNodeSetFlt(options, "texture_gamma", float(arguments[0]))
      elif param == '-lg':
         parser.CheckArgument(1)
         AiNodeSetFlt(options, "light_gamma", float(arguments[0]))
      elif param == '-sg':
         parser.CheckArgument(1)
         AiNodeSetFlt(options, "shader_gamma", float(arguments[0]))
      elif param == '-d':
         parser.CheckArgument(1)
      elif param == '-it':
         AiNodeSetBool(options, "ignore_textures", True)
      elif param == '-is':
         AiNodeSetBool(options, "ignore_shaders", True)
      elif param == '-ib':
         AiNodeSetPtr(options, "background", POINTER(AtNode)())
      elif param == '-ia':
         AiNodeSetBool(options, "ignore_atmosphere", True)
      elif param == '-il':
         AiNodeSetBool(options, "ignore_lights", True)
      elif param == '-id':
         AiNodeSetBool(options, "ignore_shadows", True)
      elif param == '-isd':
         AiNodeSetBool(options, "ignore_subdivision", True)
      elif param == '-idisp':
         AiNodeSetBool(options, "ignore_displacement", True)
      elif param == '-ibump':
         AiNodeSetBool(options, "ignore_bump", True)
      elif param == '-imb':
         AiNodeSetBool(options, "ignore_motion_blur", True)
      elif param == '-idof':
         AiNodeSetBool(options, "ignore_dof", True)
      elif param == '-isss':
         AiNodeSetBool(options, "ignore_sss", True)
      elif param == '-flat':
         AiNodeSetBool(options, "ignore_smoothing", True)
      elif param == '-idirect':
         AiNodeSetBool(options, "ignore_direct_lighting", True)      
      elif param == '-sd':
         parser.CheckArgument(1)
         AiNodeSetInt(options, "max_subdivisions", int(arguments[0]))
      elif param == '-l':
         parser.CheckArgument(1)
      elif param == '-repeat':
         parser.CheckArgument(1)
      elif param == '-turn':
         parser.CheckArgument(1)
      elif param == '-resave':
         parser.CheckArgument(1)
      elif param == '-forceexpand':
         GC.openProcedurals = True
         AiNodeSetBool(options, "procedural_force_expand", True)
      elif param == '-nstdin':
         pass
      elif param == '-set':
         parser.CheckArgument(len(arguments))
      elif param == '-cm':
         parser.CheckArgument(1)
      elif param == '-sm':
         parser.CheckArgument(1)
      elif param == '-om':
         parser.CheckArgument(1)
      elif param == '-tree':
         parser.CheckArgument(1)
         error = PrintShadingTree(arguments[0])
         sys.exit(K_SUCCESS) 
      elif param == '-dw':
         pass
      elif param == '-dp':
         pass
      elif param == '-db':
         pass
      elif param == '-v':
         if len(arguments) == 0:
            GC.verbosity = 1
         else:
            GC.verbosity = int(arguments[0])
            parser.current += 1
      elif param == '-nw':
         parser.CheckArgument(1)
      elif param == '-log':
         pass
      elif param == '-logfile':
         pass
      elif param == '-sl':
         AiNodeSetBool(options, "skip_license_check", True)
      else:
         ext = os.path.splitext(param)[1]
         if ext == '.ass' or ext == '.gz':
            pass
         elif (GC.outputFileName == ''):
            GC.outputFileName = param
         else:
            Error('Command line parameter "%s" not recognized' % param)

      parser.current += 1          
      
   return True
