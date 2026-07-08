---
type: Reference
title: "Cloud Document AI API  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/reference/rest](https://docs.cloud.google.com/document-ai/docs/reference/rest)"
timestamp: 2026-07-06T03:34:16Z
---
# Cloud Document AI API  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/reference/rest](https://docs.cloud.google.com/document-ai/docs/reference/rest)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Reference](https://docs.cloud.google.com/document-ai/docs/reference)

Send feedback

# Cloud Document AI API Stay organized with collections Save and categorize content based on your preferences.



Service to parse structured information from unstructured or semi-structured documents using state-of-the-art Google AI such as natural language, computer vision, translation, and AutoML.

## Service: documentai.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery documents:

* <https://documentai.googleapis.com/$discovery/rest?version=v1>
* <https://documentai.googleapis.com/$discovery/rest?version=v1beta3>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://documentai.googleapis.com`
* `https://eu-documentai.googleapis.com`
* `https://us-documentai.googleapis.com`

### Regional service endpoint

A regional service endpoint is a base URL that specifies the network address of an API service in a single region. A service that is available in multiple regions might have multiple regional endpoints. Select a location to see its regional service endpoint for this service.

global us eu asia-south1 asia-southeast1 northamerica-northeast1 australia-southeast1 europe-west2 europe-west3

- `https://documentai.googleapis.com`

A regional service endpoint is a base URL that specifies the network address of an API service in a single region. A service that is available in multiple regions might have multiple regional endpoints. Select a location to see its regional service endpoint for this service.

global us eu asia-south1 asia-southeast1 northamerica-northeast1 australia-southeast1 europe-west2 europe-west3

- `https://eu-documentai.googleapis.com`

A regional service endpoint is a base URL that specifies the network address of an API service in a single region. A service that is available in multiple regions might have multiple regional endpoints. Select a location to see its regional service endpoint for this service.

global us eu asia-south1 asia-southeast1 northamerica-northeast1 australia-southeast1 europe-west2 europe-west3

- `https://us-documentai.googleapis.com`

## REST Resource: [v1beta3.projects.locations](/document-ai/docs/reference/rest/v1beta3/projects.locations)

| Methods | |
| --- | --- |
| `fetchProcessorTypes` | `GET /v1beta3/{parent}:fetchProcessorTypes`   Fetches processor types. |
| `get` | `GET /v1beta3/{name}`   Gets information about a location. |
| `list` | `GET /v1beta3/{name}/locations`   Lists information about the supported locations for this service. |

## REST Resource: [v1beta3.projects.locations.operations](/document-ai/docs/reference/rest/v1beta3/projects.locations.operations)

| Methods | |
| --- | --- |
| `cancel` | `POST /v1beta3/{name}:cancel`   Starts asynchronous cancellation on a long-running operation. |
| `get` | `GET /v1beta3/{name}`   Gets the latest state of a long-running operation. |
| `list` | `GET /v1beta3/{name}`   Lists service operations that match the specified filter in the request. |

## REST Resource: [v1beta3.projects.locations.processorTypes](/document-ai/docs/reference/rest/v1beta3/projects.locations.processorTypes)

| Methods | |
| --- | --- |
| `get` | `GET /v1beta3/{name}`   Gets a processor type detail. |
| `list` | `GET /v1beta3/{parent}/processorTypes`   Lists the processor types that exist. |

## REST Resource: [v1beta3.projects.locations.processors](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors)

| Methods | |
| --- | --- |
| `batchProcess` | `POST /v1beta3/{name}:batchProcess`   LRO endpoint to batch process many documents. |
| `create` | `POST /v1beta3/{parent}/processors`   Creates a processor from the `ProcessorType` provided. |
| `delete` | `DELETE /v1beta3/{name}`   Deletes the processor, unloads all deployed model artifacts if it was enabled and then deletes all artifacts associated with this processor. |
| `disable` | `POST /v1beta3/{name}:disable`   Disables a processor |
| `enable` | `POST /v1beta3/{name}:enable`   Enables a processor |
| `get` | `GET /v1beta3/{name}`   Gets a processor detail. |
| `list` | `GET /v1beta3/{parent}/processors`   Lists all processors which belong to this project. |
| `process` | `POST /v1beta3/{name}:process`   Processes a single document. |
| `setDefaultProcessorVersion` | `POST /v1beta3/{processor}:setDefaultProcessorVersion`   Set the default (active) version of a `Processor` that will be used in `ProcessDocument` and `BatchProcessDocuments`. |
| `updateDataset` | `PATCH /v1beta3/{dataset.name}`   Updates metadata associated with a dataset. |

## REST Resource: [v1beta3.projects.locations.processors.dataset](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.dataset)

| Methods | |
| --- | --- |
| `batchDeleteDocuments` | `POST /v1beta3/{dataset}:batchDeleteDocuments`   Deletes a set of documents. |
| `getDatasetSchema` | `GET /v1beta3/{name}`   Gets the `DatasetSchema` of a `Dataset`. |
| `getDocument` | `GET /v1beta3/{dataset}:getDocument`   Returns relevant fields present in the requested document. |
| `importDocuments` | `POST /v1beta3/{dataset}:importDocuments`   Import documents into a dataset. |
| `listDocuments` | `POST /v1beta3/{dataset}:listDocuments`   Returns a list of documents present in the dataset. |
| `updateDatasetSchema` | `PATCH /v1beta3/{datasetSchema.name}`   Updates a `DatasetSchema`. |

## REST Resource: [v1beta3.projects.locations.processors.humanReviewConfig](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.humanReviewConfig)

| Methods | |
| --- | --- |
| `reviewDocument  (deprecated)` | `POST /v1beta3/{humanReviewConfig}:reviewDocument`   Send a document for Human Review. |

## REST Resource: [v1beta3.projects.locations.processors.processorVersions](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions)

| Methods | |
| --- | --- |
| `batchProcess` | `POST /v1beta3/{name}:batchProcess`   LRO endpoint to batch process many documents. |
| `delete` | `DELETE /v1beta3/{name}`   Deletes the processor version, all artifacts under the processor version will be deleted. |
| `deploy` | `POST /v1beta3/{name}:deploy`   Deploys the processor version. |
| `evaluateProcessorVersion` | `POST /v1beta3/{processorVersion}:evaluateProcessorVersion`   Evaluates a ProcessorVersion against annotated documents, producing an Evaluation. |
| `get` | `GET /v1beta3/{name}`   Gets a processor version detail. |
| `importProcessorVersion` | `POST /v1beta3/{parent}/processorVersions:importProcessorVersion`   Imports a processor version from source processor version. |
| `list` | `GET /v1beta3/{parent}/processorVersions`   Lists all versions of a processor. |
| `process` | `POST /v1beta3/{name}:process`   Processes a single document. |
| `train` | `POST /v1beta3/{parent}/processorVersions:train`   Trains a new processor version. |
| `undeploy` | `POST /v1beta3/{name}:undeploy`   Undeploys the processor version. |

## REST Resource: [v1beta3.projects.locations.processors.processorVersions.evaluations](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions.evaluations)

| Methods | |
| --- | --- |
| `get` | `GET /v1beta3/{name}`   Retrieves a specific evaluation. |
| `list` | `GET /v1beta3/{parent}/evaluations`   Retrieves a set of evaluations for a given processor version. |

## REST Resource: [v1beta3.projects.locations.schemas](/document-ai/docs/reference/rest/v1beta3/projects.locations.schemas)

| Methods | |
| --- | --- |
| `create` | `POST /v1beta3/{parent}/schemas`   Creates a schema. |
| `delete` | `DELETE /v1beta3/{name}`   Deletes a schema. |
| `get` | `GET /v1beta3/{name}`   Gets a schema. |
| `list` | `GET /v1beta3/{parent}/schemas`   Lists Schemas. |
| `patch` | `PATCH /v1beta3/{schema.name}`   Updates a schema. |

## REST Resource: [v1beta3.projects.locations.schemas.schemaVersions](/document-ai/docs/reference/rest/v1beta3/projects.locations.schemas.schemaVersions)

| Methods | |
| --- | --- |
| `create` | `POST /v1beta3/{parent}/schemaVersions`   Creates a schema version. |
| `delete` | `DELETE /v1beta3/{name}`   Deletes a schema version. |
| `generate` | `POST /v1beta3/{parent}/schemaVersions:generate`   Generates a schema version. |
| `get` | `GET /v1beta3/{name}`   Gets a schema version. |
| `list` | `GET /v1beta3/{parent}/schemaVersions`   Lists SchemaVersions. |
| `patch` | `PATCH /v1beta3/{schemaVersion.name}`   Updates a schema version. |

## REST Resource: [v1.projects.locations](/document-ai/docs/reference/rest/v1/projects.locations)

| Methods | |
| --- | --- |
| `fetchProcessorTypes` | `GET /v1/{parent}:fetchProcessorTypes`   Fetches processor types. |
| `get` | `GET /v1/{name}`   Gets information about a location. |
| `list` | `GET /v1/{name}/locations`   Lists information about the supported locations for this service. |

## REST Resource: [v1.projects.locations.operations](/document-ai/docs/reference/rest/v1/projects.locations.operations)

| Methods | |
| --- | --- |
| `cancel` | `POST /v1/{name}:cancel`   Starts asynchronous cancellation on a long-running operation. |
| `get` | `GET /v1/{name}`   Gets the latest state of a long-running operation. |
| `list` | `GET /v1/{name}`   Lists service operations that match the specified filter in the request. |

## REST Resource: [v1.projects.locations.processorTypes](/document-ai/docs/reference/rest/v1/projects.locations.processorTypes)

| Methods | |
| --- | --- |
| `get` | `GET /v1/{name}`   Gets a processor type detail. |
| `list` | `GET /v1/{parent}/processorTypes`   Lists the processor types that exist. |

## REST Resource: [v1.projects.locations.processors](/document-ai/docs/reference/rest/v1/projects.locations.processors)

| Methods | |
| --- | --- |
| `batchProcess` | `POST /v1/{name}:batchProcess`   LRO endpoint to batch process many documents. |
| `create` | `POST /v1/{parent}/processors`   Creates a processor from the `ProcessorType` provided. |
| `delete` | `DELETE /v1/{name}`   Deletes the processor, unloads all deployed model artifacts if it was enabled and then deletes all artifacts associated with this processor. |
| `disable` | `POST /v1/{name}:disable`   Disables a processor |
| `enable` | `POST /v1/{name}:enable`   Enables a processor |
| `get` | `GET /v1/{name}`   Gets a processor detail. |
| `list` | `GET /v1/{parent}/processors`   Lists all processors which belong to this project. |
| `process` | `POST /v1/{name}:process`   Processes a single document. |
| `setDefaultProcessorVersion` | `POST /v1/{processor}:setDefaultProcessorVersion`   Set the default (active) version of a `Processor` that will be used in `ProcessDocument` and `BatchProcessDocuments`. |

## REST Resource: [v1.projects.locations.processors.humanReviewConfig](/document-ai/docs/reference/rest/v1/projects.locations.processors.humanReviewConfig)

| Methods | |
| --- | --- |
| `reviewDocument  (deprecated)` | `POST /v1/{humanReviewConfig}:reviewDocument`   Send a document for Human Review. |

## REST Resource: [v1.projects.locations.processors.processorVersions](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions)

| Methods | |
| --- | --- |
| `batchProcess` | `POST /v1/{name}:batchProcess`   LRO endpoint to batch process many documents. |
| `delete` | `DELETE /v1/{name}`   Deletes the processor version, all artifacts under the processor version will be deleted. |
| `deploy` | `POST /v1/{name}:deploy`   Deploys the processor version. |
| `evaluateProcessorVersion` | `POST /v1/{processorVersion}:evaluateProcessorVersion`   Evaluates a ProcessorVersion against annotated documents, producing an Evaluation. |
| `get` | `GET /v1/{name}`   Gets a processor version detail. |
| `list` | `GET /v1/{parent}/processorVersions`   Lists all versions of a processor. |
| `process` | `POST /v1/{name}:process`   Processes a single document. |
| `train` | `POST /v1/{parent}/processorVersions:train`   Trains a new processor version. |
| `undeploy` | `POST /v1/{name}:undeploy`   Undeploys the processor version. |

## REST Resource: [v1.projects.locations.processors.processorVersions.evaluations](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions.evaluations)

| Methods | |
| --- | --- |
| `get` | `GET /v1/{name}`   Retrieves a specific evaluation. |
| `list` | `GET /v1/{parent}/evaluations`   Retrieves a set of evaluations for a given processor version. |

## REST Resource: [v1.projects.locations.schemas](/document-ai/docs/reference/rest/v1/projects.locations.schemas)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent}/schemas`   Creates a schema. |
| `delete` | `DELETE /v1/{name}`   Deletes a schema. |
| `get` | `GET /v1/{name}`   Gets a schema. |
| `list` | `GET /v1/{parent}/schemas`   Lists Schemas. |
| `patch` | `PATCH /v1/{schema.name}`   Updates a schema. |

## REST Resource: [v1.projects.locations.schemas.schemaVersions](/document-ai/docs/reference/rest/v1/projects.locations.schemas.schemaVersions)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent}/schemaVersions`   Creates a schema version. |
| `delete` | `DELETE /v1/{name}`   Deletes a schema version. |
| `generate` | `POST /v1/{parent}/schemaVersions:generate`   Generates a schema version. |
| `get` | `GET /v1/{name}`   Gets a schema version. |
| `list` | `GET /v1/{parent}/schemaVersions`   Lists SchemaVersions. |
| `patch` | `PATCH /v1/{schemaVersion.name}`   Updates a schema version. |

## REST Resource: [v1.projects.operations](/document-ai/docs/reference/rest/v1/projects.operations)

| Methods | |
| --- | --- |
| `get` | `GET /v1/{name}`   Gets the latest state of a long-running operation. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/reference](./document-ai-docs-reference.md)
