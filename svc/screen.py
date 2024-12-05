

screen_layout  = {
  "id": "2d31973eafa04208a845e88cf0d4886e",
  "tenant": "trackshipment",
  "group_name": "survey",
  "name": "survey_1",
  "title": "survey_1",
  "link": "https://beta.studio.bankbuddy.me/renderer/single/trackshipment/survey/survey_1/",
  "data": {
    "children": [
      {
        "children": [
            {
            "id": "ay7v-Co-zmG48gk41SbPk",
            "label": "Customer feedback survey",
            "type": "label",
            "variant": "h3"
          },
          {},
          {}
        ],
        "component": [],
        "path": "page1",
        "settings": {
          "sideBarType": "none"
        },
        "translations": []
      }
    ],
    "id": "survey_1",
    "title": "survey_1"
  }
}

screen_empty= {
    "id": "5ec30a645c7944838ecb55b21bedad0e",
    "tenant": "trackshipment",
    "group_name": "survey",
    "name": "survey2",
    "title": "survey2",
    "link": "https://beta.studio.bankbuddy.me/renderer/single/trackshipment/survey/survey2/",
    "data": {
        "children": [
            {
                "children": [],
                "path": "page1"
            }
        ],
        "id": "survey2",
        "title": "survey2"
    }
}




screen = {
  "id": "2d31973eafa04208a845e88cf0d4886e",
  "tenant": "trackshipment",
  "group_name": "survey",
  "name": "survey_1",
  "title": "survey_1",
  "link": "https://beta.studio.bankbuddy.me/renderer/single/trackshipment/survey/survey_1/",
  "data": {
    "children": [
      {
        "children": [
          {
            "id": "ay7v-Co-zmG48gk41SbPk",
            "label": "Customer feedback survey",
            "type": "label",
            "variant": "h3"
          },
          {
            "id": "Y8Mu-POeRrGQ5XdZ0JrFJ",
            "label": "Please enter your name",
            "placeholder": "John Doe",
            "type": "input"
          },
          {
            "id": "10EjMlIdRHpL_yo0jbyh5",
            "label": "Can you describe your experience with the product?",
            "type": "input"
          },
          {
            "actions": [
              {
                "operation": [
                  {
                    "if": [
                      {
                        "and": [
                          {
                            ">": [
                              {
                                "var": "input"
                              },
                              0
                            ]
                          },
                          {
                            "<": [
                              {
                                "var": "input"
                              },
                              5
                            ]
                          }
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
                              "formsReducer._aiSRKIyr4azr0agHxiWI",
                              "formsReducer.D8r_rtGrUG_wROj0PMODt"
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
                              "formsReducer.zysJJRa8kS8gQ5anBcCKQ"
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
                          9,
                          10
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
                              "formsReducer.zysJJRa8kS8gQ5anBcCKQ"
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
                              "formsReducer._aiSRKIyr4azr0agHxiWI",
                              "formsReducer.D8r_rtGrUG_wROj0PMODt"
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
            "id": "JOmHhSiS038mJhkIlCdG6",
            "label": "How would you rate the quality of product on scale of 1-10?",
            "type": "radio",
            "valuesAllowed": {
              "fetchOptions": false,
              "options": [
                {
                  "api_value": "1",
                  "display_value": "1"
                },
                {
                  "api_value": "2",
                  "display_value": "2"
                },
                {
                  "api_value": "3",
                  "display_value": "3"
                },
                {
                  "api_value": "4",
                  "display_value": "4"
                },
                {
                  "api_value": "5",
                  "display_value": "5"
                },
                {
                  "api_value": "6",
                  "display_value": "6"
                },
                {
                  "api_value": "7",
                  "display_value": "7"
                },
                {
                  "api_value": "8",
                  "display_value": "8"
                },
                {
                  "api_value": "9",
                  "display_value": "9"
                },
                {
                  "api_value": "10",
                  "display_value": "10"
                }
              ],
              "type": "static"
            }
          },
          {
            "actions": [],
            "id": "VDeJE7PdC0V3j8n_wRK-M",
            "label": "How was your experience while using the product?",
            "type": "rating"
          },
          {
            "hide": true,
            "id": "_aiSRKIyr4azr0agHxiWI",
            "label": "Features you liked about the product?",
            "type": "label"
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
                          "speed"
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
                              "formsReducer._aiSRKIyr4azr0agHxiWI"
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
            "id": "D8r_rtGrUG_wROj0PMODt",
            "label": "",
            "type": "checkbox",
            "valuesAllowed": {
              "fetchOptions": false,
              "options": [
                {
                  "api_value": "Value 1",
                  "display_value": "Quality"
                },
                {
                  "api_value": "Value 2",
                  "display_value": "Speed"
                },
                {
                  "api_value": "value 3",
                  "display_value": "new features"
                }
              ],
              "type": "static"
            }
          },
          {
            "hide": true,
            "id": "zysJJRa8kS8gQ5anBcCKQ",
            "label": "what are the features you want to see next?",
            "type": "checkbox",
            "valuesAllowed": {
              "fetchOptions": false,
              "options": [
                {
                  "api_value": "Value 1",
                  "display_value": "Ai Integration"
                },
                {
                  "api_value": "Value 2",
                  "display_value": "Social media compatibility"
                },
                {
                  "api_value": "menu",
                  "display_value": "Shortcut Menu"
                }
              ],
              "type": "static"
            }
          }
        ],
        "component": [],
        "path": "page1",
        "settings": {
          "sideBarType": "none"
        },
        "translations": []
      }
    ],
    "id": "survey_1",
    "title": "survey_1"
  }
}