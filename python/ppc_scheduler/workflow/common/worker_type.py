class WorkerType:
    # generic job worker
    T_API = 'T_API'
    T_PYTHON = 'T_PYTHON'
    T_SHELL = 'T_SHELL'

    # specific job worker
    T_PSI = 'T_PSI'
    T_MPC = 'T_MPC'
    T_PREPROCESSING = 'T_PREPROCESSING'
    T_FEATURE_ENGINEERING = 'T_FEATURE_ENGINEERING'
    T_TRAINING = 'T_TRAINING'
    T_PREDICTION = 'T_PREDICTION'

    # finish job
    T_ON_SUCCESS = 'T_ON_SUCCESS'
    T_ON_FAILURE = 'T_ON_FAILURE'
