###############################
# Overrider Type
###############################

def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


def implements(interface_class):
    def implement(method):
        assert(f'template_{method.__name__}' in dir(interface_class))
        return method
    return implement