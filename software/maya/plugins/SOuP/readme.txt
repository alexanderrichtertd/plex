SOuP (plug-ins for Maya) © 2011 Peter Shipkov
This software is provided with absolutely no warranty.
It can be used for commercial projects, but cannot be
modified or redistributed.

installation:
-------------
1. Copy SOuP.so(.mll/.bundle) file /usr/autodesk/maya20xx/bin/plugins/
or other location that Maya scans for plugins.
2. Copy soup_shelf.mel to /home/user/maya/20xx/prefs/shelves/
   or load it through the Maya GUI.
3. Copy all .xpm files to /home/user/maya/20xx/prefs/icons/
or another location that Maya scans for icons.
4. Copy viewTemplates directory to /home/user/maya/20xx/prefs/viewTemplates/.

Launch Maya and load the SOuP shelf. If the plugin is not
loaded already, the first time any button on the SOuP shelf
gets clicked will try to load it.

Node IDs:
------------------------------------
MUSCLE                    0x00115740
TENSIONMAP                0x00115741
GROUP                     0x00115742
BOUNDINGOBJECT            0x00115743
OBJGRPTOCOMPLIST          0x00115744
COMPLISTTOOBJGRP          0x00115745
PEAK                      0x00115746
STICKYCURVES              0x00115747
ARRAYTOMULTI              0x00115748
POINT                     0x00115749
ARRAYEXPRESSION           0x0011574A
DISPLAYCOMPONENTS         0x0011574B
BOUNDINGOBJECTMANIP       0x0011574C
TEXTURETOARRAY            0x0011574D
MULTIREMAPVALUE           0x0011574E
REMAPARRAY                0x0011574F
ATTRIBUTETRANSFER         0x00115750
MULTIATTRIBUTETRANSFER    0x00115751
POINTCLOUDFLUIDEMITTER    0x00115752
POINTCLOUDFIELD           0x00115753
POINTATTRIBUTETOARRAY     0x00115754
TIMEOFFSET                0x00115755
MULTITOARRAY              0x00115756
BOUND                     0x00115757
COMPUTEVELOCITY           0x00115758
MIRRORPLANE               0x00115759
FLUIDATTRIBUTETOARRAY     0x0011575A
ARRAYTOPOINTCOLOR         0x0011575B
POINTCLOUDTOCURVE         0x0011575C
TRAJECTORY                0x0011575D
VERTEXCONSTRAINT          0x0011575E
ARRAYTOARRAY              0x0011575F
DISPLAYATTRIBUTES         0x00115760
ARRAYDATACONTAINER        0x00115761
SCATTER                   0x00115762
SHATTER                   0x00115763
ARRAYTODYNARRAYS          0x00115764
RGBATOCOLORANDALPHA       0x00115765
UPRESFLUID                0x00115766
PFXTOARRAY                0x00115767
PROJECTIONPLANE           0x00115768
RAYPROJECT                0x00115769
RETARGET                  0x0011576A
POINTSONMESHINFO          0x0011576B
CAGE                      0x0011576C
VORONOITEXTURE            0x0011576D
ARRAYTOTEXTURE            0x0011576E
DISPLAYDRIVER             0x0011576F
SMOOTH                    0x00115770
PYEXPRESSION              0x00115771
MAPTOMESH                 0x00115772
MESHTOMAP                 0x00115773
POINTCLOUDTOMULTICURVE    0x00115774
ARRAYBLEND                0x00115775
COMPONENTTOCOMPONENT      0x00115776
SPLITRGBA                 0x00115777
FRAMECACHER               0x00115778
CREATEARRAY               0x00115779
POINTCLOUDPARTICLEEMITTER 0x00115780
BMESH                     0x0011578A
SHELL                     0x0011578B
RESIZEARRAY               0x0011578C
TENSIONMAPSIMPLE          0x0011578D
POINTCLOUDTOMESH          0x0011578E
TRANSFORMSTOARRAYS        0x0011578F
COCOON                    0x00115790
TENSIONBLENDSHAPE         0x0011579A
UVTENSION                 0x0011579B
FRAMECACHETRACKER         0x0011579C
CONVEXHULL                0x0011579D
MORPHASSEMBLY             0x0011579E
MORPH                     0x0011579F
COPIER                    0x001157A0
MESH2ARRAYS               0x001157A1
COMBINEARRAYS             0x001158A2
BLURPOINTATTRIBUTE        0x001158A3
VOXELGRID                 0x001158A4
EXTRACTOR                 0x001158A5
COLORANDALPHATORGBA       0x001158A6
RAYPROJECTXFORM           0x001158A7
UVSTOPOINTSONMESH         0x001158A8
MERGEARRAYS               0x001158A9
AUDIOTOARRAY              0x001158AA
TETRAHEDRALIZE            0x001158AB
ATTRFRAMECACHER           0x001158AC
SMOOTHSIMPLE              0x001158AD
GPUCACHER                 0x001158AE
MNGGPUCACHER              0x001158AF
CAPE                      0x001158B0
SPEEDOMETER               0x001158B1
CURVESTOPOINTCLOUD        0x001158B2
BLENDCURVES               0x001158B3
