//Maya ASCII 2016ff07 scene
//Name: Proxy.ma
//Last modified: Fri, Dec 04, 2015 06:37:55 PM
//Codeset: 1252
requires maya "2016ff07";
requires -nodeType "RedshiftProxyMesh" "redshift4maya" "1.2.82";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2016";
fileInfo "version" "2016";
fileInfo "cutIdentifier" "201510022200-973226-1";
fileInfo "osv" "Microsoft Windows 7 Home Premium Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "redshiftProxyPlaceholder1";
	rename -uid "9756F160-477F-8D38-8FAB-C5A0CE35A79E";
createNode mesh -n "redshiftProxyPlaceholderShape1" -p "redshiftProxyPlaceholder1";
	rename -uid "9F8543F6-4E3E-C426-DC33-7C97C947D48B";
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
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transformGeometry -n "transformGeometry1";
	rename -uid "681EE832-45F6-DC9A-6D7E-83A66E3E5CD6";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.9073486328125e-006 0 0 1;
createNode RedshiftProxyMesh -n "redshiftProxy1";
	rename -uid "DF2F8682-42D5-5E9D-0383-81BD50D2FC09";
	setAttr ".fn" -type "string" "G:/_3D Projects//stool.rs";
	setAttr ".dm" 1;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
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
	setAttr ".ro" yes;
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
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "redshift";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "transformGeometry1.og" "redshiftProxyPlaceholderShape1.i";
connectAttr "redshiftProxy1.o" "transformGeometry1.ig";
connectAttr "redshiftProxyPlaceholderShape1.iog" ":initialShadingGroup.dsm" -na;
// End of Proxy.ma
