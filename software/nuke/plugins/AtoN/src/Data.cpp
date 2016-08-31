/*
 Copyright (c) 2015,
 Dan Bethell, Johannes Saam, Vahan Sosoyan.
 All rights reserved. See Copyright.txt for more details.
 */

#include "Data.h"
#include <cstring>
#include <iostream>

using namespace aton;

Data::Data( int x, int y, 
            int width, int height, long long rArea,
            int spp, long long ram, int time, const char *aovName, const float *data ) :
    mType(-1),
    mX(x),
    mY(y),
    mWidth(width),
    mHeight(height),
    mRArea(rArea),
    mSpp(spp),
    mRam(ram),
    mTime(time)
{

    if ( aovName!=0 )
    {
//        mAovName = new char[aovSize];
//        strcpy(mAovName, aovName);
        
        mAovName = const_cast<char*>(aovName);
    }

    if ( data!=0 )
        mpData = const_cast<float*>(data);
}

void Data::clearAovName()
{
    delete[] mAovName;
    mAovName = nullptr;
}

Data::~Data()
{
//    delete[] mAovName;
//    mAovName = nullptr;
}
