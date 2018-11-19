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

Just a quick refresher on move semantics and c++11 to keep it in mind, since the opportunities to use this stuff isn't always there, and if ya don't use it ya lose it.


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


References
-----------
1. `Bo's video 1 <https://www.youtube.com/watch?v=IOkgBrXCtfo&index=3&list=PL5jc9xFGsL8FWtnZBeTqZBbniyw0uHyaH/>`_ 
2. `Bo's video 2 <https://www.youtube.com/watch?v=0xcCNnWEMgs&list=PL5jc9xFGsL8FWtnZBeTqZBbniyw0uHyaH&index=4/>`_
3. `Stackoverflow post. Link might die but it's good right now. <https://stackoverflow.com/questions/3413470/what-is-stdmove-and-when-should-it-be-used/>`_
4. `Scary video about move semantics and OOP <https://www.youtube.com/watch?v=PNRju6_yn3o/>`_


.. code-block:: python

    import gensim
    import multiprocessing
    
    dirname="/home/temp/nltk_data/corpora/brown"    
    documents = gensim.models.doc2vec.TaggedBrownCorpus(dirname)
    cores = multiprocessing.cpu_count()
    model = gensim.models.Doc2Vec(dm=0, dbow_words=1, size=200, window=8, min_count=19, iter=10, workers=cores)
    model.build_vocab(documents)
    model.train(documents)
    
    # I'll explain the doc_of_interest in a minute.
    doc_of_interest = "/home/temp/nltk_data/corpora/brown/ca01_SENT_0" 
    like_doc_of_interest = model.docvecs.most_similar(positive=[doc_id], topn=5)
    print(like_doc_of_interest)

And this code was throwing the following error. 
    
::
    
    /home/temp/anaconda3/lib/python3.5/site-packages/gensim/models/doc2vec.py", line 448, in most_similar
    elif doc in self.doctags or doc < self.count:
    TypeError: unorderable types: str() < int()

At this point I knew we were in for the standard procedure of working on code in a linux environment: Find the source code, read it carefully for  a few hours, scratch our heads, swear a bit, and then realize what hair-brained thing is going on before proceeding to fix it. I had been playing iwith doc2vec earlier in the day and had already seen this error and intuited that it meant the the doc_id you are passing to the most_similar function doesn't exist. I didn't know how the TaggedBrownCorpus class worked, but in the `source <https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/models/doc2vec.py>`_ it said that it takes a dirname parameter - I correctly guessed that they meant the location of the brown corpus in your nltk download. This was strange to me because in the NLTK package if you

.. code-block:: python

    from nltk.corpus import brown

and you haven't yet installed the corpus with the nltk.download() command, it spits out an error saying that it can't find the corpus, and then spits out a list of standard search paths that it has checked. But gensim didn't do that so that seemed weird - this is an idea for a simple pull request for someone to work on and send.

Anyway, I looked at the TaggedBrownCorpus class in the source

.. code-block:: python

    class TaggedBrownCorpus(object):
        """Iterate over documents from the Brown corpus (part of NLTK data), yielding
        each document out as a TaggedDocument object."""
        def __init__(self, dirname):
            self.dirname = dirname
    
        def __iter__(self):
            for fname in os.listdir(self.dirname):
                fname = os.path.join(self.dirname, fname)
                if not os.path.isfile(fname):
                    continue
                for item_no, line in enumerate(utils.smart_open(fname)):
                    line = utils.to_unicode(line)
                    # each file line is a single document in the Brown corpus
                    # each token is WORD/POS_TAG
                    token_tags = [t.split('/') for t in line.split() if len(t.split('/')) == 2]
                    # ignore words with non-alphabetic tags like ",", "!" etc (punctuation, weird stuff)
                    words = ["%s/%s" % (token.lower(), tag[:2]) for token, tag in token_tags if tag[:2].isalpha()]
                    if not words:  # don't bother sending out empty documents
                        continue
                    yield TaggedDocument(words, ['%s_SENT_%s' % (fname, item_no)])

It's hard to see this in the documentation, but the iterator given by the class gives TaggedDocuments that consist of a list of words and a list of labels. In this class, the labels are:

.. code-block:: python
    
    ['%s_SENT_%s' % (fname, item_no)]

So I just thought I'd look at the first sentence and see what it was similar to. It seemed that the first sentence would be labelled

.. code-block:: python 

    doc_id = "/home/temp/nltk_data/corpora/brown/ca01_SENT_0"
 
Because when I did an ls or ll in "/home/temp/nltk_data/corpora/brown/", ca01 was the first file listed. And the item_no in the for loop above would start at 0. *(If you don't already love it, look into the enumerate() function in python, it is very useful and idiomatic.)* Long story short, the first document was ca01_SENT_2. I figured this out with the following code:

.. code-block:: python

    import gensim
    import multiprocessing
    
    dirname="/home/temp/nltk_data/corpora/brown"
    
    documents = gensim.models.doc2vec.TaggedBrownCorpus(dirname)
    
    all_docs = list(documents)
    all_tags = [tagged_document.tags[0] for tagged_document in all_docs]
    all_tags = [at for at in all_tags if 'CONTENT' not in at] 
    all_tags = [at for at in all_tags if 'ca01' in at] 
    all_tags.sort()
    print(all_tags)

Then, I was really perplexed, so I went to look at the ca01 file. As it turns out, the lines in these files are separated by two blank lines. So, the first non-empty line is not line0, not line 1, but line 2. Then line 5, 8, and so on, skipping two lines in between.

T
