#==========
#
# Copyright (c) 2012, Chad Dombrova.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of Dan Bethell nor the names of any
#       other contributors to this software may be used to endorse or
#       promote products derived from this software without specific prior
#       written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#==========
#
# Variables defined by this module:
#   ARNOLD_FOUND       (all caps)   
#   Arnold_INCLUDE_DIR
#   Arnold_COMPILE_FLAGS
#   Arnold_LINK_FLAGS
#   Arnold_ai_LIBRARY
#   Arnold_LIBRARY_DIR
#
# Usage: 
#   FIND_PACKAGE( Arnold )
#   FIND_PACKAGE( Arnold REQUIRED )
#
# Note:
# You can tell the module where Nuke is installed by setting
# the Arnold_INSTALL_PATH (or setting the ARNOLD_HOME environment
# variable) before calling FIND_PACKAGE.
# 
# E.g. 
#   SET( Arnold_INSTALL_PATH "/usr/local/arnold-4.0.5.0" )
#   FIND_PACKAGE( Arnold REQUIRED )
#
#==========

# our includes
FIND_PATH( Arnold_INCLUDE_DIR ai.h
  $ENV{ARNOLD_HOME}/include
  ${Arnold_INSTALL_PATH}/include
  )

# our library
FIND_LIBRARY( Arnold_ai_LIBRARY ai
  $ENV{ARNOLD_HOME}/bin
  ${Arnold_INSTALL_PATH}/bin
  )

SET( Arnold_COMPILE_FLAGS "" )
SET( Arnold_LINK_FLAGS "" )

# our library path
GET_FILENAME_COMPONENT( Arnold_LIBRARY_DIR ${Arnold_ai_LIBRARY} PATH )

MESSAGE( STATUS ${Arnold_ai_LIBRARY})
MESSAGE( STATUS ${Arnold_LIBRARY_DIR})

# did we find everything?
INCLUDE( FindPackageHandleStandardArgs )
FIND_PACKAGE_HANDLE_STANDARD_ARGS( Arnold DEFAULT_MSG
  Arnold_INCLUDE_DIR
  Arnold_ai_LIBRARY
  Arnold_LIBRARY_DIR
  )

