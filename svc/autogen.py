survey =  """[
    {
        "id": "user_name",
        "label": "Please enter your name",
        "placeholder": "John Doe",
        "type": "input"
    },
    {
        "actions": [
            {
                "operation": [
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    1
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_improvement"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_often_features"
                                        ]
                                    }
                                }
                            ]
                        ]
                    },
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    2
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_improvement"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_often_features"
                                        ]
                                    }
                                }
                            ]
                        ]
                    },
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    3
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_improvement"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_often_features"
                                        ]
                                    }
                                }
                            ]
                        ]
                    }
                ],
                "trigger": "change"
            }
        ],
        "id": "DXlJci5-VCNXNYWFFdhb5",
        "label": "How long have you been using our product or service?",
        "type": "radio",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "1",
                    "display_value": "3- 6 months"
                },
                {
                    "api_value": "2",
                    "display_value": "less than 2 months"
                },
                {
                    "api_value": "3",
                    "display_value": "1 - 2 years"
                }
            ],
            "type": "static"
        }
    },
    {
        "actions": [
            {
                "operation": [
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    "no"
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_what_not_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_what_found"
                                        ]
                                    }
                                }
                            ]
                        ]
                    },
                    {
                        "if": [
                            {
                                "==": [
                                    {
                                        "var": "input"
                                    },
                                    "yes"
                                ]
                            },
                            [
                                {
                                    "update": {
                                        "body": {
                                            "hide": true
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_what_not_found"
                                        ]
                                    }
                                },
                                {
                                    "update": {
                                        "body": {
                                            "hide": false
                                        },
                                        "bodyType": "object",
                                        "entity": [
                                            "formsReducer.ask_what_found"
                                        ]
                                    }
                                }
                            ]
                        ]
                    }
                ],
                "trigger": "change"
            }
        ],
        "hide": true,
        "id": "ask_found",
        "label": "Did you found what you were looking for?",
        "type": "radio",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "no",
                    "display_value": "No"
                },
                {
                    "api_value": "yes",
                    "display_value": "Yes"
                }
            ],
            "type": "static"
        }
    },
    {
        "hide": true,
        "id": "ask_what_not_found",
        "label": "Can you please describe what you were looking for in and found missing in the product?",
        "placeholder": "",
        "type": "input"
    },
    {
        "hide": true,
        "id": "ask_what_found",
        "label": "Can you describe what features you would like to see in future?",
        "type": "input"
    },
    {
        "hide": true,
        "id": "ask_improvement",
        "label": "What do you think we should improve in our product or service?",
        "type": "checkbox",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "new_features",
                    "display_value": "Introduce new features"
                },
                {
                    "api_value": "customer_support",
                    "display_value": "Improve Customer Support"
                },
                {
                    "api_value": "performance",
                    "display_value": "Improve Performance"
                },
                {
                    "api_value": "integration",
                    "display_value": "provide support for integration"
                }
            ],
            "type": "static"
        }
    },
    {
        "hide": true,
        "id": "ask_often_features",
        "label": "What features do you use often?",
        "type": "checkbox",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "support_tickets",
                    "display_value": "Support Tickets"
                },
                {
                    "api_value": "chat_bot",
                    "display_value": "Chat Bot"
                },
                {
                    "api_value": "reports",
                    "display_value": "Analytics Reports"
                }
            ],
            "type": "static"
        }
    },
    {
        "id": "Wun7fSQFwZaPtXcO8Ibi7",
        "label": "Were your queries resolved by raising support tickets?",
        "type": "radio",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "no",
                    "display_value": "no"
                },
                {
                    "api_value": "yes",
                    "display_value": "yes"
                }
            ],
            "type": "static"
        }
    },
    {
        "id": "xMjwx0p1GUVKyrekM1vZY",
        "label": "Can you describe your pain points while using support tickets?",
        "placeholder": "e.g. long waiting time",
        "type": "input"
    },
    {
        "id": "d13IwC8KC-YU0WwP4WG8J",
        "label": "Were enough details on the report?",
        "type": "radio",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "no",
                    "display_value": "some new fields should be added"
                },
                {
                    "api_value": "yes",
                    "display_value": "yes, details were sufficient"
                }
            ],
            "type": "static"
        }
    },
    {
        "id": "MIuRbUZA8cVDWdsY83R5t",
        "label": "What fields you want to see in your report?",
        "placeholder": "e.g. predicted budget",
        "type": "input"
    },
    {
        "id": "puM5Zkndr0chuSF1lUWEr",
        "label": "What score would you give out of 10 to your experience while using bot?",
        "type": "input"
    },
    {
        "id": "pOrR2SDIMMl6FC1EUZWgf",
        "label": "What improvements would you like to suggest for bot?",
        "type": "radio",
        "valuesAllowed": {
            "fetchOptions": false,
            "options": [
                {
                    "api_value": "func",
                    "display_value": "Additional functionality"
                },
                {
                    "api_value": "performance",
                    "display_value": "Performance"
                },
                {
                    "api_value": "memo",
                    "display_value": "Should remember already provided details"
                }
            ],
            "type": "static"
        }
    },
    {
        "id": "W6kDlP0EyVP5RxeTnPM88",
        "label": "What are the features you would like to be in bot?",
        "placeholder": "e.g. AI Integration",
        "type": "input"
    },
    {
        "id": "2xaZjhRL-R814EzLH8j6f",
        "label": "Based on your experience how likely are you to recommend this product to a friend?",
        "type": "rating"
    }
]"""

import json
survey_data = json.loads(survey)