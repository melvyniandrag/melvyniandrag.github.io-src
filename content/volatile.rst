What the heck is volatile anyway?
##########################################################

:date: 2018-03-16 02:40
:modified: 2018-03-16
:tags: embedded c++ c
:category: embedded
:slug: what is volatile?
:authors: Melvyn Drag
:summary: What's the point of the volatile keyword?

I've been doing some embedded development at work and on hobby rpi and arduino projects. Seems like I ought to figure out what the point of the volatile keyword is at this stage in the game. Here's the reference I found about it: `volatileReference <https://www.embedded.com/electronics-blogs/beginner-s-corner/4023801/Introduction-to-the-Volatile-Keyword/>`_ volatile reference.


I'm unable after a half hour of experimenting to make heads or tails of it. It seems like the compiler will optimize away bits of code that deal with a variable that ought not to change. I think this is a main concern in multithreaded programming. Now I wonder if the keyword is still relevant or if the compilers these days are all aware of multithreaded programming and volatile is unneccesary.

.. code-block:: c
	#include <pthread.h>
	#include <stdio.h>
	#include <unistd.h>
	
	static int x;
  	// static volatile int x;
	
	void * f1( void* args )
	{
		x = 0;
		while( x == 0 )
		{
			sleep(1);
		}
		return NULL;
	}
	
	void * f2( void * args )
	{
		x = 10;
		return NULL;
	}
	int main(){
		x = 0;
		pthread_t t1;
		pthread_create( &t1, NULL, f1, NULL );
		int rc1;
		rc1 = pthread_detach( t1 );
	
		pthread_t t2;
		pthread_create( &t2, NULL, f2, NULL );
		int rc2;
		rc2 = pthread_detach( t2 );
	}
    
I've compiled this without the volatile keyword with -O3 and without and either way it doesn't loop infinitely. I guess my understanding from the code snippet on embedded.com was that the compiler ought to be dumb and think that x would be 0 forever and optimize the x==0 away, making the loop run forever. That didn't happen, I haven't come across "volatile" in the professional work I've done, and it's not in the texts I've read. I'm busy and I'm just going to have to assume "volatile" isn't worth using. I'll talk to coworkers and read a bit more later but for now that's the conclusion I'm drawing and I'm going to sleep.

 
