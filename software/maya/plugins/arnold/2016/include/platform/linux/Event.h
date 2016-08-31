#pragma once

#include <ai_msg.h>
#include <climits>
#include <pthread.h>
#include <ctime>
#include <cerrno>
#include <cstdlib>

class CEvent
{

public:

   CEvent(bool manual = true, bool initialValue = true)
      : m_manual(manual), m_signaled(initialValue)
   {
      pthread_mutex_init(&m_mutex, NULL);
      pthread_cond_init(&m_cond, NULL);
   }

   ~CEvent()
   {
      pthread_mutex_destroy(&m_mutex);
      pthread_cond_destroy(&m_cond);
   }

   void set()
   {
      pthread_mutex_lock(&m_mutex);
      m_signaled = true;
      pthread_cond_signal(&m_cond);
      pthread_mutex_unlock(&m_mutex);
   }

   void unset()
   {
      pthread_mutex_lock(&m_mutex);
      m_signaled = false;
      pthread_mutex_unlock(&m_mutex);
   }

   bool wait(unsigned int ms = UINT_MAX)
   {
      bool ret = true;
      int wret;
      pthread_mutex_lock(&m_mutex);

      if (ms == UINT_MAX)
      {
         while (!m_signaled)
         {
            wret = pthread_cond_wait(&m_cond, &m_mutex);
            
            if (wret != 0)
            {
               AiMsgError("[mtoa] pthread_cond_wait() error %i (%s:%d)", wret, __FILE__, __LINE__);
               abort();
            }
         }
      }
      else
      {
         struct timespec t;
         clock_gettime(CLOCK_REALTIME, &t);
         t.tv_sec += ms / 1000;
         long int dt = 1000000 * (ms % 1000);
         long int rem = 1000000000 - t.tv_nsec;
         if (dt < rem)
         {
            t.tv_nsec += dt;
         }
         else
         {
            ++t.tv_sec;
            t.tv_nsec = dt - rem;
         }

         while (!m_signaled && ret)
         {
            wret = pthread_cond_timedwait(&m_cond, &m_mutex, &t);

            switch (wret)
            {
            case 0:
               break;

            case ETIMEDOUT:
               ret = false;
               break;

            case EINVAL:
            case EPERM:
            default:
               AiMsgError("[mtoa] pthread_cond_timedwait() error %i (%s:%d)", wret, __FILE__, __LINE__);
               abort();
            }
         }
      }

      if (ret && !m_manual)
      {
         m_signaled = false;
      }

      pthread_mutex_unlock(&m_mutex);
      return ret;
   }

private:

   const bool m_manual;
   bool m_signaled;
   pthread_mutex_t m_mutex;
   pthread_cond_t m_cond;

};  // class CEvent
