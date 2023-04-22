def init(
    global_vars: any = [],
):
    """Global store for sharing variables between files

    Parameters
    ----------
    global_vars : any, optional
        Global variables to define

    Usage
    -----
    state.init({'something':1})
    print(state.something) # print 1

    or

    state.init(['something'])
    print(state.something) # print None

    """
    if isinstance(global_vars, list):
        for var in global_vars:
            globals()[var] = None
    elif isinstance(global_vars, dict):
        for key in global_vars:
            globals()[key] = global_vars[key]
