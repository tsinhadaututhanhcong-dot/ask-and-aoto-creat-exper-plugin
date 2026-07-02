# Document AI client libraries  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/libraries](https://docs.cloud.google.com/document-ai/docs/libraries)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Document AI client libraries Stay organized with collections Save and categorize content based on your preferences.



This page shows how to get started with the Cloud Client Libraries for the
Document AI API. Client libraries make it easier to access
Google Cloud APIs from a supported language. Although you can use
Google Cloud APIs directly by making raw requests to the server, client
libraries provide simplifications that significantly reduce the amount of code
you need to write.

Read more about the Cloud Client Libraries
and the older Google API Client Libraries in
[Client libraries explained](/apis/docs/client-libraries-explained).

## Install the client library

### C++

See [Setting up a C++ development environment](/cpp/docs/setup)
for details about this client library's requirements and install dependencies.

### C#

```
Install-Package Google.Cloud.DocumentAI.V1 -Pre
```

For more information, see [Setting Up a C# Development Environment](/dotnet/docs/setup).

### Go

```
go get cloud.google.com/go/documentai
```

For more information, see [Setting Up a Go Development Environment](/go/docs/setup).

### Java

If you are using [Maven](https://maven.apache.org/), add
the following to your `pom.xml` file. For more information about
BOMs, see [The Google Cloud Platform Libraries BOM](https://cloud.google.com/java/docs/bom).

```
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.google.cloud</groupId>
      <artifactId>libraries-bom</artifactId>
      <version>26.83.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>google-cloud-document-ai</artifactId>
  </dependency>
</dependencies>
```

If you are using [Gradle](https://gradle.org/),
add the following to your dependencies:

```
implementation 'com.google.cloud:google-cloud-document-ai:2.97.0'
```

If you are using [sbt](https://www.scala-sbt.org/), add
the following to your dependencies:

```
libraryDependencies += "com.google.cloud" % "google-cloud-document-ai" % "2.97.0"
```

If you're using Visual Studio Code or IntelliJ, you can add client libraries to your
project using the following IDE plugins:

* [Cloud Code for VS Code](/code/docs/vscode/client-libraries)
* [Cloud Code for IntelliJ](/code/docs/intellij/client-libraries)

The plugins provide additional functionality, such as key management for service accounts. Refer
to each plugin's documentation for details.

**Note:** Cloud Java client libraries do not currently support Android.

For more information, see [Setting Up a Java Development Environment](/java/docs/setup).

### Node.js

```
npm install @google-cloud/documentai
```

For more information, see [Setting Up a Node.js Development Environment](/nodejs/docs/setup).

### PHP

```
composer require google/cloud-document-ai
```

For more information, see [Using PHP on Google Cloud](/php/docs).

### Python

```
pip install --upgrade google-cloud-documentai
```

For more information, see [Setting Up a Python Development Environment](/python/docs/setup).

### Ruby

```
gem install google-cloud-document_ai
```

For more information, see [Setting Up a Ruby Development Environment](/ruby/docs/setup).

## Set up authentication

To authenticate calls to Google Cloud APIs, client libraries support
[Application Default Credentials (ADC)](/docs/authentication/application-default-credentials);
the libraries look for credentials in a set of defined locations and use those credentials
to authenticate requests to the API. With ADC, you can make
credentials available to your application in a variety of environments, such as local
development or production, without needing to modify your application code.

For production environments, the way you set up ADC depends on the service
and context. For more information, see [Set up Application Default Credentials](/docs/authentication/provide-credentials-adc).

For a local development environment, you can set up ADC with the credentials
that are associated with your Google Account:

1. [Install](/sdk/docs/install) the Google Cloud CLI.
   After installation,
   [initialize](/sdk/docs/initializing) the Google Cloud CLI by running the following command:

   ```
   gcloud init
   ```

   If you're using an external identity provider (IdP), you must first
   [sign in to the gcloud CLI with your federated identity](/iam/docs/workforce-log-in-gcloud).
2. If you're using a local shell, then create local authentication credentials for your user
   account:

   ```
   gcloud auth application-default login
   ```

   You don't need to do this if you're using Cloud Shell.

   If an authentication error is returned, and you are using an external identity provider
   (IdP), confirm that you have
   [signed in to the gcloud CLI with your federated identity](/iam/docs/workforce-log-in-gcloud).

   A sign-in screen appears. After you sign in, your credentials are stored in the
   [local credential file used by ADC](/docs/authentication/application-default-credentials#personal).

## Use the client library

The following example shows how to use the client library.

### C++

```
#include "google/cloud/documentai/v1/document_processor_client.h"
#include "google/cloud/location.h"
#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) try {
  if (argc != 5) {
    std::cerr << "Usage: " << argv[0]
              << " project-id location-id processor-id filename (PDF only)\n";
    return 1;
  }

  std::string const location_id = argv[2];
  if (location_id != "us" && location_id != "eu") {
    std::cerr << "location-id must be either 'us' or 'eu'\n";
    return 1;
  }
  auto const location = google::cloud::Location(argv[1], location_id);

  namespace documentai = ::google::cloud::documentai_v1;
  auto client = documentai::DocumentProcessorServiceClient(
      documentai::MakeDocumentProcessorServiceConnection(
          location.location_id()));

  google::cloud::documentai::v1::ProcessRequest req;
  req.set_name(location.FullName() + "/processors/" + argv[3]);
  req.set_skip_human_review(true);
  auto& doc = *req.mutable_raw_document();
  doc.set_mime_type("application/pdf");
  std::ifstream is(argv[4]);
  doc.set_content(std::string{std::istreambuf_iterator<char>(is), {}});

  auto resp = client.ProcessDocument(std::move(req));
  if (!resp) throw std::move(resp).status();
  std::cout << resp->document().text() << "\n";

  return 0;
} catch (google::cloud::Status const& status) {
  std::cerr << "google::cloud::Status thrown: " << status << "\n";
  return 1;
}
```

### C#

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

### Go

```
import (
	"context"
	"flag"
	"fmt"
	"os"

	documentai "cloud.google.com/go/documentai/apiv1"
	"cloud.google.com/go/documentai/apiv1/documentaipb"
	"google.golang.org/api/option"
)

func main() {
	projectID := flag.String("project_id", "PROJECT_ID", "Cloud Project ID")
	location := flag.String("location", "us", "The Processor location")
	// Create a Processor before running sample
	processorID := flag.String("processor_id", "aaaaaaaa", "The Processor ID")
	filePath := flag.String("file_path", "invoice.pdf", "The path to the file to parse")
	mimeType := flag.String("mime_type", "application/pdf", "The mimeType of the file")
	flag.Parse()

	ctx := context.Background()

	endpoint := fmt.Sprintf("%s-documentai.googleapis.com:443", *location)
	client, err := documentai.NewDocumentProcessorClient(ctx, option.WithEndpoint(endpoint))
	if err != nil {
		fmt.Println(fmt.Errorf("error creating Document AI client: %w", err))
	}
	defer client.Close()

	// Open local file.
	data, err := os.ReadFile(*filePath)
	if err != nil {
		fmt.Println(fmt.Errorf("os.ReadFile: %w", err))
	}

	req := &documentaipb.ProcessRequest{
		Name: fmt.Sprintf("projects/%s/locations/%s/processors/%s", *projectID, *location, *processorID),
		Source: &documentaipb.ProcessRequest_RawDocument{
			RawDocument: &documentaipb.RawDocument{
				Content:  data,
				MimeType: *mimeType,
			},
		},
	}
	resp, err := client.ProcessDocument(ctx, req)
	if err != nil {
		fmt.Println(fmt.Errorf("processDocument: %w", err))
	}

	// Handle the results.
	document := resp.GetDocument()
	fmt.Printf("Document Text: %s", document.GetText())
}
```

### Java

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

public class QuickStart {
  public static void main(String[] args)
      throws IOException, InterruptedException, ExecutionException, TimeoutException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "your-project-id";
    String location = "your-project-location"; // Format is "us" or "eu".
    String processorId = "your-processor-id";
    String filePath = "path/to/input/file.pdf";
    quickStart(projectId, location, processorId, filePath);
  }

  public static void quickStart(
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
// apiEndpoint regions available: eu-documentai.googleapis.com, us-documentai.googleapis.com (Required if using eu based processor)
// const client = new DocumentProcessorServiceClient({apiEndpoint: 'eu-documentai.googleapis.com'});
const client = new DocumentProcessorServiceClient();

async function quickstart() {
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
}
```

### PHP

```
# Include the autoloader for libraries installed with Composer.
require __DIR__ . '/vendor/autoload.php';

# Import the Google Cloud client library.
use Google\Cloud\DocumentAI\V1\Client\DocumentProcessorServiceClient;
use Google\Cloud\DocumentAI\V1\RawDocument;
use Google\Cloud\DocumentAI\V1\ProcessRequest;

# TODO(developer): Update the following lines before running the sample.
# Your Google Cloud Platform project ID.
$projectId = 'YOUR_PROJECT_ID';

# Your Processor Location.
$location = 'us';

# Your Processor ID as hexadecimal characters.
# Not to be confused with the Processor Display Name.
$processorId = 'YOUR_PROCESSOR_ID';

# Path for the file to read.
$documentPath = 'resources/invoice.pdf';

# Create Client.
$client = new DocumentProcessorServiceClient();

# Read in file.
$handle = fopen($documentPath, 'rb');
$contents = fread($handle, filesize($documentPath));
fclose($handle);

# Load file contents into a RawDocument.
$rawDocument = (new RawDocument())
    ->setContent($contents)
    ->SetMimeType('application/pdf');

# Get the Fully-qualified Processor Name.
$fullProcessorName = $client->processorName($projectId, $location, $processorId);

# Send a ProcessRequest and get a ProcessResponse.
$request = (new ProcessRequest())
    ->setName($fullProcessorName)
    ->setRawDocument($rawDocument);

$response = $client->processDocument($request);

# Show the text found in the document.
printf('Document Text: %s', $response->getDocument()->getText());
```

### Python

```
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1

# TODO(developer): Create a processor of type "OCR_PROCESSOR".

# TODO(developer): Update and uncomment these variables before running the sample.
# project_id = "MY_PROJECT_ID"

# Processor ID as hexadecimal characters.
# Not to be confused with the Processor Display Name.
# processor_id = "MY_PROCESSOR_ID"

# Processor location. For example: "us" or "eu".
# location = "MY_PROCESSOR_LOCATION"

# Path for file to process.
# file_path = "/path/to/local/pdf"

# Set `api_endpoint` if you use a location other than "us".
opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

# Initialize Document AI client.
client = documentai_v1.DocumentProcessorServiceClient(client_options=opts)

# Get the Fully-qualified Processor path.
full_processor_name = client.processor_path(project_id, location, processor_id)

# Get a Processor reference.
request = documentai_v1.GetProcessorRequest(name=full_processor_name)
processor = client.get_processor(request=request)

# `processor.name` is the full resource name of the processor.
# For example: `projects/{project_id}/locations/{location}/processors/{processor_id}`
print(f"Processor Name: {processor.name}")

# Read the file into memory.
with open(file_path, "rb") as image:
    image_content = image.read()

# Load binary data.
# For supported MIME types, refer to https://cloud.google.com/document-ai/docs/file-types
raw_document = documentai_v1.RawDocument(
    content=image_content,
    mime_type="application/pdf",
)

# Send a request and get the processed document.
request = documentai_v1.ProcessRequest(name=processor.name, raw_document=raw_document)
result = client.process_document(request=request)
document = result.document

# Read the text recognition output from the processor.
# For a full list of `Document` object attributes, reference this page:
# https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
print("The document contains the following text:")
print(document.text)
```

### Ruby

```
require "google/cloud/document_ai/v1"

##
# Document AI quickstart
#
# @param project_id [String] Your Google Cloud project (e.g. "my-project")
# @param location_id [String] Your Processor Location (e.g. "us")
# @param processor_id [String] Your Processor ID (e.g. "a14dae8f043b60bd")
# @param file_path [String] Path to Local File (e.g. "invoice.pdf")
# @param mime_type [String] Refer to https://cloud.google.com/document-ai/docs/file-types (e.g. "application/pdf")
#
def quickstart project_id:, location_id:, processor_id:, file_path:, mime_type:
  # Create the Document AI client.
  client = ::Google::Cloud::DocumentAI::V1::DocumentProcessorService::Client.new do |config|
    config.endpoint = "#{location_id}-documentai.googleapis.com"
  end

  # Build the resource name from the project.
  name = client.processor_path(
    project: project_id,
    location: location_id,
    processor: processor_id
  )

  # Read the bytes into memory
  content = File.binread file_path

  # Create request
  request = Google::Cloud::DocumentAI::V1::ProcessRequest.new(
    skip_human_review: true,
    name: name,
    raw_document: {
      content: content,
      mime_type: mime_type
    }
  )

  # Process document
  response = client.process_document request

  # Handle response
  puts response.document.text
end
```

## Additional resources

### C++

The following list contains links to more resources related to the
client library for C++:

* [API reference](/cpp/docs/reference/documentai/latest)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-cpp/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D%5Bc%2B%2B%5D)
* [Source code](https://github.com/googleapis/google-cloud-cpp)

### C#

The following list contains links to more resources related to the
client library for C#:

* [API reference](/dotnet/docs/reference/Google.Cloud.DocumentAI.V1/latest)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-dotnet/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bc%23%5D)
* [Source code](https://github.com/googleapis/google-cloud-dotnet)

### Go

The following list contains links to more resources related to the
client library for Go:

* [API reference](/go/docs/reference/cloud.google.com/go/documentai/latest/apiv1)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-go/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bgo%5D)
* [Source code](https://github.com/googleapis/google-cloud-go)

### Java

The following list contains links to more resources related to the
client library for Java:

* [API reference](/java/docs/reference/google-cloud-document-ai/latest/overview)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-java/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bjava%5D)
* [Source code](https://github.com/googleapis/google-cloud-java)

### Node.js

The following list contains links to more resources related to the
client library for Node.js:

* [API reference](/nodejs/docs/reference/documentai/latest)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-node/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bnode.js%5D)
* [Source code](https://github.com/googleapis/google-cloud-node)

### PHP

The following list contains links to more resources related to the
client library for PHP:

* [API reference](/php/docs/reference/cloud-document-ai/latest)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-php/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bphp%5D)
* [Source code](https://github.com/googleapis/google-cloud-php)

### Python

The following list contains links to more resources related to the
client library for Python:

* [API reference](/python/docs/reference/documentai/latest)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/python-documentai/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bpython%5D)
* [Source code](https://github.com/googleapis/python-documentai)

### Ruby

The following list contains links to more resources related to the
client library for Ruby:

* [API reference](/ruby/docs/reference/google-cloud-document_ai-v1/latest)
* [Client libraries best practices](/apis/docs/client-libraries-best-practices)
* [Issue tracker](https://github.com/googleapis/google-cloud-ruby/issues)
* [`cloud-document-ai` on Stack Overflow](https://stackoverflow.com/search?q=%5Bcloud-document-ai%5D+%5Bruby%5D)
* [Source code](https://github.com/googleapis/google-cloud-ruby)

[Previous

arrow\_back

Toolbox](/document-ai/docs/toolbox)

[Next

Sample processor output

arrow\_forward](/document-ai/docs/output)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/output](./document-ai-docs-output.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
