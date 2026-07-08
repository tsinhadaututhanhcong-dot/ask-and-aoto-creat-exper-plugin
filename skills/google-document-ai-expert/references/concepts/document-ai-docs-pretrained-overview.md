---
type: Reference
title: "Pretrained overview  |  Document AI  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/pretrained-overview](https://docs.cloud.google.com/document-ai/docs/pretrained-overview)"
timestamp: 2026-07-06T03:34:16Z
---
# Pretrained overview  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/pretrained-overview](https://docs.cloud.google.com/document-ai/docs/pretrained-overview)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Pretrained overview Stay organized with collections Save and categorize content based on your preferences.



Document AI offers multiple products to process documents for information
for different use cases.

## Pretrained parsers

For more information, go to [Explore pretrained
processors](/document-ai/docs/processors-list#explore_pretrained_processors).

### Bank statement parser

Bank statement parser extracts key-value pairs (KVP). It can extract up
to 17 generic entities. Examples include: Account number, client name, bank name,
and table items like deposits and withdrawals. You don't specify the fields
(schema) you want to extract. Bank statement parser supports
[Enrichment](/document-ai/docs/enrichment) and
[Normalization](/document-ai/docs/normalization).

### W2 parser

W2 parser extracts from the IRS Form W2 as KVP. It can extract up
to 12 generic entities, including employee name, Social Security Number,
employer, and wages. You don't specify the fields (schema) you want
to extract. W2 parser supports [Enrichment](/document-ai/docs/enrichment).

### US passport parser

US passport parser extracts KVP. It can extract up to seven generic entities.
These include given names, family names, document ID, and
date of birth. You don't specify the fields (schema) you want to
extract. US passport parser supports [Normalization](/document-ai/docs/normalization).

### Identity document proofing parser

Identity document proofing parser predicts the validity of ID documents
using multiple signals.

* `fraud_signals_is_identity_document` detection: Predicts whether an image
  contains a recognized identity document.
* `fraud_signals_suspicious_words` detection: Predicts whether words are present
  that aren't typical on IDs.
* `fraud_signals_image_manipulation` detection: Predicts whether the image was
  altered or tampered with an image editing tool.
* `fraud_signals_online_duplicate` detection: Predicts whether the image can be
  found online (US only).

### Pay slip parser

Pay slip parser extracts KVP. It can extract up to 26 generic entities from pay
slips. These include employee name, bonus, commissions, overtime, and pay date.
You don't specify the fields (schema) you want to extract. Pay slip parser supports
[Enrichment](/document-ai/docs/enrichment) and [Normalization](/document-ai/docs/normalization).

### US driver license parser

US driver license parser extracts KVP. It can extract up to eight generic entities
from a driver license. Examples include: Given name, family name, document ID, and
expiration date. You don't specify the fields (schema) you want to
extract. US driver license parser supports [Normalization](/document-ai/docs/normalization).

### Expense parser

Expense parser extracts KVP. It can extract up to 17 generic entities from expense
reports. Examples include: Expense date, supplier name, total amount, and currency.
You don't specify the fields (schema) you want to extract. Expense parser supports
[Enrichment](/document-ai/docs/enrichment) and [Normalization](/document-ai/docs/normalization).

### Invoice Parser

Invoice Parser extracts KVP. It can extract up to 46 generic entities
from invoices. These include invoice number, supplier name, invoice amount, tax
amount, invoice date, and due date. You don't specify the fields (schema) you
want to extract. Invoice Parser supports [Enrichment](/document-ai/docs/enrichment)
and [Normalization](/document-ai/docs/normalization).

[Previous

arrow\_back

CEL dialect for document validation](/document-ai/docs/ce-cel-validation)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-07-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-07-01 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/processors-list](./document-ai-docs-processors-list.md)
