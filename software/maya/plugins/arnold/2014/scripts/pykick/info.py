
from arnold import *
from common import *

# sort --> 0: name, 1: type
def PrintRangeOfNodes(first, sort):
   nodes = []
   i = 0
   it = AiUniverseGetNodeEntryIterator(AI_NODE_ALL)
   # skip first node entries to start on the specified one
   while not AiNodeEntryIteratorFinished(it) and i < first:
      AiNodeEntryIteratorGetNext(it)
      i += 1

   while not AiNodeEntryIteratorFinished(it):
      nentry   = AiNodeEntryIteratorGetNext(it)
      nodename = AiNodeEntryGetName(nentry)
      typename = AiNodeEntryGetTypeName(nentry)
      nodes.append([nodename, typename])
   AiNodeEntryIteratorDestroy(it)

   if len(nodes) == 0:
      print("none")
   else:
      if sort == 0:      
         nodes.sort(lambda x, y: -1 if x[0] < y[0] else 1)
      else:
         nodes.sort(lambda x, y: -1 if x[1] < y[1] else 1)
      for n in nodes:
         if n[0] != 'list_aggregate':
            print("%-32s %s" % (n[0], n[1]))
      print("")
   return len(nodes)

def PrintNodes(sort):
   AiBegin()
   SetLogOptions(False)
   
   ApplyAttributes()

   print("built-in nodes sorted by %s:" % ("name" if sort == 0 else "type"))

   nnodes = PrintRangeOfNodes(0, sort)

   SetupPluginSearchPath()
   
   for path in GC.libPaths:
      print("loading plugins from %s" % path)
      AiLoadPlugins(path)

      nnodes += PrintRangeOfNodes(nnodes, sort)

   AiEnd()

def GetParamValueAsString(pentry, val, type):
   if type == AI_TYPE_BYTE:
      return str(val.contents.BYTE)   
   elif type == AI_TYPE_INT:
      return str(val.contents.INT)   
   elif type == AI_TYPE_UINT:
      return str(val.contents.UINT)   
   elif type == AI_TYPE_BOOLEAN:
      return "true" if (val.contents.BOOL != 0) else "false"   
   elif type == AI_TYPE_FLOAT:
      return "%g" % val.contents.FLT
   elif type == AI_TYPE_VECTOR or type == AI_TYPE_POINT:
      return "%g, %g, %g" % (val.contents.PNT.x, val.contents.PNT.y, val.contents.PNT.z)
   elif type == AI_TYPE_POINT2:
      return "%g, %g" % (val.contents.PNT.x, val.contents.PNT.y)
   elif type == AI_TYPE_RGB:
      return "%g, %g, %g" % (val.contents.RGB.r, val.contents.RGB.g, val.contents.RGB.b)
   elif type == AI_TYPE_RGBA:
      return "%g, %g, %g, %g" % (val.contents.RGBA.r, val.contents.RGBA.g, val.contents.RGBA.b, val.contents.RGBA.a)
   elif type == AI_TYPE_STRING:
      return val.contents.STR
   elif type == AI_TYPE_POINTER:
      return "%p" % val.contents.PTR
   elif type == AI_TYPE_NODE:
      name = AiNodeGetName(val.contents.PTR)
      return str(name)
   elif type == AI_TYPE_ENUM:
      enum = AiParamGetEnum(pentry)
      return AiEnumGetString(enum, val.contents.INT)
   elif type == AI_TYPE_MATRIX:
      return ""
   elif type == AI_TYPE_ARRAY:
      array = val.contents.ARRAY.contents
      nelems = array.nelements
      if nelems == 0:
         return "(empty)"
      elif nelems == 1:
         if array.type == AI_TYPE_FLOAT:
            return "%g" % AiArrayGetFlt(array, 0)
         elif array.type == AI_TYPE_VECTOR:
            vec = AiArrayGetVec(array, 0)
            return "%g, %g, %g" % (vec.x, vec.y, vec.z)
         elif array.type == AI_TYPE_POINT:
            pnt = AiArrayGetPnt(array, 0)
            return "%g, %g, %g" % (pnt.x, pnt.y, pnt.z)
         elif array.type == AI_TYPE_RGB:
            rgb = AiArrayGetRGB(array, 0)
            return "%g, %g, %g" % (rgb.r, rgb.g, rgb.b)
         elif array.type == AI_TYPE_RGBA:
            rgba = AiArrayGetRGBA(array, 0)
            return "%g, %g, %g" % (rgba.r, rgba.g, rgba.b, rgba.a)
         elif array.type == AI_TYPE_POINTER:
            ptr = cast(AiArrayGetPtr(array, 0), POINTER(AtNode))
            return "%p" % ptr
         elif array.type == AI_TYPE_NODE:
            ptr = cast(AiArrayGetPtr(array, 0), POINTER(AtNode))
            name = AiNodeGetName(ptr)
            return str(name)
         else:
            return ""
      else:
         return "(%u elements)" % nelems  
   else:
      return ""

def PrintParamInfo(node, param):
   node_entry = AiNodeEntryLookUp(node)
   if not node_entry:
      Error('Nothing known about node "%s"' % node)
      
   pentry = AiNodeEntryLookUpParameter(node_entry, param)
   if not pentry:
      Error('Nothing known about parameter "%s" in node "%s"' % (param, node))

   param_type = AiParamGetType(pentry)
   param_value = AiParamGetDefault(pentry)
   
   if param_type == AI_TYPE_ARRAY:
      array = param_value.contents.ARRAY.contents
      type_string = "%s[]" % AiParamGetTypeName(array.type)
   else:
      type_string = AiParamGetTypeName(param_type)

   default = GetParamValueAsString(pentry, param_value, param_type)

   print("node:", node)
   print("param:", param)
   print("type:", type_string)
   print("default:", default)

   if param_type == AI_TYPE_ENUM:
      enum = AiParamGetEnum(pentry)
      values = []
      index = 0
      while True:
         value = AiEnumGetString(enum, index)
         index += 1
         if not value:
            break   
         values.append(value)

      print("enum values: " + " ".join(values))

def PrintNodeInfo(node, sort):
   AiBegin()
   SetLogOptions(False)
   SetupPluginSearchPath()
   
   ApplyAttributes()

   for path in GC.libPaths:
      AiLoadPlugins(path)

   n, sep, p = node.partition('.')
   
   if p != '':
      PrintParamInfo(n, p)
      AiEnd()
      return

   node_entry = AiNodeEntryLookUp(node)
   if not node_entry:
      AiEnd()
      Error('Nothing to know about node "%s"' % node)

   num_params = AiNodeEntryGetNumParams(node_entry)
   
   print("node:         %s" % node)
   print("type:         %s" % AiNodeEntryGetTypeName(node_entry))
   print("output:       %s" % AiParamGetTypeName(AiNodeEntryGetOutputType(node_entry)) )
   print("parameters:   %d" % num_params)
   filename = AiNodeEntryGetFilename(node_entry)
   print("filename:     %s" % (filename if filename != '' else "<built-in>"))
   print("version:      %s" % AiNodeEntryGetVersion(node_entry))
   print("")
   
   params = []
   for p in range(num_params):
      pentry = AiNodeEntryGetParameter(node_entry, p)
      params.append([AiParamGetName(pentry), p])

   if sort == 1:
      params.sort(lambda x, y: -1 if x[0] < y[0] else 1)

   for pp in params:
      pentry = AiNodeEntryGetParameter(node_entry, pp[1])
      param_type  = AiParamGetType(pentry)
      param_value = AiParamGetDefault(pentry)
      param_name  = AiParamGetName(pentry)

      if param_type == AI_TYPE_ARRAY:
         # We want to know the type of the elements in the array
         array = param_value.contents.ARRAY.contents
         type_string = "%s[]" % AiParamGetTypeName(array.type)
      else:
         type_string = AiParamGetTypeName(param_type)

      # Print it like: <type> <name> <default>
      default = GetParamValueAsString(pentry, param_value, param_type)
      print("%-12s  %-32s  %-12s" % (type_string, param_name, default))

   AiEnd()

def PrintNodeSubTree(node):
   print("TO BE IMPLEMENTED...")
   
def PrintShadingTree(node_name):
   node = AiNodeLookUpByName(node_name)
   if not node:
      Error('Nothing known about node "%s"' % node_name)
   PrintNodeSubTree(node) 

def PrintLicenseInfo():
   licenses = POINTER(AtLicenseInfo)()
   nlicenses = c_uint(0)
   diagnose_result = AiLicenseGetInfo(licenses, nlicenses)
   if diagnose_result == AI_LIC_ERROR_NOTAVAILABLE:
      print("All licenses in use")
   elif diagnose_result == AI_LIC_SUCCESS:
      n_arnold = 0;
      n_used = 0;
      for i in range(nlicenses.value):
         if licenses[i].name == "arnold":
            n_arnold += 1
         if not licenses[i].used:
            continue
         n_used += 1

         nodelocked = not licenses[i].count
         local      = not licenses[i].current_inuse    and \
                      not licenses[i].current_resuse   and \
                      not licenses[i].min_remove       and \
                      not licenses[i].nres             and \
                      not licenses[i].num_roam_allowed and \
                      not licenses[i].timeout
         str_type = "node-locked" if nodelocked else "floating"
         if nodelocked and not local:
            str_type += " (in server)"

         print("")
         print("type:              %s" % str_type)
         print("product:           %s" % licenses[i].name)
         print("version:           %s" % licenses[i].ver)
         print("expires:           %s" % licenses[i].exp)
         if not nodelocked:
            print("total licenses:    %d" % licenses[i].count)
            print("inuse:             %d" % licenses[i].current_inuse)
            if licenses[i].timeout:
               print("timeout:           %d" % licenses[i].timeout)
               print("minimum timeout:   %d" % licenses[i].min_timeout)
            else:
               print("timeout:           disabled")
      if not n_arnold:
         print("Could not find any license for arnold, the license may be expired")
      elif not n_used:
         if nlicenses.value == 1:
            data = (licenses[0].count, licenses[0].count > 1 and "s" or "", licenses[0].name, licenses[0].ver)
            print("Wrong license product/version. Found %d license%s for %s %s" % data)
         else:
            print("Wrong license product/version. Found licenses for:")
            for i in range(nlicenses.value):
               data = (licenses[i].name, licenses[i].ver, licenses[i].count, licenses[i].count > 1 and "s" or "")
               print("  %s %s (%d license%s)" % data)
      if not n_arnold or not n_used:
         print("Please contact licensing@solidangle.com")
   elif diagnose_result == AI_LIC_ERROR_CANTCONNECT:
      print("Could not connect to any license server")
   elif diagnose_result == AI_LIC_ERROR_INIT:
      print("Error initializing license system")
   elif diagnose_result == AI_LIC_ERROR_NOTFOUND:
      print("Could not find any license files, please check the license server, the license may be expired")
      print("Please contact licensing@solidangle.com")
   else:
      print("Unknown error")

   print("")
   print("environment:")
   print("")

   print("solidangle_LICENSE           = %s" % os.environ.get('solidangle_LICENSE', failobj='(null)'))
   print("RLM_LICENSE                  = %s" % os.environ.get('RLM_LICENSE', failobj='(null)'))
   print("ARNOLD_LICENSE_ATTEMPTS      = %s" % os.environ.get('ARNOLD_LICENSE_ATTEMPTS', failobj='(null)'))
   print("ARNOLD_LICENSE_ATTEMPT_DELAY = %s" % os.environ.get('ARNOLD_LICENSE_ATTEMPT_DELAY', failobj='(null)'))

   AiFree(licenses)

   return diagnose_result

