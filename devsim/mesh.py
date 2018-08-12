"""
Mesh objects and routines
"""

import uuid
import enum
from ds import *


class Region(object):
    """A Region within a Semiconductor"""
    def __init__(self, name, material):
        super(Region, self).__init__()
        self.name = name
        self.material = material

    def __str__(self):
        return self.name


class Mesh(object):
    """
    The Mesh is the base of the simulation. As of now, only 1d meshes are
    implemented

    name : give a name to this Mesh. If you don't give one, a uuid will be
           used instead

    """

    def __init__(self, name=None, dimension='1D'):
        self.name = name or 'mesh-%s' % str(uuid.uuid4())[:8]
        if dimension == '1D':
            create_1d_mesh(mesh=self.name)
        elif dimension == '2D':
            create_2d_mesh(mesh=self.name)
        elif dimension == '3D':
            create_3d_mesh(mesh=self.name)
        else:
            raise('Wrong dimension type: {}'.format(dimension))

        self.contacts = []
        self.regions = []

    def __str__(self):
        print("Mesh id: {}\n".format(self.name))
        print("Contacts: {}\n".format(','.join(self.contacts)))
        print("Regions: {}\n".format(','.join(self.regions)))

    def add_line(self, position, spacing, tag):
        """
        Add a line to the mesh

        position: Position
        spacing: Positive spacing
        tag: a tag for ...?

        The spacing option is *positive spacing* to the next line that you have
        added.

        Additional lines are spaced from the first line using ps to the next
        specified line. The spacing of the lines are gradually spaced out to
        meet the spacing line of the next added line.

        So if you have thre lines::

            x=0.0 spacing=0.1
            x=1.0 spacing=1.0
            x=10.0 spacing=1.0

        The positions of the nodes should be about: 10 nodes from `0.0 um` to
        `0.1 um` and 10 nodes from `1.0 um` to `10.0 um` and no nodes from 10
        up.

        The purpose of this is to have tight mesh spacing in areas where it is
        important. If you had tight spacing everywhere, it could make the
        simulation much slower.
        """
        scale = 1e-6
        add_1d_mesh_line(
            mesh=self.name,
            pos=position * scale,
            ps=spacing * scale,
            tag=tag
        )

    def add_contact(self, name, tag, material):
        """
        Add a contact to this mesh

        name: a name for this contact
        tag: a tag for ...?
        material: The material for the contact ...???
        """
        add_1d_contact(mesh=self.name, name=name, tag=tag, material=str(material))
        self.contacts.append(name)

    def add_region(self, name, material, tag1, tag2):
        """
        name: The name of the region
        material: Any material from the enums Metals, Semiconductors

        Example:
        mesh.add_region(
            name='Cell Substrate',
            material=materials.Semiconductors.Silicon,
            tag1='top', tag2='bottom'
        )

        Example with custom parameters for Silicon:

        mesh.add_region(
            name='Cell Substrate',
            material=materials.Silicon(T=327, taun=1e16, taup=1.44e-6),
            tag1='top', tag2='bottom'
        )
        """
        # Use the material class name as material name parameter to add_1d_region?
        add_1d_region(
            mesh=self.name, material=str(material), region=name, tag1=tag1, tag2=tag2
        )
        # Maybe add name, material as tuple?
        self.regions.append(Region(name, material))

    def add_2d_line(self, direction, position, spacing, scale=1e-6):
        add_2d_mesh_line(
            mesh=self.name,
            dir=direction,
            pos=position * scale,
            ps=spacing * scale
        )

    def add_2d_contact(self, name, material, region, **kwargs):
        """
        Add a 2D contact to this mesh
        """
        # add_2d_contact(mesh="dio", name="top", material="metal", region=region, yl=0.8e-5, yh=1e-5, xl=0, xh=0, bloat=1e-10)

        self.contacts.append(name)
        add_2d_contact(
            mesh=self.name,
            name=name,
            material=str(material),
            region=region,
            **kwargs
        )

    def add_2d_region(self, name, material, **kwargs):
        self.regions.append(Region(name, material))
        add_2d_region(mesh=self.name, material=str(material), region=name, **kwargs)

    def finalize(self):
        """
        Last step before simulation. If you use this with a Device, it will
        call this for you.
        """
        finalize_mesh(mesh=self.name)
