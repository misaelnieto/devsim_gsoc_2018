#!/bin/env python3


class DevsimData(object):
    """
    Simple object contains the coordinates
    Should probably be replace with numpy's dtype and loadtxt
    """
    def __init__(self, filename):
        self.filename = filename
        self.regions = {}
        self.name = None
        with open(filename, 'r') as fp:
            line = fp.readline().strip()
            if line.startswith('begin_device'):
                _, n = line.split()
                self.name = n.strip('"')
                line = fp.readline().strip()
                while line != 'end_device':
                    if line.startswith('begin_coordinates'):
                        self.coordinates = []
                        line = fp.readline().strip()
                        while line != 'end_coordinates':
                            self.coordinates.append([float(i) for i in line.strip().split()])
                            line = fp.readline().strip()
                    elif line.startswith('begin_region'):
                        _, rname, rmaterial = line.split()
                        rname = rname.strip('"')
                        self.regions[rname] = {
                            'material': rmaterial.strip('"'),
                            'nodes': [],
                            'node_solutions': {},
                            'edges': [],
                            'edge_solutions': {},
                        }
                        line = fp.readline().strip()
                        while line != 'end_region':
                            if line.startswith('begin_nodes'):
                                line = fp.readline().strip()
                                while line != 'end_nodes':
                                    self.regions[rname]['nodes'].append(int(line.strip()))
                                    line = fp.readline().strip()
                            elif line.startswith('begin_edges'):
                                line = fp.readline().strip()
                                while line != 'end_edges':
                                    self.regions[rname]['edges'].append(
                                        [int(e) for e in line.split()]
                                    )
                                    line = fp.readline().strip()
                            elif line.startswith('begin_node_solution'):
                                _, sname = line.split()
                                sname = sname.strip('"')
                                self.regions[rname]['node_solutions'][sname] = []
                                line = fp.readline().strip()
                                while line != 'end_node_solution':
                                    self.regions[rname]['node_solutions'][sname].append(float(line.strip()))
                                    line = fp.readline().strip()
                            elif line.startswith('begin_edge_solution'):
                                _, sname = line.split()
                                sname = sname.strip('"')
                                self.regions[rname]['edge_solutions'][sname] = []
                                line = fp.readline().strip()
                                while line != 'end_edge_solution':
                                    self.regions[rname]['edge_solutions'][sname].append(float(line.strip()))
                                    line = fp.readline().strip()
                            line = fp.readline().strip()
                    line = fp.readline().strip()
    def __str__(self):
        return 'DevsimData "{}" ({} regions)'.format(self.name, len(self.regions))


if __name__ == '__main__':
    d = DevsimData('../resistor.dat')
    print(d)
