FP vs OOP
##########################################

:date: 2018-03-15
:modified: 2018-03-15 22:20
:tags: c++ functional FP 
:category: programming
:slug: FP vs OOP
:authors: Melvyn Drag
:summary: A couple of quick thoughts about FP vs OOP

*****************************
FP vs OOP
*****************************
I've been working on a large C++/Java project at work and have found that OOP is not without it's pitfalls. 

I've been writing classes for everything and loving them for years for academic and personal projects, but did more functional/procedural coding when I was working in datascience. For me, functional programming is all about functions taking values as parameters and returning values without mutating state. Global variables being mutated inside functions would be again the FP philosophy and it does add complexity to a program because it is difficult to know the value of the variable at any point in time. 

I've always had a little bit of fear of global variables, but I understand from and optimization / resource constrained perspective they can be useful. But OOP seems to create lots of little environments with their own nefarious global variables. m_memberVariable is global within a class and when there are many member functions mutating the member variables it can become extremely unwieldy to maintain in certain large, complex classes. 

Programming is complex, there's no way around it.

Interested one day to do more serious scala projects than the little hobby things I've done to think more about the fusion of the two styles.
