---
type: Reference
title: "Error messages  |  Document AI  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/error-messages](https://docs.cloud.google.com/document-ai/docs/error-messages)"
timestamp: 2026-07-06T03:34:16Z
---
# Error messages  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/error-messages](https://docs.cloud.google.com/document-ai/docs/error-messages)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Resources](https://docs.cloud.google.com/document-ai/docs/resources)

Send feedback

# Error messages Stay organized with collections Save and categorize content based on your preferences.



Learn how to resolve some errors raised by
Document AI. This topic discusses errors whose resolutions
require more steps than can be described in an error message.

See the [Cloud API documentation](/apis/design/errors#handling_errors) for recommended practices of error handling.

## Permissions

The resolution requires a few steps to be carried out as outlined in the error message.

### Application default credentials are not available

If you receive this message:

```
The Application Default Credentials are not available. They are
available if running in Compute Engine. Otherwise, the
environment variable GOOGLE_APPLICATION_CREDENTIALS must be defined
pointing to a file defining the credentials.
See https://developers.google.com/accounts/docs/application-default-credentials
for more information.
```

Document AI uses
[*Application Default Credentials*](/accounts/docs/application-default-credentials)
for authentication.

You must have a service account for your
project, download the key (JSON file) for your service account to
your development environment, and then set the location of that
JSON file to an environment variable named
`GOOGLE_APPLICATION_CREDENTIALS`.

Furthermore, the `GOOGLE_APPLICATION_CREDENTIALS`
environment variable must be available within the
context that you call the Document AI API. For example, if you set
the variable from within a terminal session but run your code in the
debugger of your IDE, the execution context of your code might not
have access to the variable. In that circumtance, your request to
Document AI might fail for lack of proper
authentication.

For more information on how to set the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable,
see the Document AI
[quickstart](/document-ai/docs/quickstart-protocol)
or the documentation on
[using the Application Default Credentials](/accounts/docs/application-default-credentials).

### Permission denied

If you receive this message:

```
ERROR: (gcloud.auth.application-default.print-access-token) File
(pointed by GOOGLE_APPLICATION_CREDENTIALS environment variable) does not exist!
{
  "error": {
    "code": 403,
    "message": "The request is missing a valid API key.",
    "status": "PERMISSION_DENIED"
  }
}
```

Verify that you have a valid service account key JSON file in
the location stored in the `GOOGLE_APPLICATION_CREDENTIALS`
environment variable and that the variable points to the correct
place.

To diagnose this error, try opening the service account key file from
the folder from which you're attempting to call the Document AI API.

```
cat $GOOGLE_APPLICATION_CREDENTIALS
```

### Forbidden: 403 POST API has not been used or is disabled

If you receive the message:

```
Forbidden: 403 POST Document AI API has not been used in
project # before or it is disabled.
Enable it by visiting [url], then retry.
If you enabled this API recently, wait a few minutes for the action to
propagate and retry.
```

1. Visit the link specified in the error message and enable the
   Document AI API.
   Wait several minutes and then retry.
2. Verify that you have a valid service account key JSON file stored in
   the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
   To diagnose this error, try opening the service account key file from
   the folder from which you're attempting to call the Document AI API.

   ```
   cat $GOOGLE_APPLICATION_CREDENTIALS
   ```

### Error writing final output

If you receive a message like the following when receiving the results
of a batch process request:

```
{
  "name": "projects/project-name/operations/operation-id",
  "metadata": {
    "@type": "type.googleapis.com/google.cloud.document.v1beta1.OperationMetadata",
    "state": "SUCCEEDED",
    "createTime": "2019-09-19T02:02:15.885267760Z",
    "updateTime": "2019-09-19T02:02:31.896425001Z"
  },
  "done": true,
  "error": {
    "code": 5,
    "message": "Error writing final output to: gs://bucket-name/filename.json"
  }
}
```

Your service account may not have the correct permissions to create
objects in your Cloud Storage bucket. Be sure that you have
assigned the correct permissions to your service account, as
described in the
[quickstart](/document-ai/docs/quickstart-protocol#assign_permissions_to_your_service_account).

You might also have misspelled the name of your Cloud Storage
bucket. Verify that the bucket that you're attempting to access
exists.

### P4SA no access to Cloud Storage

When Document AI Per-Product Service Account (P4SA) has no permission to access
some Cloud Storage resources.

```
message: "Cloud DocumentAI P4SA doesn't have access to this Cloud Storage resource:"
```

### Service Account cannot create object in Cloud Storage

When Document AI Per-Product Service Account (P4SA) has no permission to create
object in Cloud Storage.

```
message: "Service account service-123@gcp-sa-prod-dai-core.iam.gserviceaccount.com
         does not have permission storage.objects.create to create
         Google Cloud Storage object in bucket gs://foo."
```

Document AI service account might not have the correct permissions to create
objects in your Cloud Storage bucket. Be sure that you have
assigned the correct permissions to the Document AI service account, as
described in the
[cross project file access setup](/document-ai/docs/setup#cross_project_file_access_setup).

You might also have misspelled the name of your Cloud Storage
bucket. Verify that the bucket that you're attempting to access
exists.

### Caller cannot get objects in Cloud Storage

When the caller of Document AI API has no permission to get objects in
Cloud Storage.

```
message: "The caller does not have permission storage.objects.get to get Google
         Cloud Storage objects in bucket gs://foo."
```

The caller of the API might not have the correct permissions to get
objects in your Cloud Storage bucket. Be sure that you have
assigned the correct permissions to the caller.

You might also have misspelled the name of your Cloud Storage
bucket. Verify that the bucket that you're attempting to access
exists.

## Invalid arguments

The resolution requires a few steps to be carried out as outlined in the error message.

### API version unsupported

When a request is made to an API version that doesn't support the
operation.

```
message: "The requested operation is unsupported for the API version."
```

### Processor type unsupported

When a request is made to an API method that doesn't support
the given processor type.

```
message: "The requested operation is unsupported for the processor type: ${PROCESSOR_TYPE}."
```

### Bad Request

When an API request is made but the request fields have one or more violations.
Each violation is captured as a `field_violations` in the `google.rpc.BadRequest`
details.

```
message: "Request contains an invalid argument."
details {
  [type.googleapis.com/google.rpc.BadRequest] {
    field_violations { field: "foo" description: "bar" }
  }
}
```

### Batch processing all documents failed

When every document in a batch processing request fails to process.

```
message: "Failed to process all documents."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "FAILED_TO_PROCESS_ALL_DOCUMENTS"
    domain: "documentai.googleapis.com"
  }
}
```

### No documents

When documents are required or expected but none are provided, such as when
importing documents by Cloud Storage URI.

```
message: "No valid documents found in ${training|test} directory. Ensure files are in a supported MIME type. For details, see https://cloud.google.com/document-ai/docs/file-types."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "NO_DOCUMENTS"
    domain: "documentai.googleapis.com"
  }
}
```

The [`gcsUriPrefix`](/document-ai/docs/send-request#async-processor) and `gcsOutputConfig.gcsUri` parameters need to begin with `gs://` and end with a trailing backslash character (`/`). Check the configuration for the bucket URIs.

Example: `gs://bucket/directory/`

### Training is not supported

When a train processor version request is made on a processor type that
doesn't support training.

```
message: "Training is not supported on processor type: ${DOCUMENT_TYPE}_PROCESSOR."
```

### No documents selected

When documents are expected, but none are selected in the dataset, such as when
creating data labeling jobs.

```
message: No documents selected. Please select at least one document."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "NO_DOCUMENTS_SELECTED"
    domain: "documentai.googleapis.com"
  }
}
```

### Document type not found

When a document's class (like license, passport, or invoice) does not match the
classification necessary for the processor type. An example is when the classifier step
in the W2 parser doesn't find elements from an invoice.

This may also appear as `Couldn't preview the document: Unable to find a document of type: 'foo'` in the Google Cloud console.
This error message is applicable to legacy processors.

```
message: "Unable to find a document of type: 'foo'"
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_OF_TYPE_NOT_FOUND"
    domain: "documentai.googleapis.com"
  }
}
```

### Document size limit exceeded

When the upper limit for the file size of a document has been exceeded while
importing dataset or while running prediction.

```
message: "Document size (2) exceeds limit: 1 (bytes)."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_SIZE_LIMIT_EXCEEDED"
    domain: "documentai.googleapis.com"
    metadata { key: "limit" value: "1" }
    metadata { key: "size" value: "2" }
  }
}
```

### Document limit exceeded

When the upper limit for the count of documents has been exceeded.

```
message: "Document count exceed the limit: 5 got 6"
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_LIMIT_EXCEEDED"
    domain: "documentai.googleapis.com"
    metadata { key: "document_limit" value: "5" }
    metadata { key: "documents" value: "6" }
  }
}
```

### Unsupported MIME type

When an unsupported MIME type was provided. The system verifies the file format
(MIME type) when you import a dataset or make a prediction call. Go to
[Supported files](/document-ai/docs/file-types) (and for [Layout Parser](/document-ai/docs/layout-parse-chunk#parser-types)) to see the available file types. If the
file format is not supported, you see the following error message:

```
message: "INVALID_ARGUMENT: Unsupported MIME type: 'foo'."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "UNSUPPORTED_MIME_TYPE"
    domain: "documentai.googleapis.com"
    metadata { key: "mime_type" value: "foo" }
  }
}
```

### No pages

When a document with no pages was provided, but one or more pages are required.

```
message: "No pages were found in the document."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "NO_PAGES"
    domain: "documentai.googleapis.com"
  }
}
```

### Negative page number

When a document lists a negative value for one of its page numbers.

```
message: "Page number cannot be negative."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "NEGATIVE_PAGE_NUMBER"
    domain: "documentai.googleapis.com"
  }
}
```

### Duplicate page numbers

When a document lists the same page number one or more times.

```
message: "Duplicate page number detected (page numbers to indices): [{1, [1, 2]}, {4, [4, 5]}]."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DUPLICATE_PAGE_NUMBERS"
    domain: "documentai.googleapis.com"
    metadata {
      key: "page_number_to_indices"
      value: "[{1, [1, 2]}, {4, [4, 5]}]"
    }
  }
}
```

### Page limit exceeded

When the upper limit of a document's total number of pages is exceeded. You
encounter this error during dataset import or prediction when a document within
the dataset has too many pages, exceeding the processor's limits.

```
message: "Document pages exceed the limit: 5 got 6"
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PAGE_LIMIT_EXCEEDED"
    domain: "documentai.googleapis.com"
    metadata { key: "page_limit" value: "5" }
    metadata { key: "pages" value: "6" }
  }
}
```

### Page limit exceeded in imageless mode

You encounter this error during dataset import or prediction when a document
within the dataset has too many pages, exceeding the processor's limits. You can
request your project be added to an allowlist to enable imageless mode, this
increases the page limit to 30.

```
message: "Document pages in non-imageless mode exceed the limit: 15 got 16. Try using imageless mode to increase the limit to 30."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PAGE_LIMIT_EXCEEDED_IN_IMAGELESS_MODE"
    domain: "documentai.googleapis.com"
    metadata { key: "page_limit" value: "15" }
    metadata { key: "pages" value: "16" }
    metadata { key: "imageless_page_limit" value: "30" }
  }
}
```

### Pretrained processor version state change

When a request to change the state of a pre-trained processor version was issued.
You encounter this error when trying to delete a pre-trained processor version.

```
message: "ProcessorVersion with id 'xyz' is pretrained by Google and cannot change states."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PRETRAINED_PROCESSOR_VERSION_STATE_CHANGE"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "abc" }
    metadata { key: "target_state" value: "DELETING" }
    metadata { key: "version_id" value: "xyz" }
  }
}
```

### Dataset validation

When a dataset fails to meet the validation criteria, for example, due to missing
page anchors, incorrect data, or incomplete details in some attributes of the
document proto object.

```
message: "Invalid dataset. See operation metadata for specific errors."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INVALID_DATASET"
    domain: "documentai.googleapis.com"
  }
}
```

### Human in the loop non inlined document for review

When a human review was kicked off for a document which was not defined inline.

```
message: "The document for review must be provided inline."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "HUMAN_REVIEW_NON_INLINED_DOCUMENT"
    domain: "documentai.googleapis.com"
  }
}
```

### Invalid Document Type

When the document type is invalid or unsupported by the processor. A *document type* refers to the category of the document (e.g., W2), not its file format or MIME type, like PDF or JPEG.

```
message: "Invalid document type: 'foo'."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INVALID_DOCUMENT_TYPE"
    domain: "documentai.googleapis.com"
    metadata { key: "type" value: "foo" }
  }
}
```

### Document span out of bounds

```
message: "Text span [1, 5) is out of bounds: [1, 3)."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_SPAN_OUT_OF_BOUNDS"
    domain: "documentai.googleapis.com"
    metadata { key: "bounds" value: "[1, 3)" }
    metadata { key: "span" value: "[1, 5)" }
    metadata { key: "type" value: "Text" }
  }
}
```

### Invalid document span

When an invalid document span, such as the start being after the end, is
provided.

```
message: "Character span is invalid. Ensure the max is greater than the min."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_SPAN_INVALID"
    domain: "documentai.googleapis.com"
    metadata { key: "span" value: "Character" }
  }
}
```

### Invalid UTF-8 document

When a document that includes invalid UTF-8 is provided.

```
message: "Document contains invalid UTF-8 text."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_INVALID_UTF_8"
    domain: "documentai.googleapis.com"
    metadata { key: "bytes" value: "[2, 3)" }
  }
}
```

### Dataset schema is invalid

When a processor doesn't have a [valid union schema](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions#DocumentSchema) or the given [dataset schema](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.dataset/updateDatasetSchema)
is not valid.

```
message: "The processor has an empty or invalid schema: "
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INVALID_SCHEMA_ERROR"
    domain: "documentai.googleapis.com"
  }
}
```

### OcrConfig Unsupported

When a processing request is issued for a processor which does not support
OcrConfig.

```
message: "OcrConfig is not supported for processor type: 'foo'."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "OCR_CONFIG_UNSUPPORTED"
    domain: "documentai.googleapis.com"
  }
}
```

### Invalid Import Config

When the import config is invalid.

```
message: "The import config is invalid: foo"
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INVALID_IMPORT_CONFIG"
    domain: "documentai.googleapis.com"
  }
}
```

### Source processor version is invalid

When attempting to [import a processor version](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions/importProcessorVersion#request-body), the source processor version is not valid to be imported.

```
message: "The source processor version is invalid in import processor version."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INVALID_SOURCE_PROCESSOR_VERSION_ERROR"
    domain: "documentai.googleapis.com"
  }
}
```

### Invalid chunk size

When the chunk size config is invalid.

```
message: "Invalid chunk size. Requested chunk size (${CHUNK_SIZE}) must be in the range of [${MIN_CHUNK_SIZE}, ${MAX_CHUNK_SIZE}]."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "INVALID_ARGUMENT"
    domain: "documentai.googleapis.com"
  }
}
```

### Document prompt size limit exceeded

When document prompt symbol number is greater than limit.

```
message: "Document prompt must be at most ${MAX_DOCUMENT_PROMPT_LENGTH} characters."
```

### Document prompt not available for processor type

When document prompt is not empty in schema which is being assigned to
non eligible processor type.

```
message: "Document prompt is not supported for processor type: ${PROCESSOR_TYPE}"
```

## Failed precondition

The resolution requires a few steps to be carried out as outlined in the error message.

### KMS key invalid

When an invalid key (e.g. it is disabled) was provided.

```
message: "KMS key 'projects/1/keys/abc' is invalid (KEY_DISABLED)."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "KMS_KEY_INVALID"
    domain: "documentai.googleapis.com"
    metadata { key: "details" value: "KEY_DISABLED" }
    metadata { key: "kms_key_name" value: "projects/1/keys/abc" }
  }
}
```

### Processor state change

When an invalid request to change the state of a processor is issued.

```
message: "Processor state cannot be changed to 'DISABLED' since it is 'DISABLED'."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_STATE_CHANGE_INVALID"
    domain: "documentai.googleapis.com"
    metadata { key: "current_state" value: "DISABLED" }
    metadata { key: "processor_id" value: "xyz" }
    metadata { key: "target_state" value: "DISABLED" }
  }
}
```

### Processor version state change

When an invalid request to change the state of a processor version is issued.

```
message: "ProcessorVersion state cannot be changed to 'DEPLOYING' since it is 'DEPLOYED'."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_VERSION_STATE_CHANGE_INVALID"
    domain: "documentai.googleapis.com"
    metadata { key: "current_state" value: "DEPLOYED" }
    metadata { key: "processor_id" value: "abc" }
    metadata { key: "target_state" value: "DEPLOYING" }
    metadata { key: "version_id" value: "xyz" }
  }
}
```

### Processor not enabled

When a request that depends on a specific processor is issued, but the processor
is not enabled.

```
message: "Processor 'xyz' is not enabled."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_NOT_ENABLED"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "xyz" }
    metadata { key: "state" value: "DISABLED" }
  }
}
```

### Processor version not deployed

When a request that depends on a specific processor version being deployed is
issued, but the processor is not deployed.

```
message: "ProcessorVersion 'abc' is not deployed."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_VERSION_NOT_DEPLOYED"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "xyz" }
    metadata { key: "state" value: "TRAINING" }
    metadata { key: "version_id" value: "abc" }
  }
}
```

### Processor default version

When a request which depends on a default version being configured is issued but
there is not one configured.

```
message: "Processor 'xyz' does not have a default version configured."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_DEFAULT_VERSION_UNSET"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "xyz" }
  }
}
```

### Processor remove default version

When a request to undeploy or delete a processor version is issued but it is
configured as the default version.

```
message: "ProcessorVersion 'xyz' cannot be undeployed or deleted as it is the default version."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_REMOVE_DEFAULT_VERSION"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "abc" }
    metadata { key: "version_id" value: "xyz" }
  }
}
```

### Dataset not initialized

When a request that requires a dataset to be initialized is issued, but the
dataset is not initialized.

```
message: "Dataset is not initialized."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DATASET_NOT_INITIALIZED"
    domain: "documentai.googleapis.com"
  }
}
```

### Dataset initialized or initializing

When a request that requires a dataset to be uninitialized is issued, but the
dataset is already initialized or is initializing.

```
message: "Dataset is already initialized or is initializing."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DATASET_INITIALIZED_OR_INITIALIZING"
    domain: "documentai.googleapis.com"
  }
}
```

### Dataset Location Not Empty Error

When a request requires a dataset storage location to be empty, but
the folder contains objects.

```
message: "Given dataset location is not empty. Please select an empty folder."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DATASET_LOCATION_NOT_EMPTY"
    domain: "documentai.googleapis.com"
  }
}
```

### Has Blocking Operation Error

When there are other operations running that are blocking the required operation.

```
message: "The operation cannot be performed due to an ongoing 'EXAMPLE_OPERATION_TYPE' blocking operation. Try again after the operation finishes."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "HAS_BLOCKING_OPERATION_ERROR"
    domain: "documentai.googleapis.com"
  }
}
```

### Page range unsupported error

When the `page_range` field isn't supported in some operation, such as in a
batch process.

```
message: "Page range is not supported."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PAGE_RANGE_UNSUPPORTED"
    domain: "documentai.googleapis.com"
  }
}
```

### Cloud Storage folder contains dataset error

When a Cloud Storage folder already contains a dataset.

```
message:  "The folder 'folder_uri' already has dataset 'dataset-id' under it."
details {
   [type.googleapis.com/google.rpc.ErrorInfo] {
     reason: "GCS_FOLDER_CONTAINS_DATASET_ERROR"
     domain: "documentai.googleapis.com"
   }
}
```

### Thumbnail Missing Error

When a dataset document thumbnail is failed to be fetched.

```
message:  "Failed to get dataset document thumbnail, consider running re-sync on the dataset."
details {
   [type.googleapis.com/google.rpc.ErrorInfo] {
     reason: "THUMBNAIL_MISSING"
     domain: "documentai.googleapis.com"
   }
}
```

### Dataset page limit exceeded

When the total page limit of a dataset has been exceeded.

```
message: "Dataset page count exceeds the limit of 5. Got 6."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DATASET_PAGE_LIMIT_EXCEEDED"
    domain: "documentai.googleapis.com"
  }
}
```

### Unsupported processor for synchronous processing

When a request is made for a processor version that is no longer supported for synchronous processing.

```
message: "Processor ${PROCESSOR_ID} version ${VERSION_ID} of type ${TYPE_NAME} is no longer supported for sync processing. Please upgrade to a newer version: https://cloud.google.com/document-ai/docs/manage-processor-versions."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "UNSUPPORTED_PROCESSOR"
    domain: "documentai.googleapis.com"
  }
}
```

## Not found

The resolution requires a few steps to be carried out as outlined in the error message.

### Evaluation not found

When an evaluation for a processor version cannot be found.

```
message: "Evaluation with ID 'qrs' not found."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "EVALUATION_NOT_FOUND"
    domain: "documentai.googleapis.com"
    metadata { key: "evaluation_id" value: "qrs" }
    metadata { key: "processor_id" value: "xyz" }
    metadata { key: "version_id" value: "abc" }
  }
}
```

### Document not found

When a document needed for an operation cannot be found.

```
message: "Document not found: 'gs://foo'."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "DOCUMENT_NOT_FOUND"
    domain: "documentai.googleapis.com"
    metadata { key: "document" value: "gs://foo" }
  }
}
```

### Processor not found

When a processor needed for an operation cannot be found.

```
message: "Processor with id 'xyz' not found."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_NOT_FOUND"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "xyz" }
  }
}
```

### Processor version not found

When a processor version needed for an operation cannot be found.

```
message: "ProcessorVersion with id 'abc' not found."
details {
  [type.googleapis.com/google.rpc.ErrorInfo] {
    reason: "PROCESSOR_VERSION_NOT_FOUND"
    domain: "documentai.googleapis.com"
    metadata { key: "processor_id" value: "xyz" }
    metadata { key: "version_id" value: "abc" }
  }
}
```

### Data Labeling Job Not Found

When a data labeling job cannot be found.

```
message: "Data labeling job with id 'EXAMPLE_DATA_LABELING_JOB' not found in processor EXAMPLE_PROCESSOR."
```

### Schema version not found

When a schema version cannot be found.

```
message: "Schema version with id 'EXAMPLE_SCHEMA_VERSION' not found."
```

### Schema not found

When a schema cannot be found.

```
message: "Schema with id 'EXAMPLE_SCHEMA' not found."
```

## Already exists

The resolution requires a few steps to be carried out as outlined in the error message.

### Human in the loop labeler already exists

When a creating a labeler pool which it already exists.

```
message: "The labeler pool already exists."
```

### Schema version display name already exists

When creating a schema version with a display name that already exists.

```
message: "A schema version with the name 'EXAMPLE_SCHEMA_VERSION' already exists."
```

### Schema display name already exists

When creating a schema with a display name that already exists.

```
message: "A schema with the name 'EXAMPLE_SCHEMA' already exists."
```

## Quotas and limits

The resolution requires a few steps to be carried out as outlined in the error message.

### Quota exceeded

If you receive this message:

```
RESOURCE_EXHAUSTED: Quota exceeded.
```

You have reached the limit of your per-minute or daily quota. Review the
[quotas & limits](/document-ai/quotas) for using
Document AI.

You can request an increase to your quotas from the
[Google Cloud console](https://console.cloud.google.com/).

## Outages & Latency

The resolution requires a few steps to be carried out as outlined in the error message.

### Timeouts

* For [Online Processing](/document-ai/docs/send-request#online-process), there is a server-side 2 minute timeout for requests.
* For [Batch Processing](/document-ai/docs/send-request#batch-process), there is a server-side 2 minute timeout for generating the [Long-Running Operation](https://google.aip.dev/151), but there is no timeout for completion of the batch job.
  + For more information, see the [Long-Running Operations](/document-ai/docs/long-running-operations) documentation.

### Operation did not complete within the designated timeout.

If you receive the following (or similar) error messages when polling a [Long-Running Operation (LRO)](https://google.aip.dev/151):

```
google.api_core.future.polling._OperationNotComplete
...
google.api_core.exceptions.RetryError: Deadline of 0.0s exceeded while calling target function, last exception:
...
concurrent.futures._base.TimeoutError: Operation did not complete within the designated timeout.
```

Then the user-set timeout value for completion of the operation is set too low for the document being processed. This error does **not** indicate that the batch process operation failed, the operation will continue regardless of the user-set timeout value.

### Safety filter error

An internal server-side error occurred because the request or response was blocked by the large language model (LLM) safety filters. This error cannot be retried.

```
message: "Safety filter error."
```

### SchemaGenerationError

Indicates a failure occurred during schema generation.

```
message: "Schema generation failed."
```

### Internal error

An internal server-side error has occurred. Retry the connection.

```
message: "Internal error encountered."
```

[Previous

arrow\_back

Getting support](/document-ai/docs/getting-support)

[Next

Deprecations

arrow\_forward](/document-ai/docs/deprecation)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/file-types](./document-ai-docs-file-types.md)
- [https://docs.cloud.google.com/document-ai/docs/send-request](./document-ai-docs-send-request.md)
- [https://docs.cloud.google.com/document-ai/docs/setup](./document-ai-docs-setup.md)
