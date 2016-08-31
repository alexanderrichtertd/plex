/*
Copyright (c) 2015,
Dan Bethell, Johannes Saam, Vahan Sosoyan.
All rights reserved. See Copyright.txt for more details.
 */

#include "Client.h"
#include <boost/lexical_cast.hpp>
#include <stdexcept>
#include <iostream>

using namespace aton;
using boost::asio::ip::tcp;

Client::Client( std::string hostname, int port ) :
        		mHost( hostname ),
        		mPort( port ),
        		mImageId( -1 ),
        		mSocket( mIoService )
{
}

void Client::connect( std::string hostname, int port )
{
	bool result = true;
	tcp::resolver resolver(mIoService);
	tcp::resolver::query query( hostname.c_str(), boost::lexical_cast<std::string>(port).c_str() );
	tcp::resolver::iterator endpoint_iterator = resolver.resolve(query);
	tcp::resolver::iterator end;
	boost::system::error_code error = boost::asio::error::host_not_found;
	while (error && endpoint_iterator != end)
	{
		mSocket.close();
		mSocket.connect(*endpoint_iterator++, error);
	}
	if (error)
		throw boost::system::system_error(error);
}

void Client::disconnect()
{
	mSocket.close();
}

Client::~Client()
{
	disconnect();
}

void Client::openImage( Data &header )
{
	// connect to port!
	connect(mHost, mPort);

	// send image header message with image desc information
	int key = 0;
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&key), sizeof(int)) );

	// read our imageid
	boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&mImageId), sizeof(int)) );

	// send our width & height
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&header.mWidth), sizeof(int)) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&header.mHeight), sizeof(int)) );
    boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&header.mRArea), sizeof(int)) );
}

void Client::sendPixels( Data &data )
{
	if ( mImageId<0 )
	{
		throw std::runtime_error( "Could not send data - image id is not valid!" );
	}

	// send data for image_id
	int key = 1;
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&key), sizeof(int)) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&mImageId), sizeof(int)) );
    
    // get size of the aov name in bytes
    size_t aov_size = strlen(data.mAovName)+1;
    
	// send pixel data
	int num_samples = data.mWidth * data.mHeight * data.mSpp;
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mX), sizeof(int)) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mY), sizeof(int)) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mWidth), sizeof(int)) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mHeight), sizeof(int)) );
    boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mRArea), sizeof(long long)) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mSpp), sizeof(int)) );
    boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mRam), sizeof(long long)) );
    boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mTime), sizeof(int)) );
    boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&aov_size), sizeof(size_t)) );
    boost::asio::write( mSocket, boost::asio::buffer(data.mAovName, aov_size) );
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&data.mpData[0]), sizeof(float)*num_samples) );
}

void Client::closeImage( )
{
	// send image complete message for image_id
	int key = 2;
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&key), sizeof(int)) );

	// tell the server which image we're closing
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&mImageId), sizeof(int)) );

	// disconnect from port!
	disconnect();
}

void Client::quit()
{
	connect(mHost, mPort);
	int key = 9;
	boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&key), sizeof(int)) );
	disconnect();
}
