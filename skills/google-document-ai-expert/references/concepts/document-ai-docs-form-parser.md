---
type: Reference
title: "Form Parser  |  Document AI  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/form-parser](https://docs.cloud.google.com/document-ai/docs/form-parser)"
timestamp: 2026-07-06T03:34:16Z
---
# Form Parser  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/form-parser](https://docs.cloud.google.com/document-ai/docs/form-parser)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Form Parser Stay organized with collections Save and categorize content based on your preferences.



Form Parser extracts key-value pairs (KVPs), tables, selection marks (like checkboxes),
generic fields, and text to augment and automate document processing.

**Note:** Form Parser is pre-trained and cannot be up-trained.

Form Parser can be considered over the other parsers when the use case involves:

* Dealing with structured forms: It excels at extracting KVPs from
  well-defined forms that look like conventional forms with labeled blanks to fill
  in, such as `name: __`. Form Parser's pre-trained model offers high
  accuracy for common fields like names, dates, and addresses.
* Flexible table extraction is needed: Form Parser extracts from simple
  (no cells that span rows or columns) tables that look like tables. No training
  is needed (nor possible). For trained table extraction, the custom extractor can
  be used with a parent field containing column (cell) child fields.
* Need efficiency: Avoid building and maintaining extraction parsers, especially for
  high-volume and varied forms of extraction tasks.

## Data-extraction features

Form Parser features encompass:

* **KVP:** These are sets of two items within a document—a label or key and its
  corresponding data (a value). You can directly use KVPs (if the keys are consistent)
  or build custom logic to resolve varied keys into consistent structured information.
* **Generic entities:** Parse 11 different fields from documents out of the box. These include:

  + `email`
  + `phone`
  + `url`
  + `date_time`
  + `address`
  + `person`
  + `organization`
  + `quantity`
  + `price`
  + `id`
  + `page_number`
* **Text and layout:** Use our latest OCR engine to extract text and layout
  information. This includes embedded text from digital PDFs (v2.1 only) or text from images.
* **Tables:** Detect and extract tables from images and PDFs.
* **Checkboxes:** A high-quality selection mark detector, which extracts checkboxes
  from images and PDF output as KVP, using the text nearest the checkbox, with a `valueType`
  indicating whether it is filled or unfilled.

## Languages and regions

* Form Parser 2.0 supports over 200 languages. [Learn more](/document-ai/docs/processors-list#expandable-1).
* We provide feature support in eight regions. [Learn more](/document-ai/docs/regions).

## Model versions

The following processor versions are compatible with this feature. For more
information, see [Managing processor versions](/document-ai/docs/manage-processor-versions).

## Limitations

* Prior JPEG compressions for TIFF are unsupported. Type of JPEG encapsulation defined by the TIFF [version 6.0 specification](https://gitlab.com/libtiff/libtiff/-/commit/f0a54a4fa0cfa377f493d57ee2af393005d5bbe5).
* The checkbox model doesn't support parsing radio buttons. Some detected checkboxes might not have corresponding keys.
* The model doesn't reliably parse a KVP with an unfilled value, such as a blank form.
* The KVP parsing on documents in certain languages may have lower quality than Latin languages.





## Process documents with Form Parser

This quickstart introduces you to the Form Parser feature in Document AI. In this quickstart,
you use the Google Cloud console to set up your Google Cloud project and
authorization, create a Form Parser, and then make a request for
Document AI to process a PDF form.

Learn how to:

1. Enable Document AI in a Google Cloud project.
2. Create a Form Parser processor, which can identify
   and extract text, key-value pairs, tables, and generic entities from many types of documents.
3. Use the processor to annotate a sample document.

---

To follow step-by-step guidance for this task directly in the
Google Cloud console, click **Guide me**:

[Guide me](https://console.cloud.google.com/ai/document-ai?tutorial=document-ai--documentai_form_parser_console)

---

- Sign in to your Google Cloud account. If you're new to
  Google Cloud, [create an account](https://console.cloud.google.com/freetrial) to evaluate how our products perform in
  real-world scenarios. New customers also get $300 in free credits to
  run, test, and deploy workloads.
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](/iam/docs/granting-changing-revoking-access).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- Enable the Document AI API.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](/iam/docs/granting-changing-revoking-access).

  [Enable the API](https://console.cloud.google.com/apis/enableflow?apiid=documentai.googleapis.com)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](/iam/docs/granting-changing-revoking-access).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- Enable the Document AI API.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](/iam/docs/granting-changing-revoking-access).

  [Enable the API](https://console.cloud.google.com/apis/enableflow?apiid=documentai.googleapis.com)

## Create a Form Parser processor

Use the Google Cloud console to create a Form Parser processor. See [creating and managing processors](/document-ai/docs/create-processor) for more information.

1. In the Google Cloud console navigation menu, click **Document AI** and
   select **Processor Gallery**.

   [Processor
   Gallery](https://console.cloud.google.com/ai/document-ai/processor-library)
2. In the **Processor Gallery**,
   search for
   **Form Parser** and select **Create**.

   ![Form Parser option in UI](/static/document-ai/docs/images/create/form-parser-card-ui.png)
3. In the side window, enter a **Processor name**, such as `quickstart-form-processor`.
4. Select the region closest to you.
5. Click the **Create** button.

You're taken to the **Processor Details** page of your new form parser processor.

## Test processor

After creating your processor, you can send annotation requests to it.

1. [Download the sample document](https://storage.googleapis.com/cloud-samples-data/documentai/GeneralProcessors/FormParser/intake-form.pdf).

   It's a PDF file containing a sample handwritten medical intake form. This document is stored in a publicly accessible Cloud Storage bucket.
2. Click the
    **Upload Test Document** button and select the document you just downloaded.
3. You should now be on the **Form Parser analysis** page. You can view the OCR detected text, key-value pairs, tables, and generic entities extracted from the document.

   ![sample form key-value pairs in UI](/static/document-ai/docs/images/create/form-parser-kvp.png)

## Clean up

To avoid unnecessary Google Cloud charges, use the
[Google Cloud console](https://console.cloud.google.com/) to delete your processor and [project](https://console.cloud.google.com/cloud-resource-manager) if you don't need
them.

## What's next

* Review the [Processors list](/document-ai/docs/processors-list).

[Previous

arrow\_back

Extraction overview](/document-ai/docs/extracting-overview)

[Next

Custom extractor overview

arrow\_forward](/document-ai/docs/custom-extractor-overview)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/create-processor](./document-ai-docs-create-processor.md)
- [https://docs.cloud.google.com/document-ai/docs/extracting-overview](./document-ai-docs-extracting-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/manage-processor-versions](./document-ai-docs-manage-processor-versions.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/processors-list](./document-ai-docs-processors-list.md)
