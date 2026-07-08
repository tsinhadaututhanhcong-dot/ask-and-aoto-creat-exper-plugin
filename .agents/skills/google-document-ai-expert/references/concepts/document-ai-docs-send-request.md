---
type: Reference
title: "Send a processing request  |  Document AI  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/send-request](https://docs.cloud.google.com/document-ai/docs/send-request)"
timestamp: 2026-07-06T03:34:16Z
---
# Send a processing request  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/send-request](https://docs.cloud.google.com/document-ai/docs/send-request)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Send a processing request Stay organized with collections Save and categorize content based on your preferences.



After you have set up your [Google Cloud account](https://console.cloud.google.com/)
and [created a processor](/document-ai/docs/create-processor), you can
send a request to your Document AI processor.

The code used to send the request is the same for all processors. You see
differences in processor functioning in the information each processor
outputs.

Using with the `v1` API version of Document AI or in Google Cloud console, you
can send processing requests to that specific processor version. If you don't
specify a processor version, the default version is used.
For more information, see [Managing processor versions](/document-ai/docs/manage-processor-versions).

## Online processing

Online (synchronous) requests let you send a single document for processing.
Document AI immediately processes the request and returns a [`document`](/document-ai/docs/reference/rest/v1/Document).

### Send request to a processor

The following code samples show you how to send a request to a
processor.

### REST

This sample shows you how to provide document content (raw document content in bytes
via a base64 encoded string) in the [`rawDocument`](/document-ai/docs/reference/rest/v1/RawDocument)
object.

Alternatively, you could also specify [`inlineDocument`](/document-ai/docs/reference/rest/v1/projects.locations.processors/process#request-body),
which is the same [`Document`](/document-ai/docs/reference/rest/v1/Document) JSON format returned
by Document AI. This allows you to chain requests by passing the same format back and forth
(for example, if you classify a document and then extract its content).

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* skipHumanReview: A boolean to disable human review (Supported by [Human-in-the-Loop processors](/document-ai/docs/hitl#processors_supported) only.)
  + `true` - skips human review
  + `false` - enables human review (default)
* MIME\_TYPE†: One of the valid
  [MIME type](/document-ai/docs/file-types) options.
* IMAGE\_CONTENT†: One of the valid
  Inline document content, represented as
  a stream of bytes. For JSON representations, the base64
  encoding (ASCII string) of your binary image data. This string should look similar to the
  following string:
  + `/9j/4QAYRXhpZgAA...9tAVx/zDQDlGxn//2Q==`Visit the [Base64 encode](/document-ai/docs/base64) topic for more
  information.
* FIELD\_MASK: Specifies which fields to include in the `Document` output. This is a comma-separated list of fully qualified names of fields in `FieldMask` format.
  + Example: `text,entities,pages.pageNumber`
* INDIVIDUAL\_PAGES: A list of individual pages to process.
  + Alternatively, provide field [`fromStart`](/document-ai/docs/reference/rest/v1/ProcessOptions#FIELDS.from_start) or [`fromEnd`](/document-ai/docs/reference/rest/v1/ProcessOptions#FIELDS.from_end) to process a specific quantity of pages from the beginning or end of the document.

† This content can also be specified using base64-encoded content in the
[`inlineDocument`](/document-ai/docs/reference/rest/v1/projects.locations.processors/process) object.

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:process
```

Request JSON body:

```
{
  "skipHumanReview": skipHumanReview,
  "rawDocument": {
    "mimeType": "MIME_TYPE",
    "content": "IMAGE_CONTENT"
  },
  "fieldMask": "FIELD_MASK",
  "processOptions": {
    "individualPageSelector" {
      "pages": [INDIVIDUAL_PAGES]
    }
  }
}
```

To send your request, choose one of these options:

#### curl

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
, or by using [Cloud Shell](/shell/docs),
which automatically logs you into the `gcloud` CLI
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
curl -X POST \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     -H "Content-Type: application/json; charset=utf-8" \  
     -d @request.json \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:process"
```

#### PowerShell

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
$cred = gcloud auth print-access-token  
$headers = @{ "Authorization" = "Bearer $cred" }  
  
Invoke-WebRequest `  
    -Method POST `  
    -Headers $headers `  
    -ContentType: "application/json; charset=utf-8" `  
    -InFile request.json `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:process" | Select-Object -Expand Content
```

If the request is successful, the server returns a `200 OK` HTTP status code and the
response in JSON format. The response body contains an instance of
`Document`.

### Send request to a processor version

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* PROCESSOR\_VERSION: the processor version identifier. Refer to [Select a processor version](/document-ai/docs/manage-processor#select_a_processor_version) for more information. For example:
  + `pretrained-TYPE-vX.X-YYYY-MM-DD`
  + `stable`
  + `rc`
* skipHumanReview: A boolean to disable human review (Supported by [Human-in-the-Loop processors](/document-ai/docs/hitl#processors_supported) only.)
  + `true` - skips human review
  + `false` - enables human review (default)
* MIME\_TYPE†: One of the valid
  [MIME type](/document-ai/docs/file-types) options.
* IMAGE\_CONTENT†: One of the valid
  Inline document content, represented as
  a stream of bytes. For JSON representations, the base64
  encoding (ASCII string) of your binary image data. This string should look similar to the
  following string:
  + `/9j/4QAYRXhpZgAA...9tAVx/zDQDlGxn//2Q==`Visit the [Base64 encode](/document-ai/docs/base64) topic for more
  information.
* FIELD\_MASK: Specifies which fields to include in the `Document` output. This is a comma-separated list of fully qualified names of fields in `FieldMask` format.
  + Example: `text,entities,pages.pageNumber`

† This content can also be specified using base64-encoded content in the
[`inlineDocument`](/document-ai/docs/reference/rest/v1/projects.locations.processors/process) object.

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:process
```

Request JSON body:

```
{
  "skipHumanReview": skipHumanReview,
  "rawDocument": {
    "mimeType": "MIME_TYPE",
    "content": "IMAGE_CONTENT"
  },
  "fieldMask": "FIELD_MASK"
}
```

To send your request, choose one of these options:

#### curl

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
, or by using [Cloud Shell](/shell/docs),
which automatically logs you into the `gcloud` CLI
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
curl -X POST \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     -H "Content-Type: application/json; charset=utf-8" \  
     -d @request.json \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:process"
```

#### PowerShell

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
$cred = gcloud auth print-access-token  
$headers = @{ "Authorization" = "Bearer $cred" }  
  
Invoke-WebRequest `  
    -Method POST `  
    -Headers $headers `  
    -ContentType: "application/json; charset=utf-8" `  
    -InFile request.json `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:process" | Select-Object -Expand Content
```

If the request is successful, the server returns a `200 OK` HTTP status code and the
response in JSON format. The response body contains an instance of
`Document`.

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Cloud.DocumentAI.V1;
using Google.Protobuf;
using System;
using System.IO;

public class QuickstartSample
{
    public Document Quickstart(
        string projectId = "your-project-id",
        string locationId = "your-processor-location",
        string processorId = "your-processor-id",
        string localPath = "my-local-path/my-file-name",
        string mimeType = "application/pdf"
    )
    {
        // Create client
        var client = new DocumentProcessorServiceClientBuilder
        {
            Endpoint = $"{locationId}-documentai.googleapis.com"
        }.Build();

        // Read in local file
        using var fileStream = File.OpenRead(localPath);
        var rawDocument = new RawDocument
        {
            Content = ByteString.FromStream(fileStream),
            MimeType = mimeType
        };

        // Initialize request argument(s)
        var request = new ProcessRequest
        {
            Name = ProcessorName.FromProjectLocationProcessor(projectId, locationId, processorId).ToString(),
            RawDocument = rawDocument
        };

        // Make the request
        var response = client.ProcessDocument(request);

        var document = response.Document;
        Console.WriteLine(document.Text);
        return document;
    }
}
```

### Java

For more information, see the
[Document AI Java API
reference documentation](/java/docs/reference/google-cloud-document-ai/latest/overview).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
import com.google.cloud.documentai.v1.Document;
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.DocumentProcessorServiceSettings;
import com.google.cloud.documentai.v1.ProcessRequest;
import com.google.cloud.documentai.v1.ProcessResponse;
import com.google.cloud.documentai.v1.RawDocument;
import com.google.protobuf.ByteString;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeoutException;

public class ProcessDocument {
  public static void processDocument()
      throws IOException, InterruptedException, ExecutionException, TimeoutException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "your-project-id";
    String location = "your-project-location"; // Format is "us" or "eu".
    String processerId = "your-processor-id";
    String filePath = "path/to/input/file.pdf";
    processDocument(projectId, location, processerId, filePath);
  }

  public static void processDocument(
      String projectId, String location, String processorId, String filePath)
      throws IOException, InterruptedException, ExecutionException, TimeoutException {
    // Initialize client that will be used to send requests. This client only needs
    // to be created
    // once, and can be reused for multiple requests. After completing all of your
    // requests, call
    // the "close" method on the client to safely clean up any remaining background
    // resources.
    String endpoint = String.format("%s-documentai.googleapis.com:443", location);
    DocumentProcessorServiceSettings settings =
        DocumentProcessorServiceSettings.newBuilder().setEndpoint(endpoint).build();
    try (DocumentProcessorServiceClient client = DocumentProcessorServiceClient.create(settings)) {
      // The full resource name of the processor, e.g.:
      // projects/project-id/locations/location/processor/processor-id
      // You must create new processors in the Cloud Console first
      String name =
          String.format("projects/%s/locations/%s/processors/%s", projectId, location, processorId);

      // Read the file.
      byte[] imageFileData = Files.readAllBytes(Paths.get(filePath));

      // Convert the image data to a Buffer and base64 encode it.
      ByteString content = ByteString.copyFrom(imageFileData);

      RawDocument document =
          RawDocument.newBuilder().setContent(content).setMimeType("application/pdf").build();

      // Configure the process request.
      ProcessRequest request =
          ProcessRequest.newBuilder().setName(name).setRawDocument(document).build();

      // Recognizes text entities in the PDF document
      ProcessResponse result = client.processDocument(request);
      Document documentResponse = result.getDocument();

      // Get all of the document text as one big string
      String text = documentResponse.getText();

      // Read the text recognition output from the processor
      System.out.println("The document contains the following paragraphs:");
      Document.Page firstPage = documentResponse.getPages(0);
      List<Document.Page.Paragraph> paragraphs = firstPage.getParagraphsList();

      for (Document.Page.Paragraph paragraph : paragraphs) {
        String paragraphText = getText(paragraph.getLayout().getTextAnchor(), text);
        System.out.printf("Paragraph text:\n%s\n", paragraphText);
      }

      // Form parsing provides additional output about
      // form-formatted PDFs. You must create a form
      // processor in the Cloud Console to see full field details.
      System.out.println("The following form key/value pairs were detected:");

      for (Document.Page.FormField field : firstPage.getFormFieldsList()) {
        String fieldName = getText(field.getFieldName().getTextAnchor(), text);
        String fieldValue = getText(field.getFieldValue().getTextAnchor(), text);

        System.out.println("Extracted form fields pair:");
        System.out.printf("\t(%s, %s))\n", fieldName, fieldValue);
      }
    }
  }

  // Extract shards from the text field
  private static String getText(Document.TextAnchor textAnchor, String text) {
    if (textAnchor.getTextSegmentsList().size() > 0) {
      int startIdx = (int) textAnchor.getTextSegments(0).getStartIndex();
      int endIdx = (int) textAnchor.getTextSegments(0).getEndIndex();
      return text.substring(startIdx, endIdx);
    }
    return "[NO TEXT]";
  }
}
```

### Node.js

For more information, see the
[Document AI Node.js API
reference documentation](/nodejs/docs/reference/documentai/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
/**
 * TODO(developer): Uncomment these variables before running the sample.
 */
// const projectId = 'YOUR_PROJECT_ID';
// const location = 'YOUR_PROJECT_LOCATION'; // Format is 'us' or 'eu'
// const processorId = 'YOUR_PROCESSOR_ID'; // Create processor in Cloud Console
// const filePath = '/path/to/local/pdf';

const {DocumentProcessorServiceClient} =
  require('@google-cloud/documentai').v1;

// Instantiates a client
const client = new DocumentProcessorServiceClient();

async function processDocument() {
  // The full resource name of the processor, e.g.:
  // projects/project-id/locations/location/processor/processor-id
  // You must create new processors in the Cloud Console first
  const name = `projects/${projectId}/locations/${location}/processors/${processorId}`;

  // Read the file into memory.
  const fs = require('fs').promises;
  const imageFile = await fs.readFile(filePath);

  // Convert the image data to a Buffer and base64 encode it.
  const encodedImage = Buffer.from(imageFile).toString('base64');

  const request = {
    name,
    rawDocument: {
      content: encodedImage,
      mimeType: 'application/pdf',
    },
  };

  // Recognizes text entities in the PDF document
  const [result] = await client.processDocument(request);
  const {document} = result;

  // Get all of the document text as one big string
  const {text} = document;

  // Extract shards from the text field
  const getText = textAnchor => {
    if (!textAnchor.textSegments || textAnchor.textSegments.length === 0) {
      return '';
    }

    // First shard in document doesn't have startIndex property
    const startIndex = textAnchor.textSegments[0].startIndex || 0;
    const endIndex = textAnchor.textSegments[0].endIndex;

    return text.substring(startIndex, endIndex);
  };

  // Read the text recognition output from the processor
  console.log('The document contains the following paragraphs:');
  const [page1] = document.pages;
  const {paragraphs} = page1;

  for (const paragraph of paragraphs) {
    const paragraphText = getText(paragraph.layout.textAnchor);
    console.log(`Paragraph text:\n${paragraphText}`);
  }

  // Form parsing provides additional output about
  // form-formatted PDFs. You  must create a form
  // processor in the Cloud Console to see full field details.
  console.log('\nThe following form key/value pairs were detected:');

  const {formFields} = page1;
  for (const field of formFields) {
    const fieldName = getText(field.fieldName.textAnchor);
    const fieldValue = getText(field.fieldValue.textAnchor);

    console.log('Extracted key value pair:');
    console.log(`\t(${fieldName}, ${fieldValue})`);
  }
}
```

### Python

For more information, see the
[Document AI Python API
reference documentation](/python/docs/reference/documentai/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_PROCESSOR_LOCATION" # Format is "us" or "eu"
# processor_id = "YOUR_PROCESSOR_ID" # Create processor before running sample
# file_path = "/path/to/local/pdf"
# mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
# processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use


def process_document_sample(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        # The full resource name of the processor, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}`
        name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
    # Optional: Additional configurations for processing.
    process_options = documentai.ProcessOptions(
        # Process only specific pages
        individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
            pages=[1]
        )
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    print(document.text)
```

## Batch processing

Batch (asynchronous) requests let you send multiple documents in a single
request. Document AI responds with an [`operation`](/document-ai/docs/reference/rest/v1/projects.locations.operations)
that you can poll for the status of the request. When this operation finishes,
it contains a [`BatchProcessMetadata`](/document-ai/docs/reference/rest/Shared.Types/BatchProcessMetadata)
that points to the Cloud Storage bucket where the processed results are
stored.

If the input files you want to access are in a bucket in another project,
you must provide access to that bucket before you can access the files. See [setup file access](/document-ai/docs/setup#cross_project_file_access_setup).

### Send request to a processor

The following code samples show you how to send a batch process request to a
processor.

### REST

This sample shows how to send a `POST` request to the
[`batchProcess`](/document-ai/docs/reference/rest/v1/projects.locations.processors/batchProcess) method for large document asynchronous processing.
The example uses
the access token for a service account set up for the project using the Google Cloud CLI. For
instructions on installing the Google Cloud CLI, setting up a project with a service account, and
obtaining an access token, see [Before you begin](/document-ai/docs/setup).

A `batchProcess` request starts a long-running operation and
stores results in a Cloud Storage bucket. This sample also shows how to
get the status of this long-running operation after it has started.

### Send the process request

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* INPUT\_BUCKET\_FOLDER†: A Cloud Storage
  bucket/directory to read input files from, expressed in the following form:
  + `gs://bucket/directory/`The requesting user must have read permission to the
  bucket.
* MIME\_TYPE: One of the valid
  [MIME type](/document-ai/docs/file-types) options.
* OUTPUT\_BUCKET\_FOLDER: A Cloud Storage
  bucket/directory to save output files to, expressed in the following form:
  + `gs://bucket/directory/`The requesting user must have write permission to the
  bucket.
* skipHumanReview: A boolean to disable human review (Supported by [Human-in-the-Loop processors](/document-ai/docs/hitl#processors_supported) only.)
  + `true` - skips human review
  + `false` - enables human review (default)
* FIELD\_MASK: Specifies which fields to include in the `Document` output. This is a comma-separated list of fully qualified names of fields in `FieldMask` format.
  + Example: `text,entities,pages.pageNumber`

† Instead of using `gcsPrefix` to include all the files in a GCS folder, you can also
use `documents` to individually list each file:

```
  "inputDocuments": {
    "gcsDocuments": {
      "documents": [
        {
          "gcsUri": "gs://BUCKET/PATH/TO/DOCUMENT1.ext",
          "mimeType": "MIME_TYPE"
        },
        {
          "gcsUri": "gs://BUCKET/PATH/TO/DOCUMENT2.ext",
          "mimeType": "MIME_TYPE"
        }
      ]
    }
  }
```

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:batchProcess
```

Request JSON body:

```
{
  "inputDocuments": {
    "gcsPrefix": {
      "gcsUriPrefix": "INPUT_BUCKET_FOLDER"
    }
  },
  "documentOutputConfig": {
    "gcsOutputConfig": {
      "gcsUri": "OUTPUT_BUCKET_FOLDER",
      "fieldMask": "FIELD_MASK"
    }
  },
  "skipHumanReview": BOOLEAN
}
```

To send your request, choose one of these options:

#### curl

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
, or by using [Cloud Shell](/shell/docs),
which automatically logs you into the `gcloud` CLI
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
curl -X POST \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     -H "Content-Type: application/json; charset=utf-8" \  
     -d @request.json \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:batchProcess"
```

#### PowerShell

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
$cred = gcloud auth print-access-token  
$headers = @{ "Authorization" = "Bearer $cred" }  
  
Invoke-WebRequest `  
    -Method POST `  
    -Headers $headers `  
    -ContentType: "application/json; charset=utf-8" `  
    -InFile request.json `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:batchProcess" | Select-Object -Expand Content
```

You should receive a JSON response similar to the following:

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID"
}
```

### Send request to a processor version

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* PROCESSOR\_VERSION: the processor version identifier. Refer to [Select a processor version](/document-ai/docs/manage-processor#select_a_processor_version) for more information. For example:
  + `pretrained-TYPE-vX.X-YYYY-MM-DD`
  + `stable`
  + `rc`
* INPUT\_BUCKET\_FOLDER†: A Cloud Storage
  bucket/directory to read input files from, expressed in the following form:
  + `gs://bucket/directory/`The requesting user must have read permission to the
  bucket.
* MIME\_TYPE: One of the valid
  [MIME type](/document-ai/docs/file-types) options.
* OUTPUT\_BUCKET\_FOLDER: A Cloud Storage
  bucket/directory to save output files to, expressed in the following form:
  + `gs://bucket/directory/`The requesting user must have write permission to the
  bucket.
* skipHumanReview: A boolean to disable human review (Supported by [Human-in-the-Loop processors](/document-ai/docs/hitl#processors_supported) only.)
  + `true` - skips human review
  + `false` - enables human review (default)
* FIELD\_MASK: Specifies which fields to include in the `Document` output. This is a comma-separated list of fully qualified names of fields in `FieldMask` format.
  + Example: `text,entities,pages.pageNumber`

† Instead of using `gcsPrefix` to include all the files in a GCS folder, you can also
use `documents` to individually list each file:

```
  "inputDocuments": {
    "gcsDocuments": {
      "documents": [
        {
          "gcsUri": "gs://BUCKET/PATH/TO/DOCUMENT1.ext",
          "mimeType": "MIME_TYPE"
        },
        {
          "gcsUri": "gs://BUCKET/PATH/TO/DOCUMENT2.ext",
          "mimeType": "MIME_TYPE"
        }
      ]
    }
  }
```

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:batchProcess
```

Request JSON body:

```
{
  "inputDocuments": {
    "gcsPrefix": {
      "gcsUriPrefix": "INPUT_BUCKET_FOLDER"
    }
  },
  "documentOutputConfig": {
    "gcsOutputConfig": {
      "gcsUri": "OUTPUT_BUCKET_FOLDER",
      "fieldMask": "FIELD_MASK"
    }
  },
  "skipHumanReview": BOOLEAN
}
```

To send your request, choose one of these options:

#### curl

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
, or by using [Cloud Shell](/shell/docs),
which automatically logs you into the `gcloud` CLI
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
curl -X POST \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     -H "Content-Type: application/json; charset=utf-8" \  
     -d @request.json \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:batchProcess"
```

#### PowerShell

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Save the request body in a file named `request.json`,
and execute the following command:

```
$cred = gcloud auth print-access-token  
$headers = @{ "Authorization" = "Bearer $cred" }  
  
Invoke-WebRequest `  
    -Method POST `  
    -Headers $headers `  
    -ContentType: "application/json; charset=utf-8" `  
    -InFile request.json `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:batchProcess" | Select-Object -Expand Content
```

You should receive a JSON response similar to the following:

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID"
}
```

If the request is successful, the Document AI API returns the name for your operation.

### Get the results

To get the results of your request, you must send a `GET` request to
the `operations` resource. The following shows how to send such a request.
You can read more information in the [Long-Running Operations](/document-ai/docs/long-running-operations) documentation.

Before using any of the request data,
make the following replacements:

* PROJECT\_ID: Your Google Cloud project ID.
* LOCATION: the [location](/document-ai/docs/regions) where the LRO is running, for example:
  + `us` - United States
  + `eu` - European Union
* OPERATION\_ID: The ID of your operation. The ID is the last element of the name
  of your operation. For example:
  + Operation name: `projects/PROJECT_ID/locations/LOCATION/operations/bc4e1d412863e626`
  + Operation id: `bc4e1d412863e626`

HTTP method and URL:

```
GET https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID
```

To send your request, choose one of these options:

#### curl

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
, or by using [Cloud Shell](/shell/docs),
which automatically logs you into the `gcloud` CLI
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Execute the following command:

```
curl -X GET \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID"
```

#### PowerShell

**Note:**
The following command assumes that you have logged in to
the `gcloud` CLI with your user account by running
[`gcloud init`](/sdk/gcloud/reference/init)
or
[`gcloud auth login`](/sdk/gcloud/reference/auth/login)
.
You can check the currently active account by running
[`gcloud auth list`](/sdk/gcloud/reference/auth/list).

Execute the following command:

```
$cred = gcloud auth print-access-token  
$headers = @{ "Authorization" = "Bearer $cred" }  
  
Invoke-WebRequest `  
    -Method GET `  
    -Headers $headers `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID" | Select-Object -Expand Content
```

You should receive a JSON response similar to the following:

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID",
  "metadata": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.BatchProcessMetadata",
    "state": "SUCCEEDED",
    "stateMessage": "Processed 1 document(s) successfully",
    "createTime": "TIMESTAMP",
    "updateTime": "TIMESTAMP",
    "individualProcessStatuses": [
      {
        "inputGcsSource": "INPUT_BUCKET_FOLDER/DOCUMENT1.ext",
        "status": {},
        "outputGcsDestination": "OUTPUT_BUCKET_FOLDER/OPERATION_ID/0",
        "humanReviewStatus": {
          "state": "ERROR",
          "stateMessage": "Sharded document protos are not supported for human review."
        }
      }
    ]
  },
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.BatchProcessResponse"
  }
}
```

The response body contains an instance of [`Operation`](/document-ai/docs/reference/rest/v1/projects.locations.operations) with information about the status of the operation.
If the operation has completed successfully,
the [`metadata`](/document-ai/docs/reference/rest/v1/projects.locations.operations#Operation.FIELDS.metadata)
field will be populated with an instance of [`BatchProcessMetadata`](/document-ai/docs/reference/rest/Shared.Types/BatchProcessMetadata) which contains information about the processed documents.

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Api.Gax;
using Google.Cloud.DocumentAI.V1;
using Google.LongRunning;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for BatchProcessDocuments</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void BatchProcessDocumentsRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        BatchProcessRequest request = new BatchProcessRequest
        {
            ResourceName = new UnparsedResourceName("a/wildcard/resource"),
            SkipHumanReview = false,
            InputDocuments = new BatchDocumentsInputConfig(),
            DocumentOutputConfig = new DocumentOutputConfig(),
            ProcessOptions = new ProcessOptions(),
            Labels = { { "", "" }, },
        };
        // Make the request
        Operation<BatchProcessResponse, BatchProcessMetadata> response = documentProcessorServiceClient.BatchProcessDocuments(request);

        // Poll until the returned long-running operation is complete
        Operation<BatchProcessResponse, BatchProcessMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        BatchProcessResponse result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<BatchProcessResponse, BatchProcessMetadata> retrievedResponse = documentProcessorServiceClient.PollOnceBatchProcessDocuments(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            BatchProcessResponse retrievedResult = retrievedResponse.Result;
        }
    }
}
```

### Go

For more information, see the
[Document AI Go API
reference documentation](/go/docs/reference/cloud.google.com/go/documentai/latest/apiv1).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
//go:build examples

package main

import (
	"context"

	documentai "cloud.google.com/go/documentai/apiv1"
	documentaipb "cloud.google.com/go/documentai/apiv1/documentaipb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := documentai.NewDocumentProcessorClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &documentaipb.BatchProcessRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#BatchProcessRequest.
	}
	op, err := c.BatchProcessDocuments(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}

	resp, err := op.Wait(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

For more information, see the
[Document AI Java API
reference documentation](/java/docs/reference/google-cloud-document-ai/latest/overview).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
import com.google.api.gax.longrunning.OperationFuture;
import com.google.api.gax.paging.Page;
import com.google.cloud.documentai.v1.BatchDocumentsInputConfig;
import com.google.cloud.documentai.v1.BatchProcessMetadata;
import com.google.cloud.documentai.v1.BatchProcessRequest;
import com.google.cloud.documentai.v1.BatchProcessResponse;
import com.google.cloud.documentai.v1.Document;
import com.google.cloud.documentai.v1.DocumentOutputConfig;
import com.google.cloud.documentai.v1.DocumentOutputConfig.GcsOutputConfig;
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.DocumentProcessorServiceSettings;
import com.google.cloud.documentai.v1.GcsDocument;
import com.google.cloud.documentai.v1.GcsDocuments;
import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Bucket;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import com.google.protobuf.util.JsonFormat;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class BatchProcessDocument {
  public static void batchProcessDocument()
      throws IOException, InterruptedException, TimeoutException, ExecutionException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "your-project-id";
    String location = "your-project-location"; // Format is "us" or "eu".
    String processerId = "your-processor-id";
    String outputGcsBucketName = "your-gcs-bucket-name";
    String outputGcsPrefix = "PREFIX";
    String inputGcsUri = "gs://your-gcs-bucket/path/to/input/file.pdf";
    batchProcessDocument(
        projectId, location, processerId, inputGcsUri, outputGcsBucketName, outputGcsPrefix);
  }

  public static void batchProcessDocument(
      String projectId,
      String location,
      String processorId,
      String gcsInputUri,
      String gcsOutputBucketName,
      String gcsOutputUriPrefix)
      throws IOException, InterruptedException, TimeoutException, ExecutionException {
    // Initialize client that will be used to send requests. This client only needs
    // to be created
    // once, and can be reused for multiple requests. After completing all of your
    // requests, call
    // the "close" method on the client to safely clean up any remaining background
    // resources.
    String endpoint = String.format("%s-documentai.googleapis.com:443", location);
    DocumentProcessorServiceSettings settings =
        DocumentProcessorServiceSettings.newBuilder().setEndpoint(endpoint).build();
    try (DocumentProcessorServiceClient client = DocumentProcessorServiceClient.create(settings)) {
      // The full resource name of the processor, e.g.:
      // projects/project-id/locations/location/processor/processor-id
      // You must create new processors in the Cloud Console first
      String name =
          String.format("projects/%s/locations/%s/processors/%s", projectId, location, processorId);

      GcsDocument gcsDocument =
          GcsDocument.newBuilder().setGcsUri(gcsInputUri).setMimeType("application/pdf").build();

      GcsDocuments gcsDocuments = GcsDocuments.newBuilder().addDocuments(gcsDocument).build();

      BatchDocumentsInputConfig inputConfig =
          BatchDocumentsInputConfig.newBuilder().setGcsDocuments(gcsDocuments).build();

      String fullGcsPath = String.format("gs://%s/%s/", gcsOutputBucketName, gcsOutputUriPrefix);
      GcsOutputConfig gcsOutputConfig = GcsOutputConfig.newBuilder().setGcsUri(fullGcsPath).build();

      DocumentOutputConfig documentOutputConfig =
          DocumentOutputConfig.newBuilder().setGcsOutputConfig(gcsOutputConfig).build();

      // Configure the batch process request.
      BatchProcessRequest request =
          BatchProcessRequest.newBuilder()
              .setName(name)
              .setInputDocuments(inputConfig)
              .setDocumentOutputConfig(documentOutputConfig)
              .build();

      OperationFuture<BatchProcessResponse, BatchProcessMetadata> future =
          client.batchProcessDocumentsAsync(request);

      // Batch process document using a long-running operation.
      // You can wait for now, or get results later.
      // Note: first request to the service takes longer than subsequent
      // requests.
      System.out.println("Waiting for operation to complete...");
      future.get();

      System.out.println("Document processing complete.");

      Storage storage = StorageOptions.newBuilder().setProjectId(projectId).build().getService();
      Bucket bucket = storage.get(gcsOutputBucketName);

      // List all of the files in the Storage bucket.
      Page<Blob> blobs = bucket.list(Storage.BlobListOption.prefix(gcsOutputUriPrefix + "/"));
      int idx = 0;
      for (Blob blob : blobs.iterateAll()) {
        if (!blob.isDirectory()) {
          System.out.printf("Fetched file #%d\n", ++idx);
          // Read the results

          // Download and store json data in a temp file.
          File tempFile = File.createTempFile("file", ".json");
          Blob fileInfo = storage.get(BlobId.of(gcsOutputBucketName, blob.getName()));
          fileInfo.downloadTo(tempFile.toPath());

          // Parse json file into Document.
          FileReader reader = new FileReader(tempFile);
          Document.Builder builder = Document.newBuilder();
          JsonFormat.parser().merge(reader, builder);

          Document document = builder.build();

          // Get all of the document text as one big string.
          String text = document.getText();

          // Read the text recognition output from the processor
          System.out.println("The document contains the following paragraphs:");
          Document.Page page1 = document.getPages(0);
          List<Document.Page.Paragraph> paragraphList = page1.getParagraphsList();
          for (Document.Page.Paragraph paragraph : paragraphList) {
            String paragraphText = getText(paragraph.getLayout().getTextAnchor(), text);
            System.out.printf("Paragraph text:%s\n", paragraphText);
          }

          // Form parsing provides additional output about
          // form-formatted PDFs. You must create a form
          // processor in the Cloud Console to see full field details.
          System.out.println("The following form key/value pairs were detected:");

          for (Document.Page.FormField field : page1.getFormFieldsList()) {
            String fieldName = getText(field.getFieldName().getTextAnchor(), text);
            String fieldValue = getText(field.getFieldValue().getTextAnchor(), text);

            System.out.println("Extracted form fields pair:");
            System.out.printf("\t(%s, %s))", fieldName, fieldValue);
          }

          // Clean up temp file.
          tempFile.deleteOnExit();
        }
      }
    }
  }

  // Extract shards from the text field
  private static String getText(Document.TextAnchor textAnchor, String text) {
    if (textAnchor.getTextSegmentsList().size() > 0) {
      int startIdx = (int) textAnchor.getTextSegments(0).getStartIndex();
      int endIdx = (int) textAnchor.getTextSegments(0).getEndIndex();
      return text.substring(startIdx, endIdx);
    }
    return "[NO TEXT]";
  }
}
```

### Node.js

For more information, see the
[Document AI Node.js API
reference documentation](/nodejs/docs/reference/documentai/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
/**
 * TODO(developer): Uncomment these variables before running the sample.
 */
// const projectId = 'YOUR_PROJECT_ID';
// const location = 'YOUR_PROJECT_LOCATION'; // Format is 'us' or 'eu'
// const processorId = 'YOUR_PROCESSOR_ID';
// const gcsInputUri = 'YOUR_SOURCE_PDF';
// const gcsOutputUri = 'YOUR_STORAGE_BUCKET';
// const gcsOutputUriPrefix = 'YOUR_STORAGE_PREFIX';

// Imports the Google Cloud client library
const {DocumentProcessorServiceClient} =
  require('@google-cloud/documentai').v1;
const {Storage} = require('@google-cloud/storage');

// Instantiates Document AI, Storage clients
const client = new DocumentProcessorServiceClient();
const storage = new Storage();

const {default: PQueue} = require('p-queue');

async function batchProcessDocument() {
  const name = `projects/${projectId}/locations/${location}/processors/${processorId}`;

  // Configure the batch process request.
  const request = {
    name,
    inputDocuments: {
      gcsDocuments: {
        documents: [
          {
            gcsUri: gcsInputUri,
            mimeType: 'application/pdf',
          },
        ],
      },
    },
    documentOutputConfig: {
      gcsOutputConfig: {
        gcsUri: `${gcsOutputUri}/${gcsOutputUriPrefix}/`,
      },
    },
  };

  // Batch process document using a long-running operation.
  // You can wait for now, or get results later.
  // Note: first request to the service takes longer than subsequent
  // requests.
  const [operation] = await client.batchProcessDocuments(request);

  // Wait for operation to complete.
  await operation.promise();
  console.log('Document processing complete.');

  // Query Storage bucket for the results file(s).
  const query = {
    prefix: gcsOutputUriPrefix,
  };

  console.log('Fetching results ...');

  // List all of the files in the Storage bucket
  const [files] = await storage.bucket(gcsOutputUri).getFiles(query);

  // Add all asynchronous downloads to queue for execution.
  const queue = new PQueue({concurrency: 15});
  const tasks = files.map((fileInfo, index) => async () => {
    // Get the file as a buffer
    const [file] = await fileInfo.download();

    console.log(`Fetched file #${index + 1}:`);

    // The results stored in the output Storage location
    // are formatted as a document object.
    const document = JSON.parse(file.toString());
    const {text} = document;

    // Extract shards from the text field
    const getText = textAnchor => {
      if (!textAnchor.textSegments || textAnchor.textSegments.length === 0) {
        return '';
      }

      // First shard in document doesn't have startIndex property
      const startIndex = textAnchor.textSegments[0].startIndex || 0;
      const endIndex = textAnchor.textSegments[0].endIndex;

      return text.substring(startIndex, endIndex);
    };

    // Read the text recognition output from the processor
    console.log('The document contains the following paragraphs:');

    const [page1] = document.pages;
    const {paragraphs} = page1;
    for (const paragraph of paragraphs) {
      const paragraphText = getText(paragraph.layout.textAnchor);
      console.log(`Paragraph text:\n${paragraphText}`);
    }

    // Form parsing provides additional output about
    // form-formatted PDFs. You  must create a form
    // processor in the Cloud Console to see full field details.
    console.log('\nThe following form key/value pairs were detected:');

    const {formFields} = page1;
    for (const field of formFields) {
      const fieldName = getText(field.fieldName.textAnchor);
      const fieldValue = getText(field.fieldValue.textAnchor);

      console.log('Extracted key value pair:');
      console.log(`\t(${fieldName}, ${fieldValue})`);
    }
  });
  await queue.addAll(tasks);
}
```

### Python

For more information, see the
[Document AI Python API
reference documentation](/python/docs/reference/documentai/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
import re
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import RetryError
from google.cloud import documentai  # type: ignore
from google.cloud import storage

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_PROCESSOR_LOCATION" # Format is "us" or "eu"
# processor_id = "YOUR_PROCESSOR_ID" # Create processor before running sample
# gcs_output_uri = "YOUR_OUTPUT_URI" # Must end with a trailing slash `/`. Format: gs://bucket/directory/subdirectory/
# processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Example: pretrained-ocr-v1.0-2020-09-23

# TODO(developer): You must specify either `gcs_input_uri` and `mime_type` or `gcs_input_prefix`
# gcs_input_uri = "YOUR_INPUT_URI" # Format: gs://bucket/directory/file.pdf
# input_mime_type = "application/pdf"
# gcs_input_prefix = "YOUR_INPUT_URI_PREFIX" # Format: gs://bucket/directory/
# field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.


def batch_process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_output_uri: str,
    processor_version_id: Optional[str] = None,
    gcs_input_uri: Optional[str] = None,
    input_mime_type: Optional[str] = None,
    gcs_input_prefix: Optional[str] = None,
    field_mask: Optional[str] = None,
    timeout: int = 400,
) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if gcs_input_uri:
        # Specify specific GCS URIs to process individual documents
        gcs_document = documentai.GcsDocument(
            gcs_uri=gcs_input_uri, mime_type=input_mime_type
        )
        # Load GCS Input URI into a List of document files
        gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
        input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)
    else:
        # Specify a GCS URI Prefix to process an entire directory
        gcs_prefix = documentai.GcsPrefix(gcs_uri_prefix=gcs_input_prefix)
        input_config = documentai.BatchDocumentsInputConfig(gcs_prefix=gcs_prefix)

    # Cloud Storage URI for the Output Directory
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_output_uri, field_mask=field_mask
    )

    # Where to write results
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        # The full resource name of the processor, e.g.:
        # projects/{project_id}/locations/{location}/processors/{processor_id}
        name = client.processor_path(project_id, location, processor_id)

    request = documentai.BatchProcessRequest(
        name=name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    # BatchProcess returns a Long Running Operation (LRO)
    operation = client.batch_process_documents(request)

    # Continually polls the operation until it is complete.
    # This could take some time for larger files
    # Format: projects/{project_id}/locations/{location}/operations/{operation_id}
    try:
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result(timeout=timeout)
    # Catch exception when operation doesn't finish before timeout
    except (RetryError, InternalServerError) as e:
        print(e.message)

    # NOTE: Can also use callbacks for asynchronous processing
    #
    # def my_callback(future):
    #   result = future.result()
    #
    # operation.add_done_callback(my_callback)

    # After the operation is complete,
    # get output document information from operation metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)

    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        raise ValueError(f"Batch Process Failed: {metadata.state_message}")

    storage_client = storage.Client()

    print("Output files:")
    # One process per Input Document
    for process in list(metadata.individual_process_statuses):
        # output_gcs_destination format: gs://BUCKET/PREFIX/OPERATION_NUMBER/INPUT_FILE_NUMBER/
        # The Cloud Storage API requires the bucket name and URI prefix separately
        matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
        if not matches:
            print(
                "Could not parse output GCS destination:",
                process.output_gcs_destination,
            )
            continue

        output_bucket, output_prefix = matches.groups()

        # Get List of Document Objects from the Output Bucket
        output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

        # Document AI may output multiple JSON files per source file
        for blob in output_blobs:
            # Document AI should only output JSON files to GCS
            if blob.content_type != "application/json":
                print(
                    f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}"
                )
                continue

            # Download JSON File as bytes object and convert to Document Object
            print(f"Fetching {blob.name}")
            document = documentai.Document.from_json(
                blob.download_as_bytes(), ignore_unknown_fields=True
            )

            # For a full list of Document object attributes, please reference this page:
            # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document

            # Read the text recognition output from the processor
            print("The document contains the following text:")
            print(document.text)
```

### Go

For more information, see the
[Document AI Go API
reference documentation](/go/docs/reference/cloud.google.com/go/documentai/latest/apiv1).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
use Google\ApiCore\ApiException;
use Google\ApiCore\OperationResponse;
use Google\Cloud\DocumentAI\V1\BatchProcessRequest;
use Google\Cloud\DocumentAI\V1\BatchProcessResponse;
use Google\Cloud\DocumentAI\V1\Client\DocumentProcessorServiceClient;
use Google\Rpc\Status;

/**
 * LRO endpoint to batch process many documents. The output is written
 * to Cloud Storage as JSON in the [Document] format.
 *
 * @param string $name The resource name of
 *                     [Processor][google.cloud.documentai.v1.Processor] or
 *                     [ProcessorVersion][google.cloud.documentai.v1.ProcessorVersion].
 *                     Format: `projects/{project}/locations/{location}/processors/{processor}`,
 *                     or
 *                     `projects/{project}/locations/{location}/processors/{processor}/processorVersions/{processorVersion}`
 */
function batch_process_documents_sample(string $name): void
{
    // Create a client.
    $documentProcessorServiceClient = new DocumentProcessorServiceClient();

    // Prepare the request message.
    $request = (new BatchProcessRequest())
        ->setName($name);

    // Call the API and handle any network failures.
    try {
        /** @var OperationResponse $response */
        $response = $documentProcessorServiceClient->batchProcessDocuments($request);
        $response->pollUntilComplete();

        if ($response->operationSucceeded()) {
            /** @var BatchProcessResponse $result */
            $result = $response->getResult();
            printf('Operation successful with response data: %s' . PHP_EOL, $result->serializeToJsonString());
        } else {
            /** @var Status $error */
            $error = $response->getError();
            printf('Operation failed with error data: %s' . PHP_EOL, $error->serializeToJsonString());
        }
    } catch (ApiException $ex) {
        printf('Call failed with message: %s' . PHP_EOL, $ex->getMessage());
    }
}

/**
 * Helper to execute the sample.
 *
 * This sample has been automatically generated and should be regarded as a code
 * template only. It will require modifications to work:
 *  - It may require correct/in-range values for request initialization.
 *  - It may require specifying regional endpoints when creating the service client,
 *    please see the apiEndpoint client configuration option for more details.
 */
function callSample(): void
{
    $name = '[NAME]';

    batch_process_documents_sample($name);
}
```

### Ruby

For more information, see the
[Document AI Ruby API
reference documentation](/ruby/docs/reference/google-cloud-document_ai-v1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
require "google/cloud/document_ai/v1"

##
# Snippet for the batch_process_documents call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#batch_process_documents.
#
def batch_process_documents
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::BatchProcessRequest.new

  # Call the batch_process_documents method.
  result = client.batch_process_documents request

  # The returned object is of type Gapic::Operation. You can use it to
  # check the status of an operation, cancel it, or wait for results.
  # Here is how to wait for a response.
  result.wait_until_done! timeout: 60
  if result.response?
    p result.response
  else
    puts "No response received."
  end
end
```

### Create document batches with Python SDK

Batch processing allows a [maximum of 1,000 files per request](/document-ai/quotas).
If you have more documents to process, then you must divide the documents into multiple batches for processing.

[Document AI Toolbox](/document-ai/docs/toolbox) is an SDK for Python that provides utility functions for Document AI.
One of the functions is to create batches of documents for processing from a Cloud Storage folder.

Refer to [Handling the processing response](/document-ai/docs/handle-response#toolbox) for more information on how Document AI Toolbox assists with post-processing.

#### Code Samples

The following code samples demonstrate how to use Document AI Toolbox.

### Document Batches

```
from google.cloud import documentai
from google.cloud.documentai_toolbox import gcs_utilities

# TODO(developer): Uncomment these variables before running the sample.
# Given unprocessed documents in path gs://bucket/path/to/folder
# gcs_bucket_name = "bucket"
# gcs_prefix = "path/to/folder"
# batch_size = 50


def create_batches_sample(
    gcs_bucket_name: str,
    gcs_prefix: str,
    batch_size: int = 50,
) -> None:
    # Creating batches of documents for processing
    batches = gcs_utilities.create_batches(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix, batch_size=batch_size
    )

    print(f"{len(batches)} batch(es) created.")
    for batch in batches:
        print(f"{len(batch.gcs_documents.documents)} files in batch.")
        print(batch.gcs_documents.documents)

        # Use as input for batch_process_documents()
        # Refer to https://cloud.google.com/document-ai/docs/send-request
        # for how to send a batch processing request
        request = documentai.BatchProcessRequest(
            name="processor_name", input_documents=batch
        )
        print(request)
```

[Previous

arrow\_back

Process documents with client libraries](/document-ai/docs/process-documents-client-libraries)

[Next

Handle response

arrow\_forward](/document-ai/docs/handle-response)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/create-processor](./document-ai-docs-create-processor.md)
- [https://docs.cloud.google.com/document-ai/docs/file-types](./document-ai-docs-file-types.md)
- [https://docs.cloud.google.com/document-ai/docs/handle-response](./document-ai-docs-handle-response.md)
- [https://docs.cloud.google.com/document-ai/docs/manage-processor-versions](./document-ai-docs-manage-processor-versions.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/process-documents-client-libraries](./document-ai-docs-process-documents-client-libraries.md)
- [https://docs.cloud.google.com/document-ai/docs/setup](./document-ai-docs-setup.md)
