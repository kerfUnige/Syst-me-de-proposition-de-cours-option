# On ne peut pas caster NoneType.
def null(value_ofAttribut)->bool:
    if value_ofAttribut is None:
        return True
    else:
        return False