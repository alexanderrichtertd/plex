//Maya ASCII 2015 scene
//Name: logo.ma
//Last modified: Sat, Jun 20, 2015 05:33:21 PM
//Codeset: 1252
requires maya "2015";
requires -dataType "byteArray" "Mayatomr" "2015.0 - 3.12.1.18 ";
requires -nodeType "VRayMtl" "vrayformaya" "3.05.03";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201410051530-933320";
fileInfo "osv" "Microsoft Windows 7 Home Premium Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "geo_grp";
	setAttr ".t" -type "double3" 0 0 0.050419364459210136 ;
	setAttr ".s" -type "double3" 0.88358969684426003 0.88358969684426003 0.88358969684426003 ;
	setAttr ".rp" -type "double3" 0 0 6.1311351609878719e-018 ;
	setAttr ".sp" -type "double3" 0 0 6.9388939039072284e-018 ;
	setAttr ".spt" -type "double3" 0 0 -8.0775874291935627e-019 ;
createNode transform -n "VRay_Logo" -p "geo_grp";
	setAttr ".rp" -type "double3" 9.1597046852111816 11.030832290649414 -2.3856381177902222 ;
	setAttr ".sp" -type "double3" 9.1597046852111816 11.030832290649414 -2.3856381177902222 ;
createNode mesh -n "VRay_LogoShape" -p "VRay_Logo";
	addAttr -ci true -sn "rsObjectId" -ln "rsObjectId" -min 0 -max 2147483647 -smn 
		0 -smx 100 -at "long";
	addAttr -ci true -sn "rsEnableVisibilityOverrides" -ln "rsEnableVisibilityOverrides" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsPrimaryRayVisible" -ln "rsPrimaryRayVisible" -dv 
		1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsSecondaryRayVisible" -ln "rsSecondaryRayVisible" 
		-dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsShadowCaster" -ln "rsShadowCaster" -dv 1 -min 0 
		-max 1 -at "bool";
	addAttr -ci true -k true -sn "rsShadowReceiver" -ln "rsShadowReceiver" -dv 1 -min 
		0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsReflectionCaster" -ln "rsReflectionCaster" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsReflectionVisible" -ln "rsReflectionVisible" -dv 
		1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsRefractionCaster" -ln "rsRefractionCaster" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsRefractionVisible" -ln "rsRefractionVisible" -dv 
		1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsGiCaster" -ln "rsGiCaster" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsGiVisible" -ln "rsGiVisible" -dv 1 -min 0 -max 1 
		-at "bool";
	addAttr -ci true -k true -sn "rsCausticCaster" -ln "rsCausticCaster" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsCausticVisible" -ln "rsCausticVisible" -dv 1 -min 
		0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsFgCaster" -ln "rsFgCaster" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsFgVisible" -ln "rsFgVisible" -dv 1 -min 0 -max 1 
		-at "bool";
	addAttr -ci true -k true -sn "rsSelfShadows" -ln "rsSelfShadows" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsAOCaster" -ln "rsAOCaster" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsForceBruteForceGI" -ln "rsForceBruteForceGI" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "me" -ln "rsMatteEnable" -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "masr" -ln "rsMatteApplyToSecondaryRays" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "msb" -ln "rsMatteShowBackground" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "mabml" -ln "rsMatteAffectedByMatteLights" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "ma" -ln "rsMatteAlpha" -dv 1 -min 0 -max 1 -smn 0 
		-smx 1 -at "double";
	addAttr -ci true -k true -sn "mrls" -ln "rsMatteReflectionScale" -min 0 -max 1 -smn 
		0 -smx 1 -at "double";
	addAttr -ci true -k true -sn "mrfs" -ln "rsMatteRefractionScale" -min 0 -max 1 -smn 
		0 -smx 1 -at "double";
	addAttr -ci true -k true -sn "mds" -ln "rsMatteDiffuseScale" -min 0 -max 1 -smn 
		0 -smx 1 -at "double";
	addAttr -ci true -k true -sn "mse" -ln "rsMatteShadowEnable" -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "msaa" -ln "rsMatteShadowAffectsAlpha" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "mst" -ln "rsMatteShadowTransparency" -min 0 -max 1 
		-smn 0 -smx 1 -at "double";
	addAttr -ci true -uac -sn "msc" -ln "rsMatteShadowColor" -at "float3" -nc 3;
	addAttr -ci true -sn "mscr" -ln "rsMatteShadowColorR" -min 0 -max 1 -at "float" 
		-p "rsMatteShadowColor";
	addAttr -ci true -sn "mscg" -ln "rsMatteShadowColorG" -min 0 -max 1 -at "float" 
		-p "rsMatteShadowColor";
	addAttr -ci true -sn "mscb" -ln "rsMatteShadowColorB" -min 0 -max 1 -at "float" 
		-p "rsMatteShadowColor";
	addAttr -ci true -sn "rsEnableSubdivision" -ln "rsEnableSubdivision" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsScreenSpaceAdaptive" -ln "rsScreenSpaceAdaptive" 
		-dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsDoSmoothSubdivision" -ln "rsDoSmoothSubdivision" 
		-dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsMinTessellationLength" -ln "rsMinTessellationLength" 
		-dv 4 -min 0 -max 3.4028234663852886e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -k true -sn "rsMaxTessellationSubdivs" -ln "rsMaxTessellationSubdivs" 
		-dv 6 -min 0 -max 16 -at "long";
	addAttr -ci true -k true -sn "rsOutOfFrustumTessellationFactor" -ln "rsOutOfFrustumTessellationFactor" 
		-dv 4 -min 0 -max 3.4028234663852886e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -sn "rsSubdivisionRule" -ln "rsSubdivisionRule" -min 0 -max 1 -en 
		"Catmull-Clark + Loop:Catmull-Clark Only" -at "enum";
	addAttr -ci true -sn "rsEnableDisplacement" -ln "rsEnableDisplacement" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsMaxDisplacement" -ln "rsMaxDisplacement" -dv 1 -min 
		0 -max 3.4028234663852886e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -k true -sn "rsDisplacementScale" -ln "rsDisplacementScale" -dv 
		1 -min 0 -max 3.4028234663852886e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -sn "rsAutoBumpMap" -ln "rsAutoBumpMap" -dv 1 -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 4 ".uvst[0].uvsp[0:3]" -type "float2" 0 0 1 0 0 1 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 4 ".pt[0:3]" -type "float3"  9.3269053 10.300688 -2.2357492 
		8.9925041 10.300688 -3.535527 9.3269053 11.760977 -1.2357494 8.9925041 11.760977 
		-2.535527;
	setAttr -s 4 ".vt[0:3]"  -0.5 -1.110223e-016 0.5 0.5 -1.110223e-016 0.5
		 -0.5 1.110223e-016 -0.5 0.5 1.110223e-016 -0.5;
	setAttr -s 4 ".ed[0:3]"  0 1 0 0 2 0 1 3 0 2 3 0;
	setAttr -ch 4 ".fc[0]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 3 2;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode materialInfo -n "materialInfo114";
createNode shadingEngine -n "vRay_LogoSG";
	addAttr -s false -ci true -sn "rsSurfaceShader" -ln "rsSurfaceShader" -at "message";
	addAttr -s false -ci true -sn "rsShadowShader" -ln "rsShadowShader" -at "message";
	addAttr -s false -ci true -sn "rsPhotonShader" -ln "rsPhotonShader" -at "message";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsBumpmapShader" -ln "rsBumpmapShader" -at "message";
	addAttr -s false -ci true -sn "rsDisplacementShader" -ln "rsDisplacementShader" 
		-at "message";
	addAttr -ci true -sn "rsMaterialId" -ln "rsMaterialId" -min 0 -max 2147483647 -smn 
		0 -smx 100 -at "long";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode VRayMtl -n "vRay_Logo_MAT";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".uf" yes;
	setAttr ".fde" yes;
	setAttr ".cth" 0.0010000000474974513;
	setAttr ".aal" -type "attributeAlias" {"color","diffuseColor"} ;
createNode file -n "vRay_Logo_File01";
	addAttr -ci true -k true -sn "rsFilterEnable" -ln "rsFilterEnable" -dv 2 -min 0 
		-max 2 -en "None:Magnification:Magnification/Minification" -at "enum";
	addAttr -ci true -sn "rsMipBias" -ln "rsMipBias" -min -31 -max 31 -at "double";
	addAttr -ci true -sn "rsBicubicFiltering" -ln "rsBicubicFiltering" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "rsPreferSharpFiltering" -ln "rsPreferSharpFiltering" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsAlphaMode" -ln "rsAlphaMode" -min 0 -max 2 -en "None:Coverage:Pre-Multiplied" 
		-at "enum";
	addAttr -ci true -sn "vrayFileGammaEnable" -ln "vrayFileGammaEnable" -dv 1 -at "long";
	addAttr -ci true -sn "vrayFileColorSpace" -ln "vrayFileColorSpace" -dv 1 -at "long";
	addAttr -ci true -sn "vrayFileGammaValue" -ln "vrayFileGammaValue" -dv 2.2000000476837158 
		-min 0.05000000074505806 -max 20 -smx 3 -at "float";
	addAttr -ci true -sn "resolution" -ln "resolution" -dv 32 -at "long";
	setAttr ".ftn" -type "string" "C:/Users/Admin/Documents/maya/2015-x64/Plug-Ins/SLiB/lib/scene/vRay_logo.png";
	setAttr ".resolution" 256;
createNode place2dTexture -n "vRay_Logo_p2d01";
	addAttr -ci true -sn "ruv" -ln "rsUvSet" -dt "string";
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 5 ".lnk";
	setAttr -s 5 ".slnk";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 0;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".st";
	setAttr -k on ".an";
	setAttr -k on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -s 4 ".u";
select -ne :defaultRenderingList1;
select -ne :lightList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".l";
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".tx";
select -ne :initialShadingGroup;
	addAttr -s false -ci true -sn "rsSurfaceShader" -ln "rsSurfaceShader" -at "message";
	addAttr -s false -ci true -sn "rsShadowShader" -ln "rsShadowShader" -at "message";
	addAttr -s false -ci true -sn "rsPhotonShader" -ln "rsPhotonShader" -at "message";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsBumpmapShader" -ln "rsBumpmapShader" -at "message";
	addAttr -s false -ci true -sn "rsDisplacementShader" -ln "rsDisplacementShader" 
		-at "message";
	addAttr -ci true -sn "rsMaterialId" -ln "rsMaterialId" -min 0 -max 2147483647 -smn 
		0 -smx 100 -at "long";
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
	setAttr ".micc" -type "float3" 1 1 -2.0000038 ;
select -ne :initialParticleSE;
	addAttr -s false -ci true -sn "rsSurfaceShader" -ln "rsSurfaceShader" -at "message";
	addAttr -s false -ci true -sn "rsShadowShader" -ln "rsShadowShader" -at "message";
	addAttr -s false -ci true -sn "rsPhotonShader" -ln "rsPhotonShader" -at "message";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsBumpmapShader" -ln "rsBumpmapShader" -at "message";
	addAttr -s false -ci true -sn "rsDisplacementShader" -ln "rsDisplacementShader" 
		-at "message";
	addAttr -ci true -sn "rsMaterialId" -ln "rsMaterialId" -min 0 -max 2147483647 -smn 
		0 -smx 100 -at "long";
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
	setAttr ".micc" -type "float3" 1 1 -2.0000038 ;
select -ne :defaultRenderGlobals;
	addAttr -ci true -sn "shave_old_preRenderMel" -ln "shave_old_preRenderMel" -dt "string";
	addAttr -ci true -sn "shave_old_postRenderMel" -ln "shave_old_postRenderMel" -dt "string";
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr" 25;
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr ".edl" no;
	setAttr ".ren" -type "string" "vray";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av ".outf" 32;
	setAttr -cb on ".imfkey";
	setAttr -k on ".gama";
	setAttr -k on ".an";
	setAttr -cb on ".ar";
	setAttr -k on ".fs";
	setAttr -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -cb on ".me";
	setAttr -cb on ".se";
	setAttr -k on ".be";
	setAttr -cb on ".ep";
	setAttr -k on ".fec";
	setAttr -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -cb on ".pff";
	setAttr -cb on ".peie";
	setAttr -cb on ".ifp";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -k on ".shs";
	setAttr -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -k on ".mm";
	setAttr -k on ".npu";
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".pram" -type "string" "shaveVrayPreRender;";
	setAttr -k on ".poam" -type "string" "shaveVrayPostRender;";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr ".prm" -type "string" "shave_MRFrameStart;";
	setAttr ".pom" -type "string" "shave_MRFrameEnd;";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -k on ".ope";
	setAttr -k on ".oppf";
	setAttr -cb on ".hbl";
	setAttr ".shave_old_preRenderMel" -type "string" "";
	setAttr ".shave_old_postRenderMel" -type "string" "";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av ".w" 512;
	setAttr -av ".h" 512;
	setAttr -av ".pa" 1;
	setAttr -av ".al";
	setAttr -av ".dar" 1;
	setAttr -av -k on ".ldar";
	setAttr -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -cb on ".isu";
	setAttr -cb on ".pdu";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -s 2 ".dsm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off ".eeaa";
	setAttr -k off ".engm";
	setAttr -k off ".mes";
	setAttr -k off ".emb";
	setAttr -av -k off ".mbbf";
	setAttr -k off ".mbs";
	setAttr -k off ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off ".twa";
	setAttr -k off ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr" 25;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".etmr" yes;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr -k on ".if";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -k on ".fir";
	setAttr -k on ".aap";
	setAttr -k on ".gh";
	setAttr -cb on ".sd";
connectAttr "vRay_LogoSG.msg" "materialInfo114.sg";
connectAttr "vRay_Logo_MAT.msg" "materialInfo114.m";
connectAttr "vRay_Logo_File01.msg" "materialInfo114.t" -na;
connectAttr "vRay_Logo_File01.oc" "materialInfo114.tc";
connectAttr "vRay_Logo_MAT.oc" "vRay_LogoSG.ss";
connectAttr "VRay_LogoShape.iog" "vRay_LogoSG.dsm" -na;
connectAttr "vRay_Logo_File01.oc" "vRay_Logo_MAT.dc";
connectAttr "vRay_Logo_File01.oa" "vRay_Logo_MAT.omr";
connectAttr "vRay_Logo_File01.oa" "vRay_Logo_MAT.omg";
connectAttr "vRay_Logo_File01.oa" "vRay_Logo_MAT.omb";
connectAttr "vRay_Logo_p2d01.c" "vRay_Logo_File01.c";
connectAttr "vRay_Logo_p2d01.tf" "vRay_Logo_File01.tf";
connectAttr "vRay_Logo_p2d01.rf" "vRay_Logo_File01.rf";
connectAttr "vRay_Logo_p2d01.mu" "vRay_Logo_File01.mu";
connectAttr "vRay_Logo_p2d01.mv" "vRay_Logo_File01.mv";
connectAttr "vRay_Logo_p2d01.s" "vRay_Logo_File01.s";
connectAttr "vRay_Logo_p2d01.wu" "vRay_Logo_File01.wu";
connectAttr "vRay_Logo_p2d01.wv" "vRay_Logo_File01.wv";
connectAttr "vRay_Logo_p2d01.re" "vRay_Logo_File01.re";
connectAttr "vRay_Logo_p2d01.of" "vRay_Logo_File01.of";
connectAttr "vRay_Logo_p2d01.r" "vRay_Logo_File01.ro";
connectAttr "vRay_Logo_p2d01.n" "vRay_Logo_File01.n";
connectAttr "vRay_Logo_p2d01.vt1" "vRay_Logo_File01.vt1";
connectAttr "vRay_Logo_p2d01.vt2" "vRay_Logo_File01.vt2";
connectAttr "vRay_Logo_p2d01.vt3" "vRay_Logo_File01.vt3";
connectAttr "vRay_Logo_p2d01.vc1" "vRay_Logo_File01.vc1";
connectAttr "vRay_Logo_p2d01.o" "vRay_Logo_File01.uv";
connectAttr "vRay_Logo_p2d01.ofs" "vRay_Logo_File01.fs";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "vRay_LogoSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "vRay_LogoSG.message" ":defaultLightSet.message";
connectAttr "vRay_LogoSG.pa" ":renderPartition.st" -na;
connectAttr "vRay_Logo_MAT.msg" ":defaultShaderList1.s" -na;
connectAttr "vRay_Logo_p2d01.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "vRay_Logo_File01.msg" ":defaultTextureList1.tx" -na;
dataStructure -fmt "raw" -as "name=externalContentTable:string=node:string=key:string=upath:uint32=upathcrc:string=rpath:string=roles";
applyMetadata -fmt "raw" -v "channel\nname externalContentTable\nstream\nname v1.0\nindexType numeric\nstructure externalContentTable\n0\n\"vRay_Logo_File01\" \"fileTextureName\" \"C:/Users/Admin/Documents/maya/2015-x64/Plug-Ins/SLiB/lib/scene/vRay_logo.png\" 272240854 \"C:/Users/Admin/Documents/maya/2015-x64/Plug-Ins/SLiB/lib/scene/vRay_logo.png\" \"sourceImages\"\nendStream\nendChannel\nendAssociations\n" 
		-scn;
// End of logo.ma
