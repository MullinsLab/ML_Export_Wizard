# ML_Export_Wizard
ML Export Wizard is a Django app that composes flat square data structures from Django ORM models.  It is designed to shore up a weakness of an ORM where it is hard to link models into larger data structures that span many objects, as well as multiple apps.  These flat data structures are very useful for building HTML tables that span multiple models, as well as exporting data to flat files.

Resulting data structures are queryable, sortable, and since they generate only a single database query, they are fast.

The tool uses introspection to understand the Django models used and establish their relationships.  It does this when the server is run, so it will detect any changes to models without need to update settings.

Sample settings structure:

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
