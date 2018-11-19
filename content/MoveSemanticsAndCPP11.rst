Move Semantics and Other C++11 Stuff
##########################################################

:date: 2018-11-19 02:40
:modified: 2018-11-19 02:40
:tags: c++ 
:category: c++
:slug: Move Semantics and Other C++11 Stuff
:authors: Melvyn Drag
:summary: Move Semantics and C++11


Introduction
-------------

Just a quick refresher on move semantics and c++11 to keep it in mind, since the opportunities to use this stuff isn't always there, and if ya don't use it ya lose it. move semantics let you pass by value super fast. Useful when passing by value and passing by reference are both needed. Use the copy constructor for creating new objects, use move for passing by value.


Move Semantics
---------------

R value references are mainly used for 2 things:
1. Moving things, which allows for a cool efficient type of constructor
2. Perfect forwarding, which allows for efficient passing of arguements through nested function calls.

R Value References
-------------------
I've seen lvalues and rvalues referred to as left/right values as well as locator/register values.

An lvalue is a value that has an address in memory. 

An rvalue is a temporary value that only live for a bit in a register and is discarded after being processed.

.. code-block:: c++
    
    void printInt( int& i ); // 1
    void printInt( int&& i ); // 2
    
    ...

    printInt( 1 ); //This calls version 2
    int x = 1;
    printInt( x ); // calls version 1

We cannot pass an integer rvalue to version 2, and without the existence of version 2 we would get a compilation error. We can pass rvalues as const references, however. So, this code is good:

.. code-block:: c++

    void printInt( const int& i );

    ...

    printInt( 1 );

I think that's weird, I read somewhere that Bjarne thought about including references to rvalues, but that it was ultimately deemed to complicated to reason about from a programmer perspective. The const reference to an rvalue is still kind of weird to me, and I don't know why they allow it. the logic is that the referenced value won't change so it's okay. Don't know how the compiler deals with it and one day it would be interesting to play around with godbolt to see what happens.

In the Bo Qian youtube tutorial, he shows how rvalue ref overloading functions can create ambiguities for the compiler:

.. code-block:: c++

    void printInt( int&& i );
    void printInt( int i );

    ...

    printInt( 1 ); // compiler error

This is similar to the ambiguity that you see in C++98

.. code-block:: c++

    void printInt( int& i );
    void printInt( int i );

    ...

    int x = 1;
    printInt(x);

A main use case of this (?)cryptic new syntax is creating move constructors, that allow you to move the contents of a container to a new memory location, leaving the old location in a useless, but destructable state. It performs a sort of shallow copy, transferring ownership of internal pointers and simple datatypes so that the values pointed to don't need to be recreated on copy.

For example:

.. code-block:: c++

    class hugeArray {
    public:
        int* array;
        size_t size;

        hugeArray( ...some parameters... ){
            ... construct ...
        }
        
        hugeArray( const hugeArray& rhs ){
            // the copy constructor has to copy the contents of rhs.array to array!
            size = rhs.size;
            array = new double[size];
            memcpy( array, rhs.array, size );
        }

        hugeArray( hugeArray&& rhs ){
            // move constructor just steals the ptr to the rhs.array!
            // note that the rhs.array is junked, set to nullptr, the rhs is junk now.
            size = rhs.size;
            array = rhs.array;
            rhs.array = nullptr;
            rhs.size = 0;
        }

        ~hugeArray() { delete[] array; }

    };

Why couldn't we just take the hugeArray by reference, trash its internal members and steal pointers? The copy constructor can take a non const parameter. I guess this new syntax gives us a way to differentiate between the two cases. Anyway, here is usage of the above class:

.. code-block:: c++
    
    void foo( hugeArray ha );
    void bar( hugeArray& ha );

    ...

    hugeArray ha = ha( ...stuff... );
    foo( ha ); // calls copy constructor
    bar( ha ); // no constructor call, by reference.
    foo( std::move( ha ) ); // but be sure not to use ha anymore. This calls the move constructor.

std::move() turns an lvalue into an rvalue. Notive that the last call to foo() above turns ha into junk, due to the move contructor call. This is dangerous and error prone. This move constructor stuff is usually hidden behind some RAII stuff ( I think ), so we don't have to worry about this error prone situation.

You can also create move assignment operators ( in addition to the move constructor shown above. So the old "rule of 3" for classes is now "rule of 3, or 5"

* destructor
* copy constructor
* assignment operator
* [new] move constructor
* [new] move assignment operator

.. code-block:: c++

    //assignment
    X& X::operator=( X const & rhs );
    X& X::operator=( X&& rhs );

This means that we get automatic speed up of code using the STL by moving to c++11 whenever we use pass by value.

Before when we ran this:

.. code-block:: c++

    void foo( std::vector<T> vec )

The code would call the copy constructor on the vec passed by value, which was wasteful because vec was a temporary. Now, the temporary passed to the function is moved into the function and we save 1/2 the time! The temporary is constructed and moved in, not constructed and copied in.

.. code-block:: c++

    #include <iostream>
    #include <chrono>
    #include <cstring>
    
    class hugeArray {
    public:
        int* array;
        size_t size;
    
        hugeArray( size_t N ){
            std::cout << "constructor" << std::endl;
            array = new int[N];
            for( size_t i = 0; i < N; ++i )
                array[i] = i;
        }
        
        hugeArray( const hugeArray& rhs ) = delete;
        
        //hugeArray( const hugeArray& rhs ){
        //    std::cout << "copy constructor" << std::endl;
        //    // the copy constructor has to copy the contents of rhs.array to array!
        //    size = rhs.size;
        //    array = new int[size];
        //    memcpy( array, rhs.array, size );
        //}
    
        //hugeArray( hugeArray&& rhs ) = delete;
        
        hugeArray( hugeArray&& rhs ){
            std::cout << "move constructor" << std::endl;
            // move constructor just steals the ptr to the rhs.array!
            // note that the rhs.array is junked, set to nullptr, the rhs is junk now.
            size = rhs.size;
            array = rhs.array;
            rhs.array = nullptr;
            rhs.size = 0;
        }
    
        ~hugeArray() { delete[] array; }
    
    };
    
    void foo( hugeArray ha ){
        std::cout << ha.array[100] << std::endl;
    }
    
    int main(){
        size_t N = 1000000;
        int niter = 100;
        auto start = std::chrono::steady_clock::now();
        for ( auto i = 0 ; i < niter; ++i ) {
            foo( hugeArray(N) );
        }
        auto end = std::chrono::steady_clock::now();
        auto diff = end - start;
        std::cout << std::chrono::duration <double, std::milli> (diff).count() << " ms" << std::endl;
    }

Note that the above example won't work as described in the Bo videos. This will cause copy elision, and we won't see any performance increase from the move constructor if we compile this with g++. So run this example and toggle the commented line in main() with the std::move line.

.. code-block:: c++

    class hugeArray {
    public:
        int* array;
        size_t size;
    
        hugeArray( size_t N ){
            std::cout << "constructor" << std::endl;
            array = new int[N];
            for( size_t i = 0; i < N; ++i )
                array[i] = i;
        }
        
        //hugeArray( const hugeArray& rhs ) = delete;
        
        hugeArray( const hugeArray& rhs ){
            std::cout << "copy constructor" << std::endl;
            size = rhs.size;
            array = new int[size];
            memcpy( array, rhs.array, size );
        }
    
        //hugeArray( hugeArray&& rhs ) = delete;
        
        hugeArray( hugeArray&& rhs ){
            std::cout << "move constructor" << std::endl;
            // move constructor just steals the ptr to the rhs.array!
            // note that the rhs.array is junked, set to nullptr, the rhs is junk now.
            size = rhs.size;
            array = rhs.array;
            rhs.array = nullptr;
            rhs.size = 0;
        }
    
        ~hugeArray() { delete[] array; }
    
    };
    
    void foo( hugeArray ha ){
        assert( ha.array[100] == 100 );
    }
    
    int main(){
        size_t N = 1000000;
        int niter = 100;
        auto start = std::chrono::steady_clock::now();
        for ( auto i = 0 ; i < niter; ++i ) {
            hugeArray ha(N);
            foo( ha );
            //foo( std::move(ha) );
        }
        auto end = std::chrono::steady_clock::now();
        auto diff = end - start;
        std::cout << std::chrono::duration <double, std::milli> (diff).count() << " ms" << std::endl;
    }

If you compile the above as g++ -std=c++11 -O0 $CPPFILE you will see the incredible performance increase from using move.

Perfect Forwarding
-------------------

Perfect forwarding, not port forwarding. Here's what its about:

    Why is this useful? Well, it means that a function template can pass its arguments through to another function whilst retaining the lvalue/rvalue nature of the function arguments by using std::forward. This is called "perfect forwarding", avoids excessive copying, and avoids the template author having to write multiple overloads for lvalue and rvalue references. - from ` here <http://www.justsoftwaresolutions.co.uk/cplusplus/rvalue_references_and_perfect_forwarding.html/>`_ .

.. code-block:: c++
    
    template< class T >
    void relay( T arg ) {
        foo( arg );
    }

Requirements / wishes for this template:
1. No costly, unnecessary copies of data.
2. The type of the arg passed to foo() should be the same type as the arg passed to relay().

If these conditions are met, we have perfect forwarding! The solution to achieve this is to rewrite relay( ) like this:

.. code-block:: c++

    template< typename T >
    void relay( T&& arg ){
        foo( std::forward<T>( arg ) );
    }

We can reason out the correctness of this approach using the C++ reference collapsing rules:

1. T& &   ==> T&
2. T& &&  ==> T&
3. T&& &  ==> T&
4. T&& && ==> T&&

as Bo Qian says - the single ref is infectious! Also, what is std::forward()?

1. std::move<T>( arg ); //turns arg into an rvalue type
2. std::forward<T>( arg ); //turns arg into a T&& type.

See the video C++11 Rvalue Reference - Perfect Forwarding for more information!

References
-----------
1. `Bo's video 1 <https://www.youtube.com/watch?v=IOkgBrXCtfo&index=3&list=PL5jc9xFGsL8FWtnZBeTqZBbniyw0uHyaH/>`_ 
2. `Bo's video 2 <https://www.youtube.com/watch?v=0xcCNnWEMgs&list=PL5jc9xFGsL8FWtnZBeTqZBbniyw0uHyaH&index=4/>`_
3. `Stackoverflow post. Link might die but it's good right now. <https://stackoverflow.com/questions/3413470/what-is-stdmove-and-when-should-it-be-used/>`_
4. `Scary video about move semantics and OOP <https://www.youtube.com/watch?v=PNRju6_yn3o/>`_
