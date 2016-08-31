# Example for how to override hiero versioning

import os.path
import glob
import re

from hiero.core import *
import hiero.core.VersionScanner


# We want to redefine some of the methods of VersionScanner, but may still need to use the default functionality within our custom methods.
# Therefore, we need to save a reference to the default methods, and then we will be able to call them from ours.
if not hasattr(VersionScanner.VersionScanner, "default_filterVersionSameFormat"):
  VersionScanner.VersionScanner.default_filterVersion = VersionScanner.VersionScanner.filterVersion
if not hasattr(VersionScanner.VersionScanner, "default_versionLessThan"):
  VersionScanner.VersionScanner.default_versionLessThan = VersionScanner.VersionScanner.versionLessThan
if not hasattr(VersionScanner.VersionScanner, "default_findNewVersions"):
  VersionScanner.VersionScanner.default_findNewVersions = VersionScanner.VersionScanner.findNewVersions

print "HIVE versioning v0.2"

# Determine whether the file newVersionFile should be included as a new version of originalVersion
# This filtering method only allows to add versions that have the same file format as the active one.
def filterVersionSameFormat(self, binItem, newVersionFile):
  activeVersion = binItem.activeItem()
  if binItem.activeItem() and binItem.activeItem().mediaSource():
    # Obtain active item's filename
    activeVersionFile = binItem.activeItem().mediaSource().firstpath()
    # Obtain extensions:
    ext1 = os.path.splitext(activeVersionFile)[1]
    ext2 = os.path.splitext(newVersionFile)[1]  
    return ext1 == ext2
  return False

# Compare method for sorting.
# Sort according to file formats first, then default to Hiero's original sorting (which uses version indices as first criterion).
def versionLessThanOrderByFormat(self, filename1, filename2):
  # Obtain extensions:  
  ext1 = os.path.splitext(filename1)[1]
  ext2 = os.path.splitext(filename2)[1]
  
  # If extensions are different, then sort according to extension:
  if ext1 != ext2:
    return ext1 < ext2
  
  # If extensions are equal, then default to Hiero's original sorting.
  # NB: For this to work, ensure that the original method has been saved with a different name as shown above!
  return self.default_versionLessThan(filename1, filename2)


# Scan for additional versions that belong to the specified version
# We are having a simple system that looks for new versions in a naming convention where artists add their name
# to the version, e.g: "/files/clip_v1.Mike.mov", "/files/clip_v2.Andrew.0000.dpx"
def findNewVersionsWithArtistName(self, version):
  if not(version.item() and version.item().mediaSource()):
    return
  
  activeVersionFilename = version.item().mediaSource().firstpath()
  print "activeVersionFilename", activeVersionFilename

  # We use the glob function to find files that look similar to ours.
  # We start with the active version file, and substitute relevant bits with * or ? wildcards.
  globExpression = activeVersionFilename
  print "globExpression", globExpression

  # Substitute version index with * wildcard.
  # This will also allow for artist names to appear right after the version index
  versionRegex = "v\\d+_[a-zA-Z]*" # e.g.: "v1", "v002Alex", "v100Bella", "v3Clark42", "v4a"
  globExpression = re.sub(versionRegex, "v*", globExpression)
  print "globExpression", globExpression

  # Substitute extension with * wildcard.
  # This will also allow for frame numbers to be present before the extension if they were not before
  globExpression = os.path.splitext(globExpression)[0] + ".*"
  print "globExpression", globExpression

  # Substitute frame number with * wildcard
  # Need to match files with different frame numbers.
  # This will also allow for frame numbers not to be present before the extension when they were before
  frameNumberRegex = "(\\.|_)\\d+\\." # e.g.: ".000.", "_001.", ".1000."
  globExpression = re.sub(frameNumberRegex, ".*.", globExpression)
  print "globExpression", globExpression
  
  # Use glob to find files that match globExpression.
  # We store found files in 'files', and we use 'visitedSequences' to avoid adding more than one frame of the same sequence. 
  files = set()
  visitedSequences = set()
  for foundFile in glob.iglob(globExpression):
    # Fix path separators if on Windows!
    foundFile = re.sub("\\\\", "/", foundFile)
    # Now we need to make sure that we only add one frame from each sequence:
    trimmedFileName = re.sub(frameNumberRegex, "", foundFile)
    if not trimmedFileName in visitedSequences:
      visitedSequences.add(trimmedFileName)
      # Finally add the new found file!
      files.add(foundFile)

  print files
  return files


# Override the default VersionScanner functions with the custom ones.
#VersionScanner.VersionScanner.filterVersion = filterVersionSameFormat
#VersionScanner.VersionScanner.versionLessThan = versionLessThanOrderByFormat
VersionScanner.VersionScanner.findNewVersions = findNewVersionsWithArtistName

