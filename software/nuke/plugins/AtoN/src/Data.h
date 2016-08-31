/*
 Copyright (c) 2015,
 Dan Bethell, Johannes Saam, Vahan Sosoyan.
 All rights reserved. See Copyright.txt for more details.
 */

#ifndef ATON_DATA_H_
#define ATON_DATA_H_

#include <vector>

//! \namespace aton
namespace aton
{
    /*! \class Data
     * \brief Represents image information passed from Client to Server
     *
     * This class wraps up the data sent from Client to Server. When calling
     * Client::openImage() a Data object should first be constructed that
     * specifies the full image dimensions.
     * E.g. Data( 0, 0, 320, 240, 3 );
     *
     * When sending actually pixel information it should be constructed using
     * values that represent the chunk of pixels being sent.
     * E.g. Data( 15, 15, 16, 16, 3, myPixelPointer );
     */
    class Data
    {
    friend class Client;
    friend class Server;
    public:
        //! Constructor
        Data( int x=0, int y=0,
              int width=0, int height=0, long long rArea=0,
              int spp=0, long long ram=0, int time=0, const char *aovName = 0, const float *data=0 );
        //! Destructor
        ~Data();
        
        /*! \brief The 'type' of message this Data represents
         *
         * 0: image open
         * 1: pixels
         * 2: image close
         */
        const int type() const { return mType; }

        //! X position
        int x() const { return mX; }
        //! y position
        int y() const { return mY; }
        //! Width
        int width() const { return mWidth; }
        //! Height
        int height() const { return mHeight; }
        // Area of the render region
        long long rArea() const { return mRArea; }
        //! Samples-per-pixel, aka channel depth
        int spp() const { return mSpp; }
        //! Taken memory while rendering
        long long ram() const { return mRam; }
        //! Taken time while rendering
        int time() const { return mTime; }
        // Aov name
        const char *aovName() const { return mAovName; }
        void clearAovName();
        //! Pointer to pixel data owned by the display driver (client-side)
        const float *data() const { return mpData; }
        //! Pointer to pixel data owned by this object (server-side)
        const float *pixels() const { return &mPixelStore[0]; }

    private:
        // what type of data is this?
        int mType;

        // x & y position
        int mX, mY; 
        
        // width, height, num channels (samples)
        unsigned int mWidth, mHeight, mSpp, mTime;
        
        unsigned long long mRArea, mRam;
        
        char *mAovName;

        // our pixel data pointer (for driver-owned pixels)
        float *mpData; 

        // our persistent pixel storage (for Data-owned pixels)
        std::vector<float> mPixelStore;
    };
}

#endif // ATON_DATA_H_
