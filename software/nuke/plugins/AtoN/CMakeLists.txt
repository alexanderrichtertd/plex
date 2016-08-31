#==========
#
# Copyright (c) 2015, Dan Bethell, Johannes Saam, Vahan Sosoyan.
# All rights reserved.
#
# For license information regarding redistribution and
# use, please refer to the COPYING file.
#
#==========

cmake_minimum_required( VERSION 2.6 )
project( renderconnect )

#=====
# General
set( CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/config/cmake )
find_package( Boost 1.54.0 COMPONENTS system REQUIRED )
find_package( Nuke REQUIRED )
find_package( Doxygen )

include_directories(
  ${CMAKE_SOURCE_DIR}/src
  ${Boost_INCLUDE_DIRS}
  ${Nuke_INCLUDE_DIR}
  )

#=====
# Build the Nuke plugin
add_library( nuke_plugin 
  SHARED
  ${CMAKE_SOURCE_DIR}/src/Aton.cpp 
  ${CMAKE_SOURCE_DIR}/src/Server.cpp
  ${CMAKE_SOURCE_DIR}/src/Client.cpp
  ${CMAKE_SOURCE_DIR}/src/Data.cpp
  )

set_target_properties( nuke_plugin
  PROPERTIES
  PREFIX ""
  OUTPUT_NAME "aton"
  COMPILE_FLAGS "-DUSE_GLEW ${Nuke_COMPILE_FLAGS}"
  LINK_FLAGS "${Nuke_LINK_FLAGS}"
  )

target_link_libraries( nuke_plugin 
  ${Boost_LIBRARIES}
  ${Nuke_LIBRARIES}
  )

#=====
# Build the Arnold plugin
find_package( Arnold )

if( ARNOLD_FOUND )
    include_directories( ${Arnold_INCLUDE_DIR} )
    add_library( arnold_plugin
      SHARED
      ${CMAKE_SOURCE_DIR}/src/Driver_Aton.cpp
      ${CMAKE_SOURCE_DIR}/src/Client.cpp
      ${CMAKE_SOURCE_DIR}/src/Data.cpp
      )

    set_target_properties( arnold_plugin
      PROPERTIES
      PREFIX ""
      OUTPUT_NAME "driver_aton"
      COMPILE_FLAGS "${Arnold_COMPILE_FLAGS}"
    )

    target_link_libraries( arnold_plugin
      ${Boost_LIBRARIES}
      ${Arnold_ai_LIBRARY}
      )
endif( ARNOLD_FOUND )

#=====
# Build docs (after the nuke plugin is built)
IF( DOXYGEN_FOUND )
    ADD_CUSTOM_COMMAND( TARGET nuke_plugin
        POST_BUILD
        COMMAND ${DOXYGEN_EXECUTABLE} 
        ${CMAKE_SOURCE_DIR}/"config/docs/doxygen.cfg" 
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )
ENDIF( DOXYGEN_FOUND )
