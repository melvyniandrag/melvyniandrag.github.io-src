A couple of notes about TensorFlow, Docker, and Data Formatting 
#################################################################

:date: 2018-06-22 01:59
:modified: 2018-06-22 01:59
:tags: tensorflow, docker, machine learning 
:category: linux
:slug: about-tensorflow-docker-and-dataformatting
:authors: Melvyn Drag
:summary: A Small Post About Tensorflow

I've just seriously started working with Docker and Tensorflow after a long hiatus from machine learning, during which time I've learned alot about Linux, C++, embedded systems and more.

Now that I'm returning to the machine learning / gpgpu / higher level programming world I want to make a few quick notes for my own memory's sake and to propose an experiment that I'll try to carry out tonight or in the next few days.

To start, though, here is a basic Dockerfile I'm using to setup my cpu tensorflow environment.

.. code-block:: python
    FROM python:2.7-slim
    
    WORKDIR /app
    
    ADD . /app
    
    RUN apt-get update
    RUN pip install --trusted-host pypi.python.org -r requirements.txt
    RUN apt-get --assume-yes install python3-pip python3-dev
    RUN pip3 install --upgrade tensorflow
    
    EXPOSE 80
    
    ENV NAME World

This file gets you up and running with docker and tensorflow.

If you check out the mnist dataset that is built into tensorflow at "mnist = tf.contrib.learn.datasets.load_dataset("mnist")", if you "print(mnist.train.images.shape)" you'll see the shape is (55000,  784). Seems weird that a 2d array stores a bunch of images. Turns out from http://yann.lecun.com/exdb/mnist/index.html that they have 55k train images that are 20x20 but padded to 28x28 and 28*28 = 784 so that means that the images were flattened along an axis. An interesting question arises - do alternative flattenings change the results output by the CNN?

Option 1 is to flatten along the other axis. A more interesting option is to create a mapping for pixel indices, like pixel[1][100] -> output[355] or something and do that for all pixels in the image and use the same mapping across the whole dataset. Going to experiment with that later tonight or tomorrow as now I'm just working on tinkering with setting up my environment in diff. ways and exploring docker.
