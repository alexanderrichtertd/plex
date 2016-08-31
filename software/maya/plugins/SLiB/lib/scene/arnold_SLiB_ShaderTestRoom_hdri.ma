//Maya ASCII 2016ff07 scene
//Name: arnold_SLiB_ShaderTestRoom_hdri.ma
//Last modified: Sat, Oct 17, 2015 06:15:12 PM
//Codeset: 1252
requires maya "2016ff07";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" -nodeType "aiSkyDomeLight"
		 -nodeType "aiStandard" "mtoa" "1.2.4.2";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2016";
fileInfo "version" "2016";
fileInfo "cutIdentifier" "201508242200-969261-1";
fileInfo "osv" "Microsoft Windows 7 Home Premium Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -s -n "persp";
	rename -uid "5A75A58B-4421-47EC-D630-B8838BE858A8";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 73.731577596177303 64.179592946664371 5.7368334222359181 ;
	setAttr ".r" -type "double3" 324.92811838407482 2960.59999999403 -1.9473662581313041e-014 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "57C5A743-4CA5-1CE2-C97B-75B3AE2011BD";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+038 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+038 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+038 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ff" 2;
	setAttr ".ovr" 1.3;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 94.30477185083079;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0.70873284339904785 19.359516096163716 -0.66257447004318237 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".dr" yes;
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "9B70D396-4924-867F-AA87-38A8AE70711C";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28.91997759422128 100.1 3.3575154090064099 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "E8927553-4511-904E-9A62-75AEEC29D6A1";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+038 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+038 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+038 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 57.250856370442087;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "48EA7918-4E11-B988-0C90-22B048FA0912";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -0.0669164323455953 6.1187719738813513 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "C22939D3-4FDE-989B-2C89-23A166A769E4";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+038 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+038 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+038 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 13.596379089637697;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "DEBD58A6-4487-8B95-9C3F-A5B2B74BB1B1";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 108.49142641928825 0.14913436951257286 -0.64909659135049513 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3103ACB5-46AE-429A-DBC7-83A077D264D4";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+038 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+038 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+038 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 10.907404981489321;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "renderCam";
	rename -uid "D043248A-4FE7-44BC-319A-67854DE98066";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 24.328976119868212 4.374722863017789 10.319385891569119 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" 1.9999999999768008 65.599999999975239 0 ;
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 3.9239265030322395e-016 2.3543559018193426e-015 -6.2782824048515793e-015 ;
	setAttr ".rpt" -type "double3" -5.8695126635978058e-015 2.1767468608015922e-016 
		3.3628735699898563e-015 ;
	setAttr ".sp" -type "double3" 2.2204460492503131e-015 0 3.5527136788005009e-015 ;
	setAttr ".spt" -type "double3" -2.5848279773419382e-016 0 -4.1357247637471095e-016 ;
createNode camera -n "renderCamShape" -p "renderCam";
	rename -uid "FDDBCC64-4476-5C7E-D565-2993A1A5D234";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+038 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+038 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+038 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+038 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v";
	setAttr ".ff" 2;
	setAttr ".ovr" 1.3;
	setAttr ".fl" 40;
	setAttr ".fs" 5;
	setAttr ".fd" 21;
	setAttr ".coi" 31.535945374128723;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 -1.0347884297370911 -2.9802322387695313e-008 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".dr" yes;
	setAttr ".dof" yes;
	setAttr ".frs" 4;
	setAttr ".ai_translator" -type "string" "perspective";
	setAttr -cb on ".rsFisheyeScaleX" 2;
	setAttr -cb on ".rsFisheyeScaleY" 2;
	setAttr -cb on ".rsFisheyeAngle" 30;
createNode transform -n "imagePlane1" -p "renderCamShape";
	rename -uid "747516D6-45C3-9898-0F56-F3BD18AF79A4";
createNode imagePlane -n "imagePlaneShape1" -p "imagePlane1";
	rename -uid "058D20F7-4DA9-DBDD-E69C-B4805635B925";
	setAttr -k off ".v";
	setAttr ".fc" 102;
	setAttr ".imn" -type "string" "${SLiBLib}/scene/BG_grey.png";
	setAttr ".cov" -type "short2" 3000 1696 ;
	setAttr ".f" 4;
	setAttr ".s" -type "double2" 1.5 1.2 ;
	setAttr ".w" 30;
	setAttr ".h" 16.96;
	setAttr ".cs" -type "string" "sRGB";
createNode transform -n "geo_grp";
	rename -uid "546623C8-4DB5-8515-6BE9-6F94FD4A2378";
	setAttr ".t" -type "double3" 0 0 0.050419364459210136 ;
	setAttr ".s" -type "double3" 0.88358969684426003 0.88358969684426003 0.88358969684426003 ;
	setAttr ".rp" -type "double3" 0 0 6.1311351609878719e-018 ;
	setAttr ".sp" -type "double3" 0 0 6.9388939039072284e-018 ;
	setAttr ".spt" -type "double3" 0 0 -8.0775874291935627e-019 ;
createNode transform -n "shaderRoom" -p "geo_grp";
	rename -uid "A6AC18F3-470D-06F6-1205-55A35E20819A";
	setAttr ".rp" -type "double3" -24.040282410847471 -0.00034698222534846972 -0.0085447330443757796 ;
	setAttr ".sp" -type "double3" -24.040282410847471 -0.00034698222534846972 -0.0085447330443757796 ;
createNode mesh -n "shaderRoomShape" -p "shaderRoom";
	rename -uid "979976D8-46B5-A04F-5DFD-B0A8F3661D48";
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
		-dv 4 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -k true -sn "rsMaxTessellationSubdivs" -ln "rsMaxTessellationSubdivs" 
		-dv 6 -min 0 -max 16 -at "long";
	addAttr -ci true -k true -sn "rsOutOfFrustumTessellationFactor" -ln "rsOutOfFrustumTessellationFactor" 
		-dv 4 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -sn "rsSubdivisionRule" -ln "rsSubdivisionRule" -min 0 -max 1 -en 
		"Catmull-Clark + Loop:Catmull-Clark Only" -at "enum";
	addAttr -ci true -sn "rsEnableDisplacement" -ln "rsEnableDisplacement" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsMaxDisplacement" -ln "rsMaxDisplacement" -dv 1 -min 
		0 -max 3.4028234600000001e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -k true -sn "rsDisplacementScale" -ln "rsDisplacementScale" -dv 
		1 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -sn "rsAutoBumpMap" -ln "rsAutoBumpMap" -dv 1 -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".iog[0].og[0].gcl" -type "componentList" 1 "f[0]";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.50027751922607422 1.0005568857304752 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 4 ".uvst[0].uvsp[0:3]" -type "float2" -0.50027573 1.00055706501
		 -0.50027573 3.8137659e-006 -1.50082886 1.0005569458 -1.50082886 3.9329752e-006;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 4 ".pt[0:3]" -type "float3"  -80.089668 0.49965301 56.040844 
		32.009106 0.49965301 56.040844 -80.089668 0.49965301 -56.057934 32.009106 0.49965301 
		-56.057934;
	setAttr -s 4 ".vt[0:3]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 -0.5 -0.5
		 0.5 -0.5 -0.5;
	setAttr -s 4 ".ed[0:3]"  0 1 0 2 3 0 2 0 0 3 1 0;
	setAttr -ch 4 ".fc[0]" -type "polyFaces" 
		f 4 1 3 -1 -3
		mu 0 4 0 1 3 2;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".dr" 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "shaderBall" -p "geo_grp";
	rename -uid "4152AA99-4309-F378-19A3-91B3C59EA4C5";
	setAttr ".rp" -type "double3" 2.2329428379190017 6.1481727466168135 0.21340686513299614 ;
	setAttr ".sp" -type "double3" 2.2329428379190017 6.1481727466168135 0.21340686513299614 ;
createNode mesh -n "shaderBallShape" -p "shaderBall";
	rename -uid "9B9FE5F1-4CC0-1815-E5DB-208ADE001A9A";
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
		-dv 4 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -k true -sn "rsMaxTessellationSubdivs" -ln "rsMaxTessellationSubdivs" 
		-dv 6 -min 0 -max 16 -at "long";
	addAttr -ci true -k true -sn "rsOutOfFrustumTessellationFactor" -ln "rsOutOfFrustumTessellationFactor" 
		-dv 4 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -sn "rsSubdivisionRule" -ln "rsSubdivisionRule" -min 0 -max 1 -en 
		"Catmull-Clark + Loop:Catmull-Clark Only" -at "enum";
	addAttr -ci true -sn "rsEnableDisplacement" -ln "rsEnableDisplacement" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsMaxDisplacement" -ln "rsMaxDisplacement" -dv 1 -min 
		0 -max 3.4028234600000001e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -k true -sn "rsDisplacementScale" -ln "rsDisplacementScale" -dv 
		1 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -sn "rsAutoBumpMap" -ln "rsAutoBumpMap" -dv 1 -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 437 ".uvst[0].uvsp";
	setAttr ".uvst[0].uvsp[0:249]" -type "float2" 0.050000001 0.480717 0.1 0.47834301
		 0.1 0.50682902 0.050000001 0.50682902 0.1 0.53531402 0.050000001 0.53531402 0 0.53531402
		 0 0.50682902 0 0.47834301 0.15000001 0.480717 0.2 0.47834301 0.2 0.50682902 0.15000001
		 0.50682902 0.2 0.53531402 0.15000001 0.53531402 0.25 0.480717 0.30000001 0.47834301
		 0.30000001 0.50682902 0.25 0.50682902 0.30000001 0.53531402 0.25 0.53531402 0.34999999
		 0.480717 0.40000001 0.47834301 0.40000001 0.50682902 0.34999999 0.50682902 0.40000001
		 0.53531402 0.34999999 0.53531402 0.44999999 0.480717 0.5 0.47834301 0.5 0.50682902
		 0.44999999 0.50682902 0.5 0.53531402 0.44999999 0.53531402 0.55000001 0.480717 0.60000002
		 0.47834301 0.60000002 0.50682902 0.55000001 0.50682902 0.60000002 0.53531402 0.55000001
		 0.53531402 0.64999998 0.480717 0.69999999 0.47834301 0.69999999 0.50682902 0.64999998
		 0.50682902 0.69999999 0.53531402 0.64999998 0.53531402 0.75 0.480717 0.80000001 0.47834301
		 0.80000001 0.50682902 0.75 0.50682902 0.80000001 0.53531402 0.75 0.53531402 0.85000002
		 0.480717 0.89999998 0.47834301 0.89999998 0.50682902 0.85000002 0.50682902 0.89999998
		 0.53531402 0.85000002 0.53531402 0.94999999 0.480717 1 0.47834301 1 0.50682902 0.94999999
		 0.50682902 1 0.53531402 0.94999999 0.53531402 0.1 0.56379998 0.050000001 0.56379998
		 0.1 0.59228599 0.050000001 0.59228599 0 0.59228599 0 0.56379998 0.2 0.56379998 0.15000001
		 0.56379998 0.2 0.59228599 0.15000001 0.59228599 0.30000001 0.56379998 0.25 0.56379998
		 0.30000001 0.59228599 0.25 0.59228599 0.40000001 0.56379998 0.34999999 0.56379998
		 0.40000001 0.59228599 0.34999999 0.59228599 0.5 0.56379998 0.44999999 0.56379998
		 0.5 0.59228599 0.44999999 0.59228599 0.60000002 0.56379998 0.55000001 0.56379998
		 0.60000002 0.59228599 0.55000001 0.59228599 0.69999999 0.56379998 0.64999998 0.56379998
		 0.69999999 0.59228599 0.64999998 0.59228599 0.80000001 0.56379998 0.75 0.56379998
		 0.80000001 0.59228599 0.75 0.59228599 0.89999998 0.56379998 0.85000002 0.56379998
		 0.89999998 0.59228599 0.85000002 0.59228599 1 0.56379998 0.94999999 0.56379998 1
		 0.59228599 0.94999999 0.59228599 0.1 0.620772 0.050000001 0.620772 0.1 0.649257 0.050000001
		 0.649257 0 0.649257 0 0.620772 0.2 0.620772 0.15000001 0.620772 0.2 0.649257 0.15000001
		 0.649257 0.30000001 0.620772 0.25 0.620772 0.30000001 0.649257 0.25 0.649257 0.40000001
		 0.620772 0.34999999 0.620772 0.40000001 0.649257 0.34999999 0.649257 0.5 0.620772
		 0.44999999 0.620772 0.5 0.649257 0.44999999 0.649257 0.60000002 0.620772 0.55000001
		 0.620772 0.60000002 0.649257 0.55000001 0.649257 0.69999999 0.620772 0.64999998 0.620772
		 0.69999999 0.649257 0.64999998 0.649257 0.80000001 0.620772 0.75 0.620772 0.80000001
		 0.649257 0.75 0.649257 0.89999998 0.620772 0.85000002 0.620772 0.89999998 0.649257
		 0.85000002 0.649257 1 0.620772 0.94999999 0.620772 1 0.649257 0.94999999 0.649257
		 0.1 0.67774302 0.050000001 0.67774302 0.1 0.70622897 0.050000001 0.70622802 0 0.70622897
		 0 0.67774302 0.2 0.67774302 0.15000001 0.67774302 0.2 0.70622897 0.15000001 0.70622802
		 0.30000001 0.67774302 0.25 0.67774302 0.30000001 0.70622897 0.25 0.70622802 0.40000001
		 0.67774302 0.34999999 0.67774302 0.40000001 0.70622897 0.34999999 0.70622802 0.5
		 0.67774302 0.44999999 0.67774302 0.5 0.70622897 0.44999999 0.70622802 0.60000002
		 0.67774302 0.55000001 0.67774302 0.60000002 0.70622897 0.55000001 0.70622802 0.69999999
		 0.67774302 0.64999998 0.67774302 0.69999999 0.70622897 0.64999998 0.70622802 0.80000001
		 0.67774302 0.75 0.67774302 0.80000001 0.70622897 0.75 0.70622802 0.89999998 0.67774302
		 0.85000002 0.67774302 0.89999998 0.70622897 0.85000002 0.70622802 1 0.67774302 0.94999999
		 0.67774302 1 0.70622897 0.94999999 0.70622802 0.1 0.73471397 0.050000001 0.73471397
		 0.1 0.76319999 0.050000001 0.76319999 0 0.76319999 0 0.73471397 0.2 0.73471397 0.15000001
		 0.73471397 0.2 0.76319999 0.15000001 0.76319999 0.30000001 0.73471397 0.25 0.73471397
		 0.30000001 0.76319999 0.25 0.76319999 0.40000001 0.73471397 0.34999999 0.73471397
		 0.40000001 0.76319999 0.34999999 0.76319999 0.5 0.73471397 0.44999999 0.73471397
		 0.5 0.76319999 0.44999999 0.76319999 0.60000002 0.73471397 0.55000001 0.73471397
		 0.60000002 0.76319999 0.55000001 0.76319999 0.69999999 0.73471397 0.64999998 0.73471397
		 0.69999999 0.76319999 0.64999998 0.76319999 0.80000001 0.73471397 0.75 0.73471397
		 0.80000001 0.76319999 0.75 0.76319999 0.89999998 0.73471397 0.85000002 0.73471397
		 0.89999998 0.76319999 0.85000002 0.76319999 1 0.73471397 0.94999999 0.73471397 1
		 0.76319999 0.94999999 0.76319999 0.1 0.791686 0.050000001 0.791686 0.1 0.820171 0.050000001
		 0.820171 0 0.820171 0 0.791686 0.2 0.791686 0.15000001 0.791686 0.2 0.820171 0.15000001
		 0.820171 0.30000001 0.791686 0.25 0.791686 0.30000001 0.820171 0.25 0.820171 0.40000001
		 0.791686 0.34999999 0.791686 0.40000001 0.820171 0.34999999 0.820171 0.5 0.791686;
	setAttr ".uvst[0].uvsp[250:436]" 0.44999999 0.791686 0.5 0.820171 0.44999999
		 0.820171 0.60000002 0.791686 0.55000001 0.791686 0.60000002 0.820171 0.55000001 0.820171
		 0.69999999 0.791686 0.64999998 0.791686 0.69999999 0.820171 0.64999998 0.820171 0.80000001
		 0.791686 0.75 0.791686 0.80000001 0.820171 0.75 0.820171 0.89999998 0.791686 0.85000002
		 0.791686 0.89999998 0.820171 0.85000002 0.820171 1 0.791686 0.94999999 0.791686 1
		 0.820171 0.94999999 0.820171 0.1 0.84865701 0.050000001 0.84865701 0.1 0.87714303
		 0.050000001 0.87714303 0 0.87714303 0 0.84865701 0.2 0.84865701 0.15000001 0.84865701
		 0.2 0.87714303 0.15000001 0.87714303 0.30000001 0.84865701 0.25 0.84865701 0.30000001
		 0.87714303 0.25 0.87714303 0.40000001 0.84865701 0.34999999 0.84865701 0.40000001
		 0.87714303 0.34999999 0.87714303 0.5 0.84865701 0.44999999 0.84865701 0.5 0.87714303
		 0.44999999 0.87714303 0.60000002 0.84865701 0.55000001 0.84865701 0.60000002 0.87714303
		 0.55000001 0.87714303 0.69999999 0.84865701 0.64999998 0.84865701 0.69999999 0.87714303
		 0.64999998 0.87714303 0.80000001 0.84865701 0.75 0.84865701 0.80000001 0.87714303
		 0.75 0.87714303 0.89999998 0.84865701 0.85000002 0.84865701 0.89999998 0.87714303
		 0.85000002 0.87714303 1 0.84865701 0.94999999 0.84865701 1 0.87714303 0.94999999
		 0.87714303 0.1 0.90562803 0.050000001 0.90562803 0.1 0.93411398 0.050000001 0.93173999
		 0 0.93411398 0 0.90562803 0.2 0.90562803 0.15000001 0.90562803 0.2 0.93411398 0.15000001
		 0.93173999 0.30000001 0.90562803 0.25 0.90562803 0.30000001 0.93411398 0.25 0.93173999
		 0.40000001 0.90562803 0.34999999 0.90562803 0.40000001 0.93411398 0.34999999 0.93173999
		 0.5 0.90562803 0.44999999 0.90562803 0.5 0.93411398 0.44999999 0.93173999 0.60000002
		 0.90562803 0.55000001 0.90562803 0.60000002 0.93411398 0.55000001 0.93173999 0.69999999
		 0.90562803 0.64999998 0.90562803 0.69999999 0.93411398 0.64999998 0.93173999 0.80000001
		 0.90562803 0.75 0.90562803 0.80000001 0.93411398 0.75 0.93173999 0.89999998 0.90562803
		 0.85000002 0.90562803 0.89999998 0.93411398 0.85000002 0.93173999 1 0.90562803 0.94999999
		 0.90562803 1 0.93411398 0.94999999 0.93173999 0.025 0.449857 0.050000001 0.459353
		 0.050000001 0.421372 0.075000003 0.449857 0.125 0.449857 0.15000001 0.459353 0.15000001
		 0.421372 0.175 0.449857 0.22499999 0.449857 0.25 0.459353 0.25 0.421372 0.27500001
		 0.449857 0.32499999 0.449857 0.34999999 0.459353 0.34999999 0.421372 0.375 0.449857
		 0.42500001 0.449857 0.44999999 0.459353 0.44999999 0.421372 0.47499999 0.449857 0.52499998
		 0.449857 0.55000001 0.459353 0.55000001 0.421372 0.57499999 0.449857 0.625 0.449857
		 0.64999998 0.459353 0.64999998 0.421372 0.67500001 0.449857 0.72500002 0.449857 0.75
		 0.459353 0.75 0.421372 0.77499998 0.449857 0.82499999 0.449857 0.85000002 0.459353
		 0.85000002 0.421372 0.875 0.449857 0.92500001 0.449857 0.94999999 0.459353 0.94999999
		 0.421372 0.97500002 0.449857 0.075000003 0.96259999 0.050000001 0.95310497 0.050000001
		 0.99108499 0.025 0.96259999 0.175 0.96259999 0.15000001 0.95310497 0.15000001 0.99108499
		 0.125 0.96259999 0.27500001 0.96259999 0.25 0.95310497 0.25 0.99108499 0.22499999
		 0.96259999 0.375 0.96259999 0.34999999 0.95310497 0.34999999 0.99108499 0.32499999
		 0.96259999 0.47499999 0.96259999 0.44999999 0.95310497 0.44999999 0.99108499 0.42500001
		 0.96259999 0.57499999 0.96259999 0.55000001 0.95310497 0.55000001 0.99108499 0.52499998
		 0.96259999 0.67500001 0.96259999 0.64999998 0.95310497 0.64999998 0.99108499 0.625
		 0.96259999 0.77499998 0.96259999 0.75 0.95310497 0.75 0.99108499 0.72500002 0.96259999
		 0.875 0.96259999 0.85000002 0.95310497 0.85000002 0.99108499 0.82499999 0.96259999
		 0.97500002 0.96259999 0.94999999 0.95310497 0.94999999 0.99108499 0.92500001 0.96259999;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr -s 381 ".pt";
	setAttr ".pt[1:166]" -type "float3"  0 0 -1.4901161e-008 0 -1.4901161e-008 
		0 0 0 7.4505806e-009 0 -1.4901161e-008 0 0 0 0 -1.4901161e-008 -7.4505806e-009 0 
		0 7.4505806e-009 0 0 0 0 0 0 0 -5.9604645e-008 0 0 1.4901161e-008 0 2.9802322e-008 
		0 0 2.9802322e-008 0 0 0 -2.9802322e-008 0 0 0 -2.9802322e-008 0 0 0 0 0 0 0 0 0 
		0 0 0 0 0 -2.9802322e-008 0 0 0 5.9604645e-008 0 0 2.9802322e-008 0 0 -3.7252903e-009 
		0 -5.9604645e-008 0 0 0 0 0 0 0 0 0 0 0 0 -1.4901161e-008 0 2.9802322e-008 0 -5.9604645e-008 
		0 -5.9604645e-008 0 0 0 0 0 0 0 0 0 0 0 0 0 5.9604645e-008 0 2.9802322e-008 0 1.1920929e-007 
		0 0 0 -1.1920929e-007 0 -1.4901161e-008 0 0 0 0 0 0 0 -5.9604645e-008 0 0 0 0 5.9604645e-008 
		0 0 0 0 0 1.4901161e-008 0 0 0 0 0 0 0 -5.9604645e-008 1.1920929e-007 5.9604645e-008 
		0 0 5.9604645e-008 0 0 0 0 0 0 0 -1.4901161e-008 -1.1920929e-007 0 0 0 0 -2.9802322e-008 
		0 0 3.7252903e-009 0 0 0 0 0 0 0 0 -1.1920929e-007 0 0 0 0 0 0 0 5.9604645e-008 0 
		0 5.9604645e-008 0 1.1920929e-007 0 0 0 0 0 1.1920929e-007 2.9802322e-008 0 1.1920929e-007 
		0 0 1.1920929e-007 0 0 0 0 0 0 0 0 0 0 0 -1.1920929e-007 0 0 0 0 1.4901161e-008 0 
		-2.9802322e-008 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2.9802322e-008 0 0 0 0 0 0 0 0 -2.9802322e-008 
		0 1.1920929e-007 0 0 0 0 0 0 7.4505806e-009 0 0 0 0 0 -1.4901161e-008 0 0 0 0 -1.1920929e-007 
		0 0 0 0 0 -1.1920929e-007 1.4901161e-008 0 -3.7252903e-009 0 0 0 0 0 0 0 0 7.4505806e-009 
		1.4901161e-008 0 0 0 1.4901161e-008 0 1.4901161e-008 0 0 0 0 0 0 2.9802322e-008 7.4505806e-009 
		0 0 3.7252903e-009 0 0 0 0 0 0 0 0 0 0 -1.8626451e-009 0 -2.9802322e-008 0 0 1.4901161e-008 
		0 0 0 0 2.9802322e-008 0 0 0 0 0 0 0 0 0 0 -5.9604645e-008 0 0 -5.9604645e-008 -7.4505806e-009 
		0 0 0 0 0 0 0 0 5.9604645e-008 0 5.9604645e-008 -5.9604645e-008 0 0 0 0 -3.7252903e-009 
		0 0 0 0 0 0 2.9802322e-008 0 0 0 0 0 0 -2.9802322e-008 5.9604645e-008 0 0 0 0 5.9604645e-008 
		5.9604645e-008 0 0 0 0 0 0 -5.9604645e-008 0 0 -5.9604645e-008 -5.9604645e-008 0 
		0 0 0 0 0 0 5.9604645e-008 -3.7252903e-009 -1.1920929e-007 0 0 0 0 0 0 0 5.9604645e-008 
		0 -1.1920929e-007 0 0 0 0 0 1.1920929e-007 5.9604645e-008 0 0 0 0 0 0 0 0 0 0 0 0 
		0 -5.9604645e-008 0 0 0 5.9604645e-008 7.4505806e-009 0 0 0 0 0 0 0 0 0 1.1920929e-007 
		0 0 0 0 -5.9604645e-008 0 -5.9604645e-008 0 -1.1920929e-007 -2.9802322e-008 0 0 0 
		0 0 5.9604645e-008 0 1.1920929e-007 0 0 1.1920929e-007 0 -1.4901161e-008 0 0 -2.9802322e-008 
		0 0 0 0 0 0 1.1920929e-007 0 0 1.1920929e-007 0 1.1920929e-007 0 0 -1.1920929e-007 
		0 7.4505806e-009 0 0 0 0 0 0 0 0 0 3.7252903e-009 0 0 0 0 0 0 0 0;
	setAttr ".pt[167:332]" 0 1.1920929e-007 0 0 0 2.9802322e-008 0 1.1920929e-007 
		0 0 0 -7.4505806e-009 0 0 2.9802322e-008 0 0 -2.9802322e-008 2.9802322e-008 0 0 -2.9802322e-008 
		-2.3841858e-007 -1.4901161e-008 -2.9802322e-008 0 0 0 0 -1.4901161e-008 0 0 0 0 2.3841858e-007 
		0 -5.9604645e-008 0 -7.4505806e-009 5.9604645e-008 0 -7.4505806e-009 0 0 0 0 0 0 
		0 0 2.9802322e-008 -7.4505806e-009 0 0 0 0 0 0 -2.9802322e-008 -2.9802322e-008 3.7252903e-009 
		0 5.9604645e-008 0 1.4901161e-008 0 0 0 0 0 0 0 0 0 0 -5.9604645e-008 -1.4901161e-008 
		0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -5.9604645e-008 0 0 0 5.9604645e-008 0 0 -5.9604645e-008 
		0 1.4901161e-008 0 0 0 0 0 0 0 0 -5.9604645e-008 0 0 0 5.9604645e-008 5.9604645e-008 
		-7.4505806e-009 0 0 0 0 0 0 0 5.9604645e-008 0 5.9604645e-008 0 5.9604645e-008 0 
		-2.9802322e-008 0 0 0 0 -5.9604645e-008 0 0 0 -5.9604645e-008 0 0 0 0 0 0 0 0 0 -2.9802322e-008 
		0 1.1920929e-007 0 0 0 0 0 0 0 0 0 0 0 5.9604645e-008 2.9802322e-008 0 -1.1920929e-007 
		-5.9604645e-008 0 0 0 1.4901161e-008 0 0 0 0 0 0 0 0 0 -1.1920929e-007 0 0 0 0 0 
		0 0 0 0 0 0 0 0 5.9604645e-008 0 0 0 1.1920929e-007 0 0 0 -5.9604645e-008 0 -1.1920929e-007 
		0 0 0 2.9802322e-008 0 0 0 0 0 5.9604645e-008 0 0 5.9604645e-008 0 0 0 0 1.1920929e-007 
		0 5.9604645e-008 0 5.9604645e-008 0 0 0 0 0 0 1.4901161e-008 1.1920929e-007 -1.4901161e-008 
		0 1.1920929e-007 0 -1.4901161e-008 0 0 0 -1.1920929e-007 0 0 0 0 0 1.1920929e-007 
		0 0 0 0 0 0 0 0 -1.1920929e-007 0 0 0 0 -1.4901161e-008 0 0 0 0 0 0 0 -2.9802322e-008 
		5.9604645e-008 -1.1920929e-007 0 -5.9604645e-008 0 0 0 0 0 0 0 0 0 0 -1.8626451e-009 
		0 3.7252903e-009 0 -3.7252903e-009 0 0 -9.3132257e-010 0 0 0 0 -1.4901161e-008 -7.4505806e-009 
		0 0 0 0 0 0 0 0 0 1.8626451e-009 0 0 0 0 5.9604645e-008 0 0 0 0 0 -2.9802322e-008 
		0 -1.4901161e-008 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2.9802322e-008 0 
		0 0 0 -1.4901161e-008 0 0 0 0 -1.4901161e-008 0 2.9802322e-008 0 0 0 2.9802322e-008 
		0 -5.9604645e-008 0 0 0 -5.9604645e-008 0 0 0 0 0 0 0 0 0 -2.9802322e-008 0 0 0 0 
		0 0 1.4901161e-008 0 0 0 0 0 0 0 -2.9802322e-008 0 -5.9604645e-008 0 -2.9802322e-008 
		0 0 0 0 0 2.9802322e-008 0 0 -5.9604645e-008 0 0 0 -2.9802322e-008 0 0 0 0 0 0 0 
		0 0 0 0 0 0 0 0 2.9802322e-008 0 0 2.9802322e-008 0 0 -2.9802322e-008 5.9604645e-008 
		5.9604645e-008 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -5.9604645e-008 0 1.1920929e-007 
		0 -5.9604645e-008 0 0 0 0 0 5.9604645e-008 0 0 0 0 0 0 -2.9802322e-008 0 0 -5.9604645e-008 
		1.1920929e-007 0 0 0 0 0 1.1920929e-007 0 0 0 5.9604645e-008 1.1920929e-007 0 0 0 
		0 0 0 -5.9604645e-008 0 0 0 -5.9604645e-008;
	setAttr ".pt[333:381]" 0 1.1920929e-007 0 0 0 0 0 1.1920929e-007 0 0 0 -5.9604645e-008 
		0 1.1920929e-007 5.9604645e-008 -5.9604645e-008 0 0 0 0 0 -1.1920929e-007 0 0 0 0 
		0 0 0 0 0 0 0 0 0 0 0 0 0 -9.3132257e-010 0 0 0 0 -5.9604645e-008 0 -1.1920929e-007 
		0 0 0 0 -1.1920929e-007 -1.1920929e-007 0 0 1.1920929e-007 0 5.9604645e-008 0 2.9802322e-008 
		2.9802322e-008 1.1920929e-007 0 -1.4901161e-008 0 0 0 2.3841858e-007 -2.3283064e-010 
		0 0 0 0 0 0 0 0 0 0 0 0 0 1.1920929e-007 0 0 0 -2.9802322e-008 0 0 0 0 0 -3.7252903e-009 
		-1.8626451e-009 0 0 0 7.4505806e-009 0 4.6566129e-010 0 0 0 0 0 1.4901161e-008 0 
		0 0 -3.7252903e-009 0 0 0 0 0 0 0 -5.9604645e-008 0 0 0 0 1.4901161e-008 0 0 -1.4901161e-008 
		0 0 0 0 0 0 0 0 0 0 0 0 5.9604645e-008 0 0 0 1.1920929e-007 0 0 0 0;
	setAttr -s 382 ".vt";
	setAttr ".vt[0:165]"  1.99287498 0.213825 -0.83531201 0.85762101 0.441834 -1.054003954
		 -0.219056 0.72447598 -0.58117002 -0.825903 0.95379102 0.40258199 -0.73112398 1.042188048 1.52149296
		 0.029079 0.95590299 2.34817696 1.16433299 0.72789401 2.56686902 2.24100995 0.445252 2.094036102
		 2.84785604 0.215937 1.11028397 2.75307703 0.12754001 -0.0086270003 3.023346901 0.718701 -2.2923789
		 0.906376 1.14388299 -2.70018601 -1.10136294 1.670941 -1.81846702 -2.23298311 2.098556995 0.015989
		 -2.056242943 2.26339507 2.10248399 -0.63865203 2.10249496 3.64404702 1.47831798 1.67731297 4.051854134
		 3.48605704 1.15025496 3.17013597 4.61767721 0.72263902 1.33567905 4.440938 0.55779999 -0.75081497
		 3.99706101 1.75380802 -3.53601503 1.083300948 2.33902097 -4.097312927 -1.68011498 3.064454079 -2.88373089
		 -3.23765612 3.65301704 -0.35881901 -2.99439502 3.87989807 2.512995 -1.043248057 3.65843701 4.63477516
		 1.87051105 3.073225021 5.1960721 4.63392687 2.34779191 3.98249102 6.19146776 1.75922894 1.45757902
		 5.9482069 1.53234804 -1.414235 4.79809093 3.2190671 -4.41263103 1.37276101 3.90702605 -5.07247591
		 -1.87583005 4.7598238 -3.6458261 -3.70683002 5.45172119 -0.67761302 -3.42085791 5.71843576 2.69840693
		 -1.12714803 5.45809317 5.19270802 2.29818201 4.77013397 5.85255289 5.546772 3.91733694 4.42590284
		 7.3777709 3.22544003 1.45769095 7.091801167 2.95872498 -1.918329 5.3480258 4.97104692 -4.83641911
		 1.74642098 5.69440985 -5.53022099 -1.66934896 6.59109497 -4.030151844 -3.59457588 7.31859779 -0.90918797
		 -3.29388905 7.59903908 2.64056897 -0.88213903 7.32529783 5.26323318 2.71946692 6.60193586 5.95703411
		 6.13523579 5.70525122 4.45696592 8.060462952 4.97774792 1.33600295 7.75977516 4.69730711 -2.21375394
		 5.59303617 6.83825302 -4.76589394 2.16770601 7.52621078 -5.42573881 -1.080885053 8.37900925 -3.999089
		 -2.91188502 9.070905685 -1.03087604 -2.6259129 9.33762074 2.34514403 -0.332203 9.077278137 4.83944607
		 3.093127012 8.38931942 5.49928999 6.34171677 7.53652191 4.072639942 8.17271614 6.844625 1.10442805
		 7.88674593 6.57790995 -2.2715919 5.5091362 8.63790798 -4.20796013 2.59537601 9.22312069 -4.76925898
		 -0.16804001 9.94855404 -3.55567694 -1.72558105 10.537117 -1.030763984 -1.482319 10.76399803 1.84104896
		 0.46882701 10.54253674 3.96282911 3.38258696 9.95732498 4.52412605 6.14600182 9.23189163 3.31054592
		 7.70354414 8.64332867 0.78563303 7.46028185 8.41644764 -2.086179972 5.10453987 10.19385147 -3.21723294
		 2.98756909 10.61903286 -3.62504005 0.97983003 11.14609146 -2.74332094 -0.15178999 11.57370663 -0.90886497
		 0.02495 11.73854637 1.17762995 1.442541 11.5776453 2.71919298 3.55951095 11.15246296 3.1269989
		 5.56724977 10.62540627 2.24528193 6.69887018 10.19779015 0.41082501 6.52213097 10.032951355 -1.67567003
		 4.43680906 11.34044266 -1.921363 3.30155492 11.56845188 -2.14005494 2.22487807 11.85109425 -1.66722095
		 1.61803102 12.08040905 -0.683469 1.71281004 12.16880608 0.435442 2.47301292 12.082521439 1.26212597
		 3.60826707 11.85451126 1.48081803 4.68494415 11.5718689 1.0079840422 5.29179001 11.34255505 0.024232
		 5.19701099 11.25415802 -1.094678998 0.94138497 0.26802701 0.787359 3.52450299 12.028318405 -0.360544
		 1.45679402 0.315126 -1.069329023 0.270156 0.58907598 -0.93299001 -0.63300598 0.86372602 -0.151573
		 -0.90771502 1.034168959 0.97644502 -0.44904199 1.035302043 2.020200968 0.56781501 0.86669201 2.58101511
		 1.75445294 0.59274203 2.44467497 2.65761495 0.31809199 1.66325903 2.93232393 0.14764901 0.53524101
		 2.47365189 0.146516 -0.508515 2.0035951138 0.90725899 -2.6553309 -0.162166 1.40725195 -2.4064939
		 -1.81054795 1.90852201 -0.980313 -2.31192708 2.21960211 1.078461051 -1.474792 2.22166991 2.98344398
		 0.38109899 1.91393602 4.0069990158 2.54685998 1.41394305 3.75816298 4.19524193 0.912673 2.33198094
		 4.69662094 0.60159302 0.27320799 3.85948706 0.59952497 -1.63177502 2.59349298 2.013336897 -4.035575867
		 -0.38742101 2.70151806 -3.6930809 -2.65622497 3.39145803 -1.730111 -3.34631395 3.81962299 1.10354805
		 -2.19409609 3.822469 3.72553301 0.36031899 3.39890909 5.13433599 3.34123302 2.71072793 4.79184198
		 5.61003685 2.020788908 2.82887101 6.30012608 1.592623 -0.0047869999 5.14790916 1.58977699 -2.62677193
		 3.14809799 3.52416205 -4.99989986 -0.356177 4.33316708 -4.59727383 -3.023315907 5.14423895 -2.28966403
		 -3.83456397 5.64757776 1.041501999 -2.48005104 5.65092421 4.12382984 0.52284497 5.15299892 5.77997684
		 4.02711916 4.34399414 5.37735081 6.69425821 3.53292108 3.069741011 7.50550604 3.029582977 -0.26142401
		 6.15099382 3.026237011 -3.3437531 3.61312103 5.29184294 -5.45390987 -0.071491003 6.14248085 -5.030562878
		 -2.87588811 6.99529314 -2.60419893 -3.72888398 7.52453423 0.89839602 -2.30466509 7.52805185 4.13934803
		 0.85276598 7.0045027733 5.88072395 4.53737783 6.15386486 5.45737791 7.34177399 5.30105305 3.031013012
		 8.19477081 4.77181196 -0.47158101 6.77055216 4.76829386 -3.712533 3.94304299 7.14334679 -5.35316277
		 0.43876901 7.95235205 -4.9505372 -2.2283709 8.76342487 -2.64292598 -3.039618969 9.26676273 0.68823898
		 -1.68510604 9.27010918 3.77056694 1.31779003 8.77218437 5.42671394 4.82206392 7.96317911 5.024087906
		 7.48920298 7.15210676 2.71647811 8.30045128 6.64876795 -0.61468703 6.94593906 6.64542294 -3.69701505
		 4.10556889 8.8974371 -4.70752192 1.12465405 9.58561802 -4.36502695 -1.14415002 10.27555656 -2.40205693
		 -1.83423901 10.70372295 0.431602 -0.68202102 10.70656872 3.05358696 1.87239504 10.28300858 4.46238995
		 4.8533082 9.59482765 4.11989594 7.1221118 8.90488815 2.15692496 7.81220102 8.47672272 -0.67673302
		 6.65998411 8.47387695 -3.29871798 4.084787846 10.38241005 -3.58018494 1.91902804 10.88240242 -3.33134794
		 0.27064499 11.38367271 -1.90516698 -0.23073401 11.69475269 0.153606;
	setAttr ".vt[166:331]" 0.60640103 11.69682121 2.058589935 2.46229196 11.38908577 3.082144976
		 4.62805319 10.88909435 2.83330894 6.27643585 10.3878231 1.40712702 6.77781487 10.076743126 -0.65164602
		 5.94068003 10.07467556 -2.5566299 3.898072 11.42965412 -2.15420008 2.71143508 11.70360374 -2.017860889
		 1.80827296 11.97825432 -1.236444 1.53356302 12.1486969 -0.108426 1.99223602 12.14982986 0.93532902
		 3.0090939999 11.98122025 1.49614298 4.19573116 11.70726967 1.35980403 5.098893166 11.43262005 0.57838798
		 5.37360287 11.26217747 -0.54962999 4.91492987 11.26104355 -1.59338605 2.501086 0.39650699 -1.56973696
		 0.86611599 0.72488201 -1.88469303 -0.68449199 1.13193703 -1.20372796 -1.55845904 1.46219099 0.21305101
		 -1.42196 1.589499 1.82448399 -0.327133 1.46523297 3.015057087 1.30783606 1.13685799 3.33001208
		 2.85844398 0.72980303 2.64904809 3.73241091 0.39954901 1.23226905 3.59591293 0.272241 -0.37916401
		 3.52602601 1.17540896 -2.95293999 0.97950202 1.68686402 -3.44349408 -1.43562698 2.32086706 -2.3828671
		 -2.79686403 2.8352499 -0.176181 -2.58426189 3.033536911 2.33368301 -0.87902802 2.83998704 4.18804407
		 1.66749597 2.32853198 4.67859888 4.082624912 1.69452906 3.6179719 5.44386101 1.18014598 1.411286
		 5.23125887 0.98185903 -1.098577976 4.42438984 2.4410789 -4.02619791 1.21558297 3.08555007 -4.64433289
		 -1.82765698 3.8844409 -3.30786395 -3.54291511 4.53260088 -0.52727801 -3.27502203 4.78245687 2.63533497
		 -1.12630105 4.53856993 4.97196579 2.082505941 3.894099 5.5901022 5.12574577 3.09520793 4.25363302
		 6.84100294 2.44704795 1.47304797 6.57310915 2.19719291 -1.68956602 5.10824013 4.069624901 -4.68445492
		 1.55124998 4.7840271 -5.36966181 -1.82220805 5.66960382 -3.88817501 -3.72358608 6.3880949 -0.80587202
		 -3.42662311 6.66506195 2.69991207 -1.044749022 6.39471197 5.29008818 2.51224089 5.68030977 5.97529507
		 5.88569784 4.79473305 4.49380922 7.787076 4.07624197 1.41150606 7.49011421 3.79927492 -2.094278097
		 5.51063585 5.90163279 -4.8632741 1.95364594 6.61603594 -5.54848099 -1.41981196 7.50161314 -4.066995144
		 -3.32119012 8.22010422 -0.98469102 -3.024226904 8.49707127 2.52109289 -0.642353 8.22672081 5.11126804
		 2.91463804 7.51231909 5.79647589 6.288095 6.62674189 4.31499004 8.18947315 5.90825081 1.232687
		 7.89250994 5.63128424 -2.27309704 5.59218884 7.75777483 -4.54515219 2.38338208 8.40224743 -5.16328716
		 -0.65985799 9.20113659 -3.82681894 -2.37511611 9.84929752 -1.046233058 -2.10722208 10.099154472 2.11638093
		 0.041498002 9.85526657 4.45301199 3.25030494 9.21079636 5.071146965 6.29354477 8.41190529 3.73467898
		 8.0088033676 7.76374483 0.95409298 7.7409091 7.51388884 -2.20851994 5.34491587 9.45635796 -3.76122999
		 2.79839206 9.96781445 -4.25178385 0.38326299 10.60181713 -3.1911571 -0.977974 11.11620045 -0.98447198
		 -0.76537198 11.31448555 1.52539301 0.93986201 11.12093735 3.37975407 3.48638606 10.60948181 3.87030911
		 5.90151501 9.97547913 2.80968094 7.2627511 9.46109581 0.60299599 7.050148964 9.2628088 -1.90686798
		 4.7930212 10.83111286 -2.58824205 3.15805197 11.15948772 -2.903198 1.60744298 11.56654263 -2.22223306
		 0.73347598 11.89679718 -0.80545402 0.86997497 12.024105072 0.805978 1.96480203 11.8998394 1.99655199
		 3.59977102 11.57146358 2.31150699 5.15037918 11.16440868 1.63054204 6.024346828 10.83415508 0.213763
		 5.8878479 10.70684719 -1.39766896 1.53234899 0.17565 -0.13939799 0.87978899 0.30671301 -0.26510599
		 0.26089999 0.469179 0.0066860002 -0.087922998 0.60099298 0.57216001 -0.033443 0.65180397 1.215325
		 0.403532 0.60220701 1.69051397 1.056090951 0.47114399 1.816221 1.67498004 0.30867699 1.54443002
		 2.023802996 0.176864 0.97895598 1.96932304 0.12605201 0.33579099 4.062355995 11.69413853 -1.26370001
		 3.40979695 11.82520199 -1.38940704 2.7909081 11.98766899 -1.11761606 2.44208407 12.11948204 -0.55214202
		 2.4965651 12.17029381 0.091023996 2.93353891 12.12069607 0.56621301 3.58609891 11.98963261 0.69191998
		 4.20498705 11.8271656 0.420129 4.55381107 11.69535255 -0.145345 4.499331 11.64454079 -0.78851002
		 1.713516 0.54213399 -1.85005105 0.040865 0.92828602 -1.65787101 -1.23220694 1.31542504 -0.55640799
		 -1.61942899 1.55567706 1.033614039 -0.97289699 1.55727398 2.50486302 0.460437 1.31960595 3.2953701
		 2.13308692 0.93345398 3.10318995 3.40615892 0.54631501 2.0017280579 3.79338098 0.306063 0.411706
		 3.14685011 0.30446601 -1.059543014 2.29935694 1.402228 -3.389539 -0.30585799 2.0036730766 -3.090209961
		 -2.28871298 2.60665607 -1.37464297 -2.89182711 2.98085809 1.10187495 -1.88482904 2.98334503 3.39339805
		 0.34764099 2.613168 4.62464285 2.95285511 2.011723042 4.325315 4.93570995 1.40874004 2.60974789
		 5.53882408 1.034538031 0.13323 4.53182602 1.032050967 -2.15829396 2.87869692 2.72688699 -4.57634497
		 -0.40406501 3.48475289 -4.19916916 -2.90260911 4.24455595 -2.037427902 -3.66257596 4.71607685 1.083166957
		 -2.3936851 4.7192111 3.97065496 0.41939101 4.25276184 5.52211285 3.70215297 3.49489594 5.14493799
		 6.20069599 2.73509312 2.98319697 6.9606638 2.26357198 -0.137398 5.69177294 2.26043797 -3.024885893
		 3.39482594 4.386446 -5.29429722 -0.24414299 5.22654676 -4.876194 -3.013799906 6.068795204 -2.47988605
		 -3.85623097 6.59147978 0.97931999 -2.4496541 6.59495401 4.18012524 0.66866499 6.077890873 5.89993
		 4.30763388 5.23779011 5.48182821 7.077291012 4.39554214 3.085520029 7.91972113 3.87285709 -0.37368599
		 6.51314497 3.8693819 -3.57449102 3.79722309 6.21845484 -5.47311592 0.158253 7.05855608 -5.055014133
		 -2.61140394 7.90080404 -2.658705 -3.45383406 8.42348862 0.80050099 -2.0472579 8.42696285 4.001306057
		 1.071061015 7.90990019 5.72111082 4.71003008 7.069798946 5.30300903 7.47968721 6.22755098 2.9066999
		 8.32211685 5.70486593 -0.55250502 6.91554117 5.70139122 -3.75331092;
	setAttr ".vt[332:381]" 4.046495914 8.04358387 -5.095298767 0.76373398 8.80144978 -4.71812391
		 -1.73480904 9.56125259 -2.55638194 -2.49477696 10.032773972 0.56421298 -1.22588599 10.035907745 3.45169997
		 1.58719099 9.56945896 5.0031590462 4.8699522 8.81159306 4.62598324 7.36849594 8.051790237 2.46424294
		 8.12846279 7.58026886 -0.65635198 6.85957193 7.57713413 -3.54383993 4.11824703 9.68317699 -4.19782877
		 1.51303196 10.28462315 -3.89849997 -0.469823 10.88760567 -2.18293309 -1.072936058 11.26180744 0.293585
		 -0.065939002 11.26429462 2.58510804 2.16653109 10.89411831 3.81635308 4.7717452 10.29267216 3.51702499
		 6.75460005 9.68968964 1.801458 7.35771418 9.31548786 -0.67505997 6.35071611 9.31300068 -2.96658397
		 4.0054512024 10.97673988 -2.86855602 2.33279991 11.36289215 -2.6763761 1.059728026 11.75003147 -1.57491302
		 0.67250597 11.99028301 0.015109 1.31903803 11.99188042 1.48635805 2.75237203 11.75421238 2.27686501
		 4.42502308 11.36806011 2.084685087 5.69809389 10.98092079 0.98322302 6.085317135 10.74066925 -0.60679901
		 5.43878412 10.73907185 -2.078047991 1.26110601 0.23450901 -0.408797 0.49263099 0.41192099 -0.32050201
		 -0.092262998 0.58978701 0.18554901 -0.27016699 0.700167 0.91606098 0.026873 0.70090097 1.59200501
		 0.68539703 0.59170699 1.95519197 1.45387197 0.414296 1.86689699 2.038765907 0.23643 1.360847
		 2.21667004 0.12605 0.63033402 1.91963005 0.12531599 -0.045609001 3.78049111 11.70463753 -1.52837801
		 3.012016058 11.88204956 -1.44008303 2.42712212 12.059915543 -0.93403202 2.24921799 12.17029572 -0.20352
		 2.54625797 12.17102909 0.472424 3.20478201 12.061836243 0.83561099 3.97325706 11.88442516 0.74731702
		 4.55815077 11.70655918 0.241266 4.7360549 11.59617901 -0.48924699 4.43901491 11.59544468 -1.16518998;
	setAttr -s 760 ".ed";
	setAttr ".ed[0:165]"  92 1 1 1 183 1 183 282 1 282 92 1 183 11 1 11 102 1
		 102 282 1 102 10 1 10 182 1 182 282 1 182 0 1 0 92 1 93 2 1 2 184 1 184 283 1 283 93 1
		 184 12 1 12 103 1 103 283 1 103 11 1 183 283 1 1 93 1 94 3 1 3 185 1 185 284 1 284 94 1
		 185 13 1 13 104 1 104 284 1 104 12 1 184 284 1 2 94 1 95 4 1 4 186 1 186 285 1 285 95 1
		 186 14 1 14 105 1 105 285 1 105 13 1 185 285 1 3 95 1 96 5 1 5 187 1 187 286 1 286 96 1
		 187 15 1 15 106 1 106 286 1 106 14 1 186 286 1 4 96 1 97 6 1 6 188 1 188 287 1 287 97 1
		 188 16 1 16 107 1 107 287 1 107 15 1 187 287 1 5 97 1 98 7 1 7 189 1 189 288 1 288 98 1
		 189 17 1 17 108 1 108 288 1 108 16 1 188 288 1 6 98 1 99 8 1 8 190 1 190 289 1 289 99 1
		 190 18 1 18 109 1 109 289 1 109 17 1 189 289 1 7 99 1 100 9 1 9 191 1 191 290 1 290 100 1
		 191 19 1 19 110 1 110 290 1 110 18 1 190 290 1 8 100 1 101 0 1 182 291 1 291 101 1
		 10 111 1 111 291 1 111 19 1 191 291 1 9 101 1 11 193 1 193 292 1 292 102 1 193 21 1
		 21 112 1 112 292 1 112 20 1 20 192 1 192 292 1 192 10 1 12 194 1 194 293 1 293 103 1
		 194 22 1 22 113 1 113 293 1 113 21 1 193 293 1 13 195 1 195 294 1 294 104 1 195 23 1
		 23 114 1 114 294 1 114 22 1 194 294 1 14 196 1 196 295 1 295 105 1 196 24 1 24 115 1
		 115 295 1 115 23 1 195 295 1 15 197 1 197 296 1 296 106 1 197 25 1 25 116 1 116 296 1
		 116 24 1 196 296 1 16 198 1 198 297 1 297 107 1 198 26 1 26 117 1 117 297 1 117 25 1
		 197 297 1 17 199 1 199 298 1 298 108 1 199 27 1 27 118 1 118 298 1 118 26 1 198 298 1
		 18 200 1 200 299 1 299 109 1 200 28 1 28 119 1 119 299 1 119 27 1 199 299 1;
	setAttr ".ed[166:331]" 19 201 1 201 300 1 300 110 1 201 29 1 29 120 1 120 300 1
		 120 28 1 200 300 1 192 301 1 301 111 1 20 121 1 121 301 1 121 29 1 201 301 1 21 203 1
		 203 302 1 302 112 1 203 31 1 31 122 1 122 302 1 122 30 1 30 202 1 202 302 1 202 20 1
		 22 204 1 204 303 1 303 113 1 204 32 1 32 123 1 123 303 1 123 31 1 203 303 1 23 205 1
		 205 304 1 304 114 1 205 33 1 33 124 1 124 304 1 124 32 1 204 304 1 24 206 1 206 305 1
		 305 115 1 206 34 1 34 125 1 125 305 1 125 33 1 205 305 1 25 207 1 207 306 1 306 116 1
		 207 35 1 35 126 1 126 306 1 126 34 1 206 306 1 26 208 1 208 307 1 307 117 1 208 36 1
		 36 127 1 127 307 1 127 35 1 207 307 1 27 209 1 209 308 1 308 118 1 209 37 1 37 128 1
		 128 308 1 128 36 1 208 308 1 28 210 1 210 309 1 309 119 1 210 38 1 38 129 1 129 309 1
		 129 37 1 209 309 1 29 211 1 211 310 1 310 120 1 211 39 1 39 130 1 130 310 1 130 38 1
		 210 310 1 202 311 1 311 121 1 30 131 1 131 311 1 131 39 1 211 311 1 31 213 1 213 312 1
		 312 122 1 213 41 1 41 132 1 132 312 1 132 40 1 40 212 1 212 312 1 212 30 1 32 214 1
		 214 313 1 313 123 1 214 42 1 42 133 1 133 313 1 133 41 1 213 313 1 33 215 1 215 314 1
		 314 124 1 215 43 1 43 134 1 134 314 1 134 42 1 214 314 1 34 216 1 216 315 1 315 125 1
		 216 44 1 44 135 1 135 315 1 135 43 1 215 315 1 35 217 1 217 316 1 316 126 1 217 45 1
		 45 136 1 136 316 1 136 44 1 216 316 1 36 218 1 218 317 1 317 127 1 218 46 1 46 137 1
		 137 317 1 137 45 1 217 317 1 37 219 1 219 318 1 318 128 1 219 47 1 47 138 1 138 318 1
		 138 46 1 218 318 1 38 220 1 220 319 1 319 129 1 220 48 1 48 139 1 139 319 1 139 47 1
		 219 319 1 39 221 1 221 320 1 320 130 1 221 49 1 49 140 1 140 320 1;
	setAttr ".ed[332:497]" 140 48 1 220 320 1 212 321 1 321 131 1 40 141 1 141 321 1
		 141 49 1 221 321 1 41 223 1 223 322 1 322 132 1 223 51 1 51 142 1 142 322 1 142 50 1
		 50 222 1 222 322 1 222 40 1 42 224 1 224 323 1 323 133 1 224 52 1 52 143 1 143 323 1
		 143 51 1 223 323 1 43 225 1 225 324 1 324 134 1 225 53 1 53 144 1 144 324 1 144 52 1
		 224 324 1 44 226 1 226 325 1 325 135 1 226 54 1 54 145 1 145 325 1 145 53 1 225 325 1
		 45 227 1 227 326 1 326 136 1 227 55 1 55 146 1 146 326 1 146 54 1 226 326 1 46 228 1
		 228 327 1 327 137 1 228 56 1 56 147 1 147 327 1 147 55 1 227 327 1 47 229 1 229 328 1
		 328 138 1 229 57 1 57 148 1 148 328 1 148 56 1 228 328 1 48 230 1 230 329 1 329 139 1
		 230 58 1 58 149 1 149 329 1 149 57 1 229 329 1 49 231 1 231 330 1 330 140 1 231 59 1
		 59 150 1 150 330 1 150 58 1 230 330 1 222 331 1 331 141 1 50 151 1 151 331 1 151 59 1
		 231 331 1 51 233 1 233 332 1 332 142 1 233 61 1 61 152 1 152 332 1 152 60 1 60 232 1
		 232 332 1 232 50 1 52 234 1 234 333 1 333 143 1 234 62 1 62 153 1 153 333 1 153 61 1
		 233 333 1 53 235 1 235 334 1 334 144 1 235 63 1 63 154 1 154 334 1 154 62 1 234 334 1
		 54 236 1 236 335 1 335 145 1 236 64 1 64 155 1 155 335 1 155 63 1 235 335 1 55 237 1
		 237 336 1 336 146 1 237 65 1 65 156 1 156 336 1 156 64 1 236 336 1 56 238 1 238 337 1
		 337 147 1 238 66 1 66 157 1 157 337 1 157 65 1 237 337 1 57 239 1 239 338 1 338 148 1
		 239 67 1 67 158 1 158 338 1 158 66 1 238 338 1 58 240 1 240 339 1 339 149 1 240 68 1
		 68 159 1 159 339 1 159 67 1 239 339 1 59 241 1 241 340 1 340 150 1 241 69 1 69 160 1
		 160 340 1 160 68 1 240 340 1 232 341 1 341 151 1 60 161 1 161 341 1;
	setAttr ".ed[498:663]" 161 69 1 241 341 1 61 243 1 243 342 1 342 152 1 243 71 1
		 71 162 1 162 342 1 162 70 1 70 242 1 242 342 1 242 60 1 62 244 1 244 343 1 343 153 1
		 244 72 1 72 163 1 163 343 1 163 71 1 243 343 1 63 245 1 245 344 1 344 154 1 245 73 1
		 73 164 1 164 344 1 164 72 1 244 344 1 64 246 1 246 345 1 345 155 1 246 74 1 74 165 1
		 165 345 1 165 73 1 245 345 1 65 247 1 247 346 1 346 156 1 247 75 1 75 166 1 166 346 1
		 166 74 1 246 346 1 66 248 1 248 347 1 347 157 1 248 76 1 76 167 1 167 347 1 167 75 1
		 247 347 1 67 249 1 249 348 1 348 158 1 249 77 1 77 168 1 168 348 1 168 76 1 248 348 1
		 68 250 1 250 349 1 349 159 1 250 78 1 78 169 1 169 349 1 169 77 1 249 349 1 69 251 1
		 251 350 1 350 160 1 251 79 1 79 170 1 170 350 1 170 78 1 250 350 1 242 351 1 351 161 1
		 70 171 1 171 351 1 171 79 1 251 351 1 71 253 1 253 352 1 352 162 1 253 81 1 81 172 1
		 172 352 1 172 80 1 80 252 1 252 352 1 252 70 1 72 254 1 254 353 1 353 163 1 254 82 1
		 82 173 1 173 353 1 173 81 1 253 353 1 73 255 1 255 354 1 354 164 1 255 83 1 83 174 1
		 174 354 1 174 82 1 254 354 1 74 256 1 256 355 1 355 165 1 256 84 1 84 175 1 175 355 1
		 175 83 1 255 355 1 75 257 1 257 356 1 356 166 1 257 85 1 85 176 1 176 356 1 176 84 1
		 256 356 1 76 258 1 258 357 1 357 167 1 258 86 1 86 177 1 177 357 1 177 85 1 257 357 1
		 77 259 1 259 358 1 358 168 1 259 87 1 87 178 1 178 358 1 178 86 1 258 358 1 78 260 1
		 260 359 1 359 169 1 260 88 1 88 179 1 179 359 1 179 87 1 259 359 1 79 261 1 261 360 1
		 360 170 1 261 89 1 89 180 1 180 360 1 180 88 1 260 360 1 252 361 1 361 171 1 80 181 1
		 181 361 1 181 89 1 261 361 1 0 262 1 262 362 1 362 92 1 262 90 1;
	setAttr ".ed[664:759]" 90 263 1 263 362 1 263 1 1 263 363 1 363 93 1 90 264 1
		 264 363 1 264 2 1 264 364 1 364 94 1 90 265 1 265 364 1 265 3 1 265 365 1 365 95 1
		 90 266 1 266 365 1 266 4 1 266 366 1 366 96 1 90 267 1 267 366 1 267 5 1 267 367 1
		 367 97 1 90 268 1 268 367 1 268 6 1 268 368 1 368 98 1 90 269 1 269 368 1 269 7 1
		 269 369 1 369 99 1 90 270 1 270 369 1 270 8 1 270 370 1 370 100 1 90 271 1 271 370 1
		 271 9 1 271 371 1 371 101 1 262 371 1 81 273 1 273 372 1 372 172 1 273 91 1 91 272 1
		 272 372 1 272 80 1 82 274 1 274 373 1 373 173 1 274 91 1 273 373 1 83 275 1 275 374 1
		 374 174 1 275 91 1 274 374 1 84 276 1 276 375 1 375 175 1 276 91 1 275 375 1 85 277 1
		 277 376 1 376 176 1 277 91 1 276 376 1 86 278 1 278 377 1 377 177 1 278 91 1 277 377 1
		 87 279 1 279 378 1 378 178 1 279 91 1 278 378 1 88 280 1 280 379 1 379 179 1 280 91 1
		 279 379 1 89 281 1 281 380 1 380 180 1 281 91 1 280 380 1 272 381 1 381 181 1 281 381 1;
	setAttr -s 382 ".n";
	setAttr ".n[0:165]" -type "float3"  -0.14119901 -0.95460206 -0.26229504 -0.245938
		 -0.93091404 -0.27002701 -0.24959901 -0.87947702 -0.40524104 -0.107991 -0.91362405
		 -0.391956 -0.24794702 -0.80802703 -0.53443003 -0.070748001 -0.85114205 -0.52014601
		 0.099290997 -0.88886899 -0.44727299 0.02746 -0.94247508 -0.33314699 -0.042769998
		 -0.97551405 -0.21574 -0.34629604 -0.90484506 -0.247659 -0.43143004 -0.88222003 -0.188567
		 -0.50200707 -0.81321698 -0.29439402 -0.38478404 -0.84517598 -0.37096903 -0.56317103
		 -0.72527605 -0.395996 -0.41670504 -0.76444906 -0.491909 -0.49718401 -0.86115098 -0.10596101
		 -0.531066 -0.84732997 -0.001301 -0.64013398 -0.767223 -0.039967 -0.589818 -0.78713804
		 -0.18035701 -0.73929799 -0.66872799 -0.078998998 -0.674842 -0.69256002 -0.254852
		 -0.53610802 -0.83675104 0.111517 -0.50364804 -0.83483708 0.222231 -0.60415906 -0.751046
		 0.26631001 -0.64505804 -0.75553209 0.11433001 -0.69629407 -0.64893502 0.306687 -0.74788803
		 -0.65378803 0.115002 -0.44404304 -0.83652401 0.32102099 -0.357519 -0.846901 0.39362299
		 -0.40286201 -0.76663703 0.49996999 -0.51986098 -0.75522298 0.39922804 -0.44125202
		 -0.66799206 0.59923601 -0.58998102 -0.65339804 0.47433603 -0.25749701 -0.86055905
		 0.43946999 -0.15216102 -0.88152999 0.44693699 -0.121991 -0.81227803 0.57037103 -0.26540101
		 -0.78633702 0.557886 -0.088582002 -0.72410405 0.68397808 -0.26810199 -0.69155502
		 0.670726 -0.051038001 -0.90411603 0.424229 0.033330999 -0.930224 0.365477 0.13041702
		 -0.87853801 0.45952299 0.013719001 -0.84419203 0.53586507 0.22664201 -0.80685502
		 0.54554409 0.081156008 -0.763219 0.64102304 0.098488003 -0.95400906 0.28313601 0.130777
		 -0.97508502 0.17918402 0.264732 -0.94188905 0.20679002 0.216426 -0.91282201 0.346288
		 0.39733702 -0.88813299 0.23096099 0.33599201 -0.85013807 0.40543202 0.135179 -0.98857701
		 0.066650003 0.101987 -0.99382401 -0.043739002 0.22634201 -0.96906406 -0.098413005
		 0.26780701 -0.96199602 0.053315002 0.350842 -0.92382199 -0.15317301 0.40348402 -0.91419506
		 0.038046002 0.043114003 -0.98880404 -0.14285301 0.142611 -0.96230507 -0.23158202
		 0.24557699 -0.91458499 -0.32128799 -0.24044199 -0.71451706 -0.65700406 -0.030168002
		 -0.76604503 -0.642079 -0.22733201 -0.60489601 -0.76316506 0.011032 -0.66301107 -0.748528
		 0.243055 -0.71488899 -0.65563601 0.17303002 -0.81174707 -0.55778801 -0.613976 -0.61645907
		 -0.49296302 -0.44006103 -0.66276908 -0.605874 -0.64993107 -0.493958 -0.57757705 -0.45283499
		 -0.54654002 -0.70443898 -0.82727903 -0.54915297 -0.118493 -0.74805301 -0.57758999
		 -0.32681304 -0.89605707 -0.41585699 -0.15538301 -0.80338401 -0.44921601 -0.39087
		 -0.77881199 -0.525289 0.34281501 -0.83971399 -0.53112209 0.113089 -0.84389007 -0.38731599
		 0.371263 -0.91253 -0.39436904 0.108454 -0.471755 -0.54827398 0.69053805 -0.65077102
		 -0.53065598 0.54304898 -0.49120101 -0.414857 0.765908 -0.69670999 -0.39383599 0.59957403
		 -0.051599003 -0.61507004 0.78678209 -0.264696 -0.57639605 0.77311301 -0.013683 -0.49238604
		 0.87026906 -0.255032 -0.44786203 0.85695904 0.32193503 -0.71312708 0.62274098 0.14923
		 -0.661313 0.735116 0.40891603 -0.603324 0.684681 0.21310399 -0.54489499 0.81097203
		 0.52855402 -0.81086904 0.25124201 0.45318902 -0.76485103 0.45784703 0.64791107 -0.71388906
		 0.26565599 0.55938399 -0.66165698 0.49930003 0.47571903 -0.85461998 -0.208124 0.53795499
		 -0.84271204 0.021008 0.59100705 -0.76399505 -0.25888601 0.661111 -0.75028104 0.003274
		 0.34901202 -0.84317797 -0.40895104 0.44529104 -0.75081408 -0.48784703 -0.20913699
		 -0.48262304 -0.85049206 0.051696002 -0.54515499 -0.83674008 -0.18635701 -0.35041803
		 -0.91786605 0.090999007 -0.415126 -0.90520108 0.36434603 -0.47228602 -0.80261904
		 0.30731103 -0.60091406 -0.73787707 -0.67048699 -0.36151302 -0.64788598 -0.455062
		 -0.41941899 -0.78549701 -0.67570299 -0.22195801 -0.70296508 -0.44707602 -0.28417799
		 -0.84815502 -0.94347501 -0.27256599 -0.188582 -0.83953905 -0.311194 -0.44534603 -0.96838897
		 -0.12242601 -0.217336 -0.85608506 -0.16650401 -0.48927999 -0.88895106 -0.23866101
		 0.39090401 -0.96367007 -0.24720001 0.101159 -0.91233498 -0.082672 0.40101102 -0.99147701
		 -0.092917003 0.091325007 -0.49892804 -0.27146804 0.82302904 -0.72603899 -0.246613
		 0.64191097 -0.49471602 -0.12125501 0.86055398 -0.73772401 -0.092289999 0.668764 0.024102001
		 -0.359797 0.93271905 -0.23946501 -0.30971199 0.92018205 0.061035998 -0.22013801 0.973557
		 -0.21840702 -0.164929 0.96182007 0.48545104 -0.48090699 0.73011303 0.271207 -0.41762504
		 0.86720008 0.55038202 -0.34859803 0.75865602 0.32265604 -0.282276 0.90344507 0.751858
		 -0.59981602 0.273734 0.65177 -0.54367203 0.52878797 0.83801901 -0.47111601 0.275271
		 0.72867703 -0.413551 0.54589802 0.69289899 -0.65391809 -0.30378103 0.76900005 -0.63908005
		 -0.01465 0.77852201 -0.52654505 -0.341546 0.85874408 -0.51138401 -0.032340001 0.53136998
		 -0.63966805 -0.55540198 0.60499108 -0.51201105 -0.60977906 -0.159594 -0.21138902
		 -0.964284 0.12803601 -0.27613702 -0.95255202 -0.12939101 -0.068138011 -0.98925006
		 0.162082 -0.131065 -0.97803408 0.45105502 -0.18431002 -0.87325799 0.41263899 -0.33233404
		 -0.84810603 -0.66582304 -0.078497007 -0.74196905 -0.42933002 -0.143875 -0.89161408
		 -0.64126498 0.066234998 -0.76445508 -0.40231201 -0.000994 -0.91550201 -0.97007203
		 0.030646 -0.24087501 -0.85288101 -0.018633002 -0.52177298 -0.94846404 0.183082 -0.25864601
		 -0.83017409 0.12941501 -0.54227602 -0.91286999 0.076209001 0.40107301 -0.99478906
		 0.064212002 0.079191998 -0.89024407 0.23370102 0.39095899 -0.97329801 0.22013201
		 0.065053999 -0.47863701 0.031860001 0.87743503 -0.73115307 0.064862996 0.67912406
		 -0.45105502 0.18431002 0.87325799 -0.70632797 0.220792 0.67257106 0.096335001 -0.076614998
		 0.99239606 -0.192423 -0.017002 0.98116505 0.12939101 0.068139002 0.98925006 -0.162082
		 0.131065 0.97803408;
	setAttr ".n[166:331]" -type "float3"  0.60256308 -0.20950602 0.77008098 0.36655802
		 -0.141909 0.91950899 0.64126498 -0.066234998 0.76445508 0.40231201 0.000994 0.91550201
		 0.90407407 -0.33112004 0.27020401 0.78849405 -0.27450499 0.55038601 0.94846404 -0.183082
		 0.25864601 0.83017409 -0.12941501 0.54227602 0.84499007 -0.38525203 -0.37090799 0.92750198
		 -0.37055501 -0.049291 0.89024407 -0.23370102 -0.39095899 0.97329801 -0.22013201 -0.065053999
		 0.66386503 -0.371207 -0.64922208 0.70632899 -0.220792 -0.67256999 -0.096335001 0.076614998
		 -0.99239606 0.192423 0.017002 -0.98116505 -0.061035998 0.22013801 -0.973557 0.21840702
		 0.164929 -0.96182007 0.49471602 0.12125601 -0.86055398 0.47863701 -0.031860001 -0.87743407
		 -0.60256398 0.209507 -0.77008098 -0.36655802 0.141909 -0.91950899 -0.55038202 0.34859803
		 -0.75865602 -0.32265604 0.282276 -0.90344507 -0.90407407 0.33112004 -0.27020401 -0.78849405
		 0.274506 -0.550385 -0.83801901 0.47111601 -0.275271 -0.72867703 0.413551 -0.54589802
		 -0.84499007 0.38525203 0.37090799 -0.92750108 0.37055501 0.049291 -0.77852201 0.52654505
		 0.341546 -0.85874408 0.51138401 0.032340001 -0.41263899 0.33233404 0.84810603 -0.66386503
		 0.371207 0.64922208 -0.36434603 0.47228602 0.80261904 -0.60499108 0.51201105 0.60977906
		 0.159594 0.21138902 0.964284 -0.12803601 0.27613702 0.95255202 0.18635701 0.35041803
		 0.91786605 -0.090999007 0.415126 0.90520108 0.66582304 0.078497998 0.74196905 0.42933002
		 0.143875 0.89161408 0.67570299 0.22195801 0.70296508 0.44707602 0.28417799 0.84815502
		 0.97007203 -0.030646 0.24087501 0.85288101 0.018633002 0.52177298 0.96838897 0.122425
		 0.217336 0.85608506 0.16650401 0.48927999 0.91286999 -0.076209001 -0.40107301 0.99478906
		 -0.064212002 -0.079191998 0.91233498 0.082672 -0.40101102 0.99147701 0.092916004
		 -0.091325007 0.73115307 -0.064862996 -0.67912298 0.73772502 0.092289999 -0.668764
		 -0.024102001 0.359797 -0.93271905 0.23946501 0.30971199 -0.92018205 0.013683 0.49238604
		 -0.87026906 0.25503299 0.44786203 -0.85695904 0.49120101 0.414857 -0.765908 0.49892804
		 0.27146804 -0.82302904 -0.48545104 0.48090699 -0.73011303 -0.271207 0.41762504 -0.86720008
		 -0.40891603 0.603324 -0.684681 -0.21310399 0.54489499 -0.81097203 -0.751858 0.59981602
		 -0.273734 -0.65177 0.54367203 -0.52878797 -0.64791107 0.71388906 -0.26565599 -0.55938399
		 0.66165698 -0.49930003 -0.69289899 0.65391809 0.30378103 -0.76900005 0.639081 0.01465
		 -0.59100705 0.76399505 0.25888601 -0.66111004 0.75028104 -0.003274 -0.30731103 0.60091406
		 0.73787707 -0.53136998 0.63966805 0.55540198 -0.243055 0.71488899 0.655635 -0.44529003
		 0.75081408 0.48784703 0.20913699 0.48262304 0.85049206 -0.051696002 0.54515499 0.83674008
		 0.22733201 0.60489601 0.76316506 -0.011032 0.66301107 0.748528 0.67048699 0.36151302
		 0.64788598 0.455062 0.41941899 0.78549701 0.64993107 0.493958 0.57757705 0.45283499
		 0.54654002 0.70443898 0.94347501 0.27256599 0.188583 0.83953905 0.311194 0.44534603
		 0.89605707 0.41585699 0.155384 0.80338401 0.44921601 0.39087 0.88895202 0.23866101
		 -0.39090401 0.96367007 0.24720001 -0.101159 0.84389007 0.38731599 -0.371263 0.91253
		 0.39436904 -0.10845301 0.72603899 0.246613 -0.64191097 0.69670999 0.39383501 -0.59957403
		 0.051599003 0.61507004 -0.78678209 0.264696 0.57639605 -0.77311301 0.088582002 0.72410405
		 -0.68397808 0.26810199 0.69155502 -0.670726 0.44125202 0.66799206 -0.59923601 0.471755
		 0.54827398 -0.69053805 -0.32193503 0.71312797 -0.62274098 -0.14923 0.661313 -0.735116
		 -0.22664201 0.80685502 -0.54554409 -0.081156008 0.763219 -0.64102304 -0.52855402
		 0.81086904 -0.25124201 -0.45318902 0.76485103 -0.45784703 -0.39733702 0.88813299
		 -0.23096099 -0.33599201 0.85013807 -0.40543202 -0.47571903 0.85461998 0.208124 -0.53795499
		 0.84271204 -0.021008 -0.350842 0.92382199 0.15317301 -0.40348503 0.91419506 -0.038046002
		 -0.17303002 0.81174707 0.55778801 -0.34901202 0.84317905 0.40895104 -0.099290997
		 0.88886899 0.44727299 -0.24557699 0.91458499 0.32128799 0.24044199 0.71451706 0.65700406
		 0.030168002 0.76604402 0.642079 0.24794702 0.80802703 0.53442901 0.070748001 0.85114205
		 0.52014601 0.613976 0.61645907 0.49296302 0.44006103 0.66276908 0.605874 0.56317103
		 0.72527605 0.395996 0.41670504 0.76444906 0.491909 0.82727903 0.54915202 0.118493
		 0.74805301 0.57758999 0.32681304 0.73929799 0.66872907 0.078998998 0.674842 0.69256002
		 0.254852 0.77881306 0.525289 -0.34281501 0.83971399 0.53112209 -0.113089 0.69629407
		 0.64893502 -0.306687 0.74788803 0.65378803 -0.115002 0.65077102 0.53065598 -0.54304898
		 0.58998102 0.65339708 -0.47433603 0.121991 0.81227803 -0.57037103 0.26540101 0.78633702
		 -0.557886 0.15216102 0.88152999 -0.44693699 0.25749701 0.86055905 -0.43946999 0.357519
		 0.846901 -0.39362299 0.40286201 0.76663703 -0.49996999 -0.13041702 0.87853801 -0.45952299
		 -0.013719001 0.84419203 -0.53586507 -0.033330999 0.930224 -0.36547601 0.051038001
		 0.90411603 -0.424229 -0.264732 0.94188905 -0.20679002 -0.216426 0.91282201 -0.34628701
		 -0.130777 0.97508502 -0.17918402 -0.098488003 0.95400906 -0.28313601 -0.22634201
		 0.96906406 0.098413005 -0.26780701 0.96199602 -0.053315002 -0.101987 0.99382401 0.043739002
		 -0.135179 0.98857701 -0.066648997 -0.02746 0.94247508 0.33314699 -0.14261001 0.96230507
		 0.231583 0.042769998 0.97551405 0.21574 -0.043114003 0.98880404 0.14285301 0.24959901
		 0.87947702 0.40524104 0.107991 0.91362405 0.391956 0.245938 0.93091297 0.27002701
		 0.14119901 0.95460099 0.26229504 0.50200707 0.81321698 0.29439402 0.38478404 0.84517705
		 0.37096903 0.43143004 0.88221902 0.188567 0.34629604 0.90484506 0.247659 0.64013398
		 0.767223 0.039967 0.589818 0.78713804 0.18035701;
	setAttr ".n[332:381]" -type "float3"  0.531066 0.84732997 0.001301 0.49718401
		 0.86115098 0.10596101 0.60415906 0.751046 -0.26631001 0.64505804 0.75553209 -0.11433001
		 0.50364804 0.83483708 -0.222232 0.53610802 0.83675104 -0.111518 0.51986098 0.75522298
		 -0.39922804 0.44404304 0.83652306 -0.32102099 -0.13570002 -0.98941505 -0.051421005
		 -0.17551902 -0.97842598 -0.108973 -0.21356501 -0.97230798 0.094905004 -0.232748 -0.96941507
		 -0.077868007 -0.29384503 -0.95051008 -0.100927 -0.32140502 -0.94614106 -0.038933001
		 -0.38029 -0.92467105 -0.019046001 -0.36809701 -0.92840707 0.050639 -0.40170103 -0.90962797
		 0.10589001 -0.35450301 -0.92181706 0.156785 -0.34894201 -0.90949798 0.22595002 -0.28550002
		 -0.92820305 0.23859602 -0.24241601 -0.92433107 0.29469904 -0.18792701 -0.94581097
		 0.26481 -0.12361701 -0.95008898 0.28644201 -0.099270009 -0.96908498 0.22587602 -0.037645999
		 -0.97808599 0.20477101 -0.053103 -0.98921108 0.13653702 -0.017005002 -0.99663508
		 0.080177002 -0.067023002 -0.997284 0.030534999 -0.069764003 -0.99676597 -0.039882999
		 0.18792701 0.94581097 -0.26481 0.24241701 0.92433107 -0.29469803 0.21356501 0.97230798
		 -0.094905004 0.28550002 0.92820305 -0.23859602 0.099270009 0.96908498 -0.22587501
		 0.12361701 0.95008898 -0.28644201 0.053103 0.98921108 -0.13653702 0.037645999 0.97808599
		 -0.20477101 0.067023002 0.997284 -0.030534999 0.017005002 0.99663597 -0.080177002
		 0.13570002 0.98941505 0.051421005 0.069764003 0.99676597 0.039882999 0.232748 0.96941507
		 0.077868007 0.17551902 0.97842598 0.108973 0.32140502 0.94614106 0.038933001 0.29384503
		 0.95051008 0.100927 0.36809701 0.92840707 -0.050639 0.38029 0.92467105 0.019046001
		 0.35450301 0.92181706 -0.156785 0.40170103 0.90962797 -0.10589001 0.34894201 0.90949798
		 -0.22595002;
	setAttr -s 380 -ch 1520 ".fc[0:379]" -type "polyFaces" 
		f 4 0 1 2 3
		mu 0 4 0 1 2 3
		f 4 4 5 6 -3
		mu 0 4 2 4 5 3
		f 4 7 8 9 -7
		mu 0 4 5 6 7 3
		f 4 10 11 -4 -10
		mu 0 4 7 8 0 3
		f 4 12 13 14 15
		mu 0 4 9 10 11 12
		f 4 16 17 18 -15
		mu 0 4 11 13 14 12
		f 4 19 -5 20 -19
		mu 0 4 14 4 2 12
		f 4 -2 21 -16 -21
		mu 0 4 2 1 9 12
		f 4 22 23 24 25
		mu 0 4 15 16 17 18
		f 4 26 27 28 -25
		mu 0 4 17 19 20 18
		f 4 29 -17 30 -29
		mu 0 4 20 13 11 18
		f 4 -14 31 -26 -31
		mu 0 4 11 10 15 18
		f 4 32 33 34 35
		mu 0 4 21 22 23 24
		f 4 36 37 38 -35
		mu 0 4 23 25 26 24
		f 4 39 -27 40 -39
		mu 0 4 26 19 17 24
		f 4 -24 41 -36 -41
		mu 0 4 17 16 21 24
		f 4 42 43 44 45
		mu 0 4 27 28 29 30
		f 4 46 47 48 -45
		mu 0 4 29 31 32 30
		f 4 49 -37 50 -49
		mu 0 4 32 25 23 30
		f 4 -34 51 -46 -51
		mu 0 4 23 22 27 30
		f 4 52 53 54 55
		mu 0 4 33 34 35 36
		f 4 56 57 58 -55
		mu 0 4 35 37 38 36
		f 4 59 -47 60 -59
		mu 0 4 38 31 29 36
		f 4 -44 61 -56 -61
		mu 0 4 29 28 33 36
		f 4 62 63 64 65
		mu 0 4 39 40 41 42
		f 4 66 67 68 -65
		mu 0 4 41 43 44 42
		f 4 69 -57 70 -69
		mu 0 4 44 37 35 42
		f 4 -54 71 -66 -71
		mu 0 4 35 34 39 42
		f 4 72 73 74 75
		mu 0 4 45 46 47 48
		f 4 76 77 78 -75
		mu 0 4 47 49 50 48
		f 4 79 -67 80 -79
		mu 0 4 50 43 41 48
		f 4 -64 81 -76 -81
		mu 0 4 41 40 45 48
		f 4 82 83 84 85
		mu 0 4 51 52 53 54
		f 4 86 87 88 -85
		mu 0 4 53 55 56 54
		f 4 89 -77 90 -89
		mu 0 4 56 49 47 54
		f 4 -74 91 -86 -91
		mu 0 4 47 46 51 54
		f 4 92 -11 93 94
		mu 0 4 57 58 59 60
		f 4 -9 95 96 -94
		mu 0 4 59 61 62 60
		f 4 97 -87 98 -97
		mu 0 4 62 55 53 60
		f 4 -84 99 -95 -99
		mu 0 4 53 52 57 60
		f 4 -6 100 101 102
		mu 0 4 5 4 63 64
		f 4 103 104 105 -102
		mu 0 4 63 65 66 64
		f 4 106 107 108 -106
		mu 0 4 66 67 68 64
		f 4 109 -8 -103 -109
		mu 0 4 68 6 5 64
		f 4 -18 110 111 112
		mu 0 4 14 13 69 70
		f 4 113 114 115 -112
		mu 0 4 69 71 72 70
		f 4 116 -104 117 -116
		mu 0 4 72 65 63 70
		f 4 -101 -20 -113 -118
		mu 0 4 63 4 14 70
		f 4 -28 118 119 120
		mu 0 4 20 19 73 74
		f 4 121 122 123 -120
		mu 0 4 73 75 76 74
		f 4 124 -114 125 -124
		mu 0 4 76 71 69 74
		f 4 -111 -30 -121 -126
		mu 0 4 69 13 20 74
		f 4 -38 126 127 128
		mu 0 4 26 25 77 78
		f 4 129 130 131 -128
		mu 0 4 77 79 80 78
		f 4 132 -122 133 -132
		mu 0 4 80 75 73 78
		f 4 -119 -40 -129 -134
		mu 0 4 73 19 26 78
		f 4 -48 134 135 136
		mu 0 4 32 31 81 82
		f 4 137 138 139 -136
		mu 0 4 81 83 84 82
		f 4 140 -130 141 -140
		mu 0 4 84 79 77 82
		f 4 -127 -50 -137 -142
		mu 0 4 77 25 32 82
		f 4 -58 142 143 144
		mu 0 4 38 37 85 86
		f 4 145 146 147 -144
		mu 0 4 85 87 88 86
		f 4 148 -138 149 -148
		mu 0 4 88 83 81 86
		f 4 -135 -60 -145 -150
		mu 0 4 81 31 38 86
		f 4 -68 150 151 152
		mu 0 4 44 43 89 90
		f 4 153 154 155 -152
		mu 0 4 89 91 92 90
		f 4 156 -146 157 -156
		mu 0 4 92 87 85 90
		f 4 -143 -70 -153 -158
		mu 0 4 85 37 44 90
		f 4 -78 158 159 160
		mu 0 4 50 49 93 94
		f 4 161 162 163 -160
		mu 0 4 93 95 96 94
		f 4 164 -154 165 -164
		mu 0 4 96 91 89 94
		f 4 -151 -80 -161 -166
		mu 0 4 89 43 50 94
		f 4 -88 166 167 168
		mu 0 4 56 55 97 98
		f 4 169 170 171 -168
		mu 0 4 97 99 100 98
		f 4 172 -162 173 -172
		mu 0 4 100 95 93 98
		f 4 -159 -90 -169 -174
		mu 0 4 93 49 56 98
		f 4 -96 -110 174 175
		mu 0 4 62 61 101 102
		f 4 -108 176 177 -175
		mu 0 4 101 103 104 102
		f 4 178 -170 179 -178
		mu 0 4 104 99 97 102
		f 4 -167 -98 -176 -180
		mu 0 4 97 55 62 102
		f 4 -105 180 181 182
		mu 0 4 66 65 105 106
		f 4 183 184 185 -182
		mu 0 4 105 107 108 106
		f 4 186 187 188 -186
		mu 0 4 108 109 110 106
		f 4 189 -107 -183 -189
		mu 0 4 110 67 66 106
		f 4 -115 190 191 192
		mu 0 4 72 71 111 112
		f 4 193 194 195 -192
		mu 0 4 111 113 114 112
		f 4 196 -184 197 -196
		mu 0 4 114 107 105 112
		f 4 -181 -117 -193 -198
		mu 0 4 105 65 72 112
		f 4 -123 198 199 200
		mu 0 4 76 75 115 116
		f 4 201 202 203 -200
		mu 0 4 115 117 118 116
		f 4 204 -194 205 -204
		mu 0 4 118 113 111 116
		f 4 -191 -125 -201 -206
		mu 0 4 111 71 76 116
		f 4 -131 206 207 208
		mu 0 4 80 79 119 120
		f 4 209 210 211 -208
		mu 0 4 119 121 122 120
		f 4 212 -202 213 -212
		mu 0 4 122 117 115 120
		f 4 -199 -133 -209 -214
		mu 0 4 115 75 80 120
		f 4 -139 214 215 216
		mu 0 4 84 83 123 124
		f 4 217 218 219 -216
		mu 0 4 123 125 126 124
		f 4 220 -210 221 -220
		mu 0 4 126 121 119 124
		f 4 -207 -141 -217 -222
		mu 0 4 119 79 84 124
		f 4 -147 222 223 224
		mu 0 4 88 87 127 128
		f 4 225 226 227 -224
		mu 0 4 127 129 130 128
		f 4 228 -218 229 -228
		mu 0 4 130 125 123 128
		f 4 -215 -149 -225 -230
		mu 0 4 123 83 88 128
		f 4 -155 230 231 232
		mu 0 4 92 91 131 132
		f 4 233 234 235 -232
		mu 0 4 131 133 134 132
		f 4 236 -226 237 -236
		mu 0 4 134 129 127 132
		f 4 -223 -157 -233 -238
		mu 0 4 127 87 92 132
		f 4 -163 238 239 240
		mu 0 4 96 95 135 136
		f 4 241 242 243 -240
		mu 0 4 135 137 138 136
		f 4 244 -234 245 -244
		mu 0 4 138 133 131 136
		f 4 -231 -165 -241 -246
		mu 0 4 131 91 96 136
		f 4 -171 246 247 248
		mu 0 4 100 99 139 140
		f 4 249 250 251 -248
		mu 0 4 139 141 142 140
		f 4 252 -242 253 -252
		mu 0 4 142 137 135 140
		f 4 -239 -173 -249 -254
		mu 0 4 135 95 100 140
		f 4 -177 -190 254 255
		mu 0 4 104 103 143 144
		f 4 -188 256 257 -255
		mu 0 4 143 145 146 144
		f 4 258 -250 259 -258
		mu 0 4 146 141 139 144
		f 4 -247 -179 -256 -260
		mu 0 4 139 99 104 144
		f 4 -185 260 261 262
		mu 0 4 108 107 147 148
		f 4 263 264 265 -262
		mu 0 4 147 149 150 148
		f 4 266 267 268 -266
		mu 0 4 150 151 152 148
		f 4 269 -187 -263 -269
		mu 0 4 152 109 108 148
		f 4 -195 270 271 272
		mu 0 4 114 113 153 154
		f 4 273 274 275 -272
		mu 0 4 153 155 156 154
		f 4 276 -264 277 -276
		mu 0 4 156 149 147 154
		f 4 -261 -197 -273 -278
		mu 0 4 147 107 114 154
		f 4 -203 278 279 280
		mu 0 4 118 117 157 158
		f 4 281 282 283 -280
		mu 0 4 157 159 160 158
		f 4 284 -274 285 -284
		mu 0 4 160 155 153 158
		f 4 -271 -205 -281 -286
		mu 0 4 153 113 118 158
		f 4 -211 286 287 288
		mu 0 4 122 121 161 162
		f 4 289 290 291 -288
		mu 0 4 161 163 164 162
		f 4 292 -282 293 -292
		mu 0 4 164 159 157 162
		f 4 -279 -213 -289 -294
		mu 0 4 157 117 122 162
		f 4 -219 294 295 296
		mu 0 4 126 125 165 166
		f 4 297 298 299 -296
		mu 0 4 165 167 168 166
		f 4 300 -290 301 -300
		mu 0 4 168 163 161 166
		f 4 -287 -221 -297 -302
		mu 0 4 161 121 126 166
		f 4 -227 302 303 304
		mu 0 4 130 129 169 170
		f 4 305 306 307 -304
		mu 0 4 169 171 172 170
		f 4 308 -298 309 -308
		mu 0 4 172 167 165 170
		f 4 -295 -229 -305 -310
		mu 0 4 165 125 130 170
		f 4 -235 310 311 312
		mu 0 4 134 133 173 174
		f 4 313 314 315 -312
		mu 0 4 173 175 176 174
		f 4 316 -306 317 -316
		mu 0 4 176 171 169 174
		f 4 -303 -237 -313 -318
		mu 0 4 169 129 134 174
		f 4 -243 318 319 320
		mu 0 4 138 137 177 178
		f 4 321 322 323 -320
		mu 0 4 177 179 180 178
		f 4 324 -314 325 -324
		mu 0 4 180 175 173 178
		f 4 -311 -245 -321 -326
		mu 0 4 173 133 138 178
		f 4 -251 326 327 328
		mu 0 4 142 141 181 182
		f 4 329 330 331 -328
		mu 0 4 181 183 184 182
		f 4 332 -322 333 -332
		mu 0 4 184 179 177 182
		f 4 -319 -253 -329 -334
		mu 0 4 177 137 142 182
		f 4 -257 -270 334 335
		mu 0 4 146 145 185 186
		f 4 -268 336 337 -335
		mu 0 4 185 187 188 186
		f 4 338 -330 339 -338
		mu 0 4 188 183 181 186
		f 4 -327 -259 -336 -340
		mu 0 4 181 141 146 186
		f 4 -265 340 341 342
		mu 0 4 150 149 189 190
		f 4 343 344 345 -342
		mu 0 4 189 191 192 190
		f 4 346 347 348 -346
		mu 0 4 192 193 194 190
		f 4 349 -267 -343 -349
		mu 0 4 194 151 150 190
		f 4 -275 350 351 352
		mu 0 4 156 155 195 196
		f 4 353 354 355 -352
		mu 0 4 195 197 198 196
		f 4 356 -344 357 -356
		mu 0 4 198 191 189 196
		f 4 -341 -277 -353 -358
		mu 0 4 189 149 156 196
		f 4 -283 358 359 360
		mu 0 4 160 159 199 200
		f 4 361 362 363 -360
		mu 0 4 199 201 202 200
		f 4 364 -354 365 -364
		mu 0 4 202 197 195 200
		f 4 -351 -285 -361 -366
		mu 0 4 195 155 160 200
		f 4 -291 366 367 368
		mu 0 4 164 163 203 204
		f 4 369 370 371 -368
		mu 0 4 203 205 206 204
		f 4 372 -362 373 -372
		mu 0 4 206 201 199 204
		f 4 -359 -293 -369 -374
		mu 0 4 199 159 164 204
		f 4 -299 374 375 376
		mu 0 4 168 167 207 208
		f 4 377 378 379 -376
		mu 0 4 207 209 210 208
		f 4 380 -370 381 -380
		mu 0 4 210 205 203 208
		f 4 -367 -301 -377 -382
		mu 0 4 203 163 168 208
		f 4 -307 382 383 384
		mu 0 4 172 171 211 212
		f 4 385 386 387 -384
		mu 0 4 211 213 214 212
		f 4 388 -378 389 -388
		mu 0 4 214 209 207 212
		f 4 -375 -309 -385 -390
		mu 0 4 207 167 172 212
		f 4 -315 390 391 392
		mu 0 4 176 175 215 216
		f 4 393 394 395 -392
		mu 0 4 215 217 218 216
		f 4 396 -386 397 -396
		mu 0 4 218 213 211 216
		f 4 -383 -317 -393 -398
		mu 0 4 211 171 176 216
		f 4 -323 398 399 400
		mu 0 4 180 179 219 220
		f 4 401 402 403 -400
		mu 0 4 219 221 222 220
		f 4 404 -394 405 -404
		mu 0 4 222 217 215 220
		f 4 -391 -325 -401 -406
		mu 0 4 215 175 180 220
		f 4 -331 406 407 408
		mu 0 4 184 183 223 224
		f 4 409 410 411 -408
		mu 0 4 223 225 226 224
		f 4 412 -402 413 -412
		mu 0 4 226 221 219 224
		f 4 -399 -333 -409 -414
		mu 0 4 219 179 184 224
		f 4 -337 -350 414 415
		mu 0 4 188 187 227 228
		f 4 -348 416 417 -415
		mu 0 4 227 229 230 228
		f 4 418 -410 419 -418
		mu 0 4 230 225 223 228
		f 4 -407 -339 -416 -420
		mu 0 4 223 183 188 228
		f 4 -345 420 421 422
		mu 0 4 192 191 231 232
		f 4 423 424 425 -422
		mu 0 4 231 233 234 232
		f 4 426 427 428 -426
		mu 0 4 234 235 236 232
		f 4 429 -347 -423 -429
		mu 0 4 236 193 192 232
		f 4 -355 430 431 432
		mu 0 4 198 197 237 238
		f 4 433 434 435 -432
		mu 0 4 237 239 240 238
		f 4 436 -424 437 -436
		mu 0 4 240 233 231 238
		f 4 -421 -357 -433 -438
		mu 0 4 231 191 198 238
		f 4 -363 438 439 440
		mu 0 4 202 201 241 242
		f 4 441 442 443 -440
		mu 0 4 241 243 244 242
		f 4 444 -434 445 -444
		mu 0 4 244 239 237 242
		f 4 -431 -365 -441 -446
		mu 0 4 237 197 202 242
		f 4 -371 446 447 448
		mu 0 4 206 205 245 246
		f 4 449 450 451 -448
		mu 0 4 245 247 248 246
		f 4 452 -442 453 -452
		mu 0 4 248 243 241 246
		f 4 -439 -373 -449 -454
		mu 0 4 241 201 206 246
		f 4 -379 454 455 456
		mu 0 4 210 209 249 250
		f 4 457 458 459 -456
		mu 0 4 249 251 252 250
		f 4 460 -450 461 -460
		mu 0 4 252 247 245 250
		f 4 -447 -381 -457 -462
		mu 0 4 245 205 210 250
		f 4 -387 462 463 464
		mu 0 4 214 213 253 254
		f 4 465 466 467 -464
		mu 0 4 253 255 256 254
		f 4 468 -458 469 -468
		mu 0 4 256 251 249 254
		f 4 -455 -389 -465 -470
		mu 0 4 249 209 214 254
		f 4 -395 470 471 472
		mu 0 4 218 217 257 258
		f 4 473 474 475 -472
		mu 0 4 257 259 260 258
		f 4 476 -466 477 -476
		mu 0 4 260 255 253 258
		f 4 -463 -397 -473 -478
		mu 0 4 253 213 218 258
		f 4 -403 478 479 480
		mu 0 4 222 221 261 262
		f 4 481 482 483 -480
		mu 0 4 261 263 264 262
		f 4 484 -474 485 -484
		mu 0 4 264 259 257 262
		f 4 -471 -405 -481 -486
		mu 0 4 257 217 222 262
		f 4 -411 486 487 488
		mu 0 4 226 225 265 266
		f 4 489 490 491 -488
		mu 0 4 265 267 268 266
		f 4 492 -482 493 -492
		mu 0 4 268 263 261 266
		f 4 -479 -413 -489 -494
		mu 0 4 261 221 226 266
		f 4 -417 -430 494 495
		mu 0 4 230 229 269 270
		f 4 -428 496 497 -495
		mu 0 4 269 271 272 270
		f 4 498 -490 499 -498
		mu 0 4 272 267 265 270
		f 4 -487 -419 -496 -500
		mu 0 4 265 225 230 270
		f 4 -425 500 501 502
		mu 0 4 234 233 273 274
		f 4 503 504 505 -502
		mu 0 4 273 275 276 274
		f 4 506 507 508 -506
		mu 0 4 276 277 278 274
		f 4 509 -427 -503 -509
		mu 0 4 278 235 234 274
		f 4 -435 510 511 512
		mu 0 4 240 239 279 280
		f 4 513 514 515 -512
		mu 0 4 279 281 282 280
		f 4 516 -504 517 -516
		mu 0 4 282 275 273 280
		f 4 -501 -437 -513 -518
		mu 0 4 273 233 240 280
		f 4 -443 518 519 520
		mu 0 4 244 243 283 284
		f 4 521 522 523 -520
		mu 0 4 283 285 286 284
		f 4 524 -514 525 -524
		mu 0 4 286 281 279 284
		f 4 -511 -445 -521 -526
		mu 0 4 279 239 244 284
		f 4 -451 526 527 528
		mu 0 4 248 247 287 288
		f 4 529 530 531 -528
		mu 0 4 287 289 290 288
		f 4 532 -522 533 -532
		mu 0 4 290 285 283 288
		f 4 -519 -453 -529 -534
		mu 0 4 283 243 248 288
		f 4 -459 534 535 536
		mu 0 4 252 251 291 292
		f 4 537 538 539 -536
		mu 0 4 291 293 294 292
		f 4 540 -530 541 -540
		mu 0 4 294 289 287 292
		f 4 -527 -461 -537 -542
		mu 0 4 287 247 252 292
		f 4 -467 542 543 544
		mu 0 4 256 255 295 296
		f 4 545 546 547 -544
		mu 0 4 295 297 298 296
		f 4 548 -538 549 -548
		mu 0 4 298 293 291 296
		f 4 -535 -469 -545 -550
		mu 0 4 291 251 256 296
		f 4 -475 550 551 552
		mu 0 4 260 259 299 300
		f 4 553 554 555 -552
		mu 0 4 299 301 302 300
		f 4 556 -546 557 -556
		mu 0 4 302 297 295 300
		f 4 -543 -477 -553 -558
		mu 0 4 295 255 260 300
		f 4 -483 558 559 560
		mu 0 4 264 263 303 304
		f 4 561 562 563 -560
		mu 0 4 303 305 306 304
		f 4 564 -554 565 -564
		mu 0 4 306 301 299 304
		f 4 -551 -485 -561 -566
		mu 0 4 299 259 264 304
		f 4 -491 566 567 568
		mu 0 4 268 267 307 308
		f 4 569 570 571 -568
		mu 0 4 307 309 310 308
		f 4 572 -562 573 -572
		mu 0 4 310 305 303 308
		f 4 -559 -493 -569 -574
		mu 0 4 303 263 268 308
		f 4 -497 -510 574 575
		mu 0 4 272 271 311 312
		f 4 -508 576 577 -575
		mu 0 4 311 313 314 312
		f 4 578 -570 579 -578
		mu 0 4 314 309 307 312
		f 4 -567 -499 -576 -580
		mu 0 4 307 267 272 312
		f 4 -505 580 581 582
		mu 0 4 276 275 315 316
		f 4 583 584 585 -582
		mu 0 4 315 317 318 316
		f 4 586 587 588 -586
		mu 0 4 318 319 320 316
		f 4 589 -507 -583 -589
		mu 0 4 320 277 276 316
		f 4 -515 590 591 592
		mu 0 4 282 281 321 322
		f 4 593 594 595 -592
		mu 0 4 321 323 324 322
		f 4 596 -584 597 -596
		mu 0 4 324 317 315 322
		f 4 -581 -517 -593 -598
		mu 0 4 315 275 282 322
		f 4 -523 598 599 600
		mu 0 4 286 285 325 326
		f 4 601 602 603 -600
		mu 0 4 325 327 328 326
		f 4 604 -594 605 -604
		mu 0 4 328 323 321 326
		f 4 -591 -525 -601 -606
		mu 0 4 321 281 286 326
		f 4 -531 606 607 608
		mu 0 4 290 289 329 330
		f 4 609 610 611 -608
		mu 0 4 329 331 332 330
		f 4 612 -602 613 -612
		mu 0 4 332 327 325 330
		f 4 -599 -533 -609 -614
		mu 0 4 325 285 290 330
		f 4 -539 614 615 616
		mu 0 4 294 293 333 334
		f 4 617 618 619 -616
		mu 0 4 333 335 336 334
		f 4 620 -610 621 -620
		mu 0 4 336 331 329 334
		f 4 -607 -541 -617 -622
		mu 0 4 329 289 294 334
		f 4 -547 622 623 624
		mu 0 4 298 297 337 338
		f 4 625 626 627 -624
		mu 0 4 337 339 340 338
		f 4 628 -618 629 -628
		mu 0 4 340 335 333 338
		f 4 -615 -549 -625 -630
		mu 0 4 333 293 298 338
		f 4 -555 630 631 632
		mu 0 4 302 301 341 342
		f 4 633 634 635 -632
		mu 0 4 341 343 344 342
		f 4 636 -626 637 -636
		mu 0 4 344 339 337 342
		f 4 -623 -557 -633 -638
		mu 0 4 337 297 302 342
		f 4 -563 638 639 640
		mu 0 4 306 305 345 346
		f 4 641 642 643 -640
		mu 0 4 345 347 348 346
		f 4 644 -634 645 -644
		mu 0 4 348 343 341 346
		f 4 -631 -565 -641 -646
		mu 0 4 341 301 306 346
		f 4 -571 646 647 648
		mu 0 4 310 309 349 350
		f 4 649 650 651 -648
		mu 0 4 349 351 352 350
		f 4 652 -642 653 -652
		mu 0 4 352 347 345 350
		f 4 -639 -573 -649 -654
		mu 0 4 345 305 310 350
		f 4 -577 -590 654 655
		mu 0 4 314 313 353 354
		f 4 -588 656 657 -655
		mu 0 4 353 355 356 354
		f 4 658 -650 659 -658
		mu 0 4 356 351 349 354
		f 4 -647 -579 -656 -660
		mu 0 4 349 309 314 354
		f 4 -12 660 661 662
		mu 0 4 0 8 357 358
		f 4 663 664 665 -662
		mu 0 4 357 359 360 358
		f 4 666 -1 -663 -666
		mu 0 4 360 1 0 358
		f 4 -22 -667 667 668
		mu 0 4 9 1 361 362
		f 4 -665 669 670 -668
		mu 0 4 361 363 364 362
		f 4 671 -13 -669 -671
		mu 0 4 364 10 9 362
		f 4 -32 -672 672 673
		mu 0 4 15 10 365 366
		f 4 -670 674 675 -673
		mu 0 4 365 367 368 366
		f 4 676 -23 -674 -676
		mu 0 4 368 16 15 366
		f 4 -42 -677 677 678
		mu 0 4 21 16 369 370
		f 4 -675 679 680 -678
		mu 0 4 369 371 372 370
		f 4 681 -33 -679 -681
		mu 0 4 372 22 21 370
		f 4 -52 -682 682 683
		mu 0 4 27 22 373 374
		f 4 -680 684 685 -683
		mu 0 4 373 375 376 374
		f 4 686 -43 -684 -686
		mu 0 4 376 28 27 374
		f 4 -62 -687 687 688
		mu 0 4 33 28 377 378
		f 4 -685 689 690 -688
		mu 0 4 377 379 380 378
		f 4 691 -53 -689 -691
		mu 0 4 380 34 33 378
		f 4 -72 -692 692 693
		mu 0 4 39 34 381 382
		f 4 -690 694 695 -693
		mu 0 4 381 383 384 382
		f 4 696 -63 -694 -696
		mu 0 4 384 40 39 382
		f 4 -82 -697 697 698
		mu 0 4 45 40 385 386
		f 4 -695 699 700 -698
		mu 0 4 385 387 388 386
		f 4 701 -73 -699 -701
		mu 0 4 388 46 45 386
		f 4 -92 -702 702 703
		mu 0 4 51 46 389 390
		f 4 -700 704 705 -703
		mu 0 4 389 391 392 390
		f 4 706 -83 -704 -706
		mu 0 4 392 52 51 390
		f 4 -100 -707 707 708
		mu 0 4 57 52 393 394
		f 4 -705 -664 709 -708
		mu 0 4 393 395 396 394
		f 4 -661 -93 -709 -710
		mu 0 4 396 58 57 394
		f 4 -585 710 711 712
		mu 0 4 318 317 397 398
		f 4 713 714 715 -712
		mu 0 4 397 399 400 398
		f 4 716 -587 -713 -716
		mu 0 4 400 319 318 398
		f 4 -595 717 718 719
		mu 0 4 324 323 401 402
		f 4 720 -714 721 -719
		mu 0 4 401 403 404 402
		f 4 -711 -597 -720 -722
		mu 0 4 404 317 324 402
		f 4 -603 722 723 724
		mu 0 4 328 327 405 406
		f 4 725 -721 726 -724
		mu 0 4 405 407 408 406
		f 4 -718 -605 -725 -727
		mu 0 4 408 323 328 406
		f 4 -611 727 728 729
		mu 0 4 332 331 409 410
		f 4 730 -726 731 -729
		mu 0 4 409 411 412 410
		f 4 -723 -613 -730 -732
		mu 0 4 412 327 332 410
		f 4 -619 732 733 734
		mu 0 4 336 335 413 414
		f 4 735 -731 736 -734
		mu 0 4 413 415 416 414
		f 4 -728 -621 -735 -737
		mu 0 4 416 331 336 414
		f 4 -627 737 738 739
		mu 0 4 340 339 417 418
		f 4 740 -736 741 -739
		mu 0 4 417 419 420 418
		f 4 -733 -629 -740 -742
		mu 0 4 420 335 340 418
		f 4 -635 742 743 744
		mu 0 4 344 343 421 422
		f 4 745 -741 746 -744
		mu 0 4 421 423 424 422
		f 4 -738 -637 -745 -747
		mu 0 4 424 339 344 422
		f 4 -643 747 748 749
		mu 0 4 348 347 425 426
		f 4 750 -746 751 -749
		mu 0 4 425 427 428 426
		f 4 -743 -645 -750 -752
		mu 0 4 428 343 348 426
		f 4 -651 752 753 754
		mu 0 4 352 351 429 430
		f 4 755 -751 756 -754
		mu 0 4 429 431 432 430
		f 4 -748 -653 -755 -757
		mu 0 4 432 347 352 430
		f 4 -657 -717 757 758
		mu 0 4 356 355 433 434
		f 4 -715 -756 759 -758
		mu 0 4 433 435 436 434
		f 4 -753 -659 -759 -760
		mu 0 4 436 351 356 434;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".dr" 3;
	setAttr ".dsm" 2;
	setAttr ".ai_translator" -type "string" "polymesh";
	setAttr -cb on ".rsEnableSubdivision" yes;
	setAttr -k on ".rsScreenSpaceAdaptive" no;
	setAttr -k on ".rsMinTessellationLength" 0;
	setAttr -k on ".rsMaxTessellationSubdivs" 4;
	setAttr -cb on ".rsEnableDisplacement" yes;
createNode transform -n "logo_geo_grp";
	rename -uid "50CB6A17-4D38-99F6-8CDB-A8A9C4750FFF";
	setAttr ".t" -type "double3" 0 0 0.050419364459210136 ;
	setAttr ".s" -type "double3" 0.88358969684426003 0.88358969684426003 0.88358969684426003 ;
	setAttr ".rp" -type "double3" 0 0 6.1311351609878719e-018 ;
	setAttr ".sp" -type "double3" 0 0 6.9388939039072284e-018 ;
	setAttr ".spt" -type "double3" 0 0 -8.0775874291935627e-019 ;
createNode transform -n "Arnold_Logo" -p "logo_geo_grp";
	rename -uid "422479C0-4FCC-A4BA-9F27-3DA01030DFCB";
	setAttr ".rp" -type "double3" 9.1597046852111816 11.030832290649414 -2.3856381177902222 ;
	setAttr ".sp" -type "double3" 9.1597046852111816 11.030832290649414 -2.3856381177902222 ;
createNode mesh -n "Arnold_LogoShape" -p "Arnold_Logo";
	rename -uid "19426D9A-4E83-2D1F-499B-C0AF09845ED1";
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
		-dv 4 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -k true -sn "rsMaxTessellationSubdivs" -ln "rsMaxTessellationSubdivs" 
		-dv 6 -min 0 -max 16 -at "long";
	addAttr -ci true -k true -sn "rsOutOfFrustumTessellationFactor" -ln "rsOutOfFrustumTessellationFactor" 
		-dv 4 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 32 -at "double";
	addAttr -ci true -sn "rsSubdivisionRule" -ln "rsSubdivisionRule" -min 0 -max 1 -en 
		"Catmull-Clark + Loop:Catmull-Clark Only" -at "enum";
	addAttr -ci true -sn "rsEnableDisplacement" -ln "rsEnableDisplacement" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -k true -sn "rsMaxDisplacement" -ln "rsMaxDisplacement" -dv 1 -min 
		0 -max 3.4028234600000001e+038 -smn 0 -smx 1000 -at "double";
	addAttr -ci true -k true -sn "rsDisplacementScale" -ln "rsDisplacementScale" -dv 
		1 -min 0 -max 3.4028234600000001e+038 -smn 0 -smx 1000 -at "double";
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
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".dr" 1;
	setAttr ".ai_opaque" no;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "directionalLight1";
	rename -uid "ACEE6A5A-4F72-D3A3-FCCE-678C2953B369";
	setAttr ".t" -type "double3" 5.5511151231257827e-017 7.4536028044484146 -14.930710822325572 ;
	setAttr ".r" -type "double3" -82.892 123.57400000000001 -19.734 ;
	setAttr ".s" -type "double3" 5.2433391155213416 5.2433391155213416 5.2433391155213416 ;
createNode directionalLight -n "directionalLightShape1" -p "directionalLight1";
	rename -uid "961BD63B-4507-25C6-CE61-8EAE1303036A";
	addAttr -ci true -sn "rsEmitCausticPhotons" -ln "rsEmitCausticPhotons" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsEmitGIPhotons" -ln "rsEmitGIPhotons" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "rsPhotonCausticsMultiplier" -ln "rsPhotonCausticsMultiplier" 
		-dv 1 -min 0 -max 1.7976931348623157e+308 -at "double";
	addAttr -ci true -sn "rsPhotonGIMultiplier" -ln "rsPhotonGIMultiplier" -dv 1 -min 
		0 -max 1.7976931348623157e+308 -at "double";
	addAttr -ci true -sn "rsCausticPhotons" -ln "rsCausticPhotons" -dv 10000 -min 0 
		-max 2147483647 -at "long";
	addAttr -ci true -sn "rsGIPhotons" -ln "rsGIPhotons" -dv 10000 -min 0 -max 2147483647 
		-at "long";
	addAttr -s false -ci true -sn "rsLightShader" -ln "rsLightShader" -at "message";
	addAttr -s false -ci true -sn "rsPhotonShader" -ln "rsPhotonShader" -at "message";
	setAttr -k off ".v";
	setAttr ".in" 0.30000001192092896;
createNode transform -n "aiSkyDomeLight1";
	rename -uid "058BC1AF-4607-4368-A96D-C09F4FEB5C45";
createNode aiSkyDomeLight -n "aiSkyDomeLightShape1" -p "aiSkyDomeLight1";
	rename -uid "8FF3F771-455A-5EB7-7491-01BC56D8C59A";
	setAttr -k off ".v";
	setAttr ".resolution" 500;
	setAttr ".ai_samples" 4;
	setAttr ".ai_volume_samples" 0;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "84E1C94F-41FE-8EAC-2A92-55B9FAC6E715";
	setAttr -s 6 ".lnk";
	setAttr -s 6 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "38EAA577-4624-4779-24D8-54A6619BED76";
createNode displayLayer -n "defaultLayer";
	rename -uid "F3D45A43-43AD-FEE0-3BA0-089F4C92C46F";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "F2838478-4FDD-2C41-FE87-EC8D437425F9";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "D008FCA9-4EC2-C45E-1B91-928F660CE3B4";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "5315FCCC-419C-839B-1CEB-AB990290A7AA";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 8192\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 8192\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n"
		+ "            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n"
		+ "                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 8192\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n"
		+ "            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 8192\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n"
		+ "            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 8192\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n"
		+ "                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n"
		+ "                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n"
		+ "                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 8192\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n"
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"renderCam\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n"
		+ "                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 1\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 8192\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n"
		+ "                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n"
		+ "                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1366\n                -height 768\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"renderCam\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 8192\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1366\n            -height 768\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 0\n                -showReferenceMembers 1\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n"
		+ "                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n"
		+ "                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 0\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n"
		+ "            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n"
		+ "            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n"
		+ "                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n"
		+ "                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.041667\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n"
		+ "                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n"
		+ "                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.041667\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n"
		+ "                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n"
		+ "                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n"
		+ "                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n"
		+ "                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n"
		+ "                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n"
		+ "                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n"
		+ "                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n"
		+ "                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n"
		+ "                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"ffxPanel\" (localizedPanelLabel(\"FumeFX Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"ffxPanel\" -l (localizedPanelLabel(\"FumeFX Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"FumeFX Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 20 100 -ps 2 80 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 0\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 0\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"renderCam\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 8192\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1366\\n    -height 768\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"renderCam\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 8192\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1366\\n    -height 768\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 50 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels yes -displayOrthographicLabels yes -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition axis;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "449DAAF9-46D6-FA2E-E896-4889B8D33896";
	setAttr ".b" -type "string" "playbackOptions -min 1.041667 -max 125 -ast 1.041667 -aet 208.333333 ";
	setAttr ".st" 6;
createNode file -n "ai_CheckerRoom_File01";
	rename -uid "F6698BEE-4BE8-70FE-47E4-30ACCBBE98A8";
	addAttr -ci true -k true -sn "rsFilterEnable" -ln "rsFilterEnable" -dv 2 -min 0 
		-max 2 -en "None:Magnification:Magnification/Minification" -at "enum";
	addAttr -ci true -sn "rsMipBias" -ln "rsMipBias" -min -31 -max 31 -at "double";
	addAttr -ci true -sn "rsBicubicFiltering" -ln "rsBicubicFiltering" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "rsPreferSharpFiltering" -ln "rsPreferSharpFiltering" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsAlphaMode" -ln "rsAlphaMode" -min 0 -max 2 -en "None:Coverage:Pre-Multiplied" 
		-at "enum";
	addAttr -ci true -sn "gamma" -ln "gamma" -at "double";
	setAttr ".ftn" -type "string" "${SLiBLib}/scene/Checker.tga";
	setAttr ".ft" 0;
	setAttr ".cs" -type "string" "sRGB";
	setAttr -k on ".gamma" 0.45454545454545453;
createNode place2dTexture -n "ai_CheckerRoom_p2d01";
	rename -uid "205760A0-4CD7-3593-64D8-7A989389712E";
	addAttr -ci true -sn "ruv" -ln "rsUvSet" -dt "string";
	setAttr ".re" -type "float2" 10 10 ;
createNode file -n "ai_CheckerBall_File01";
	rename -uid "CB88E9A6-4EF6-4C82-2F64-F9BE5DECA30F";
	addAttr -ci true -k true -sn "rsFilterEnable" -ln "rsFilterEnable" -dv 2 -min 0 
		-max 2 -en "None:Magnification:Magnification/Minification" -at "enum";
	addAttr -ci true -sn "rsMipBias" -ln "rsMipBias" -min -31 -max 31 -at "double";
	addAttr -ci true -sn "rsBicubicFiltering" -ln "rsBicubicFiltering" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "rsPreferSharpFiltering" -ln "rsPreferSharpFiltering" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsAlphaMode" -ln "rsAlphaMode" -min 0 -max 2 -en "None:Coverage:Pre-Multiplied" 
		-at "enum";
	addAttr -ci true -sn "gamma" -ln "gamma" -at "double";
	setAttr ".ftn" -type "string" "${SLiBLib}/scene/Checker.tga";
	setAttr ".ft" 0;
	setAttr ".cs" -type "string" "sRGB";
	setAttr -k on ".gamma" 0.45454545454545453;
createNode place2dTexture -n "ai_CheckerBall_p2d01";
	rename -uid "AFBBADF3-4978-B3CE-EF94-E09473C3A985";
	addAttr -ci true -sn "ruv" -ln "rsUvSet" -dt "string";
	setAttr ".re" -type "float2" 3.2 3.2 ;
createNode file -n "ai_Logo_File01";
	rename -uid "136F62F1-4E38-888E-BC3A-FBBC51C3F651";
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
	addAttr -ci true -sn "gamma" -ln "gamma" -at "double";
	setAttr ".ftn" -type "string" "${SLiBLib}/scene/arnold_logo.png";
	setAttr ".cs" -type "string" "sRGB";
	setAttr ".resolution" 256;
	setAttr -k on ".gamma" 0.45454545454545453;
createNode place2dTexture -n "ai_Logo_p2d01";
	rename -uid "28F6C52F-4856-DEFA-1C12-88AFAD79E881";
	addAttr -ci true -sn "ruv" -ln "rsUvSet" -dt "string";
createNode shadingEngine -n "mRay_Logo_MATSG";
	rename -uid "1CEF4A27-48A7-ED3B-1394-B4984A43BDAA";
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
createNode materialInfo -n "materialInfo120";
	rename -uid "C954201A-4962-185E-C66A-A894E79FA918";
createNode nodeGraphEditorBookmarkInfo -n "nodeGraphEditorBookmarkInfo1";
	rename -uid "9601E673-4E28-CEDE-1D26-7A90389FA846";
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "4F9A307E-4343-D020-B462-B5B1B1EDDCC8";
	setAttr ".GI_diffuse_depth" 2;
	setAttr ".GI_total_depth" 5;
	setAttr ".version" -type "string" "1.2.4.2";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "BD0E1B0D-44F7-8F69-3DC9-1F8766D43019";
	setAttr ".ai_translator" -type "string" "blackman_harris";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "AC8C7E19-4524-84BE-D21E-A09963126F26";
	setAttr ".ai_translator" -type "string" "exr";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "D24BA2DC-4EB3-861C-1E16-939035DF933C";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode aiStandard -n "ai_CheckerBall_MAT";
	rename -uid "A7675A4E-4839-F5BE-1961-09ABC6AD0202";
	setAttr ".Kd" 1;
createNode aiStandard -n "ai_CheckerRoom_MAT";
	rename -uid "2A8A5449-446C-B8B3-16D5-E596A02C6548";
	setAttr ".Kd" 1;
createNode shadingEngine -n "ai_CheckerBall_MATSG";
	rename -uid "09DFE04E-4CA0-9E46-1A15-EBBC51C383BB";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo122";
	rename -uid "D52C5410-453C-B81C-D1C4-209F31EA9AAA";
createNode shadingEngine -n "_CheckerRoom_MATSG";
	rename -uid "D7D3A254-4C03-C298-4E01-4D81DB54403B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo123";
	rename -uid "D7711BD1-441E-DABB-C678-77AC5FBCD706";
createNode file -n "file1";
	rename -uid "FEC2D05B-4FF1-95F3-F0EF-E1923477BE27";
	setAttr ".ftn" -type "string" "${SLiBLib}/scene/TestRoom.hdr";
	setAttr ".cs" -type "string" "sRGB";
createNode place2dTexture -n "place2dTexture1";
	rename -uid "FBE9851A-42BB-1B92-E357-BB8B8F20928B";
createNode aiStandard -n "Arnold_Logo_MAT";
	rename -uid "82183640-41AB-90D9-FF50-D6B29265B7A2";
	setAttr ".ai_matte_color_a" 1;
	setAttr ".Kd" 1;
	setAttr ".Ks_color" -type "float3" 0 0 0 ;
	setAttr ".specular_roughness" 0;
	setAttr ".specular_anisotropy" 0;
	setAttr ".Kt" 1;
createNode shadingEngine -n "Arnold_Logo_MATSG";
	rename -uid "2879716B-4B8D-2AB2-ADCA-21BB123D96C5";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo124";
	rename -uid "067BE5F7-463D-E334-C6FE-83BCBA09D1C5";
createNode file -n "ai_Logo_File02";
	rename -uid "D76683AE-4157-E55D-FFE2-08905E8B6509";
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
	addAttr -ci true -sn "gamma" -ln "gamma" -at "double";
	setAttr ".ftn" -type "string" "${SLiBLib}/scene/arnold_logo_mask.png";
	setAttr ".cs" -type "string" "sRGB";
	setAttr ".resolution" 256;
	setAttr -k on ".gamma" 0.45454545454545453;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "595D0D34-4764-1782-B8A9-F8877A1F9337";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 12.92353428499975 -192.85713519368886 ;
	setAttr ".tgi[0].vh" -type "double2" 965.64785540149592 48.809521870007671 ;
	setAttr -s 5 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 785.71429443359375;
	setAttr ".tgi[0].ni[0].y" -12.857142448425293;
	setAttr ".tgi[0].ni[0].nvs" 1923;
	setAttr ".tgi[0].ni[1].x" 1124.2857666015625;
	setAttr ".tgi[0].ni[1].y" -72.857139587402344;
	setAttr ".tgi[0].ni[1].nvs" 1923;
	setAttr ".tgi[0].ni[2].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[2].y" -35.714286804199219;
	setAttr ".tgi[0].ni[2].nvs" 1923;
	setAttr ".tgi[0].ni[3].x" 526.809326171875;
	setAttr ".tgi[0].ni[3].y" -2.1677179336547852;
	setAttr ".tgi[0].ni[3].nvs" 18306;
	setAttr ".tgi[0].ni[4].x" 262.85714721679687;
	setAttr ".tgi[0].ni[4].y" -12.857142448425293;
	setAttr ".tgi[0].ni[4].nvs" 1923;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".etmr" yes;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".st";
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
	setAttr -s 7 ".s";
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
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".tx";
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
select -ne :defaultRenderGlobals;
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
	setAttr ".ren" -type "string" "arnold";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av ".outf" 51;
	setAttr -cb on ".imfkey" -type "string" "exr";
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
	setAttr -k on ".pram" -type "string" "";
	setAttr -k on ".poam" -type "string" "";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
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
	setAttr ".ocp" 3;
	setAttr -cb on ".hbl";
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
select -ne :defaultColorMgtGlobals;
	setAttr ".ote" yes;
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
connectAttr "imagePlaneShape1.msg" "renderCamShape.ip" -na;
connectAttr ":defaultColorMgtGlobals.cme" "imagePlaneShape1.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "imagePlaneShape1.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "imagePlaneShape1.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "imagePlaneShape1.ws";
connectAttr "file1.oc" "aiSkyDomeLightShape1.sc";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "Arnold_Logo_MATSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "mRay_Logo_MATSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "ai_CheckerBall_MATSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "_CheckerRoom_MATSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "Arnold_Logo_MATSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "mRay_Logo_MATSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "ai_CheckerBall_MATSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "_CheckerRoom_MATSG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "ai_CheckerRoom_p2d01.c" "ai_CheckerRoom_File01.c";
connectAttr "ai_CheckerRoom_p2d01.tf" "ai_CheckerRoom_File01.tf";
connectAttr "ai_CheckerRoom_p2d01.rf" "ai_CheckerRoom_File01.rf";
connectAttr "ai_CheckerRoom_p2d01.mu" "ai_CheckerRoom_File01.mu";
connectAttr "ai_CheckerRoom_p2d01.mv" "ai_CheckerRoom_File01.mv";
connectAttr "ai_CheckerRoom_p2d01.s" "ai_CheckerRoom_File01.s";
connectAttr "ai_CheckerRoom_p2d01.wu" "ai_CheckerRoom_File01.wu";
connectAttr "ai_CheckerRoom_p2d01.wv" "ai_CheckerRoom_File01.wv";
connectAttr "ai_CheckerRoom_p2d01.re" "ai_CheckerRoom_File01.re";
connectAttr "ai_CheckerRoom_p2d01.of" "ai_CheckerRoom_File01.of";
connectAttr "ai_CheckerRoom_p2d01.r" "ai_CheckerRoom_File01.ro";
connectAttr "ai_CheckerRoom_p2d01.n" "ai_CheckerRoom_File01.n";
connectAttr "ai_CheckerRoom_p2d01.vt1" "ai_CheckerRoom_File01.vt1";
connectAttr "ai_CheckerRoom_p2d01.vt2" "ai_CheckerRoom_File01.vt2";
connectAttr "ai_CheckerRoom_p2d01.vt3" "ai_CheckerRoom_File01.vt3";
connectAttr "ai_CheckerRoom_p2d01.vc1" "ai_CheckerRoom_File01.vc1";
connectAttr "ai_CheckerRoom_p2d01.o" "ai_CheckerRoom_File01.uv";
connectAttr "ai_CheckerRoom_p2d01.ofs" "ai_CheckerRoom_File01.fs";
connectAttr ":defaultColorMgtGlobals.cme" "ai_CheckerRoom_File01.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "ai_CheckerRoom_File01.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "ai_CheckerRoom_File01.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "ai_CheckerRoom_File01.ws";
connectAttr "ai_CheckerBall_p2d01.c" "ai_CheckerBall_File01.c";
connectAttr "ai_CheckerBall_p2d01.tf" "ai_CheckerBall_File01.tf";
connectAttr "ai_CheckerBall_p2d01.rf" "ai_CheckerBall_File01.rf";
connectAttr "ai_CheckerBall_p2d01.mu" "ai_CheckerBall_File01.mu";
connectAttr "ai_CheckerBall_p2d01.mv" "ai_CheckerBall_File01.mv";
connectAttr "ai_CheckerBall_p2d01.s" "ai_CheckerBall_File01.s";
connectAttr "ai_CheckerBall_p2d01.wu" "ai_CheckerBall_File01.wu";
connectAttr "ai_CheckerBall_p2d01.wv" "ai_CheckerBall_File01.wv";
connectAttr "ai_CheckerBall_p2d01.re" "ai_CheckerBall_File01.re";
connectAttr "ai_CheckerBall_p2d01.of" "ai_CheckerBall_File01.of";
connectAttr "ai_CheckerBall_p2d01.r" "ai_CheckerBall_File01.ro";
connectAttr "ai_CheckerBall_p2d01.n" "ai_CheckerBall_File01.n";
connectAttr "ai_CheckerBall_p2d01.vt1" "ai_CheckerBall_File01.vt1";
connectAttr "ai_CheckerBall_p2d01.vt2" "ai_CheckerBall_File01.vt2";
connectAttr "ai_CheckerBall_p2d01.vt3" "ai_CheckerBall_File01.vt3";
connectAttr "ai_CheckerBall_p2d01.vc1" "ai_CheckerBall_File01.vc1";
connectAttr "ai_CheckerBall_p2d01.o" "ai_CheckerBall_File01.uv";
connectAttr "ai_CheckerBall_p2d01.ofs" "ai_CheckerBall_File01.fs";
connectAttr ":defaultColorMgtGlobals.cme" "ai_CheckerBall_File01.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "ai_CheckerBall_File01.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "ai_CheckerBall_File01.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "ai_CheckerBall_File01.ws";
connectAttr "ai_Logo_p2d01.c" "ai_Logo_File01.c";
connectAttr "ai_Logo_p2d01.tf" "ai_Logo_File01.tf";
connectAttr "ai_Logo_p2d01.rf" "ai_Logo_File01.rf";
connectAttr "ai_Logo_p2d01.mu" "ai_Logo_File01.mu";
connectAttr "ai_Logo_p2d01.mv" "ai_Logo_File01.mv";
connectAttr "ai_Logo_p2d01.s" "ai_Logo_File01.s";
connectAttr "ai_Logo_p2d01.wu" "ai_Logo_File01.wu";
connectAttr "ai_Logo_p2d01.wv" "ai_Logo_File01.wv";
connectAttr "ai_Logo_p2d01.re" "ai_Logo_File01.re";
connectAttr "ai_Logo_p2d01.of" "ai_Logo_File01.of";
connectAttr "ai_Logo_p2d01.r" "ai_Logo_File01.ro";
connectAttr "ai_Logo_p2d01.n" "ai_Logo_File01.n";
connectAttr "ai_Logo_p2d01.vt1" "ai_Logo_File01.vt1";
connectAttr "ai_Logo_p2d01.vt2" "ai_Logo_File01.vt2";
connectAttr "ai_Logo_p2d01.vt3" "ai_Logo_File01.vt3";
connectAttr "ai_Logo_p2d01.vc1" "ai_Logo_File01.vc1";
connectAttr "ai_Logo_p2d01.o" "ai_Logo_File01.uv";
connectAttr "ai_Logo_p2d01.ofs" "ai_Logo_File01.fs";
connectAttr ":defaultColorMgtGlobals.cme" "ai_Logo_File01.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "ai_Logo_File01.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "ai_Logo_File01.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "ai_Logo_File01.ws";
connectAttr "mRay_Logo_MATSG.msg" "materialInfo120.sg";
connectAttr ":defaultArnoldDisplayDriver.msg" ":defaultArnoldRenderOptions.drivers"
		 -na;
connectAttr ":defaultArnoldFilter.msg" ":defaultArnoldRenderOptions.filt";
connectAttr ":defaultArnoldDriver.msg" ":defaultArnoldRenderOptions.drvr";
connectAttr "ai_CheckerBall_File01.oc" "ai_CheckerBall_MAT.Kd_color";
connectAttr "ai_CheckerRoom_File01.oc" "ai_CheckerRoom_MAT.Kd_color";
connectAttr "ai_CheckerBall_MAT.out" "ai_CheckerBall_MATSG.ss";
connectAttr "shaderBallShape.iog" "ai_CheckerBall_MATSG.dsm" -na;
connectAttr "ai_CheckerBall_MATSG.msg" "materialInfo122.sg";
connectAttr "ai_CheckerBall_MAT.msg" "materialInfo122.m";
connectAttr "ai_CheckerBall_MAT.msg" "materialInfo122.t" -na;
connectAttr "ai_CheckerRoom_MAT.out" "_CheckerRoom_MATSG.ss";
connectAttr "shaderRoomShape.iog" "_CheckerRoom_MATSG.dsm" -na;
connectAttr "_CheckerRoom_MATSG.msg" "materialInfo123.sg";
connectAttr "ai_CheckerRoom_MAT.msg" "materialInfo123.m";
connectAttr "ai_CheckerRoom_MAT.msg" "materialInfo123.t" -na;
connectAttr ":defaultColorMgtGlobals.cme" "file1.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "file1.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "file1.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "file1.ws";
connectAttr "place2dTexture1.c" "file1.c";
connectAttr "place2dTexture1.tf" "file1.tf";
connectAttr "place2dTexture1.rf" "file1.rf";
connectAttr "place2dTexture1.mu" "file1.mu";
connectAttr "place2dTexture1.mv" "file1.mv";
connectAttr "place2dTexture1.s" "file1.s";
connectAttr "place2dTexture1.wu" "file1.wu";
connectAttr "place2dTexture1.wv" "file1.wv";
connectAttr "place2dTexture1.re" "file1.re";
connectAttr "place2dTexture1.of" "file1.of";
connectAttr "place2dTexture1.r" "file1.ro";
connectAttr "place2dTexture1.n" "file1.n";
connectAttr "place2dTexture1.vt1" "file1.vt1";
connectAttr "place2dTexture1.vt2" "file1.vt2";
connectAttr "place2dTexture1.vt3" "file1.vt3";
connectAttr "place2dTexture1.vc1" "file1.vc1";
connectAttr "place2dTexture1.o" "file1.uv";
connectAttr "place2dTexture1.ofs" "file1.fs";
connectAttr "ai_Logo_File01.oc" "Arnold_Logo_MAT.Kd_color";
connectAttr "ai_Logo_File02.oc" "Arnold_Logo_MAT.opacity";
connectAttr "Arnold_Logo_MAT.out" "Arnold_Logo_MATSG.ss";
connectAttr "Arnold_LogoShape.iog" "Arnold_Logo_MATSG.dsm" -na;
connectAttr "Arnold_Logo_MATSG.msg" "materialInfo124.sg";
connectAttr "Arnold_Logo_MAT.msg" "materialInfo124.m";
connectAttr "Arnold_Logo_MAT.msg" "materialInfo124.t" -na;
connectAttr "Arnold_Logo_MATSG.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "ai_Logo_File02.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "ai_Logo_p2d01.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "Arnold_Logo_MAT.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "ai_Logo_File01.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "mRay_Logo_MATSG.pa" ":renderPartition.st" -na;
connectAttr "ai_CheckerBall_MATSG.pa" ":renderPartition.st" -na;
connectAttr "_CheckerRoom_MATSG.pa" ":renderPartition.st" -na;
connectAttr "Arnold_Logo_MATSG.pa" ":renderPartition.st" -na;
connectAttr "ai_CheckerBall_MAT.msg" ":defaultShaderList1.s" -na;
connectAttr "ai_CheckerRoom_MAT.msg" ":defaultShaderList1.s" -na;
connectAttr "Arnold_Logo_MAT.msg" ":defaultShaderList1.s" -na;
connectAttr "ai_CheckerRoom_p2d01.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "ai_CheckerBall_p2d01.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "ai_Logo_p2d01.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "place2dTexture1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "directionalLightShape1.ltd" ":lightList1.l" -na;
connectAttr "ai_CheckerRoom_File01.msg" ":defaultTextureList1.tx" -na;
connectAttr "ai_CheckerBall_File01.msg" ":defaultTextureList1.tx" -na;
connectAttr "ai_Logo_File01.msg" ":defaultTextureList1.tx" -na;
connectAttr "file1.msg" ":defaultTextureList1.tx" -na;
connectAttr "ai_Logo_File02.msg" ":defaultTextureList1.tx" -na;
connectAttr "renderCamShape.msg" ":defaultRenderGlobals.sc";
connectAttr "directionalLight1.iog" ":defaultLightSet.dsm" -na;
connectAttr "aiSkyDomeLight1.iog" ":defaultLightSet.dsm" -na;
// End of arnold_SLiB_ShaderTestRoom_hdri.ma
