# Google Summer of Code 2018 Report

- Project name: **Enable DEVSIM to simulate solar cells**
- GSOC project : https://summerofcode.withgoogle.com/projects/#6392690430705664
- Student: **Noe Nieto** <nnnieto@noenieto.com>
- Link to the repository: https://github.com/misaelnieto/devsim_gsoc_2018 (master branch)
- 

## Introduction

This project is about enhancing DEVSIM to make it able to simulate solar cells. All the code for this project is on the Github repository. This document is also part of it. Also there are no branches, so everything is in master.

The main task to solve on this project was: "In order to simulate a solar cell it is necessary to simulate the propagation of light into the structure and calculate the resulting electrical current."

While studying the examples on devsim I reorganized the code a little bit and the result started to become an object-oriented API over the devsim core functions. So a lot of time was spentto propose an object oriented framework in which users could 

The process to simulate a solar cell I came aout after the project is as follows:

1. Mesh creation.
2. Material configuration.
3. Doping of the structure.
4. Setup illumination conditions (i.e. AM0).
5. Setup Beer-Lambert model for photogeneration.
6. Compute initial solution
7. Solve the simulation with different conditions.
8. Compute/extract the figures of merit (Isc, Voc, IV Curve, etc.)
8. Export data (can be done in between the steps before)

The implementation details will be explained in the following sections.

## Mesh creation

Initially we thought that we'd need an external tool to define the mesh for the simulation, but after reading through the examples I found that there was already an example of the simulation of a diode in 1D, so I took this as a base because the structure of a simple solar is like a diode.


## Material configuration

Devsim needs to know the different parameters of a material. The upstream version of devsim has a collection of functions that help to configure parameters for materials. 


So the A Mesh was created by using devsim's native functions. Devsim supports the extraction of the mesh along with the resulting data into a data file in plain text. Altough it was not required, a tool called (tracey)[https://github.com/misaelnieto/tracey] was developed to inspect the data dumped by devsim.

2. Material configuration. Devsim can account for properties of materials like Silicon. As i was working to understand the 

Modeling the propagation of light through the semiconductor structure using one of
these methods:
a.
Ray tracing
b.
Transfer matrix method
c.
Beam propagation method
d.
Finite difference time domain
3.
Implementing the equations coupling light intensity and the generation of current in
the semiconductor, on 1D and 2D.
4.
Simulate figures of merit: Isc, Voc, Jsc, Pmax, Power curve, Fill Factor and IV curve.

