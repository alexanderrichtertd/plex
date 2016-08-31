_lightFilterNodes = {}
def addLightFilterClassification(lights, lightFilterType):
    for light in lights.split(" "):
        if not light in _lightFilterNodes:
            _lightFilterNodes[light] = [];
        _lightFilterNodes[light].append(lightFilterType)
    
    
def getLightFilterClassification(light):
    if light in _lightFilterNodes:
        return _lightFilterNodes[light]
    return []
    
