# Cloud Document AI API  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/reference/rpc](https://docs.cloud.google.com/document-ai/docs/reference/rpc)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Reference](https://docs.cloud.google.com/document-ai/docs/reference)

Send feedback

# Cloud Document AI API Stay organized with collections Save and categorize content based on your preferences.



Service to parse structured information from unstructured or semi-structured documents using state-of-the-art Google AI such as natural language, computer vision, translation, and AutoML.

## Service: documentai.googleapis.com

The Service name `documentai.googleapis.com` is needed to create RPC client stubs.

## `google.cloud.documentai.v1.DocumentProcessorService`

| Methods | |
| --- | --- |
| `BatchProcessDocuments` | LRO endpoint to batch process many documents. |
| `CreateProcessor` | Creates a processor from the `ProcessorType` provided. |
| `DeleteProcessor` | Deletes the processor, unloads all deployed model artifacts if it was enabled and then deletes all artifacts associated with this processor. |
| `DeleteProcessorVersion` | Deletes the processor version, all artifacts under the processor version will be deleted. |
| `DeployProcessorVersion` | Deploys the processor version. |
| `DisableProcessor` | Disables a processor |
| `EnableProcessor` | Enables a processor |
| `EvaluateProcessorVersion` | Evaluates a ProcessorVersion against annotated documents, producing an Evaluation. |
| `FetchProcessorTypes` | Fetches processor types. |
| `GetEvaluation` | Retrieves a specific evaluation. |
| `GetProcessor` | Gets a processor detail. |
| `GetProcessorType` | Gets a processor type detail. |
| `GetProcessorVersion` | Gets a processor version detail. |
| `ListEvaluations` | Retrieves a set of evaluations for a given processor version. |
| `ListProcessorTypes` | Lists the processor types that exist. |
| `ListProcessorVersions` | Lists all versions of a processor. |
| `ListProcessors` | Lists all processors which belong to this project. |
| `ProcessDocument` | Processes a single document. |
| `ReviewDocument  (deprecated)` | Send a document for Human Review. |
| `SetDefaultProcessorVersion` | Set the default (active) version of a `Processor` that will be used in `ProcessDocument` and `BatchProcessDocuments`. |
| `TrainProcessorVersion` | Trains a new processor version. |
| `UndeployProcessorVersion` | Undeploys the processor version. |

## `google.cloud.documentai.v1.SchemaService`

| Methods | |
| --- | --- |
| `CreateSchema` | Creates a schema. |
| `CreateSchemaVersion` | Creates a schema version. |
| `DeleteSchema` | Deletes a schema. |
| `DeleteSchemaVersion` | Deletes a schema version. |
| `GenerateSchemaVersion` | Generates a schema version. |
| `GetSchema` | Gets a schema. |
| `GetSchemaVersion` | Gets a schema version. |
| `ListSchemaVersions` | Lists SchemaVersions. |
| `ListSchemas` | Lists Schemas. |
| `UpdateSchema` | Updates a schema. |
| `UpdateSchemaVersion` | Updates a schema version. |

## `google.cloud.documentai.v1beta3.DocumentProcessorService`

| Methods | |
| --- | --- |
| `BatchProcessDocuments` | LRO endpoint to batch process many documents. |
| `CreateProcessor` | Creates a processor from the `ProcessorType` provided. |
| `DeleteProcessor` | Deletes the processor, unloads all deployed model artifacts if it was enabled and then deletes all artifacts associated with this processor. |
| `DeleteProcessorVersion` | Deletes the processor version, all artifacts under the processor version will be deleted. |
| `DeployProcessorVersion` | Deploys the processor version. |
| `DisableProcessor` | Disables a processor |
| `EnableProcessor` | Enables a processor |
| `EvaluateProcessorVersion` | Evaluates a ProcessorVersion against annotated documents, producing an Evaluation. |
| `FetchProcessorTypes` | Fetches processor types. |
| `GetEvaluation` | Retrieves a specific evaluation. |
| `GetProcessor` | Gets a processor detail. |
| `GetProcessorType` | Gets a processor type detail. |
| `GetProcessorVersion` | Gets a processor version detail. |
| `ImportProcessorVersion` | Imports a processor version from source processor version. |
| `ListEvaluations` | Retrieves a set of evaluations for a given processor version. |
| `ListProcessorTypes` | Lists the processor types that exist. |
| `ListProcessorVersions` | Lists all versions of a processor. |
| `ListProcessors` | Lists all processors which belong to this project. |
| `ProcessDocument` | Processes a single document. |
| `ReviewDocument  (deprecated)` | Send a document for Human Review. |
| `SetDefaultProcessorVersion` | Set the default (active) version of a `Processor` that will be used in `ProcessDocument` and `BatchProcessDocuments`. |
| `TrainProcessorVersion` | Trains a new processor version. |
| `UndeployProcessorVersion` | Undeploys the processor version. |

## `google.cloud.documentai.v1beta3.DocumentService`

| Methods | |
| --- | --- |
| `BatchDeleteDocuments` | Deletes a set of documents. |
| `GetDatasetSchema` | Gets the `DatasetSchema` of a `Dataset`. |
| `GetDocument` | Returns relevant fields present in the requested document. |
| `ImportDocuments` | Import documents into a dataset. |
| `ListDocuments` | Returns a list of documents present in the dataset. |
| `UpdateDataset` | Updates metadata associated with a dataset. |
| `UpdateDatasetSchema` | Updates a `DatasetSchema`. |

## `google.cloud.documentai.v1beta3.SchemaService`

| Methods | |
| --- | --- |
| `CreateSchema` | Creates a schema. |
| `CreateSchemaVersion` | Creates a schema version. |
| `DeleteSchema` | Deletes a schema. |
| `DeleteSchemaVersion` | Deletes a schema version. |
| `GenerateSchemaVersion` | Generates a schema version. |
| `GetSchema` | Gets a schema. |
| `GetSchemaVersion` | Gets a schema version. |
| `ListSchemaVersions` | Lists SchemaVersions. |
| `ListSchemas` | Lists Schemas. |
| `UpdateSchema` | Updates a schema. |
| `UpdateSchemaVersion` | Updates a schema version. |

## `google.cloud.location.Locations`

| Methods | |
| --- | --- |
| `GetLocation` | Gets information about a location. |
| `ListLocations` | Lists information about the supported locations for this service. |

## `google.longrunning.Operations`

| Methods | |
| --- | --- |
| `CancelOperation` | Starts asynchronous cancellation on a long-running operation. |
| `GetOperation` | Gets the latest state of a long-running operation. |
| `ListOperations` | Lists service operations that match the specified filter in the request. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/reference](./document-ai-docs-reference.md)
