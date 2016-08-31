/*
 Copyright (c) 2015,
 Dan Bethell, Johannes Saam, Vahan Sosoyan.
 All rights reserved. See Copyright.txt for more details.
 */

#ifndef ATON_SERVER_H_
#define ATON_SERVER_H_

#include "Data.h"
#include <boost/asio.hpp>

//! \namespace aton
namespace aton
{
    /*! \class Server
     * \brief Represents a listening Server, ready to accept incoming images.
     *
     * This class wraps up the provision of a TCP port, and handles incoming
     * connections from Client objects when they're ready to send image data.
     */
    class Server
    {
    public:
        /*! \brief Constructor.
         *
         * Creates a new server. By default the Server is not connected at
         * creation time.
         */
        Server();
        /*! \brief Constructor.
         *
         * Creates a new server and calls connect() with the specified port
         * number.
         */
        Server( int port );
        /*! \brief Destructor.
         *
         *  Shuts down the server, closing any open ports if the server is
         *  connected.
         */
        ~Server();
        
        /*! \brief Connects the server to a port.
         *
         * If true is passed as the second parameter then the server will
         * search for the first available port if the specified one is not
         * available. To find out which port the server managed to connect to,
         * call getPort() afterwards.
         */
        void connect( int port, bool seach=false );

        /*! \brief Sets up the server to accept an incoming Client connections.
         */
        void accept();

        /*! \brief Listens for incoming messages from a Client.
         *
         * This function blocks (and so may be require running on a separate
         * thread), returning once a Client has sent a message.
         *
         * The returned Data object is filled with the relevant information and
         * passed back ready for handling by the parent application.
         */
        Data listen();

        /*! \brief Sends a 'quit' message to the server.
         *
         * This can be used to exit a listening loop running on a separate
         * thread.
         */
        void quit();

        //! Returns whether or not the server is connected to a port.
        bool isConnected(){ return mAcceptor.is_open(); }

        //! Returns the port the server is currently connected to.
        int getPort(){ return mPort; }

    private:

        // the port we're listening to
        int mPort;

        // boost::asio tcp stuff
        boost::asio::io_service mIoService;
        boost::asio::ip::tcp::socket mSocket;
        boost::asio::ip::tcp::acceptor mAcceptor;
    };
}

/*! \mainpage RenderConnect
 * \section Overview
 * The RenderConnect project is a RenderMan Interface-compatible display driver
 * and Nuke plugin for direct rendering into the Nuke interface.
 *
 * <b>RenderMan® is a registered trademark of Pixar.<br>
 * Nuke® is a registered trademark of The Foundry.</b>
 *
 * \image html nuke_examplebuild_small.jpg
 *
 * The code is freely available from http://github.com/danbethell/renderconnect
 * and is released under the New BSD license. See \link COPYING \endlink
 * for more details.
 *
 * RenderConnect is based on a simple Client/Server model, suitable for rendering
 * to/from a variety of applications. The classes are described
 * <a href="annotated.html">here</a>. The TCP/IP interface code is handled using
 * the <a href="http://www.boost.org/doc/libs/1_40_0/doc/html/boost_asio.html">
 * Boost.Asio</a> library. The display driver will theoretically build
 * using any RenderMan-compatible renderer
 * but the included <a href="http://cmake.com"> CMake</a> build script assumes
 * you have <a href="http://3delight.com">3Delight</a> or 
 * <a href="http://renderender.pixar.com">PRMan</a> installed.
 *
 * \section building Building
 * Ensure you have <a href="http://www.thefoundry.co.uk">Nuke</a> (5.2),
 * either <a href="http://www.3delight.com">3Delight</a> (9.0) or 
 * <a href="http://renderender.pixar.com">PRMan</a> (15.0),
 * <a href="http://www.boost.org/">Boost</a> (1.40) and
 * <a href="http://cmake.org/">CMake</a> (2.8) installed. You should set the
 * following environment variables before running <i>cmake</i>.
 * <ul>
 *  <li><b>RENDER</b> - set to either <b>3Delight</b> or <b>PRMan</b>
 *  <li><b>DELIGHT</b> - (3Delight only) the path to your 3Delight installation.
 *  <li><b>RENDERTREE</b> - (PRMan only) the path to your RPS installation.
 *  <li><b>NDK_PATH</b> - The path to your Nuke libraries.
 * </ul>
 *
 * \section render_plugin Display Driver
 *
 * The display driver works just like any other, but has two additional
 * parameters: <b>hostname</b> and <b>port</b>. Using these you can control
 * which host and socket the display is rendered to.
 *
 * You should refer to your renderer's documentation for setting up the display
 * driver but it is normally as simple as putting something akin to the
 * following in your <i>rendermn.ini</i> configuration.
 *
 * \code
 * /display/dso/RenderConnect /full/path/to/d_renderConnect
 * \endcode
 *
 * It's important that you always render images as 32-bit floating-point
 * (i.e. the quantize settings are all zero).
 *
 * Here is an example of a rib snippet which renders the primary display to port
 * <i>9201</i> on <i>localhost</i>.
 *
 * \code
 * # Render beauty to port 9201
 * Display "rgba" "RenderConnect" "rgba"
 *   "int[4] quantize" [ 0 0 0 0 ]
 *   "string filter" [ "gaussian" ]
 *   "float[2] filterwidth" [ 2 2 ]
 *   "string hostname" [ "localhost" ]
 *   "integer port" [ 9201 ]
 * \endcode
 *
 * You can render multiple displays to different hosts/ports at the same time.
 *
 * \code
 * # Render the __Pworld AOV to port 9202
 * Display "+Pworld" "RenderConnect" "point __Pworld"
 *   "int[4] quantize" [ 0 0 0 0 ]
 *   "string filter" [ "gaussian" ]
 *   "float[2] filterwidth" [ 2 2 ]
 *   "string hostname" [ "localhost" ]
 *   "integer port" [ 9202 ]
 *
 * # Render the __Nworld AOV to port 9203
 * Display "+Nworld" "RenderConnect" "point __Nworld"
 *   "int[4] quantize" [ 0 0 0 0 ]
 *   "string filter" [ "gaussian" ]
 *   "float[2] filterwidth" [ 2 2 ]
 *   "string hostname" [ "localhost" ]
 *   "integer port" [ 9203 ]
 * \endcode
 *
 * \section nuke_plugin Nuke Plugin
 *
 * \image html nuke_examplebuild_rendering.jpg
 *
 * The nuke plugin defines a node called <b>RenderConnect</b>. Once it's built you
 * just need to ensure it's somewhere on your <i>NUKE_PATH</i>.
 *
 * \code
 * nuke.load("nk_renderConnect")
 * nuke.createNode("RenderConnect")
 * \endcode
 *
 * The node has two knobs: a format knob, and a port knob.
 * The <b>format</b> sets the output buffer size for the node. If an incoming
 * image is a different size to the buffer then it will be padded with black or
 * cropped.
 * The <b>port</b> knob sets the TCP port address that the node will listen for
 * connections on.
 *
 * \image html nukeplugin_knobs.jpg
 *
 * By default <b>port</b> is set to <i>9201</i> and if a node cannot connect
 * then it will report an error. Change the port value will disconnect the
 * server and reconnect it to the new port. All instances of the
 * <b>RenderConnect</b> node will need unique port addresses.
 *
 * \image html nukeplugin_portclash.jpg
 *
 * \section authors Authors
 * <ul><li>Dan Bethell (danbethell at gmail dot com)</li>
 * <li>Johannes Saam (johannes dot saam at googlemail dot com)</li></ul>
 */

/*! \page COPYING
© Copyright 2010, Dan Bethell, Johannes Saam.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

<ul>
    <li>Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.</li>

    <li>Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.</li>

    <li>Neither the name of RenderConnect nor the names of its contributors may be
    used to endorse or promote products derived from this software without
    specific prior written permission.</li>
</ul>
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#endif // ATON_SERVER_H_
