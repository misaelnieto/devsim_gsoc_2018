"""
Mesh objects and routines
"""

import uuid
import enum

class Mesh(object):
    """
    The Mesh is the base of the simulation. As of now, only 1d meshes are
    implemented

    name : give a name to this Mesh. If you don't give one, a uuid will be
           used instead

    """

    def __init__(self, name=None):
        self.name = name or 'mesh-%s'%str(uuid.uuid4())[:8]
        create_1d_mesh(mesh=self.name)
        self._contacts = []
        self._regions = []

    def __str__(self):
        print("Mesh id: {}\n".format(self.name))
        print("Contacts: {}\n".format(','.join(self._contacts)))
        print("Regions: {}\n".format(','.join(self._regions)))

    def add_line(pos, ps, tag):
        """
        Add a line to the mesh

        pos: position
        ps: dunno
        tag: a tag for ...?
        """
        add_1d_mesh_line(mesh=self.name, pos=pos, ps=ps, tag=tag)

    def add_contact(self, name, tag, material):
        """
        Add a contact to this mesh

        name: a name for this contact
        tag: a tag for ...?
        material: The material for the contact ...???
        """
        add_1d_contact(mesh=self.name, name, tag, material)
        self._contacts.append(name)

    def add_region(self, name, material, region, tag1, tag2):
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
            material=materials.Semiconductors.Silicon(T=327, taun=1e16, taup=1.44e-6),
            tag1='top', tag2='bottom'
        )
        """
        _mat = isinstance(material, enum.Enum) and material() or material
        else:
        add_1d_region(
            mesh=self.name, _mat, region, tag1, tag2
        )
        self._regions.append(name)

    def finalize(self):
        """
        Last step before simulation. If you use this with a Device, it will
        call this for you.
        """
        finalize_mesh(self.name)

