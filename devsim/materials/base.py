from ds import set_parameter


class MaterialProperty(object):
    def __init__(self, value):
        self.value = value


class Material(object):
    name = 'isolator'
    __parameters = None

    def __init__(self, **kwargs):
        self.__parameters = []
        for name, value in kwargs.items():
            setattr(self, name, value)
            self.__parameters.append(name)

    def __repr__(self):
        return self.name

    def set_parameters_for(self, device_name, region_name):
        props = [
            p for p in dir(self)
            if not p.startswith('_') and isinstance(getattr(self, p), MaterialProperty)
        ]
        for pname in props:
            set_parameter(
                device=device_name,
                region=region_name,
                name=pname, value=getattr(self, pname)
            )

