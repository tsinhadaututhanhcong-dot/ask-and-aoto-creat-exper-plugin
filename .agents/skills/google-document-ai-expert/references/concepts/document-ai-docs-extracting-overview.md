# Extraction overview  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/extracting-overview](https://docs.cloud.google.com/document-ai/docs/extracting-overview)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Extraction overview Stay organized with collections Save and categorize content based on your preferences.



Document AI offers multiple products to extract information from documents
for different use cases:

* [Form Parser](#form-parser)
* Custom extractor, which offers three different modeling types:

  + Foundation model
  + Custom model based
  + Custom template based
* [Layout Parser](#layout-parser)

## Form Parser

Form Parser extracts key-value pairs (KVP), tables, selection marks (checkboxes),
and generic fields to augment and automate extraction. It can extract up to 11
generic entities and checkboxes out of the box. You don't specify the fields (schema),
you want to extract with the Form Parser. The model detects and returns entities
of interest from each page of documents.

## Custom extractor

The custom extractor extracts entities you define in schema and offers three modeling options:
foundation model, custom model based, and custom template based. Given promising
results from foundation models with little to no training data, we recommend starting
with the foundation model as the first option and try out other options as needed.
The foundation models do zero- to few-shot prediction, based on up to 5 labeled
documents in the dataset, and fine-tuned prediction with more than 10 labeled documents in the dataset.

| **Training method** | | **Document examples** | **Document layout variation** | **Free form text or paragraphs** | **Number of training documents for production-ready quality, depending on variability** |
| --- | --- | --- | --- | --- | --- |
| Fine tune and foundation model (generative AI). | | Contract, terms of service, invoice, bank statement, bill of lading, payslips. | High to Low (preferred). | High. | Medium: 0-50+ documents. |
| Custom model. | Model. | Similar forms with layout variation across years or vendors (for example, W9). | Low to medium. | Low. | High: 10-100+ documents. |
| Template. | Tax forms with a fixed layout (for example, Forms 941 and 709). | None. | Low. | Low (3 documents). |

Because foundation models typically require fewer training documents, they're
recommended as the first option for all variable layouts.

## Layout Parser

**Note:** Layout Parser is in Public preview

Layout Parser transforms documents in various formats into structured
representations, making content like paragraphs, tables, lists, and structural
elements like headings, page headers, and footers accessible, and creating
context-aware chunks that facilitate information retrieval in a range of
generative AI and discovery apps.

[Next

Form Parser

arrow\_forward](/document-ai/docs/form-parser)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/form-parser](./document-ai-docs-form-parser.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
