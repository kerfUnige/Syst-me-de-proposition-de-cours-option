# On ne peut pas caster NoneType.
def avoidException(variable, value):
    if value is None:
        variable = None
    else:
        try:
            variable = float("{0:.1f}".format(float(value)))
        except TypeError:
            variable = str(value)
        except ValueError:
            variable = str(value)
    return variable