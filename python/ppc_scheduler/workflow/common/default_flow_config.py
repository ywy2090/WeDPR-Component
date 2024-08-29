flow_dict = {
    "PSI": [
        {
            "index": 1,
            "type": "T_PSI",
            "isParamsProvided": False,
            "params": {
                "type": 0,
                "algorithm": 0,
                "syncResult": True,
                "parties": [
                    {
                        "index": "",
                        "partyIndex": 1
                    },
                    {
                        "index": "",
                        "partyIndex": 0,
                        "data": {
                            "index": "",
                            "input": {
                                "type": 2,
                                "path": ""
                            },
                            "output": {
                                "type": 2,
                                "path": ""
                            }
                        }
                    }
                ]
            }
        }
    ],

    "MPC": [
        {
            "index": 1,
            "type": "T_MPC"
        }
    ],

    "PSI_MPC": [
        {
            "index": 1,
            "type": "T_PSI"
        },
        {
            "index": 2,
            "type": "T_MPC",
            "upstreams": [
                {
                    "index": 1,
                    "output_input_map": [
                        "0:0"
                    ]
                }
            ]
        }
    ],

    "PREPROCESSING": [
        {
            "index": 1,
            "type": "T_PREPROCESSING"
        }
    ],

    "FEATURE_ENGINEERING": [
        {
            "index": 1,
            "type": "T_PREPROCESSING"
        },
        {
            "index": 2,
            "type": "T_FEATURE_ENGINEERING",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        }
    ],

    "TRAINING": [
        {
            "index": 1,
            "type": "T_PREPROCESSING"
        },
        {
            "index": 2,
            "type": "T_TRAINING",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        }
    ],

    "PREDICTION": [
        {
            "index": 1,
            "type": "T_PREPROCESSING"
        },
        {
            "index": 2,
            "type": "T_PREDICTION",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        }
    ],

    "FEATURE_ENGINEERING_TRAINING": [
        {
            "index": 1,
            "type": "T_PREPROCESSING"
        },
        {
            "index": 2,
            "type": "T_FEATURE_ENGINEERING",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        },
        {
            "index": 3,
            "type": "T_TRAINING",
            "upstreams": [
                {
                    "index": 2
                }
            ]
        }
    ],

    "PSI_FEATURE_ENGINEERING": [
        {
            "index": 1,
            "type": "T_PSI"
        },
        {
            "index": 2,
            "type": "T_PREPROCESSING",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        },
        {
            "index": 3,
            "type": "T_FEATURE_ENGINEERING",
            "upstreams": [
                {
                    "index": 2
                }
            ]
        }
    ],

    "PSI_TRAINING": [
        {
            "index": 1,
            "type": "T_PSI"
        },
        {
            "index": 2,
            "type": "T_PREPROCESSING",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        },
        {
            "index": 3,
            "type": "T_TRAINING",
            "upstreams": [
                {
                    "index": 2
                }
            ]
        }
    ],

    "PSI_FEATURE_ENGINEERING_TRAINING": [
        {
            "index": 1,
            "type": "T_PSI"
        },
        {
            "index": 2,
            "type": "T_PREPROCESSING",
            "upstreams": [
                {
                    "index": 1
                }
            ]
        },
        {
            "index": 3,
            "type": "T_FEATURE_ENGINEERING",
            "upstreams": [
                {
                    "index": 2
                }
            ]
        },
        {
            "index": 4,
            "type": "T_TRAINING",
            "upstreams": [
                {
                    "index": 3
                }
            ]
        }
    ]
}
