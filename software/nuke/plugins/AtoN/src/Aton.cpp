/*
 Copyright (c) 2015,
 Dan Bethell, Johannes Saam, Vahan Sosoyan.
 All rights reserved. See Copyright.txt for more details.
 */

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstdio>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

#include "DDImage/Iop.h"
#include "DDImage/Row.h"
#include "DDImage/Thread.h"
#include "DDImage/Knobs.h"
#include "DDImage/DDMath.h"

using namespace DD::Image;

#include "Data.h"
#include "Server.h"

#include "boost/format.hpp"
#include "boost/foreach.hpp"
#include "boost/regex.hpp"
#include "boost/filesystem.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/algorithm/string.hpp"

// class name
static const char* const CLASS = "Aton";

// version
static const char* const VERSION = "1.0.0";

// help
static const char* const HELP =
    "Listens for renders coming from the Aton display driver.";

// our default port
const int aton_default_port = 9201;

// our listener method
static void atonListen(unsigned index, unsigned nthreads, void* data);

// lightweight pixel class
class RenderColour
{
    public:
        RenderColour()
        {
            _val[0] = _val[1] = _val[2] = 0.f;
            _val[3] = 1.f;
        }

        float& operator[](int i){ return _val[i]; }
        const float& operator[](int i) const { return _val[i]; }

        // data
        float _val[4];
};

// our image buffer class
class RenderBuffer
{
    public:
        RenderBuffer() :
            _width(0),
            _height(0)
        {
        }

        void init(const unsigned int width, const unsigned int height)
        {
            _width = width;
            _height = height;
            _data.resize(_width * _height);
        }

        RenderColour& get(unsigned int x, unsigned int y)
        {
            unsigned int index = (_width * y) + x;
            return _data[index];
        }

        const RenderColour& get(unsigned int x, unsigned int y) const
        {
            unsigned int index = (_width * y) + x;
            return _data[index];
        }

        const unsigned int size() const
        {
            return _data.size();
        }

        // data
        std::vector<RenderColour> _data;
        unsigned int _width;
        unsigned int _height;
};

// status bar parameters
class Status
{
public:
    Status(): progress(0),
              ram(0),
              p_ram(0),
              time(0) {}
    unsigned int progress;
    unsigned long long ram;
    unsigned long long p_ram;
    unsigned int time;
};
// our nuke node
class Aton: public Iop
{
    public:
        FormatPair m_fmtp; // our buffer format (knob)
        Format m_fmt; // The nuke display format
        int m_port; // the port we're listening on (knob)
        const char * m_path; // default path for Write node
        std::string m_status; // status bar text
        Status m_stat; // object to hold status bar parameters
        const char * m_comment;
        bool m_stamp;
        int m_stamp_size;
        int m_slimit; // The limit size
        RenderBuffer m_buffer; // our pixel buffer
        Lock m_mutex; // mutex for locking the pixel buffer
        unsigned int hash_counter; // our refresh hash counter
        aton::Server m_server; // our aton::Server
        bool m_inError; // some error handling
        bool m_formatExists;
        bool m_capturing; // capturing signal
        std::vector<std::string> garbageList;
        std::vector<std::string> m_aovs;
        std::vector<RenderBuffer> m_buffers;
        std::string m_connectionError;
        ChannelSet m_channels;
        bool m_legit;
    
        Aton(Node* node) :
            Iop(node),
            m_port(aton_default_port),
            m_path(getPath()),
            m_status("Progress: 0%  "
                     "Used Memory: 0MB  "
                     "Peak Memory: 0MB  "
                     "Time: 00h:00m:00s"),
            m_comment(""),
            m_stamp(true),
            m_stamp_size(15),
            m_slimit(20),
            m_fmt(Format(0, 0, 1.0)),
            m_inError(false),
            m_formatExists(false),
            m_capturing(false),
            m_connectionError(""),
            m_channels(Mask_RGBA),
            m_legit(false)
        {
            inputs(0);
        }
    
        ~Aton()
        {
            disconnect();
            delete[] m_path;
        }

        // It seems additional instances of a node get copied/constructed upon
        // very frequent calls to asapUpdate() and this causes us a few
        // problems - we don't want new sockets getting opened etc.
        // Fortunately attach() only gets called for nodes in the dag so we can
        // use this to mark the DAG node as 'legit' and open the port accordingly.
        void attach()
		{
			m_legit = true;
            
            // We don't need to see these knobs
			knob("formats_knob")->hide();
            knob("port_number")->hide();
            knob("capturing_knob")->hide();

			// Running python code to check if we've already our format in the script
			script_command("bool([i.name() for i in nuke.formats() if i.name()=='Aton'])");
            std::string result = script_result();
            script_unlock();
			
            // Checking if the format is already exist
            if (result.compare("True") != 0)
				m_fmt.add("Aton");
            else m_formatExists = true;
            
		}

        void detach()
        {
            // even though a node still exists once removed from a scene (in the
            // undo stack) we should close the port and reopen if attach() gets
            // called.
            m_legit = false;
            disconnect();
        }

        void flagForUpdate()
        {
            if ( hash_counter==UINT_MAX )
                hash_counter=0;
            else
                hash_counter++;
            asapUpdate();
        }

        // we can use this to change our tcp port
        void changePort( int port )
        {
            m_inError = false;
            m_connectionError = "";

            // try to reconnect
            disconnect();
            try
            {
                m_server.connect( m_port );
            }
            catch ( ... )
            {
                std::stringstream ss;
                ss << "Could not connect to port: " << port;
                m_connectionError = ss.str();
                m_inError = true;
                print_name( std::cerr );
                std::cerr << ": " << ss.str() << std::endl;
                return;
            }

            // success
            if ( m_server.isConnected() )
            {
                Thread::spawn(::atonListen, 1, this);
                print_name( std::cout );
                std::cout << ": Connected to port " << m_server.getPort() << std::endl;
            }
        }

        // disconnect the server for it's port
        void disconnect()
        {
            if ( m_server.isConnected() )
            {
                m_server.quit();
                Thread::wait(this);

                print_name( std::cout );
                std::cout << ": Disconnected from port " << m_server.getPort() << std::endl;
            }
        }

        void append(Hash& hash)
        {
            hash.append(hash_counter);
        }

        void _validate(bool for_real)
        {
            // do we need to open a port?
            if ( m_server.isConnected()==false && !m_inError && m_legit )
                changePort(m_port);
            
            if (m_stat.progress > 0)
                status(m_stat.progress,
                       m_stat.ram,
                       m_stat.p_ram,
                       m_stat.time);
            
            // handle any connection error
            if ( m_inError )
                error(m_connectionError.c_str());

            // setup format etc
            info_.format(*m_fmtp.fullSizeFormat());
            info_.full_size_format(*m_fmtp.format());
            
            // add aovs as nuke channels
            std::string rgba = "RGBA";
            std::string z = "Z";
            std::string n = "N";
            std::string p = "P";
            
            for(auto it = m_aovs.begin(); it != m_aovs.end(); ++it)
            {
                if (it->compare(rgba)==0)
                {
                    if (!m_channels.contains(Chan_Red))
                    {
                        m_channels.insert(Chan_Red);
                        m_channels.insert(Chan_Green);
                        m_channels.insert(Chan_Blue);
                        m_channels.insert(Chan_Alpha);
                    }
                }
                else if (it->compare(z)==0)
                {
                    if (!m_channels.contains(Chan_Z))
                        m_channels.insert( Chan_Z );
                }
                else if (it->compare(n)==0 || it->compare(p)==0)
                {
                    if (!m_channels.contains(channel((boost::format("%s.X")%it->c_str()).str().c_str())))
                    {
                        m_channels.insert( channel((boost::format("%s.X")%it->c_str()).str().c_str()) );
                        m_channels.insert( channel((boost::format("%s.Y")%it->c_str()).str().c_str()) );
                        m_channels.insert( channel((boost::format("%s.Z")%it->c_str()).str().c_str()) );
                    }
                }
                else
                {
                    if (!m_channels.contains( channel((boost::format("%s.red")%it->c_str()).str().c_str())))
                    {
                        m_channels.insert( channel((boost::format("%s.red")%it->c_str()).str().c_str()) );
                        m_channels.insert( channel((boost::format("%s.blue")%it->c_str()).str().c_str()) );
                        m_channels.insert( channel((boost::format("%s.green")%it->c_str()).str().c_str()) );
                    }
                }
            }
            
            info_.channels( m_channels );
            info_.set(info().format());
        }

        void engine(int y, int xx, int r, ChannelMask channels, Row& out)
        {
            // don't have a buffer yet
            if ( m_buffer._width==0 && m_buffer._height==0 )
            {
                
                float *rOut = out.writable(Chan_Red) + xx;
                float *gOut = out.writable(Chan_Green) + xx;
                float *bOut = out.writable(Chan_Blue) + xx;
                float *aOut = out.writable(Chan_Alpha) + xx;
                const float *END = rOut + (r - xx);
                unsigned int xxx = static_cast<unsigned int> (xx);
                
                m_mutex.lock();
                while (rOut < END)
                {
                    *rOut = *gOut = *bOut = *aOut = 0.f;
                    ++rOut;
                    ++gOut;
                    ++bOut;
                    ++aOut;
                    ++xxx;
                }
                m_mutex.unlock();
            }
            
            foreach(z, channels)
            {
                int b_index = 0;
                std::string layer = getLayerName(z);
                
                for(auto it = m_aovs.begin(); it != m_aovs.end(); ++it)
                {
                    if (it->compare(layer) == 0)
                        b_index = static_cast<int>(it - m_aovs.begin());
                    else if ( it->compare("Z") == 0 && layer.compare("depth") == 0 )
                        b_index = static_cast<int>(it - m_aovs.begin());
                }

                float *rOut = out.writable(brother (z, 0)) + xx;
                float *gOut = out.writable(brother (z, 1)) + xx;
                float *bOut = out.writable(brother (z, 2)) + xx;
                float *aOut = out.writable(Chan_Alpha) + xx;
                const float *END = rOut + (r - xx);
                unsigned int xxx = static_cast<unsigned int> (xx);
                unsigned int yyy = static_cast<unsigned int> (y);
                
                if ( m_buffer._width > 0 && m_buffer._height > 0 )
                {
                    m_mutex.lock();
                    while (rOut < END)
                    {
                        if ( xxx >= m_buffer._width || yyy >= m_buffer._height )
                        {
                            *rOut = *gOut = *bOut = *aOut = 0.f;
                        }
                        else
                        {
                            *rOut = m_buffers[b_index].get(xxx, yyy)[0];
                            *gOut = m_buffers[b_index].get(xxx, yyy)[1];
                            *bOut = m_buffers[b_index].get(xxx, yyy)[2];
                            *aOut = m_buffers[0].get(xxx, yyy)[3];
                        }
                        ++rOut;
                        ++gOut;
                        ++bOut;
                        ++aOut;
                        ++xxx;
                    }
                    m_mutex.unlock();
                }
            }
        }
    
        void knobs(Knob_Callback f)
        {
            Format_knob(f, &m_fmtp, "formats_knob", "format");
            Int_knob(f, &m_port, "port_number", "port");
            Bool_knob(f, &m_capturing, "capturing_knob");
            
            Newline(f);
            Int_knob(f, &m_slimit, "limit_knob", "limit");
            Spacer(f, 1000);
            Help_knob(f, (boost::format("Aton ver%s")%VERSION).str().c_str());
            File_knob(f, &m_path, "path_knob", "path");

            Newline(f);
            Bool_knob(f, &m_stamp, "use_stamp_knob", "Use stamp");
            Spacer(f, 10);
            Knob * stamp_size = Int_knob(f, &m_stamp_size, "stamp_size_knob", "size");
            stamp_size->clear_flag(Knob::STARTLINE);

            // this will show up in the viewer as status bar
            BeginToolbar(f, "status_bar");
            Knob * statusKnob = String_knob(f, &m_status, "status_knob", "");
            statusKnob->set_flag(Knob::DISABLED, true);
            statusKnob->set_flag(Knob::OUTPUT_ONLY, true);
            EndToolbar(f);
            
            String_knob(f, &m_comment, "comment_knob", "comment");
            Newline(f);
            Button(f, "capture_knob", "Capture");
            Button(f, "import_latest_knob", "Import latest");
            Button(f, "import_all_knob", "Import all");
        }

        int knob_changed(Knob* _knob)
        {
			if (_knob->is("port_number"))
            {
                changePort(m_port);
                return 1;
            }
            if (_knob->is("capture_knob"))
            {
                captureCmd();
                return 1;
            }
            
            if (_knob->is("use_stamp_knob"))
            {
                if(!m_stamp)
                {
                    knob("stamp_size_knob")->enable(false);
                    knob("comment_knob")->enable(false);
                }
                else
                {
                    knob("stamp_size_knob")->enable(true);
                    knob("comment_knob")->enable(true);
                }
 
                return 1;
            }
            if (_knob->is("import_latest_knob"))
            {
                importLatestCmd();
                return 1;
            }
            if (_knob->is("import_all_knob"))
            {
                importAllCmd();
                return 1;
            }
            return 0;
        }
    
        char * getPath()
        {
            char * aton_path;
            std::string def_path;
            
            aton_path = getenv("ATON_CAPTURE_PATH");
            
            if (aton_path == NULL)
            {
                // Get OS specific tmp directory path
                def_path = boost::filesystem::temp_directory_path().string();
            }
            else def_path = aton_path;
            
            boost::replace_all(def_path, "\\", "/");
            
            // Construct the full path for Write node
            boost::filesystem::path dir = def_path;
            boost::filesystem::path file = "Aton.exr";
            boost::filesystem::path fullPath = dir / file;
            
            std::string str_path = fullPath.string();
            boost::replace_all(str_path, "\\", "/");
            
            char * full_path = new char[str_path.length()+1];
            strcpy(full_path, str_path.c_str());
            
            return full_path;
        }
    
        std::string getDateTime()
        {
            // Returns date and time
            time_t rawtime;
            struct tm * timeinfo;
            char time_buffer[20];
            
            time (&rawtime);
            timeinfo = localtime (&rawtime);
            
            // Setting up the Date and Time format style
            strftime(time_buffer, 20, "%Y-%m-%d_%H-%M-%S", timeinfo);
            
            std::string path = std::string(m_path);
            std::string key (".");

            return std::string(time_buffer);
        }
    
        std::vector<std::string> getCaptures()
        {
            // Our captured filenames list
            std::vector<std::string> results;
            
            boost::filesystem::path filepath(m_path);
            boost::filesystem::directory_iterator it(filepath.parent_path());
            boost::filesystem::directory_iterator end;
            
            // Regex expression to find captured files
            std::string exp = ( boost::format("%s.+.%s")%filepath.stem().string()
                                                        %filepath.extension().string() ).str();
            const boost::regex filter(exp);
            
            // Iterating through directory to find matching files
            BOOST_FOREACH(boost::filesystem::path const &p, std::make_pair(it, end))
            {
                if(boost::filesystem::is_regular_file(p))
                {
                    boost::match_results<std::string::const_iterator> what;
                    if (boost::regex_search(it->path().filename().string(), what, filter, boost::match_default))
                    {
                        std::string res = p.filename().string();
                        results.push_back(res);
                    }
                }
            }
            return results;
        }
    
        void cleanByLimit()
        {
            if ( !garbageList.empty() )
            {
                // in windows sometimes files can't be deleted due to lack of
                // access so we collecting a garbage list and trying to remove
                // them next time when user make a capture
                for(std::vector<std::string>::iterator it = garbageList.begin();
                    it != garbageList.end(); ++it)
                {
                    std::remove(it->c_str());
                }
            }
            
            int count = 0;
            std::vector<std::string> captures = getCaptures();
            boost::filesystem::path filepath(m_path);
            boost::filesystem::path dir = filepath.parent_path();
            
            // Reverse iterating through file list
            if ( !captures.empty() )
            {
                for(std::vector<std::string>::reverse_iterator it = captures.rbegin();
                    it != captures.rend(); ++it)
                {
                    boost::filesystem::path file = *it;
                    boost::filesystem::path path = dir / file;
                    std::string str_path = path.string();
                    boost::replace_all(str_path, "\\", "/");
                    
                    count += 1;
                    
                    // Remove the file if it's out of limit
                    if (count >= m_slimit)
                    {
                        if (std::remove(str_path.c_str()) != 0)
                            garbageList.push_back(str_path);
                        
                        std::string cmd; // Our python command buffer
                        
                        // Remove appropriate Read nodes as well
                        cmd = ( boost::format("exec('''for i in nuke.allNodes('Read'):\n\t"
                                                          "if '%s' == i['file'].value():\n\t\t"
                                                              "nuke.delete(i)''')")%str_path ).str();
                        script_command(cmd.c_str(), true, false);
                        script_unlock();
                    }
                }
            }
        }

        void captureCmd()
        {
            if  (m_slimit != 0)
            {
                // Get the path and add time date suffix to it
                std::string key (".");
                std::string path = std::string(m_path);
                std::string timeSuffix = "_" + getDateTime() + ".";
                
                std::size_t found = path.rfind(key);
                if (found!=std::string::npos)
                    path.replace(found, key.length(), timeSuffix);
                
                std::string cmd; // Our python command buffer
                
                // Create a Write node and return it's name
                cmd = (boost::format("nuke.nodes.Write(file='%s').name()")%path.c_str()).str();
                script_command(cmd.c_str());
                std::string writeNodeName = script_result();
                script_unlock();
                
                // Connect to Write node
                cmd = (boost::format("nuke.toNode('%s').setInput(0, nuke.toNode('%s'));"
                                     "nuke.toNode('%s')['channels'].setValue('all')")%writeNodeName
                                                                                     %node_name()
                                                                                     %writeNodeName).str();
                script_command(cmd.c_str(), true, false);
                script_unlock();

                // Add text node in between to put a stamp on the capture
                if (m_stamp)
                {
                    // Adding after render script to create a Read node and remove the Write and Text nodes
                    cmd = (boost::format("nuke.toNode('%s')['afterRender']."
                                         "setValue( '''nuke.nodes.Read(file='%s');"
                                         "nuke.delete(nuke.toNode('%s').input(0));"
                                         "nuke.delete(nuke.toNode('%s'))''' )")%writeNodeName
                                                                               %path.c_str()
                                                                               %writeNodeName
                                                                               %writeNodeName).str();
                    script_command(cmd.c_str(), true, false);
                    script_unlock();
                    
                    std::string str_status = status(m_stat.progress, m_stat.ram, m_stat.p_ram, m_stat.time);
                    
                    cmd = (boost::format("exec('''stamp = nuke.nodes.Text(message='%s  Comment: %s',"
                                                                         "yjustify='bottom', size=%s)\n"
                                                 "stamp['font'].setValue(nuke.defaultFontPathname())\n"
                                                 "stamp.setInput(0, nuke.toNode('%s'))\n"
                                                 "nuke.toNode('%s').setInput(0, stamp)''')")%str_status%m_comment
                                                                                            %m_stamp_size%node_name()
                                                                                            %writeNodeName ).str();
                    script_command(cmd.c_str(), true, false);
                    script_unlock();
                }
                else
                {
                    // Adding after render script to create a Read node and remove the Write node
                    cmd = (boost::format("nuke.toNode('%s')['afterRender']."
                                         "setValue( '''nuke.nodes.Read(file='%s');"
                                         "nuke.delete(nuke.toNode('%s'))''' )")%writeNodeName
                                                                               %path.c_str()
                                                                               %writeNodeName).str();
                    script_command(cmd.c_str(), true, false);
                    script_unlock();
                }
                
                // Execute the Write node
                cmd = (boost::format("exec('''import thread\n"
                                             "def writer():\n\t"
                                                 "def status(b): nuke.toNode('%s')['capturing_knob'].setValue(b)\n\t"
                                                 "nuke.executeInMainThread(status, args=True)\n\t"
                                                 "nuke.executeInMainThread(nuke.execute,"
                                                                           "args='%s',"
                                                                           "kwargs={'start':1, 'end':1})\n\t"
                                                 "nuke.executeInMainThread(status, args=False)\n"
                                              "thread.start_new_thread(writer,())''')")%node_name()%writeNodeName).str();
                script_command(cmd.c_str(), true, false);
                script_unlock();
            }
            cleanByLimit();
        }
    
        void importLatestCmd()
        {
            std::vector<std::string> captures = getCaptures();
            boost::filesystem::path filepath(m_path);
            boost::filesystem::path dir = filepath.parent_path();
            
            if ( !captures.empty() )
            {
                // Getting last ellemnt of the vector
                boost::filesystem::path file = captures.back();
                boost::filesystem::path path = dir / file;
                std::string str_path = path.string();
                boost::replace_all(str_path, "\\", "/");
                
                std::string cmd; // Our python command buffer
                
                cmd = ( boost::format("exec('''readNodes = nuke.allNodes('Read')\n"
                                              "exist = False\n"
                                              "if len(readNodes)>0:\n\t"
                                                  "for i in readNodes:\n\t\t"
                                                      "if '%s' == i['file'].value():\n\t\t\t"
                                                          "exist = True\n"
                                               "if exist != True:\n\t"
                                               "nuke.nodes.Read(file='%s')''')")%str_path
                                                                                %str_path ).str();
                script_command(cmd.c_str(), true, false);
                script_unlock();
            }
            
        }
    
        void importAllCmd()
        {
            std::vector<std::string> captures = getCaptures();
            boost::filesystem::path filepath(m_path);
            boost::filesystem::path dir = filepath.parent_path();
            
            if ( !captures.empty() )
            {
                // Reverse iterating through vector
                for(std::vector<std::string>::reverse_iterator it = captures.rbegin();
                    it != captures.rend(); ++it)
                {
                    boost::filesystem::path file = *it;
                    boost::filesystem::path path = dir / file;
                    std::string str_path = path.string();
                    boost::replace_all(str_path, "\\", "/");
                    
                    std::string cmd; // Our python command buffer
                    
                    cmd = ( boost::format("exec('''readNodes = nuke.allNodes('Read')\n"
                                                  "exist = False\n"
                                                  "if len(readNodes)>0:\n\t"
                                                      "for i in readNodes:\n\t\t"
                                                          "if '%s' == i['file'].value():\n\t\t\t"
                                                              "exist = True\n"
                                                   "if exist != True:\n\t"
                                                      "nuke.nodes.Read(file='%s')''')")%str_path
                                                                                       %str_path ).str();
                    script_command(cmd.c_str(), true, false);
                    script_unlock();
                }
            }
        }

        std::string status(int progress=0,
                           unsigned long long ram=0,
                           unsigned long long p_ram=0,
                           unsigned int time=0)
        {
            ram /= 1024*1024;
            p_ram /= 1024*1024;
            
            int hour = time / (1000*60*60);
            int minute = (time % (1000*60*60)) / (1000*60);
            int second = ((time % (1000*60*60)) % (1000*60)) / 1000;
            
            if (progress>100) progress=100;
            
            std::string str_status = (boost::format("Progress: %s%%  "
                                                    "Used Memory: %sMB  "
                                                    "Peak Memory: %sMB  "
                                                    "Time: %02ih:%02im:%02is")%progress%ram%p_ram
                                                                              %hour%minute
                                                                              %second).str();
            knob("status_knob")->set_text(str_status.c_str());
            return str_status;
        }

        const char* Class() const { return CLASS; }
        const char* displayName() const { return CLASS; }
        const char* node_help() const { return HELP; }
        static const Iop::Description desc;
};
//=====
//=====
// @brief our listening thread method
static void atonListen(unsigned index, unsigned nthreads, void* data)
{
    bool killThread = false;
    std::vector<std::string> active_aovs;
    
    Aton * node = reinterpret_cast<Aton*> (data);
    
    while (!killThread)
    {
        // accept incoming connections!
        node->m_server.accept();

        // our incoming data object
        aton::Data d;
        
        // for progress percentage
        long long imageArea = 0;
        int progress = 0;
        
        // loop over incoming data
        while ((d.type()==2||d.type()==9)==false)
        {
            // listen for some data
            try
            {
                d = node->m_server.listen();
            }
            catch( ... )
            {
                break;
            }

            // handle the data we received
            switch (d.type())
            {
                case 0: // open a new image
                {
                    node->m_mutex.lock();
                    node->m_buffer.init(d.width(), d.height());
                    
                    node->m_mutex.unlock();
					
					// set the nuke display format
                    if (node->m_formatExists == false)
                    {
                        node->m_fmt.set(0, 0, d.width(), d.height());
                        node->m_fmt.width(d.width());
                        node->m_fmt.height(d.height());
                    }
                    else
                    {
                        // if the format is already exist
                        // we need to get its pointer
                        Format *m_fmt_exist = nullptr;
                        for (int i=0; i < Format::size(); i++)
                        {
                            m_fmt_exist = Format::index(i);
                            if (std::string(m_fmt_exist->name()).compare("Aton") == 0)
                                break;
                        }
                        m_fmt_exist->set(0, 0, d.width(), d.height());
                        m_fmt_exist->width(d.width());
                        m_fmt_exist->height(d.height());
                    }
                    
                    // get image area to help calculate the progress percentage
                    if (d.width()*d.height() == d.rArea())
                        imageArea = d.width()*d.height();
                    else imageArea = d.rArea();
                    
                    // reset aovs
                    if (!active_aovs.empty() &&
                        !node->m_aovs.empty() && active_aovs!=node->m_aovs)
                    {
                        node->m_mutex.lock();
                        node->m_aovs.clear();
                        // reset channels before every render session
                        if (node->m_channels.size()>4)
                        {
                            node->m_channels.clear();
                            node->m_channels.insert(Chan_Red);
                            node->m_channels.insert(Chan_Green);
                            node->m_channels.insert(Chan_Blue);
                            node->m_channels.insert(Chan_Alpha);
                        }
                        node->m_mutex.unlock();
                    }
                    
                    if(!active_aovs.empty())
                        active_aovs.clear();
                    
                    // reset buffers
                    if (!node->m_buffers.empty() &&
                        node->m_buffers[0]._width != d.width() &&
                        node->m_buffers[0]._height != d.height())
                    {
                        node->m_mutex.lock();
                        node->m_buffers.clear();
                        node->m_aovs.clear();
                        node->m_mutex.unlock();
                    }
                    
                    // automatically set the knob to the right format
                    node->knob("formats_knob")->set_text("Aton");
                    break;
                }
                case 1: // image data
                {
                    // lock buffer
                    node->m_mutex.lock();

                    // copy data from d into node->m_buffer
                    int _w = node->m_buffer._width;
                    int _h = node->m_buffer._height;

                    unsigned int _x, _x0, _y, _y0, _s, offset;
                    _x = _x0 = _y = _y0 = _s = 0;

                    int _xorigin = d.x();
                    int _yorigin = d.y();
                    int _width = d.width();
                    int _height = d.height();
                    int _spp = d.spp();
                    long long _ram = d.ram();
                    int _time = d.time();
                    
                    // get aov names
                    if(!(std::find(active_aovs.begin(),
                                   active_aovs.end(),
                                   d.aovName()) != active_aovs.end()))
                        active_aovs.push_back(d.aovName());
                    
                    if(!(std::find(node->m_aovs.begin(),
                                   node->m_aovs.end(),
                                   d.aovName()) != node->m_aovs.end()))
                    {
                        node->m_aovs.push_back(d.aovName());

                        if (node->m_buffers.size() < node->m_aovs.size())
                        {
                            RenderBuffer buffer;
                            buffer.init(_w, _h);
                            node->m_buffers.push_back(buffer);
                        }
                    }
                    
                    if (node->m_buffers.size() > node->m_aovs.size())
                        node->m_buffers.resize(node->m_aovs.size());
                    
                    for(auto it = node->m_aovs.begin(); it != node->m_aovs.end(); ++it)
                    {
                        if (it->compare(d.aovName()) == 0)
                        {
                            // writing to buffer
                            const float* pixel_data = d.pixels();
                            for (_x = 0; _x < _width; ++_x)
                                for (_y = 0; _y < _height; ++_y)
                                {
                                    int b_index = static_cast<int>(it - node->m_aovs.begin());
                                    RenderColour &pix = node->m_buffers[b_index].get(_x+ _xorigin, _h - (_y + _yorigin + 1));
                                    offset = (_width * _y * _spp) + (_x * _spp);
                                    for (_s = 0; _s < _spp; ++_s)
                                        pix[_s] = pixel_data[offset+_s];
                                }
                            break;
                        }
                    }
                    
                    // release lock
                    node->m_mutex.unlock();
                    
                    // skip while capturing
                    if (node->m_capturing)
                        continue;
                    
                    // calculating the progress percentage
                    if( node->m_aovs.back().compare(d.aovName()) == 0 )
                    {
                        imageArea -= (_width*_height);
                        progress = static_cast<int>(100 - (imageArea*100) / (_w * _h));
                        
                        // setting status parameters,
                        node->m_mutex.lock();
                        node->m_stat.progress = progress;
                        node->m_stat.ram = _ram;
                        node->m_stat.p_ram = _ram > node->m_stat.p_ram ? _ram : node->m_stat.p_ram;
                        node->m_stat.time = _time;
                        node->m_mutex.unlock();
                        
                        // update the image
                        node->flagForUpdate();
                    }
                    
                    // deallocate aov name
                    d.clearAovName();
                    
                    break;
                }
                case 2: // close image
                {
                    // update the image
                    node->flagForUpdate();
                    break;
                }
                case 9: // this is sent when the parent process want to kill
                        // the listening thread
                {
                    killThread = true;
                    break;
                }
            }
        }
    }
}
//=====
// nuke builder stuff
static Iop* constructor(Node* node){ return new Aton(node); }
const Iop::Description Aton::desc(CLASS, 0, constructor);
