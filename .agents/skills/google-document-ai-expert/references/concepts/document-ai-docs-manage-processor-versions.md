# Managing processor versions  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/manage-processor-versions](https://docs.cloud.google.com/document-ai/docs/manage-processor-versions)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Managing processor versions Stay organized with collections Save and categorize content based on your preferences.



New versions are released for a variety of reasons, for example, to improve accuracy,
increase availability, and support new document elements, such as selection marks.

Given that Document AI is powered by generative AI, future versions are using
new foundation models so you can benefit from generative AI enhancements.

As we improve foundation models,
[earlier foundation models are deprecated](/vertex-ai/docs/generative-ai/learn/model-versioning#stable-versions-available).
Similarly, processor versions are deprecated six months after new versions are
released.

A processor can have one of the following *versions*:

* [Stable version](#google_stable_versions)
* [Release candidate (RC)](#google_release_candidates_rc)
* [Customized version](#customized_versions) and its associated [base version](#base_versions)

This page describes how processors are versioned, and how to view and select
a particular version.

![managing-processor-versions-1](/static/document-ai/docs/images/get_started/managing-processor-versions-1.png)

## Processor versions overview

There are two categories of processor versions:

* **Google versions** are either stable (for production use cases) or release
  candidates (experimental with latest functionality).
* **User versions** are created by you to customize predictions for your documents
  and have alphanumeric version IDs.

## Google versions

Each Google version is identified by a *Version ID*, for example `pretrained-TYPE-vX.X-YYYY-MM-DD`.
Each processor version Google offers is named either *Google Stable* or *Google Release Candidate (RC)*.

### Google stable versions

Stable versions are production-quality and ready for use.

* Google prioritizes stability of the processor behaviour, but still includes
  critical fixes.
* Earlier Google stable versions are deprecated six months after the newest stable
  version is released as depicted in the following figure.

![managing-processor-versions-2](/static/document-ai/docs/images/get_started/managing-processor-versions-2.png)

### Google release candidates (RC)

Release candidates are experimental and are upgraded regularly with the latest
features. These are not production-quality versions, and their stability
may vary.

## Customized versions

Customized versions are the processor versions that you can create based on your
documents to customize predictions.
Customized versions have a `Type`, which shows the kind of model used for predictions.
If you create a version using a foundation model (either by creating a version or
fine tuning), then the type is **Generative AI**. If you create a processor version
by training a smaller, custom model (either model or template based), then the
type is **Custom**. If you create processor versions, you decide the name and ID.

### Base versions

If you create a processor version, the "base version" shows which Google version powers
your customized user version. The base version dictates the lifecycle of your user version.
You need to make decisions about how to manage the lifecycle of your customized user version.

## Available stable processor versions

You can review the available stable processor versions for the different
processor types in the following tables.

| **Custom Extractor** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-foundation-model-v1.5-2025-05-05` | May 5, 2025 | Not applicable |
| `pretrained-foundation-model-v1.5-pro-2025-06-20` | June 20, 2025 | Not applicable |

| **Form Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-form-parser-v1.0-2020-09-23` | September 23, 2020 | Not applicable |
| `pretrained-form-parser-v2.0-2022-11-10` | November 10, 2022 | Not applicable |

| **Layout Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-layout-parser-v1.0-2024-06-03` | June 3, 2024 | Not applicable |

| **Bank Statement Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-bankstatement-v1.0-2021-08-08` | August 8, 2021 | Not applicable |
| `pretrained-bankstatement-v1.1-2021-08-13` | August 13, 2021 | Not applicable |
| `pretrained-bankstatement-v2.0-2021-12-10` | December 10, 2021 | Not applicable |
| `pretrained-bankstatement-v3.0-2022-05-16` | May 16, 2022 | Not applicable |
| `pretrained-bankstatement-v5.0-2023-12-06` | December 6, 2023 | Not applicable |

| **W2 Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-w2-v1.0-2020-10-01` | October 1, 2020 | March 31, 2024 |
| `pretrained-w2-v1.1-2022-01-27` | January 27, 2022 | March 31, 2024 |
| `pretrained-w2-v1.2-2022-01-28` | January 28, 2022 | Not applicable |
| `pretrained-w2-v2.1-2022-06-08` | June 8, 2022 | Not applicable |

| **Identity Document Proofing Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-id-proofing-v1.0-2022-10-03` | October 3, 2022 | Not applicable |

| **Pay Slip Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-paystub-v1.0-2021-03-19` | March 19, 2021 | Not applicable |
| `pretrained-paystub-v1.1-2021-08-13` | August 13, 2021 | Not applicable |
| `pretrained-paystub-v1.2-2021-12-10` | December 10, 2021 | Not applicable |
| `pretrained-paystub-v2.0-2022-07-22` | July 22, 2022 | Not applicable |
| `pretrained-paystub-v3.0-2023-12-06` | December 6, 2023 | Not applicable |

| **US Driver License Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-us-driver-license-v1.0-2021-06-14` | June 14, 2021 | Not applicable |

| **Expense Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-expense-v1.1-2021-04-09` | April 9, 2024 | Not applicable |
| `pretrained-expense-v1.4-2022-11-18` | November 18, 2022 | Not applicable |
| `pretrained-expense-v1.4.2-2024-09-12` | September 12, 2024 | Not applicable |

| **Invoice Parser** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-invoice-v1.1-2021-04-09` | April 9, 2024 | Not applicable |
| `pretrained-invoice-v1.2-2022-02-18` | February 18, 2022 | Not applicable |
| `pretrained-invoice-v1.3-2022-07-15` | July 15, 2022 | Not applicable |
| `pretrained-invoice-v2.0-2023-12-06` | December 6, 2023 | Not applicable |

| **Enterprise Document OCR (Optical Character Recognition)** | **Release date** | **Deprecation date** |
| --- | --- | --- |
| `pretrained-ocr-v1.2-2022-11-10` | November 10, 2022 | Not applicable |
| `pretrained-ocr-v2.0-2023-06-02` | June 2, 2023 | Not applicable |
| `pretrained-ocr-v2.1-2024-08-07` | August 7, 2024 | Not applicable |

![managing-processor-versions-3](/static/document-ai/docs/images/get_started/managing-processor-versions-3.png)

## Processor version lifecycle

As soon as a new Google version is available, you should
[create and evaluate new user versions](/document-ai/docs/workbench/cde-with-genai)
with the new base version. Then, deploy your new version and undeploy (or delete)
earlier user versions that use the prior stable version as their base. Stable
versions are discontinued after a new one is released. Google gives you at least
six months' notice when this occurs.

### What happens when a base version is deprecated?

User versions depending on earlier base versions stop returning predictions when
the base version is deprecated.

### How are processor versions selected for your requests?

When you call a processor endpoint without specifying the processor version, the
default processor version is used. When the default processor version changes,
you might need to update the code.

| **Endpoint used** | **Experience** |
| --- | --- |
| If you do not specify a processor version ID | Requests processed using a new default processor version.  If your default processor version is deprecated, the default updates to the most recently launched stable Google version when the older default version is deprecated. |
| If you specify the processor version ID | The response fails if you call a processor endpoint and specify a version ID which has been deprecated. |

**Note:** We recommend you to not specify the processor version ID in your production
requests to process documents. Instead, we recommend you to call the processor's
endpoint and rely on the default processor to control which version processes
requests. This helps you to upgrade and benefit from automatic default version
updates. See how to [change the default version](#change-default).

## Deprecation example of a customized version

Consider the following scenario that describes the sequence of events in a
customized version deprecation:

1. As a developer, you're using a Custom Extractor to get data from documents.
   Given the complexity and volume of documents you process, you fine tune the
   foundation model to create a version named `fine-tune-A`. You set the
   `fine-tune-A` version as the default version for your processor and use it to
   process documents. The base version that powers the `fine-tune-A` model is the
   `pretrained-foundation-model-v1.0-2023-08-22 (v1.0)` stable version.
2. Google published a new stable version named `pretrained-foundation-model-v1.2-2024-05-10 (v1.2)`
   and announced that the `v1.0` stable version is to be deprecated on April 9, 2025.
3. Since you kept your training and test documents in your processor's dataset,
   you fine-tune another version based on the newest Google stable version, `v1.2`,
   and name it `fine-tune-B`. After you evaluate its performance, you set the
   `fine-tune-B` version as the new default version for your processor and
   decommission the `fine-tune-A` version. Your new version now uses the latest
   supported Google stable version.

On the other hand, had you not created and evaluated the customized `fine-tune-B`
version, then Google would have updated the default version of your processor to
`v1.2` on April 9, 2025. Because you are calling the processor's endpoint and not
specifying a processor version, the new `v1.2` version is used as the new default
to process your requests.

## Deprecation and migration resources

For deprecated parsers and processors, you can consult
[Document AI deprecations](/document-ai/docs/deprecation).

See the following resources for migrations:

* For creation and training of a new Expense Parser, you can refer to
  [uptrain pretrained processor](/document-ai/docs/uptrain-pretrained-processor).
* For creation and tuning of a new Custom Extractor processor, you can refer to
  [Custom Extractor with GenAI](/document-ai/docs/ce-with-genai).

## Select a processor version

There are three ways to specify which processor version to use for online and batch processing:

* If you **do not specify a version**, the processor's default is used.

  + Example: `projects/my-proj/locations/us/processors/my-processor:process`
* If you **specify a version**, then that specific version is used. If the
  specific version does not exist, the request fails with an error.

  + Example:
    `projects/my-proj/locations/us/processors/my-processor/processorVersions/pretrained-invoice-v1.2-2022-02-18:process`
* If you **specify a channel** then the latest version in that channel is
  used. (Options: `stable`, `rc`)

  + Example:
    `projects/my-proj/locations/us/processors/my-processor/processorVersions/stable:process`

## View available version

**Note:** Some processors have only one version.

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to Processors](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to view details for.
3. Select the **Manage Versions** (or **Deploy & use**) tab, which will display all of the available
   processor versions.

### REST

This sample shows how to list the available processor versions for your
processor using the [`processorVersions.list`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions/list) method.

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.

HTTP method and URL:

```
GET https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions
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
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions"
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
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions" | Select-Object -Expand Content
```

The response contains a list of
[`ProcessorVersions`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions#ProcessorVersion),
which contains information about each processor version such as its
`name`, `state`, and other details.

```
{
  "processorVersions": [
    {
      "name": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/pretrained-ocr-v1.1-2022-09-12",
      "displayName": "Google Release Candidate",
      "state": "DEPLOYED",
      "createTime": "2022-09-13T23:39:12.156648Z",
      "googleManaged": true
    },
    {
      "name": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/pretrained-ocr-v1.0-2020-09-23",
      "displayName": "Google Stable",
      "state": "DEPLOYED",
      "createTime": "2022-09-12T23:35:09.829557Z",
      "googleManaged": true,
      "deprecationInfo": {
        "deprecationTime": "1970-01-01T00:00:00Z"
      }
    }
  ]
}
```

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
using System;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for ListProcessorVersions</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void ListProcessorVersionsRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        ListProcessorVersionsRequest request = new ListProcessorVersionsRequest
        {
            ParentAsProcessorName = ProcessorName.FromProjectLocationProcessor("[PROJECT]", "[LOCATION]", "[PROCESSOR]"),
        };
        // Make the request
        PagedEnumerable<ListProcessorVersionsResponse, ProcessorVersion> response = documentProcessorServiceClient.ListProcessorVersions(request);

        // Iterate over all response items, lazily performing RPCs as required
        foreach (ProcessorVersion item in response)
        {
            // Do something with each item
            Console.WriteLine(item);
        }

        // Or iterate over pages (of server-defined size), performing one RPC per page
        foreach (ListProcessorVersionsResponse page in response.AsRawResponses())
        {
            // Do something with each page of items
            Console.WriteLine("A page of results:");
            foreach (ProcessorVersion item in page)
            {
                // Do something with each item
                Console.WriteLine(item);
            }
        }

        // Or retrieve a single page of known size (unless it's the final page), performing as many RPCs as required
        int pageSize = 10;
        Page<ProcessorVersion> singlePage = response.ReadPage(pageSize);
        // Do something with the page of items
        Console.WriteLine($"A page of {pageSize} results (unless it's the final page):");
        foreach (ProcessorVersion item in singlePage)
        {
            // Do something with each item
            Console.WriteLine(item);
        }
        // Store the pageToken, for when the next page is required.
        string nextPageToken = singlePage.NextPageToken;
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
	"google.golang.org/api/iterator"
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

	req := &documentaipb.ListProcessorVersionsRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#ListProcessorVersionsRequest.
	}
	it := c.ListProcessorVersions(ctx, req)
	for {
		resp, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			// TODO: Handle error.
		}
		// TODO: Use resp.
		_ = resp

		// If you need to access the underlying RPC response,
		// you can do so by casting the `Response` as below.
		// Otherwise, remove this line. Only populated after
		// first call to Next(). Not safe for concurrent access.
		_ = it.Response.(*documentaipb.ListProcessorVersionsResponse)
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
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.ListProcessorVersionsRequest;
import com.google.cloud.documentai.v1.ProcessorName;
import com.google.cloud.documentai.v1.ProcessorVersion;

public class SyncListProcessorVersions {

  public static void main(String[] args) throws Exception {
    syncListProcessorVersions();
  }

  public static void syncListProcessorVersions() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DocumentProcessorServiceClient documentProcessorServiceClient =
        DocumentProcessorServiceClient.create()) {
      ListProcessorVersionsRequest request =
          ListProcessorVersionsRequest.newBuilder()
              .setParent(ProcessorName.of("[PROJECT]", "[LOCATION]", "[PROCESSOR]").toString())
              .setPageSize(883849137)
              .setPageToken("pageToken873572522")
              .build();
      for (ProcessorVersion element :
          documentProcessorServiceClient.listProcessorVersions(request).iterateAll()) {
        // doThingsWith(element);
      }
    }
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
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample


def list_processor_versions_sample(
    project_id: str, location: str, processor_id: str
) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    parent = client.processor_path(project_id, location, processor_id)

    # Make ListProcessorVersions request
    processor_versions = client.list_processor_versions(parent=parent)

    # Print the processor version information
    for processor_version in processor_versions:
        processor_version_id = client.parse_processor_version_path(
            processor_version.name
        )["processor_version"]

        print(f"Processor Version: {processor_version_id}")
        print(f"Display Name: {processor_version.display_name}")
        print(f"DEPLOYED: {processor_version.state}")
        print("")
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
# Snippet for the list_processor_versions call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#list_processor_versions.
#
def list_processor_versions
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::ListProcessorVersionsRequest.new

  # Call the list_processor_versions method.
  result = client.list_processor_versions request

  # The returned object is of type Gapic::PagedEnumerable. You can iterate
  # over elements, and API calls will be issued to fetch pages as needed.
  result.each do |item|
    # Each element is of type ::Google::Cloud::DocumentAI::V1::ProcessorVersion.
    p item
  end
end
```

## View details about a version

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to Processors](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to view details for.
3. Select the **Manage Versions** (or **Deploy & use**) tab, which will display
   all of the available processor versions and their details.

### REST

This sample shows how to get details about a processor version for your
processor using the [`processorVersions.get`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions/get)
method.

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

HTTP method and URL:

```
GET https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION
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
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION"
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
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION" | Select-Object -Expand Content
```

The response is a
[`ProcessorVersion`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions#ProcessorVersion),
which contains information about the processor version such as its
`name`, `state`, and other details.

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/pretrained-ocr-v1.1-2022-09-12",
  "displayName": "Google Release Candidate",
  "state": "DEPLOYED",
  "createTime": "2022-09-13T23:39:12.156648Z",
  "googleManaged": true
}
```

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Cloud.DocumentAI.V1;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for GetProcessorVersion</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void GetProcessorVersionRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        GetProcessorVersionRequest request = new GetProcessorVersionRequest
        {
            ProcessorVersionName = ProcessorVersionName.FromProjectLocationProcessorProcessorVersion("[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]"),
        };
        // Make the request
        ProcessorVersion response = documentProcessorServiceClient.GetProcessorVersion(request);
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

	req := &documentaipb.GetProcessorVersionRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#GetProcessorVersionRequest.
	}
	resp, err := c.GetProcessorVersion(ctx, req)
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
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.GetProcessorVersionRequest;
import com.google.cloud.documentai.v1.ProcessorVersion;
import com.google.cloud.documentai.v1.ProcessorVersionName;

public class SyncGetProcessorVersion {

  public static void main(String[] args) throws Exception {
    syncGetProcessorVersion();
  }

  public static void syncGetProcessorVersion() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DocumentProcessorServiceClient documentProcessorServiceClient =
        DocumentProcessorServiceClient.create()) {
      GetProcessorVersionRequest request =
          GetProcessorVersionRequest.newBuilder()
              .setName(
                  ProcessorVersionName.of(
                          "[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]")
                      .toString())
              .build();
      ProcessorVersion response = documentProcessorServiceClient.getProcessorVersion(request);
    }
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
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'


def get_processor_version_sample(
    project_id: str, location: str, processor_id: str, processor_version_id: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g.: projects/project_id/locations/location/processors/processor_id/processorVersions/processor_version_id
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    # Make GetProcessorVersion request
    processor_version = client.get_processor_version(name=name)

    # Print the processor version information
    print(f"Processor Version: {processor_version_id}")
    print(f"Display Name: {processor_version.display_name}")
    print(f"DEPLOYED: {processor_version.state}")
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
# Snippet for the get_processor_version call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#get_processor_version.
#
def get_processor_version
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::GetProcessorVersionRequest.new

  # Call the get_processor_version method.
  result = client.get_processor_version request

  # The returned object is of type Google::Cloud::DocumentAI::V1::ProcessorVersion.
  p result
end
```

## Change the default version

A processor's *default version* specifies the version that is used to
process documents when you don't specify a specific version.
When you [create a processor](/document-ai/docs/create-processor), the initial
default version is the latest version in the stable channel.

If you change the default version, incoming requests are processed using the newly
selected version. If you change the default version while the processor is in the
middle of a request, the request will continue to use the previously selected version.

To change the default version:

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to the Processors page](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to view details for.
3. In the processor's **Manage Versions** (or **Deploy & use**) tab, in the **Default version**
   dropdown menu, choose a version of the processor that you want to use as
   the default version.

### REST

This sample shows how to set the default processor version for your
processor using the
[`processors.setDefaultProcessorVersion`](/document-ai/docs/reference/rest/v1/projects.locations.processors/setDefaultProcessorVersion)
method.

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

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:setDefaultProcessorVersion
```

Request JSON body:

```
{
  "defaultProcessorVersion": "PROCESSOR_VERSION"
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
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:setDefaultProcessorVersion"
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
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID:setDefaultProcessorVersion" | Select-Object -Expand Content
```

The response is a [long running operation](/document-ai/docs/long-running-operations). To poll the long-running operation, call [`operations.get`](/document-ai/docs/reference/rest/v1/projects.locations.operations/get)

The [`SetDefaultProcessorVersionMetadata`](/document-ai/docs/reference/rest/Shared.Types/SetDefaultProcessorVersionMetadata) in the response indicates the state of the operation.

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION",
  "metadata": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.SetDefaultProcessorVersionMetadata",
    "commonMetadata": {
      "state": "SUCCEEDED",
      "createTime": "2022-03-02T22:52:49.957096Z",
      "updateTime": "2022-03-02T22:52:50.175976Z",
      "resource": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION"
    }
  },
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.SetDefaultProcessorVersionResponse"
  }
}
```

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Cloud.DocumentAI.V1;
using Google.LongRunning;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for SetDefaultProcessorVersion</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void SetDefaultProcessorVersionRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        SetDefaultProcessorVersionRequest request = new SetDefaultProcessorVersionRequest
        {
            ProcessorAsProcessorName = ProcessorName.FromProjectLocationProcessor("[PROJECT]", "[LOCATION]", "[PROCESSOR]"),
            DefaultProcessorVersionAsProcessorVersionName = ProcessorVersionName.FromProjectLocationProcessorProcessorVersion("[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]"),
        };
        // Make the request
        Operation<SetDefaultProcessorVersionResponse, SetDefaultProcessorVersionMetadata> response = documentProcessorServiceClient.SetDefaultProcessorVersion(request);

        // Poll until the returned long-running operation is complete
        Operation<SetDefaultProcessorVersionResponse, SetDefaultProcessorVersionMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        SetDefaultProcessorVersionResponse result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<SetDefaultProcessorVersionResponse, SetDefaultProcessorVersionMetadata> retrievedResponse = documentProcessorServiceClient.PollOnceSetDefaultProcessorVersion(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            SetDefaultProcessorVersionResponse retrievedResult = retrievedResponse.Result;
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

	req := &documentaipb.SetDefaultProcessorVersionRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#SetDefaultProcessorVersionRequest.
	}
	op, err := c.SetDefaultProcessorVersion(ctx, req)
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
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.ProcessorName;
import com.google.cloud.documentai.v1.ProcessorVersionName;
import com.google.cloud.documentai.v1.SetDefaultProcessorVersionRequest;
import com.google.cloud.documentai.v1.SetDefaultProcessorVersionResponse;

public class SyncSetDefaultProcessorVersion {

  public static void main(String[] args) throws Exception {
    syncSetDefaultProcessorVersion();
  }

  public static void syncSetDefaultProcessorVersion() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DocumentProcessorServiceClient documentProcessorServiceClient =
        DocumentProcessorServiceClient.create()) {
      SetDefaultProcessorVersionRequest request =
          SetDefaultProcessorVersionRequest.newBuilder()
              .setProcessor(ProcessorName.of("[PROJECT]", "[LOCATION]", "[PROCESSOR]").toString())
              .setDefaultProcessorVersion(
                  ProcessorVersionName.of(
                          "[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]")
                      .toString())
              .build();
      SetDefaultProcessorVersionResponse response =
          documentProcessorServiceClient.setDefaultProcessorVersionAsync(request).get();
    }
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
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'


def set_default_processor_version_sample(
    project_id: str, location: str, processor_id: str, processor_version_id: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor = client.processor_path(project_id, location, processor_id)

    # The full resource name of the processor version
    # e.g.: projects/project_id/locations/location/processors/processor_id/processorVersions/processor_version_id
    processor_version = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    request = documentai.SetDefaultProcessorVersionRequest(
        processor=processor, default_processor_version=processor_version
    )

    # Make SetDefaultProcessorVersion request
    try:
        operation = client.set_default_processor_version(request)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    except NotFound as e:
        print(e.message)
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
# Snippet for the set_default_processor_version call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#set_default_processor_version.
#
def set_default_processor_version
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::SetDefaultProcessorVersionRequest.new

  # Call the set_default_processor_version method.
  result = client.set_default_processor_version request

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

## Deploy a processor version

After [creating a new processor version](/document-ai/workbench/docs/training-overview)
with Document AI, you will need to deploy it before you can process documents
with this version.

**Note:** You cannot change the deployment status for pretrained processor versions
or the current default version.

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to the Processors page](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to view details for.
3. In the processor's **Manage Versions** (or **Deploy & use**) tab, select the
   checkbox next to the processor version you want to deploy.
4. Click **Deploy**, then again click **Deploy** on the dialog window. This
   process takes a few minutes.

### REST

This sample shows how to deploy a processor version for your
processor using the
[`processorVersions.deploy`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions/deploy)
method.

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* PROCESSOR\_VERSION: the processor version identifier.

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:deploy
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
curl -X POST \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     -H "Content-Type: application/json; charset=utf-8" \  
     -d "" \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:deploy"
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
    -Method POST `  
    -Headers $headers `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:deploy" | Select-Object -Expand Content
```

The response is a [long running operation](/document-ai/docs/long-running-operations). To poll the long-running operation, call [`operations.get`](/document-ai/docs/reference/rest/v1/projects.locations.operations/get)

The [`DeployProcessorVersionMetadata`](/document-ai/docs/reference/rest/Shared.Types/DeployProcessorVersionMetadata) in the response indicates the state of the operation.

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION",
  "metadata": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.DeployProcessorVersionMetadata",
    "commonMetadata": {
      "state": "SUCCEEDED",
      "createTime": "2022-08-29T16:27:00.195539Z",
      "updateTime": "2022-08-29T16:32:01.963962Z",
      "resource": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION"
    }
  },
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.DeployProcessorVersionResponse"
  }
}
```

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Cloud.DocumentAI.V1;
using Google.LongRunning;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for DeployProcessorVersion</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void DeployProcessorVersionRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        DeployProcessorVersionRequest request = new DeployProcessorVersionRequest
        {
            ProcessorVersionName = ProcessorVersionName.FromProjectLocationProcessorProcessorVersion("[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]"),
        };
        // Make the request
        Operation<DeployProcessorVersionResponse, DeployProcessorVersionMetadata> response = documentProcessorServiceClient.DeployProcessorVersion(request);

        // Poll until the returned long-running operation is complete
        Operation<DeployProcessorVersionResponse, DeployProcessorVersionMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        DeployProcessorVersionResponse result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<DeployProcessorVersionResponse, DeployProcessorVersionMetadata> retrievedResponse = documentProcessorServiceClient.PollOnceDeployProcessorVersion(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            DeployProcessorVersionResponse retrievedResult = retrievedResponse.Result;
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

	req := &documentaipb.DeployProcessorVersionRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#DeployProcessorVersionRequest.
	}
	op, err := c.DeployProcessorVersion(ctx, req)
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
import com.google.cloud.documentai.v1.DeployProcessorVersionRequest;
import com.google.cloud.documentai.v1.DeployProcessorVersionResponse;
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.ProcessorVersionName;

public class SyncDeployProcessorVersion {

  public static void main(String[] args) throws Exception {
    syncDeployProcessorVersion();
  }

  public static void syncDeployProcessorVersion() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DocumentProcessorServiceClient documentProcessorServiceClient =
        DocumentProcessorServiceClient.create()) {
      DeployProcessorVersionRequest request =
          DeployProcessorVersionRequest.newBuilder()
              .setName(
                  ProcessorVersionName.of(
                          "[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]")
                      .toString())
              .build();
      DeployProcessorVersionResponse response =
          documentProcessorServiceClient.deployProcessorVersionAsync(request).get();
    }
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
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import FailedPrecondition
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID'
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'


def deploy_processor_version_sample(
    project_id: str, location: str, processor_id: str, processor_version_id: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g.: projects/project_id/locations/location/processors/processor_id/processorVersions/processor_version_id
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    # Make DeployProcessorVersion request
    try:
        operation = client.deploy_processor_version(name=name)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Deploy request will fail if the
    # processor version is already deployed
    except FailedPrecondition as e:
        print(e.message)
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
# Snippet for the deploy_processor_version call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#deploy_processor_version.
#
def deploy_processor_version
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::DeployProcessorVersionRequest.new

  # Call the deploy_processor_version method.
  result = client.deploy_processor_version request

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

## Undeploy a processor version

After
[creating a new processor version](/document-ai/workbench/docs/training-overview)
with Document AI and deploying it, you can undeploy it if you don't want the
processor version to be able to handle processing requests.

**Note:** You cannot change the deployment status for pretrained processor versions
or the current default version.

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to the Processors page](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to view details for.
3. In the processor's **Manage Versions** (or **Deploy & use**) tab, select the
   checkbox next to the processor version you want to undeploy.
4. Click **Undeploy**, then again click **Undeploy** on the dialog window.
   This process takes a few minutes.

### REST

This sample shows how to undeploy a processor version for your processor using the
[`processorVersions.undeploy`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions/undeploy)
method.

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* PROCESSOR\_VERSION: the processor version identifier.

HTTP method and URL:

```
POST https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:undeploy
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
curl -X POST \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     -H "Content-Type: application/json; charset=utf-8" \  
     -d "" \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:undeploy"
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
    -Method POST `  
    -Headers $headers `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION:undeploy" | Select-Object -Expand Content
```

The response is a [long running operation](/document-ai/docs/long-running-operations). To poll the long-running operation, call [`operations.get`](/document-ai/docs/reference/rest/v1/projects.locations.operations/get)

The [`UndeployProcessorVersionMetadata`](/document-ai/docs/reference/rest/Shared.Types/UndeployProcessorVersionMetadata) in the response indicates the state of the operation.

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION",
  "metadata": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.UndeployProcessorVersionMetadata",
    "commonMetadata": {
      "state": "SUCCEEDED",
      "createTime": "2022-08-29T16:27:00.195539Z",
      "updateTime": "2022-08-29T16:32:01.963962Z",
      "resource": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION"
    }
  },
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.UndeployProcessorVersionResponse"
  }
}
```

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Cloud.DocumentAI.V1;
using Google.LongRunning;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for UndeployProcessorVersion</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void UndeployProcessorVersionRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        UndeployProcessorVersionRequest request = new UndeployProcessorVersionRequest
        {
            ProcessorVersionName = ProcessorVersionName.FromProjectLocationProcessorProcessorVersion("[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]"),
        };
        // Make the request
        Operation<UndeployProcessorVersionResponse, UndeployProcessorVersionMetadata> response = documentProcessorServiceClient.UndeployProcessorVersion(request);

        // Poll until the returned long-running operation is complete
        Operation<UndeployProcessorVersionResponse, UndeployProcessorVersionMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        UndeployProcessorVersionResponse result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<UndeployProcessorVersionResponse, UndeployProcessorVersionMetadata> retrievedResponse = documentProcessorServiceClient.PollOnceUndeployProcessorVersion(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            UndeployProcessorVersionResponse retrievedResult = retrievedResponse.Result;
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

	req := &documentaipb.UndeployProcessorVersionRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#UndeployProcessorVersionRequest.
	}
	op, err := c.UndeployProcessorVersion(ctx, req)
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
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.ProcessorVersionName;
import com.google.cloud.documentai.v1.UndeployProcessorVersionRequest;
import com.google.cloud.documentai.v1.UndeployProcessorVersionResponse;

public class SyncUndeployProcessorVersion {

  public static void main(String[] args) throws Exception {
    syncUndeployProcessorVersion();
  }

  public static void syncUndeployProcessorVersion() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DocumentProcessorServiceClient documentProcessorServiceClient =
        DocumentProcessorServiceClient.create()) {
      UndeployProcessorVersionRequest request =
          UndeployProcessorVersionRequest.newBuilder()
              .setName(
                  ProcessorVersionName.of(
                          "[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]")
                      .toString())
              .build();
      UndeployProcessorVersionResponse response =
          documentProcessorServiceClient.undeployProcessorVersionAsync(request).get();
    }
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
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import FailedPrecondition
from google.api_core.exceptions import InvalidArgument
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'


def undeploy_processor_version_sample(
    project_id: str, location: str, processor_id: str, processor_version_id: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g.: projects/project_id/locations/location/processors/processor_id/processorVersions/processor_version_id
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    # Make UndeployProcessorVersion request
    try:
        operation = client.undeploy_processor_version(name=name)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Undeploy request will fail if the
    # processor version is already undeployed
    # or if a request is made on a pretrained processor version
    except (FailedPrecondition, InvalidArgument) as e:
        print(e.message)
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
# Snippet for the undeploy_processor_version call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#undeploy_processor_version.
#
def undeploy_processor_version
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::UndeployProcessorVersionRequest.new

  # Call the undeploy_processor_version method.
  result = client.undeploy_processor_version request

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

## Delete a processor version

After [creating a new processor version](/document-ai/workbench/docs/training-overview)
with Document AI, you can delete it if you have no further use for the processor
version.

**Note:** You cannot delete pretrained processor versions or the current default version.

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to the Processors page](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to view details for.
3. In the processor's **Manage Versions** (or **Deploy & use**) tab, click the
   action menu more\_vert next to the processor version you want to delete.
4. Click **Delete**, then again click **Delete** on the dialog window.

### REST

This sample shows how to delete a processor version for your processor using the
[`processorVersions.delete`](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions/delete)
method.

Before using any of the request data,
make the following replacements:

* LOCATION: your processor's [location](/document-ai/docs/regions), for example:
  + `us` - United States
  + `eu` - European Union
* PROJECT\_ID: Your Google Cloud project ID.
* PROCESSOR\_ID: the ID of your custom processor.
* PROCESSOR\_VERSION: the processor version identifier.

HTTP method and URL:

```
DELETE https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION
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
curl -X DELETE \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION"
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
    -Method DELETE `  
    -Headers $headers `  
    -Uri "https://LOCATION-documentai.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION" | Select-Object -Expand Content
```

The response is a [long running operation](/document-ai/docs/long-running-operations). To poll the long-running operation, call [`operations.get`](/document-ai/docs/reference/rest/v1/projects.locations.operations/get)

The [`DeleteProcessorVersionMetadata`](/document-ai/docs/reference/rest/Shared.Types/DeleteProcessorVersionMetadata) in the response indicates the state of the operation.

```
{
  "name": "projects/PROJECT_ID/locations/LOCATION/operations/OPERATION",
  "metadata": {
    "@type": "type.googleapis.com/google.cloud.documentai.v1.DeleteProcessorVersionMetadata",
    "commonMetadata": {
      "state": "SUCCEEDED",
      "createTime": "2022-08-29T16:27:00.195539Z",
      "updateTime": "2022-08-29T16:32:01.963962Z",
      "resource": "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID/processorVersions/PROCESSOR_VERSION"
    }
  },
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.protobuf.Empty"
  }
}
```

### C#

For more information, see the
[Document AI C# API
reference documentation](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest).

To authenticate to Document AI, set up Application Default Credentials.
For more information, see
[Set up authentication for a local development environment](/docs/authentication/set-up-adc-local-dev-environment).

```
using Google.Cloud.DocumentAI.V1;
using Google.LongRunning;
using Google.Protobuf.WellKnownTypes;

public sealed partial class GeneratedDocumentProcessorServiceClientSnippets
{
    /// <summary>Snippet for DeleteProcessorVersion</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void DeleteProcessorVersionRequestObject()
    {
        // Create client
        DocumentProcessorServiceClient documentProcessorServiceClient = DocumentProcessorServiceClient.Create();
        // Initialize request argument(s)
        DeleteProcessorVersionRequest request = new DeleteProcessorVersionRequest
        {
            ProcessorVersionName = ProcessorVersionName.FromProjectLocationProcessorProcessorVersion("[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]"),
        };
        // Make the request
        Operation<Empty, DeleteProcessorVersionMetadata> response = documentProcessorServiceClient.DeleteProcessorVersion(request);

        // Poll until the returned long-running operation is complete
        Operation<Empty, DeleteProcessorVersionMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        Empty result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<Empty, DeleteProcessorVersionMetadata> retrievedResponse = documentProcessorServiceClient.PollOnceDeleteProcessorVersion(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            Empty retrievedResult = retrievedResponse.Result;
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

	req := &documentaipb.DeleteProcessorVersionRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/documentai/apiv1/documentaipb#DeleteProcessorVersionRequest.
	}
	op, err := c.DeleteProcessorVersion(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}

	err = op.Wait(ctx)
	if err != nil {
		// TODO: Handle error.
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
import com.google.cloud.documentai.v1.DeleteProcessorVersionRequest;
import com.google.cloud.documentai.v1.DocumentProcessorServiceClient;
import com.google.cloud.documentai.v1.ProcessorVersionName;
import com.google.protobuf.Empty;

public class SyncDeleteProcessorVersion {

  public static void main(String[] args) throws Exception {
    syncDeleteProcessorVersion();
  }

  public static void syncDeleteProcessorVersion() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DocumentProcessorServiceClient documentProcessorServiceClient =
        DocumentProcessorServiceClient.create()) {
      DeleteProcessorVersionRequest request =
          DeleteProcessorVersionRequest.newBuilder()
              .setName(
                  ProcessorVersionName.of(
                          "[PROJECT]", "[LOCATION]", "[PROCESSOR]", "[PROCESSOR_VERSION]")
                      .toString())
              .build();
      documentProcessorServiceClient.deleteProcessorVersionAsync(request).get();
    }
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
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import FailedPrecondition
from google.api_core.exceptions import InvalidArgument
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'


def delete_processor_version_sample(
    project_id: str, location: str, processor_id: str, processor_version_id: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g.: projects/project_id/locations/location/processors/processor_id/processorVersions/processor_version_id
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    # Make DeleteProcessorVersion request
    try:
        operation = client.delete_processor_version(name=name)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Delete request will fail if the
    # processor version doesn't exist
    # or if a request is made on a pretrained processor version
    # or the default processor version
    except (FailedPrecondition, InvalidArgument) as e:
        print(e.message)
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
# Snippet for the delete_processor_version call in the DocumentProcessorService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client#delete_processor_version.
#
def delete_processor_version
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::DocumentAI::V1::DeleteProcessorVersionRequest.new

  # Call the delete_processor_version method.
  result = client.delete_processor_version request

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

## Import a processor version

After [creating a new processor](/document-ai/workbench/docs/training-overview) with Document AI, you can import a [processor version](/document-ai/docs/reference/rest/v1/projects.locations.processors.processorVersions#resource:-processorversion) from the same or a different project.

The `destination project` is where you begin the import and where the processor version becomes available after the import.

The `source project` is where the source processor version lives.

**Note:** Processor version import is not supported for destination projects operating
in [single-region locations](/document-ai/docs/regions), except for `asia-south1`,
and `northamerica-northeast1`.

The source or destination processors must meet the following requirements to import:

* Processor types must match. Examples: `CUSTOM_EXTRACTION_PROCESSOR` or `INVOICE_PROCESSOR`
* Processor schemas must not conflict.
* Destination processor can have existing datasets and versions.
* Destination processor must be in `ENABLED` state.
* Source processor version must be in one of the following states:
  + `DEPLOYED`
  + `DEPLOYING`
  + `UNDEPLOYED`
  + `UNDEPLOYING`

You must grant the [DocumentAI Core Service Agent](/iam/docs/service-agents) of
the destination project [Document AI Editor](/document-ai/docs/access-control/iam-roles)
permission on the source project to avoid a permission denied error.

**Note:** This applies if importing processor versions within the same project or
between separate projects.

For processor versions based on Gemini 1.5 and later, such as
[custom extractors](/document-ai/docs/custom-extractor-overview)
`pretrained-foundation-model-v1.2-2024-05-10`, you can import fine-tuned
processor versions.

Complete the following steps to set up permission before importing a processor version:

### Console

1. Look up [DocumentAI Core Service Agent](/iam/docs/service-agents) and fill in
   your destination project number. The DocumentAI Core Service Agent is formatted
   like an email address. For example: `service-123@gcp-sa-prod-dai-core.iam.gserviceaccount.com`
2. Open the IAM page in the Google Cloud console.

   [Open
   the IAM page](https://console.cloud.google.com/iam-admin/iam)
3. Select your source project.
4. Click grant access.
5. Add the destination project's DocumentAI Core Service Agent as a new principal,
   and assign [Document AI Editor](/document-ai/docs/access-control/iam-roles) role.

### gcloud

Use the following `gcloud` command to grant the necessary permissions:

```
gcloud projects add-iam-policy-binding SOURCE_PROJECT \
    --member=serviceAccount:service-DESTINATION_PROJECT NUMBER@gcp-sa-prod-dai-core.iam.gserviceaccount.com \
    --role=roles/documentai.editor
```

Provide the following values:

* `SOURCE_PROJECT`: The source project number or project id.
* `DESTINATION_PROJECT NUMBER`: The destination project **number**.

After updating the permissions, use the following steps to import a processor version:

### Console

1. In the Google Cloud console, in the Document AI section, go to the
   **Processors** page.

   [Go to the Processors page](https://console.cloud.google.com/ai/document-ai/processors)
2. From the list of processors, click the name of the processor that you
   want to import a processor version to as a destination processor.
3. Go to the **Manage Versions** (or **Deploy & use**) tab, and click **Import**.
4. Choose the project, the processor, and the processor version as the source
   processor version in the window.
5. Click **IMPORT** button in the window, and the import operation will start.

### REST

This sample shows you how to use the
[`processorVersions.importProcessorVersion`](/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions/importProcessorVersion)
method to import a processor version.

Before using any of the request data,
make the following replacements:

* Destination Project
  + DESTINATION\_PROJECT\_ID: your destination Google Cloud project ID.
  + DESTINATION\_LOCATION: your destination processor's [location](/document-ai/docs/regions).
  + DESTINATION\_PROCESSOR\_ID: the ID of your destination processor.
* Source Project
  + SOURCE\_PROJECT\_ID: your source Google Cloud project ID.
  + SOURCE\_LOCATION: the source processor's location.
  + SOURCE\_PROCESSOR\_ID: the ID of your source processor.
  + SOURCE\_PROCESSOR\_VERSION: the source processor version to import.

HTTP method and URL:

```
POST https://DESTINATION_LOCATION-documentai.googleapis.com/v1beta3/projects/DESTINATION_PROJECT_ID/locations/DESTINATION_LOCATION/processors/DESTINATION_PROCESSOR_ID/processorVersions:importProcessorVersion
```

Request JSON body:

```
{
  "processorVersionSource": "projects/SOURCE_PROJECT_ID/locations/SOURCE_LOCATION/processors/SOURCE_PROCESSOR_ID/processorVersions/SOURCE_PROCESSOR_VERSION"
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
     "https://DESTINATION_LOCATION-documentai.googleapis.com/v1beta3/projects/DESTINATION_PROJECT_ID/locations/DESTINATION_LOCATION/processors/DESTINATION_PROCESSOR_ID/processorVersions:importProcessorVersion"
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
    -Uri "https://DESTINATION_LOCATION-documentai.googleapis.com/v1beta3/projects/DESTINATION_PROJECT_ID/locations/DESTINATION_LOCATION/processors/DESTINATION_PROCESSOR_ID/processorVersions:importProcessorVersion" | Select-Object -Expand Content
```

You should receive a JSON response similar to the following:

```
{
  "name": "projects/DESTINATION_PROJECT_ID/locations/DESTINATION_LOCATION/operations/OPERATION_ID"
}
```

If you're importing across a Virtual Private Cloud service controls (VPC-SC) perimeter,
review [configuring ingress and egress policies](/vpc-service-controls/docs/configuring-ingress-egress-policies)
and [set up a VPC Service Controls perimeter](/vpc-service-controls/docs/set-up-service-perimeter-verify-access),
then set the following rules.

**Note:** You must run a dummy fine tuning in the destination processor before importing
a processor version. This will initialize the necessary resources for a fresh processor.

Provide the following values for **ingress**:

* `DESTINATION_PROJECT`: The destination project number.
* `SOURCE_PROJECT`: The source project number.

```
- ingressFrom:
    identities:
    - ANY_SERVICE_ACCOUNT
    sources:
    - resource: DESTINATION_PROJECT
  ingressTo:
    operations:
    - serviceName: aiplatform.googleapis.com
      methodSelectors:
      - method: all actions
    - serviceName: documentai.googleapis.com
      methodSelectors:
      - method: all actions
    resources:
    - projects/SOURCE_PROJECT
```

Provide the following values for **egress**:

```
- egressTo:
    operations:
    - serviceName: storage.googleapis.com
      methodSelectors:
      - method: google.storage.objects.create
      - method: google.storage.buckets.testIamPermissions
    resources:
    - projects/DESTINATION_PROJECT
  egressFrom:
    identities:
    - ANY_SERVICE_ACCOUNT
```

Set up a VPC destination perimeter with the following values.

```
- egressTo:
    operations:
    - serviceName: aiplatform.googleapis.com
      methodSelectors:
      - method: all actions
    - serviceName: documentai.googleapis.com
      methodSelectors:
      - method: all actions
    - serviceName: storage.googleapis.com
      methodSelectors:
      - method: google.storage.buckets.testIamPermissions
      - method: google.storage.objects.get
      - method: google.storage.objects.create
    resources:
    - projects/SOURCE_PROJECT
  egressFrom:
    identities:
    - ANY_SERVICE_ACCOUNT
    sourceRestriction: DISABLED
```

## What's next?

* Learn how to [set up](/document-ai/docs/setup) Document AI.
* Review the [processors list](/document-ai/docs/processors-list).

[Previous

arrow\_back

Build a document processing pipeline with Workflows](/document-ai/docs/workflows)

[Next

Migrate processor versions and datasets

arrow\_forward](/document-ai/docs/copy-processor-versions)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-07-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-07-01 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/create-processor](./document-ai-docs-create-processor.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/processors-list](./document-ai-docs-processors-list.md)
- [https://docs.cloud.google.com/document-ai/docs/setup](./document-ai-docs-setup.md)
