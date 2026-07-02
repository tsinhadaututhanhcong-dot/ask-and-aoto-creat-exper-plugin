# Document AI overview  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/overview](https://docs.cloud.google.com/document-ai/docs/overview)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Document AI overview Stay organized with collections Save and categorize content based on your preferences.



This document is a guide to the fundamental concepts of using Document AI.
You should read this page before proceeding to any other documentation or quickstarts.

## Automate document processing workflows

Businesses all over the world rely heavily on documents to store and convey information.
This information often needs to be digitized for it to become useful. However,
this is usually accomplished through time-intensive, manual processes.

For example:

* Digitizing books for e-readers.
* Processing medical intake forms at doctor's offices.
* Parsing receipts and invoices for expense report validation.
* Authenticating identity based on ID cards.
* Extracting income information from tax forms for approving loans.
* Understanding contracts for key business agreement terms.

Each of these workflows involve getting the raw text from documents, then
extracting specific text from that which corresponds to the data needed (the fields or entities).
However, each document type has a different structure and layout, and the pattern of fields
vary depending on the specific use case.

## Document AI components

Document AI is a [document processing and understanding](https://en.wikipedia.org/wiki/Document_processing)
platform that takes unstructured data from documents and transforms it into
structured data (specific fields, suitable for a database), making it easier to understand, analyze, and consume.

Document AI is built on top of products within Vertex AI with generative AI to help you
create scalable, end-to-end, cloud-based document processing applications without specialized machine learning expertise.

Using Document AI, you can:

* **Digitize documents** using OCR to get text, layout, and various add ons such as image
  quality detection (for readability) and deskewing (fully automatic).
* **Extract** text and layout information, from document files and normalize entities.
* **Identify key-value pairs (kvp)** in structured forms and regular tables. For example: `Name: Jill Smith` is a kvp.
* **Classify** document types to drive downstream processes such as extraction and storage.
* **Split** and classify documents by type. For example, a PDF file with multiple real documents.
* **Prepare datasets** to be used in fine-tuning and model evaluations using auto-labeling,
  schema management, and dataset management features such as document and prediction review.
* **Integrate it with products** like Cloud Storage, BigQuery, and Agent Search
  to help you store, search, organize, govern, and analyze documents and metadata.

This diagram illustrates all of the key document processing steps that are
supported by Document AI and how they can connect to each other.

![docai-overview-1](/static/document-ai/docs/images/discover/docai-overview-1.png)

## Processor

A Document AI processor lies between the document file and a machine
learning model that performs document processing and understanding actions.
They can be used to classify, split, parse, or analyze a document.

Each Google Cloud project needs to create its own processor instances.

Processors fit into one of the following categories:

* **Digitize**: OCR.
* **Extract**: Custom extractor, Form Parser, layout parser, and pretrained parsers.
* **Classify**: Custom classifier and custom splitter.

Refer to the [Full processor and detail list](/document-ai/docs/processors-list) for information about all
available processor types for Document AI.

### Which processor should I use?

To decide what processor type to use for a specific application, here are some general guidelines:

**Note:** All processors can extract text and layout information.

| **Category** | **Use case** | **Processor type** |
| --- | --- | --- |
| Digitize | Extract text and layout information from documents. | [Enterprise Document OCR](/document-ai/docs/processors-list#processor_doc-ocr) |
| Analyze the scanned image quality (readability) of a document. | [Enterprise Document OCR](/document-ai/docs/processors-list#processor_doc-ocr) with  [image-quality analysis](/document-ai/docs/processors-list#processor_doc-quality-processor)  enabled |
| Extract entities from a custom document that does not meet the [custom processor criteria](/document-ai/quotas). |  |
| Extract | Extract tables or kvp from a structured form in a document. | [Form Parser](/document-ai/docs/processors-list#processor_form-parser) |
| Extract elements like text, tables, and lists in a document and return context aware chunks. | [Layout Parser](/document-ai/docs/layout-parse-chunk) |
| Extract entities from a custom document that meets the [custom processor criteria](/document-ai/quotas). | [Create a custom extractor](/document-ai/docs/workbench/build-custom-processor) |
| Extract entities from a specialized document type. | A [pretrained processor](/document-ai/docs/processors-list#specialized_processors) ([Up-train](/document-ai/docs/uptrain-pretrained-processor) to improve quality.) |
| Classify | Classify documents. | [Create a Custom Classifier](/document-ai/docs/workbench/build-custom-classification-processor) |
| Split documents. | [Create a Custom Splitter](/document-ai/docs/workbench/build-custom-splitter-processor) |

This diagram helps determine which processor works best for each use case.

![docai-overview-2](/static/document-ai/docs/images/discover/docai-overview-2.png)

### Use Document AI processors

Here are the major steps to use Document AI to start processing documents:

1. **Choose a processor** that is suitable for your use case.

   * For complete information on each processor, see the [Full processor and detail list](/document-ai/docs/processors-list).
2. **Create a processor** using the Google Cloud console or the Document AI API.

   * Document AI creates a **prediction endpoint** where you can send your documents.
   * For detailed instructions, see [Creating a processor](/document-ai/docs/create-processor).
3. **Train a processor** with train and test data from scratch, or uptrain a new (pretrained) processor version on top of an existing one.

   * For detailed instructions, see [Train processor](/document-ai/docs/workbench/train-processor).
4. **Send your documents** for processing.

   * Document AI processes the documents and returns one or more [`Document`](/document-ai/docs/reference/rest/v1/Document) objects, which contain the extracted, structured information.
   * For detailed instructions, see [Sending a processing request](/document-ai/docs/send-request) and [Handle the processing response](/document-ai/docs/handle-response).

[Next

Try Document AI

arrow\_forward](/document-ai/docs/try-docai)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/create-processor](./document-ai-docs-create-processor.md)
- [https://docs.cloud.google.com/document-ai/docs/handle-response](./document-ai-docs-handle-response.md)
- [https://docs.cloud.google.com/document-ai/docs/processors-list](./document-ai-docs-processors-list.md)
- [https://docs.cloud.google.com/document-ai/docs/send-request](./document-ai-docs-send-request.md)
