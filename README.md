# ML_Export_Wizard
Django tool for exporting and querying structures built of multiple models.

```python
ML_EXPORT_WIZARD = {
    'Working_Files_Dir': os.path.join('/', env('WORKING_FILES_DIR'), ''),
    'Logger': 'app',
    'Log_Exceptions': True,
    "Setup_On_Start": True,
    'Exporters': [
        {
            # IntegrationFeatures - Broad export that contains all the features for all the integrations
            "name": "IntegrationFeatures",
            "exclude_fields": ["added", "updated"],
            "extra_field":[
                {
                    "column_name": "orientation_in_feature",
                    "function": "case",
                    "case_expression": {
                        "source_field": ["orientation_in_landmark", "feature_orientation"],
                        "operator": "join",
                    },
                    "when": [
                        {"condition": "FF", "value": "F"},
                        {"condition": "RR", "value": "F"},
                        {"condition": "FR", "value": "R"},
                        {"condition": "RF", "value": "R"},
                    ],
                },
            ],
            "apps" : [
                {
                    "name": "core",
                    #"include_models": [],
                    "exclude_models": ["PublicationData", "SubjectData", "SampleData", "LandmarkChromosome"],
                    "primary_model": "IntegrationLocation",
                    "models": {
                        "Integration": {
                            "dont_link_to": ["DataSet"]
                        },
                        "DataSet": {
                            "dont_link_to": ["GenomeVersion"]
                        },
                    },
                }
            ],
        },
    }
}
```
