/*
 Copyright (c) 2015,
 Dan Bethell, Johannes Saam, Vahan Sosoyan.
 All rights reserved. See Copyright.txt for more details.
 */

#include "Server.h"
#include "Client.h"
#include <boost/lexical_cast.hpp>
#include <vector>
#include <iostream>
#include <stdexcept>

using namespace aton;
using boost::asio::ip::tcp;

Server::Server() :
        mPort(0),
        mSocket( mIoService ),
        mAcceptor( mIoService )
{
}

Server::Server( int port ) :
        mPort(0),
        mSocket( mIoService ),
        mAcceptor( mIoService )
{
    connect( port );
}

Server::~Server()
{
    if ( mAcceptor.is_open() )
        mAcceptor.close();
}

void Server::connect( int port, bool search )
{
    // disconnect if necessary
    if ( mAcceptor.is_open() )
        mAcceptor.close();

    // reconnect at specified port
    int start_port = port;
    while (!mAcceptor.is_open() && port < start_port + 99)
    {
        try
        {
            tcp::endpoint endpoint( boost::asio::ip::tcp::v4(), port );
            mAcceptor.open(endpoint.protocol());
            mAcceptor.set_option(boost::asio::ip::tcp::acceptor::reuse_address(true));
            mAcceptor.bind(endpoint);
            mAcceptor.listen();
            mPort = port;
        }
        catch (...)
        {
            mAcceptor.close();
            if (!search)
                break;
            else
                port++;
        }
    }

    // handle failed connection
    if ( !mAcceptor.is_open() )
    {
        char buffer[32];
        sprintf(buffer, "port: %d", start_port);
        if (search)
            sprintf(buffer, "port: %d-%d", start_port, start_port + 99);
        std::string error = "Failed to connect to port ";
        error += buffer;
        throw std::runtime_error( error.c_str() );
    }
}

void Server::quit()
{
    std::string hostname("localhost");
    aton::Client client(hostname, mPort);
    client.quit();
}

void Server::accept()
{
    if ( mSocket.is_open() )
        mSocket.close();
    mAcceptor.accept(mSocket);
}

Data Server::listen()
{
    Data d;

    // read the key from the incoming data
    try
    {
        int key = -1;
        boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&key), sizeof(int)) );

        switch( key )
        {
            case 0: // open image
            {
                // send back an image id
                int image_id = 1;
                boost::asio::write( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&image_id), sizeof(int) ) );

                // get width & height
                int width, height, rArea;
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&width), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&height), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&rArea), sizeof(int)) );

                // create data object
                d.mType = key;
                d.mWidth = width;
                d.mHeight = height;
                d.mRArea = rArea;
                break;
            }
            case 1: // image data
            {
                d.mType = key;
                
                // receive image id
                int image_id;
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&image_id), sizeof(int)) );
                
                // get data info
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mX), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mY), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mWidth), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mHeight), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mRArea), sizeof(long long)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mSpp), sizeof(int)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mRam), sizeof(long long)) );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mTime), sizeof(int)) );
                
                // get aov name's size
                size_t aov_size=0;
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&aov_size), sizeof(size_t)) );
                
                // get aov name
                d.mAovName = new char[aov_size];
                boost::asio::read( mSocket, boost::asio::buffer(d.mAovName, aov_size));

                // get pixels
                int num_samples = d.width() * d.height() * d.spp();
                d.mPixelStore.resize( num_samples );
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&d.mPixelStore[0]), sizeof(float)*num_samples ) ) ;
                break;
            }
            case 2: // close image
            {
                int image_id;
                d.mType = key;
                boost::asio::read( mSocket, boost::asio::buffer(reinterpret_cast<char*>(&image_id), sizeof(int)) );
                mSocket.close();
                break;
            }
            case 9: // quit
            {
                d.mType = 9;

                //debug Closing socket
                std::cout << "Socket closed" << std::endl;

                mSocket.close();

                // This fixes all nuke destructor issues on windows
                mAcceptor.close();
                break;
            }
        }
    }
    catch( ... )
    {
        mSocket.close();
        throw std::runtime_error( "Could not read from socket!" );
    }

    return d;
}
