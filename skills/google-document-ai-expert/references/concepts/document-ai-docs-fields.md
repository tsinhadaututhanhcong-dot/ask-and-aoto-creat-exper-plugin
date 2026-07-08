---
type: Reference
title: "Processor list  |  Document AI  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/fields](https://docs.cloud.google.com/document-ai/docs/fields)"
timestamp: 2026-07-06T03:34:16Z
---
# Processor list  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/fields](https://docs.cloud.google.com/document-ai/docs/fields)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Processor list Stay organized with collections Save and categorize content based on your preferences.



This page contains detailed information on all processors offered by
Document AI. You can see a list of all processors by solution type.

All Document AI processors adhere to the
[Data Processing and Security Terms](https://cloud.google.com/terms/data-processing-terms).

Refer to the [Managing processor versions](/document-ai/docs/manage-processor-versions)
documentation for more details. Also, specific processor limits apply in addition
to overall product [quotas and limits](/document-ai/quotas).

## Digitize text

### Enterprise Document OCR (Optical Character Recognition)

|  |  |
| --- | --- |
| **Description** | Identify and extract text in different types of documents.  This processor allows you to identify and extract text, including handwritten text, from documents in more than 200 languages. The processor also uses machine learning to perform a quality assessment of a document based on the readability of its content. |
| **Category** | Digitize |
| **Functions** | OCR, Quality Analysis |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `OCR_PROCESSOR` |
| **Supported languages** | Full list of languages  | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | Afrikaans | `af` | `Latn` |  | | Albanian | `sq` | `Latn` |  | | Arabic | `ar` | `Arab` |  | | Armenian | `hy` | `Armn` |  | | Belarusian | `be` | `Cyrl` |  | | Bangla | `bn` | `Beng` |  | | Bengali | `bn` | `Beng` |  | | Bulgarian | `bg` | `Cyrl` |  | | Catalan | `ca` | `Latn` |  | | Chinese | `zh` | `Hani` |  | | Croatian | `hr` | `Latn` |  | | Czech | `cs` | `Latn` |  | | Danish | `da` | `Latn` |  | | Dutch | `nl` | `Latn` |  | | English | `en` | `Latn` |  | | Estonian | `et` | `Latn` |  | | Filipino | `fil` | `Latn` |  | | Finnish | `fi` | `Latn` |  | | French | `fr` | `Latn` |  | | German | `de` | `Latn` |  | | Greek | `el` | `Grek` |  | | Gujarati | `gu` | `Gujr` |  | | Hebrew | `iw` | `Hebr` |  | | Hindi | `hi` | `Deva` |  | | Hungarian | `hu` | `Latn` |  | | Icelandic | `is` | `Latn` |  | | Indonesian | `id` | `Latn` |  | | Italian | `it` | `Latn` |  | | Japanese | `ja` | `Jpan` |  | | Kannada | `kn` | `Knda` |  | | Khmer | `km` | `Khmr` |  | | Korean | `ko` | `Kore` |  | | Lao | `lo` | `Laoo` |  | | Latvian | `lv` | `Latn` |  | | Lithuanian | `lt` | `Latn` |  | | Macedonian | `mk` | `Cyrl` |  | | Malay | `ms` | `Latn` |  | | Malayalam | `ml` | `Mlym` |  | | Marathi | `mr` | `Deva` |  | | Nepali | `ne` | `Deva` |  | | Norwegian | `no` | `Latn` |  | | Persian | `fa` | `Arab` |  | | Polish | `pl` | `Latn` |  | | Portuguese (Portugal & Brazil) | `pt` | `Latn` |  | | Punjabi | `pa` | `Guru` |  | | Romanian | `ro` | `Latn` |  | | Russian | `ru` | `Cyrl` |  | | Serbian | `sr` | `Cyrl` |  | | Slovak | `sk` | `Latn` |  | | Slovenian | `sl` | `Latn` |  | | Spanish | `es` | `Latn` |  | | Swedish | `sv` | `Latn` |  | | Tagalog | `tl` | `Latn` |  | | Tamil | `ta` | `Taml` |  | | Telugu | `te` | `Telu` |  | | Thai | `th` | `Thai` |  | | Turkish | `tr` | `Latn` |  | | Ukrainian | `uk` | `Cyrl` |  | | Vietnamese | `vi` | `Latn` |  | | Yiddish | `yi` | `Hebr` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-ocr-v1.2-2022-11-10` | Stable | GA | Frozen model version of v1.0: Model files, configurations, and binaries of a version snapshot frozen in a container image for up to 18 months. | | `pretrained-ocr-v2.0-2023-06-02` | Stable | GA | Production-ready model specialized for document use cases. Includes access to all OCR add-ons. | | `pretrained-ocr-v2.1-2024-08-07` | Stable | GA | The main areas of improvement for v2.1 are: better printed text recognition, more precise checkbox detection and more accurate reading order. | | `pretrained-ocr-v2.1.1-2025-01-31` | Release candidate | Public Preview | v2.1.1 is similar to V2.1, and is available in all regions except: `US`, `EU`, and `asia-southeast1`. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 500 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/OCR_PROCESSOR/Winnie_the_Pooh_3_Pages.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_doc-ocr) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-south1` * `asia-southeast1` * `australia-southeast1` * `eu` * `europe-west2` * `europe-west3` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |
| **More information** | [Enterprise Document OCR](/document-ai/docs/document-ocr) |

  

## Extract entities from documents

Refer to [Sample datasets](/document-ai/docs/create-dataset#sample-datasets)
for sample labeled and unlabeled datasets to use for training.

### Custom Extractor

|  |  |
| --- | --- |
| **Description** | Extract fields from documents using generative AI or custom models; fine-tune models to accurately extract data from your documents. |
| **Category** | Extract |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `CUSTOM_EXTRACTION_PROCESSOR` |
| **Notes** | * If using generative AI for extraction, then:   + Only the English language is officially supported.   + Region availability is in the `US`, `EU`, `northamerica-northeast1` and `asia-southeast1`. |
| **Supported languages** | Full list of languages  | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | Afrikaans | `af` | `Latn` |  | | Arabic | `ar` | `Arab` |  | | Azerbaijani | `az` | `Latn` |  | | Azerbaijani (Cyrillic) | `az-Cyrl` | `Cyrl` |  | | Belarusian | `be` | `Cyrl` |  | | Bulgarian | `bg` | `Cyrl` |  | | Bosnian | `bs` | `Latn` |  | | Catalan | `ca` | `Latn` |  | | Cebuano | `ceb` | `Latn` |  | | Czech | `cs` | `Latn` |  | | Welsh | `cy` | `Latn` |  | | Danish | `da` | `Latn` |  | | German | `de` | `Latn` |  | | Greek | `el` | `Grek` |  | | English | `en` | `Latn` |  | | Esperanto | `eo` | `Latn` |  | | Spanish | `es` | `Latn` |  | | Estonian | `et` | `Latn` |  | | Basque | `eu` | `Latn` |  | | Persian | `fa` | `Arab` |  | | Finnish | `fi` | `Latn` |  | | Filipino | `fil` | `Latn` |  | | French | `fr` | `Latn` |  | | Irish | `ga` | `Latn` |  | | Galician | `gl` | `Latn` |  | | Hindi | `hi` | `Deva` |  | | Croatian | `hr` | `Latn` |  | | Haitian Creole | `ht` | `Latn` |  | | Hungarian | `hu` | `Latn` |  | | Indonesian | `id` | `Latn` |  | | Icelandic | `is` | `Latn` |  | | Italian | `it` | `Latn` |  | | Hebrew | `iw` | `Hebr` |  | | Japanese | `ja` | `Jpan` |  | | Javanese | `jv` | `Latn` |  | | Kazakh | `kk` | `Cyrl` |  | | Korean | `ko` | `Kore` |  | | Kyrgyz | `ky` | `Cyrl` |  | | Latin | `la` | `Latn` |  | | Lithuanian | `lt` | `Latn` |  | | Latvian | `lv` | `Latn` |  | | Macedonian | `mk` | `Cyrl` |  | | Mongolian | `mn` | `Cyrl` |  | | Marathi | `mr` | `Deva` |  | | Malay | `ms` | `Latn` |  | | Maltese | `mt` | `Latn` |  | | Nepali | `ne` | `Deva` |  | | Dutch | `nl` | `Latn` |  | | Norwegian | `no` | `Latn` |  | | Polish | `pl` | `Latn` |  | | Pashto | `ps` | `Arab` |  | | Portuguese (Portugal & Brazil) | `pt` | `Latn` |  | | Romanian | `ro` | `Latn` |  | | Russian | `ru` | `Cyrl` |  | | Russian (Petrine Orthography) | `ru-PETR1708` | `Cyrl` |  | | Sanskrit | `sa` | `Deva` |  | | Slovak | `sk` | `Latn` |  | | Slovenian | `sl` | `Latn` |  | | Albanian | `sq` | `Latn` |  | | Serbian | `sr` | `Cyrl` |  | | Swedish | `sv` | `Latn` |  | | Swahili | `sw` | `Latn` |  | | Tagalog | `tl` | `Latn` |  | | Turkish | `tr` | `Latn` |  | | Ukrainian | `uk` | `Cyrl` |  | | Urdu | `ur` | `Arab` |  | | Uzbek | `uz` | `Latn` |  | | Uzbek (Cyrillic) | `uz-Cyrl` | `Cyrl` |  | | Vietnamese | `vi` | `Latn` |  | | Yiddish | `yi` | `Hebr` |  | | Chinese simplified | `zh-Hans` | `Hani` |  | | Chinese traditional | `zh-Hant` | `Hani` |  | | Zulu | `zu` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-foundation-model-v1.5-2025-05-05` | Stable | GA | Production-ready candidate powered by Gemini 2.5 Flash LLM. Recommended for those who want to experiment with newer models. | | `pretrained-foundation-model-v1.5-pro-2025-06-20` | Stable | GA | Production-ready model powered by the Gemini 2.5 Pro LLM. Supports a quota of up to 30 pages per minute for online process requests. This model has improved quality compared to v1.5, and may have a higher latency. | | `pretrained-foundation-model-v1.5.1-2025-08-07` | Release candidate | Public Preview | Public preview model powered by the Gemini 2.5 Flash LLM. This model has the same features as v1.5, and has improved adaptive few-shot learning. | | `pretrained-foundation-model-v1.6-pro-2025-12-01` | Release candidate | Public Preview | Preview model powered by the Gemini 3 Pro LLM. **Note:** This processor version uses the Vertex AI Gemini global endpoint and is not compliant with [Data Residency (DMZ)](/vertex-ai/generative-ai/docs/learn/data-residency) standards. For example, requests in US and EU endpoints might route to anywhere globally. | | `pretrained-foundation-model-v1.6-2026-01-13` | Release candidate | Public Preview | Preview model powered by the Gemini 3 Flash LLM. **Note:** This processor version uses the Vertex AI Gemini global endpoint and is not compliant with [Data Residency (DMZ)](/vertex-ai/generative-ai/docs/learn/data-residency) standards. For example, requests in US and EU endpoints might route to anywhere globally. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 200 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Normalized data types** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment), and [Create dataset](/document-ai/docs/create-dataset#choose_label_attributes) pages.  Full list of normalized data types  * `dateTime as STRING` * `currency as STRING` * `money as google.type.Money` * `number as FLOAT or INTEGER` |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/CUSTOM_EXTRACTION_PROCESSOR/us_008.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_cde) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-south1` * `asia-southeast1` * `australia-southeast1` * `eu` * `europe-west2` * `europe-west3` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |
| **More information** | [Custom Extractor](/document-ai/docs/custom-extractor-overview) |

  

### Form Parser

|  |  |
| --- | --- |
| **Description** | Extract general key-value pairs (entity and checkbox), tables, and generic entities from documents in addition to OCR text.  This processor applies advanced machine learning technologies to extract key-value pairs, checkboxes, and tables from documents more than 200 languages. This processor also leverages deep learning models to extract 11 generic entities that are common in various document types. |
| **Category** | Extract |
| **Functions** | OCR, Form Parsing, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `FORM_PARSER_PROCESSOR` |
| **Supported languages** | Full list of languages  | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | Afrikaans | `af` | `Latn` |  | | Albanian | `sq` | `Latn` |  | | Arabic | `ar` | `Arab` |  | | Belarusian | `be` | `Cyrl` |  | | Catalan | `ca` | `Latn` |  | | Chinese | `zh` | `Hani` |  | | Croatian | `hr` | `Latn` |  | | Czech | `cs` | `Latn` |  | | Danish | `da` | `Latn` |  | | Dutch | `nl` | `Latn` |  | | English | `en` | `Latn` |  | | Estonian | `et` | `Latn` |  | | Filipino | `fil` | `Latn` |  | | Finnish | `fi` | `Latn` |  | | French | `fr` | `Latn` |  | | German | `de` | `Latn` |  | | Hebrew | `iw` | `Hebr` |  | | Hindi | `hi` | `Deva` |  | | Hungarian | `hu` | `Latn` |  | | Icelandic | `is` | `Latn` |  | | Indonesian | `id` | `Latn` |  | | Italian | `it` | `Latn` |  | | Japanese | `ja` | `Jpan` |  | | Korean | `ko` | `Kore` |  | | Latvian | `lv` | `Latn` |  | | Lithuanian | `lt` | `Latn` |  | | Macedonian | `mk` | `Cyrl` |  | | Malay | `ms` | `Latn` |  | | Marathi | `mr` | `Deva` |  | | Nepali | `ne` | `Deva` |  | | Norwegian | `no` | `Latn` |  | | Persian | `fa` | `Arab` |  | | Polish | `pl` | `Latn` |  | | Portuguese (Portugal & Brazil) | `pt` | `Latn` |  | | Romanian | `ro` | `Latn` |  | | Russian | `ru` | `Cyrl` |  | | Serbian | `sr` | `Cyrl` |  | | Slovak | `sk` | `Latn` |  | | Slovenian | `sl` | `Latn` |  | | Spanish | `es` | `Latn` |  | | Swedish | `sv` | `Latn` |  | | Tagalog | `tl` | `Latn` |  | | Turkish | `tr` | `Latn` |  | | Ukrainian | `uk` | `Cyrl` |  | | Vietnamese | `vi` | `Latn` |  | | Yiddish | `yi` | `Hebr` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Additional fields detected | Description | | --- | --- | --- | --- | --- | | `pretrained-form-parser-v1.0-2020-09-23` | Stable | GA | None | Legacy version. For best quality and full feature set, use the Form Parser v2.0. | | `pretrained-form-parser-v2.0-2022-11-10` | Stable | GA | Show fields  * `email` * `phone` * `url` * `date_time` * `address` * `person` * `organization` * `quantity` * `price` * `id` * `page_number` | Recommended version. Supports generic entities and includes upgraded table, KVP, and checkbox model, as well as more than 200 languages. | | `pretrained-form-parser-v2.1-2023-06-26` | Release Candidate | Public Preview | None | Public Preview version. Same model as v2.0 with native text extraction from digital PDF files enabled. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 100 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/FORM_PARSER_PROCESSOR/intake-form.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_form-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-south1` * `asia-southeast1` * `australia-southeast1` * `eu` * `europe-west2` * `europe-west3` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |
| **More information** | [Form Parser](/document-ai/docs/form-parser) |

  

### Layout Parser

|  |  |
| --- | --- |
| **Description** | Extracts document content elements (text, tables, and lists) and creates context-aware chunks.  Layout Parser extracts document content elements like text, tables, and lists, and creates context-aware chunks that facilitate information retrieval in generative AI and discovery applications. |
| **Category** | Extract |
| **Functions** | Layout Parsing, Document Chunking |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `LAYOUT_PARSER_PROCESSOR` |
| **Notes** | * This parser supports PDF, HTML, DOCX, PPTX, and XLSX/XLSM files. |
| **Supported languages** | Full list of languages  | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | Afrikaans | `af` | `Latn` |  | | Albanian | `sq` | `Latn` |  | | Arabic | `ar` | `Arab` |  | | Armenian | `hy` | `Armn` |  | | Belarusian | `be` | `Cyrl` |  | | Bangla | `bn` | `Beng` |  | | Bengali | `bn` | `Beng` |  | | Bulgarian | `bg` | `Cyrl` |  | | Catalan | `ca` | `Latn` |  | | Chinese | `zh` | `Hani` |  | | Croatian | `hr` | `Latn` |  | | Czech | `cs` | `Latn` |  | | Danish | `da` | `Latn` |  | | Dutch | `nl` | `Latn` |  | | English | `en` | `Latn` |  | | Estonian | `et` | `Latn` |  | | Filipino | `fil` | `Latn` |  | | Finnish | `fi` | `Latn` |  | | French | `fr` | `Latn` |  | | German | `de` | `Latn` |  | | Greek | `el` | `Grek` |  | | Gujarati | `gu` | `Gujr` |  | | Hebrew | `iw` | `Hebr` |  | | Hindi | `hi` | `Deva` |  | | Hungarian | `hu` | `Latn` |  | | Icelandic | `is` | `Latn` |  | | Indonesian | `id` | `Latn` |  | | Italian | `it` | `Latn` |  | | Japanese | `ja` | `Jpan` |  | | Kannada | `kn` | `Knda` |  | | Khmer | `km` | `Khmr` |  | | Korean | `ko` | `Kore` |  | | Lao | `lo` | `Laoo` |  | | Latvian | `lv` | `Latn` |  | | Lithuanian | `lt` | `Latn` |  | | Macedonian | `mk` | `Cyrl` |  | | Malay | `ms` | `Latn` |  | | Malayalam | `ml` | `Mlym` |  | | Marathi | `mr` | `Deva` |  | | Nepali | `ne` | `Deva` |  | | Norwegian | `no` | `Latn` |  | | Persian | `fa` | `Arab` |  | | Polish | `pl` | `Latn` |  | | Portuguese (Portugal & Brazil) | `pt` | `Latn` |  | | Punjabi | `pa` | `Guru` |  | | Romanian | `ro` | `Latn` |  | | Russian | `ru` | `Cyrl` |  | | Serbian | `sr` | `Cyrl` |  | | Slovak | `sk` | `Latn` |  | | Slovenian | `sl` | `Latn` |  | | Spanish | `es` | `Latn` |  | | Swedish | `sv` | `Latn` |  | | Tagalog | `tl` | `Latn` |  | | Tamil | `ta` | `Taml` |  | | Telugu | `te` | `Telu` |  | | Thai | `th` | `Thai` |  | | Turkish | `tr` | `Latn` |  | | Ukrainian | `uk` | `Cyrl` |  | | Vietnamese | `vi` | `Latn` |  | | Yiddish | `yi` | `Hebr` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-layout-parser-v1.0-2024-06-03` | Stable | GA | General availability version for document layout analysis. This is the default pre-trained processor version. | | `pretrained-layout-parser-v1.5-2025-08-25` | Release Candidate | Public Preview | Preview version powered by Gemini 2.5 Flash LLM for better layout analysis on PDF files. Recommended for those who want to experiment with new versions. **Note:** If it's used for non-PDF files, it will have the same behavior as the stable `pretrained-layout-parser-v1.0-2024-06-03`. | | `pretrained-layout-parser-v1.5-pro-2025-08-25` | Release Candidate | Public Preview | Preview version powered by Gemini 2.5 Pro LLM for better layout analysis on PDF files. v1.5-pro has higher latency than v1.5. **Note:** If it's used for non-PDF files, it will have the same behavior as the stable `pretrained-layout-parser-v1.0-2024-06-03`. | | `pretrained-layout-parser-v1.6-pro-2025-12-01` | Release Candidate | Public Preview | Preview version powered by Gemini 3.0 Pro LLM. **Note:**This processor version uses the Vertex AI Gemini global endpoint and is not compliant with [Data Residency (DMZ)](/vertex-ai/generative-ai/docs/learn/data-residency) standards. For example, requests in US and EU endpoints might route to anywhere globally. | | `pretrained-layout-parser-v1.6-2026-01-13` | Release Candidate | Public Preview | Preview version powered by Gemini 3.0 Flash LLM. **Note:**This processor version uses the Vertex AI Gemini global endpoint and is not compliant with [Data Residency (DMZ)](/vertex-ai/generative-ai/docs/learn/data-residency) standards. For example, requests in US and EU endpoints might route to anywhere globally. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 500 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/LAYOUT_PARSER_PROCESSOR/Winnie_the_Pooh.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_layout-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `eu` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |
| **More information** | [Layout Parser](/document-ai/docs/layout-parse-chunk) |

  

## Explore pretrained processors

### Bank Statement Parser

|  |  |
| --- | --- |
| **Description** | Extract from bank statements including name, account, transactions, etc. |
| **Category** | Pretrained |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `BANK_STATEMENT_PROCESSOR` |
| **Notes** | * If a page of a multi-page input file is the correct document type and one of the supported versions, the processor performs entity extraction on the first supported document. If the processor doesn't find any applicable documents in the input file, the processor returns an error message. |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-bankstatement-v1.0-2021-08-08` | Stable | GA |  | | `pretrained-bankstatement-v1.1-2021-08-13` | Stable | GA |  | | `pretrained-bankstatement-v2.0-2021-12-10` | Stable | GA |  | | `pretrained-bankstatement-v3.0-2022-05-16` | Stable | GA | This version assumes that the input file contains a single bank statement. Unlike the default version, this version does not check the input file for bank statements and will not return an error if no bank statements are found. | | `pretrained-bankstatement-v4.0-2023-07-31` | Release Candidate | Public Preview |  | | `pretrained-bankstatement-v5.0-2023-12-06` | Stable | GA |  |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 30 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `account_number` * `account_type` * `bank_address` * `bank_name` * `client_address` * `client_name` * `ending_balance` * `starting_balance` * `statement_date` * `statement_end_date` * `statement_start_date` * `table_item`  + `table_item/transaction_deposit` + `table_item/transaction_deposit_date` + `table_item/transaction_deposit_description` + `table_item/transaction_withdrawal` + `table_item/transaction_withdrawal_date` + `table_item/transaction_withdrawal_description` |
| **Enriched fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of enriched fields  * `bank_address` * `bank_name` |
| **Normalized fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of normalized fields  * `ending_balance` * `starting_balance` * `statement_date` * `statement_end_date` * `statement_start_date` * `table_item/transaction_deposit` * `table_item/transaction_deposit_date` * `table_item/transaction_withdrawal` * `table_item/transaction_withdrawal_date` |
| **Uptraining** |  |
| **Labeling Instructions** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/labeling-instructions/pretrained-bankstatement-v3.0-2022-05-16.pdf) |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/BANK_STATEMENT_PROCESSOR/lending_bankstatement.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_bank-statement-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `eu` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

### W2 Parser

|  |  |
| --- | --- |
| **Description** | Extract from Form W2, including employee, employer, wages, etc. |
| **Category** | Pretrained |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `FORM_W2_PROCESSOR` |
| **Notes** | * If a page of a multi-page input file is the correct document type and one of the supported versions, the processor performs entity extraction on the first supported document. If the processor doesn't find any applicable documents in the input file, the processor returns an error message. |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Supported form/versions** | * 2020 (standard and customized versions) * 2019 (standard and customized versions) * 2018 (standard and customized versions) |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Additional fields detected | Description | | --- | --- | --- | --- | --- | | `pretrained-w2-v1.0-2020-10-01` | Stable | GA | None |  | | `pretrained-w2-v1.1-2022-01-27` | Stable | GA | None |  | | `pretrained-w2-v1.2-2022-01-28` | Stable | GA | Show fields  * `AllocatedTips` * `ControlNumber` * `DependentCareBenefits` * `EIN` * `EmployeeAddress` * `EmployeeName` * `EmployerNameAndAddress` * `EmployerStateIdNumber_Line1` * `FederalIncomeTaxWithheld` * `FormYear` * `LocalIncomeTax_Line1` * `LocalityName_Line1` * `LocalWagesTipsEtc_Line1` * `MedicareTaxWithheld` * `MedicareWagesAndTips` * `NonqualifiedPlans` * `SocialSecurityTaxWithheld` * `SocialSecurityTips` * `SocialSecurityWages` * `SSN` * `State_Line1` * `StateIncomeTax_Line1` * `StateWagesTipsEtc_Line1` * `WagesTipsOtherCompensation` | Quality improvements and supporting new fields; does not include splitter. | | `pretrained-w2-v2.0-2022-03-30` | Release Candidate | Public Preview | Show fields  * `AllocatedTips` * `ControlNumber` * `DependentCareBenefits` * `EIN` * `EmployeeAddress_AdditionalStreetAddressOrPostalBox` * `EmployeeAddress_City` * `EmployeeAddress_State` * `EmployeeAddress_StreetAddressOrPostalBox` * `EmployeeAddress_Zip` * `EmployeeName_FirstName` * `EmployeeName_LastName` * `EmployeeName_MiddleNameOrInitial` * `EmployerAddress_AdditionalStreetAddressOrPostalBox` * `EmployerAddress_City` * `EmployerAddress_State` * `EmployerAddress_StreetAddressOrPostalBox` * `EmployerAddress_Zip` * `EmployerName` * `EmployerStateIdNumber_Line1` * `FederalIncomeTaxWithheld` * `FormYear` * `LocalIncomeTax_Line1` * `LocalWagesTipsEtc_Line1` * `LocalityName_Line1` * `MedicareTaxWithheld` * `MedicareWagesAndTips` * `NonqualifiedPlans` * `SSN` * `SocialSecurityTaxWithheld` * `SocialSecurityTips` * `SocialSecurityWages` * `StateIncomeTax_Line1` * `StateWagesTipsEtc_Line1` * `State_Line1` * `WagesTipsOtherCompensation` * `a_Code` * `a_Value` * `b_Code` * `b_Value` * `c_Code` * `c_Value` * `d_Code` * `d_Value` | Quality improvements and support for box 12 fields and fine-grained predictions of `EmployeeName`, `EmployeeAddress`, and `EmployerNameAndAddress`, all of which are no longer part of the output and are replaced with additional fields. | | `pretrained-w2-v2.1-2022-06-08` | Stable | GA | Show fields  * `AllocatedTips` * `ControlNumber` * `DependentCareBenefits` * `EIN` * `EmployeeAddress_AdditionalStreetAddressOrPostalBox` * `EmployeeAddress_City` * `EmployeeAddress_State` * `EmployeeAddress_StreetAddressOrPostalBox` * `EmployeeAddress_Zip` * `EmployeeName_FirstName` * `EmployeeName_LastName` * `EmployeeName_MiddleNameOrInitial` * `EmployeeName_Suffix` * `EmployerAddress_AdditionalStreetAddressOrPostalBox` * `EmployerAddress_City` * `EmployerAddress_State` * `EmployerAddress_StreetAddressOrPostalBox` * `EmployerAddress_Zip` * `EmployerName` * `EmployerStateIdNumber_Line1` * `FederalIncomeTaxWithheld` * `FormYear` * `LocalIncomeTax_Line1` * `LocalWagesTipsEtc_Line1` * `LocalityName_Line1` * `MedicareTaxWithheld` * `MedicareWagesAndTips` * `NonqualifiedPlans` * `SSN` * `SocialSecurityTaxWithheld` * `SocialSecurityTips` * `SocialSecurityWages` * `StateIncomeTax_Line1` * `StateWagesTipsEtc_Line1` * `State_Line1` * `WagesTipsOtherCompensation` * `a_Code` * `a_Value` * `b_Code` * `b_Value` * `c_Code` * `c_Value` * `d_Code` * `d_Value` | Similar to version `pretrained-w2-v2.0-2022-03-30` with further quality enhancements and introducing one more entity `EmployeeName_Suffix`. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 15 | | Maximum pages (imageless mode online/synchronous requests): | 15 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `ControlNumber` * `EIN` * `EmployeeAddress` * `EmployeeName` * `EmployerNameAndAddress` * `FederalIncomeTaxWithheld` * `MedicareTaxWithheld` * `MedicareWagesAndTips` * `SSN` * `SocialSecurityTaxWithheld` * `SocialSecurityWages` * `WagesTipsOtherCompensation` |
| **Enriched fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of enriched fields  * `EmployerNameAndAddress` * `EIN` |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/FORM_W2_PROCESSOR/2020FormW-2.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_w2-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `eu` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

### Identity Document Proofing Parser

|  |  |
| --- | --- |
| **Description** | Predict the validity of ID documents using multiple signals.  Identity Document Proofing Processor is designed to help predict the validity of ID documents with four different signals.  The processor currently returns information from the following signals:   * `fraud_signals_is_identity_document` detection: Predicts whether an image contains a recognized identity document. * `fraud_signals_suspicious_words` detection: Predicts whether words are present that aren't typical on IDs. * `fraud_signals_image_manipulation` detection: Predicts whether the image was altered or tampered with an image editing tool. * `fraud_signals_online_duplicate` detection: Predicts whether the image can be found online (US only). |
| **Category** | Pretrained |
| **Functions** | OCR, Quality Analysis |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `ID_PROOFING_PROCESSOR` |
| **Notes** | * The Online Duplicate Detection feature is currently processed in US data centers. Regional and multi-regional support is unavailable for this feature outside of the US. * This processor is supported by algorithms that are updated more frequently than new processor versions are released. For this reason, the processor might return different outputs over time even when using the same processor version. For example, the Online Duplicate Detection system monitors images present on the web. The system's behavior can then change more quickly than can be tracked in processor versions. * Refer to notes on Responsible AI[[†]](#footnote2) and Human review.[[‡]](#footnote3) |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Supported form/versions** | * Support for US passports, passcards and driver's licenses. |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Additional fields detected | Description | | --- | --- | --- | --- | --- | | `pretrained-id-proofing-v1.0-2022-10-03` | Stable | GA | None |  | | `pretrained-id-proofing-v1.1-2023-05-18` | Release Candidate | Public Preview | Show fields  * `fraud_signals_photocopy_detection` | Additional photocopy detection signal | | `pretrained-id-proofing-v1.2-2023-10-04` | Release Candidate | Public Preview | Show fields  * `fraud_signals_photocopy_detection` |  |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 2 | | Maximum pages (batch/offline/asynchronous requests): | 2 | | Maximum pages (imageless mode online/synchronous requests): | 2 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `fraud_signals_is_identity_document` * `fraud_signals_suspicious_words` * `evidence_suspicious_word` * `evidence_inconclusive_suspicious_word` * `fraud_signals_image_manipulation` * `fraud_signals_online_duplicate (US only)` * `fraud_signals_photocopy_detection` * `evidence_hostname (US only)` * `evidence_thumbnail_url (US only)` |
| **Normalized fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of normalized fields  * `fraud_signals_image_manipulation` * `fraud_signals_online_duplicate (US only)` * `fraud_signals_is_identity_document` * `fraud_signals_suspicious_words` |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/ID_PROOFING_PROCESSOR/identity_fraud_two_pages_id.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_id-proofing-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `eu` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

### Pay Slip Parser

|  |  |
| --- | --- |
| **Description** | Extract from pay slips, including name, business, amounts, etc. |
| **Category** | Pretrained |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `PAYSTUB_PROCESSOR` |
| **Notes** | * If the multi-page input document contains more than one valid pay slips, the processor extracts entities from only the first valid pay slip. If no pay slips are found in the input file, the processor returns an error message. |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Additional fields detected | Description | | --- | --- | --- | --- | --- | | `pretrained-paystub-v1.0-2021-03-19` | Stable | GA | None |  | | `pretrained-paystub-v1.1-2021-08-13` | Stable | GA | Show fields  * `net_pay` * `net_pay_ytd` * `employee_account_number` | Quality improvement and new fields support; | | `pretrained-paystub-v1.2-2021-12-10` | Stable | GA | None |  | | `pretrained-paystub-v2.0-2022-05-17` | Release Candidate | Public Preview | Show fields  * `deduction_item` * `deduction_item/deduction_type` * `deduction_item/deduction_this_period` * `deduction_item/deduction_ytd` * `direct_deposit_item` * `direct_deposit_item/direct_deposit` * `direct_deposit_item/employee_account_number` * `earning_item` * `earning_item/earning_type` * `earning_item/earning_rate` * `earning_item/earning_hours` * `earning_item/earning_this_period` * `earning_item/earning_ytd` * `page_number` * `tax_item` * `tax_item/tax_type` * `tax_item/tax_this_period` * `tax_item/tax_ytd` * `federal_additional_tax` * `federal_allowance` * `federal_marital_status` * `state_additional_tax` * `state_allowance` * `state_marital_status` | This version assumes that the input file contains a single pay slip. Unlike the default version, this version does not check the input file for pay slips and will not return an error if no pay slips are found. Quality improvement, new fields support and new schema. Bonus, Commissions, Holiday, Overtime, Regular Pay and Vacation are now part of earning\_item/earning\_this\_period, and their year-to-date versions are in earning\_item/earning\_ytd. Direct Deposit and Employee Account Number are now nested under direct\_deposit\_item.  Async page limit is 10. | | `pretrained-paystub-v2.0-2022-07-22` | Stable | GA | None | Quality improvement and uptraining enhancements. | | `pretrained-paystub-v3.0-2023-12-06` | Stable | GA | None |  |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 50 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `bonus` * `bonus_ytd` * `commissions` * `commissions_ytd` * `direct_deposit` * `employee_account_number (Added in "pretrained-paystub-v1.1-2021-08-13")` * `employee_address` * `employee_name` * `employer_address` * `employer_name` * `end_date` * `gross_earnings` * `gross_earnings_ytd` * `holiday` * `holiday_ytd` * `net_pay (Added in "pretrained-paystub-v1.1-2021-08-13")` * `net_pay_ytd (Added in "pretrained-paystub-v1.1-2021-08-13")` * `overtime` * `overtime_ytd` * `pay_date` * `regular_pay` * `regular_pay_ytd` * `ssn` * `start_date` * `vacation` * `vacation_ytd` |
| **Enriched fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of enriched fields  * `employer_address` * `employer_name` |
| **Normalized fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of normalized fields  * `bonus` * `bonus_ytd` * `commissions` * `commissions_ytd` * `direct_deposit` * `end_date` * `gross_earnings` * `gross_earnings_ytd` * `holiday` * `holiday_ytd` * `net_pay` * `net_pay_ytd` * `overtime` * `overtime_ytd` * `pay_date` * `regular_pay` * `regular_pay_ytd` * `start_date` * `vacation` * `vacation_ytd` |
| **Uptraining** |  |
| **Labeling Instructions** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/labeling-instructions/pretrained-paystub-v2.0-2022-07-22.pdf) |
| **[Supported regions](/document-ai/docs/regions)** | * `eu` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

### US Driver License Parser

|  |  |
| --- | --- |
| **Description** | Extract fields such as names, document ID, date of birth, etc. |
| **Category** | Pretrained |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `US_DRIVER_LICENSE_PROCESSOR` |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Supported form/versions** | * Supports all 50 States and D.C. |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-us-driver-license-v1.0-2021-06-14` | Stable | GA |  |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 2 | | Maximum pages (batch/offline/asynchronous requests): | 2 | | Maximum pages (imageless mode online/synchronous requests): | 2 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `Family Name` * `Given Names` * `Document Id` * `Expiration Date` * `Date Of Birth` * `Issue Date` * `Address` * `Portrait` |
| **Normalized fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of normalized fields  * `Date Of Birth` * `Expiration Date` * `Issue Date` |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/US_DRIVER_LICENSE_PROCESSOR/dl3.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_us-driver-license-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `eu` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

### Expense Parser

|  |  |
| --- | --- |
| **Description** | Extract text and values from expense documents such as expense date, supplier name, total amount, and currency. |
| **Category** | Pretrained |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `EXPENSE_PROCESSOR` |
| **Supported languages** | Full list of languages  | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | German | `de` | `Latn` |  | | English | `en` | `Latn` |  | | Spanish | `es` | `Latn` |  | | French | `fr` | `Latn` |  | | Japanese | `ja` | `Jpan` |  | | Dutch | `nl` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Additional fields detected | Additional languages supported | Description | | --- | --- | --- | --- | --- | --- | | `pretrained-expense-v1.1-2021-04-09` | Stable | GA | None | None | Fine-tuned version of the v1.0 processor. Launched in April 2021. | | `pretrained-expense-v1.3.2-2024-09-11` | Release Candidate | Public Preview | Show fields  * `credit_card_last_four_digits` * `line_item/quantity` * `payment_type` | * `ja`: Japanese | A fine-tuned upgrade to v1.3 with an enhanced underlying vision model. | | `pretrained-expense-v1.4-2022-11-18` | Stable | GA | Show fields  * `traveler_name` * `reservation_id` * `line_item/transaction_date` | * `ja`: Japanese * `it`: Italian * `pt`: Portuguese (Portugal & Brazil) | Performance improvements and support for uptraining. Maximum pages (online/synchronous requests) limit has been increased to 15. **Note:** Discontinued in the United States (US) and European Union (EU) starting April 30, 2025. | | `pretrained-expense-v1.4.2-2024-09-12` | Stable | GA | Show fields  * `traveler_name` * `reservation_id` * `line_item/transaction_date` | * `ja`: Japanese * `it`: Italian * `pt`: Portuguese (Portugal & Brazil) | An upgrade to v1.4 with an enhanced underlying vision model. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 10 | | Maximum pages (batch/offline/asynchronous requests): | 10 | | Maximum pages (imageless mode online/synchronous requests): | 10 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `credit_card_last_four_digits` * `currency` * `end_date` * `net_amount` * `payment_type` * `purchase_time` * `receipt_date` * `start_date` * `supplier_address` * `supplier_city` * `supplier_name` * `tip_amount` * `total_amount` * `total_tax_amount` * `line_item`  + `line_item/amount` + `line_item/description` + `line_item/product_code` |
| **Enriched fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of enriched fields  * `supplier_address` * `supplier_name` * `supplier_phone` |
| **Normalized fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of normalized fields  * `currency` * `total_amount` * `total_tax_amount` * `net_amount` * `receipt_date` * `purchase_time` * `start_date` * `end_date` * `line_item/amount` * `line_item/payment_date` * `line_item/payment_amount` |
| **Uptraining** |  |
| **Labeling Instructions** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/labeling-instructions/pretrained-expense-v1.3-2022-07-15.pdf) |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/EXPENSE_PROCESSOR/office-depot-redacted.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_expense-parser) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-southeast1` * `australia-southeast1` * `eu` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

### Invoice Parser

|  |  |
| --- | --- |
| **Description** | Extract text and values from invoices such as invoice number, supplier name, invoice amount, tax amount, invoice date, due date.  The invoice Parser extracts both header and line item fields, such as invoice number, supplier name, invoice amount, tax amount, invoice date, due date, and line item amounts. |
| **Category** | Pretrained |
| **Functions** | OCR, Entity Extraction |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `INVOICE_PROCESSOR` |
| **Supported languages** | Full list of languages  | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | German | `de` | `Latn` |  | | English | `en` | `Latn` |  | | Spanish | `es` | `Latn` |  | | Estonian | `et` | `Latn` |  | | French | `fr` | `Latn` |  | | Italian | `it` | `Latn` |  | | Latvian | `lv` | `Latn` |  | | Lithuanian | `lt` | `Latn` |  | | Dutch | `nl` | `Latn` |  | | Portuguese (Portugal & Brazil) | `pt` | `Latn` |  | | Romanian | `ro` | `Latn` |  | | Swedish | `sv` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Additional languages supported | Description | | --- | --- | --- | --- | --- | | `pretrained-invoice-v1.1-2021-04-09` | Stable | GA | None |  | | `pretrained-invoice-v1.2-2022-02-18` | Stable | GA | None | Deprecation is planned soon. | | `pretrained-invoice-v1.3-2022-07-15` | Stable | GA | * `it`: Italian * `pt`: Portuguese (Portugal & Brazil) * `ro`: Romanian * `sv`: Swedish * `et`: Estonian * `lv`: Latvian * `lt`: Lithuanian | Uptrainable processor version. Maximum pages (online/synchronous requests) has been increased to 15. | | `pretrained-invoice-v1.4-2022-10-21` | Release Candidate | Public Preview | None | Uptrainable processor version. Maximum pages (online/synchronous requests) has been increased to 15. | | `pretrained-invoice-v1.5-2023-09-15` | Release Candidate | Public Preview | None |  | | `pretrained-invoice-v2.0-2023-12-06` | Stable | GA | None |  |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 200 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Fields detected in the earliest version** | You can also find this information in the [Field detected](/document-ai/docs/fields) page.  Full list of fields  * `amount_paid_since_last_invoice` * `carrier` * `currency` * `currency_exchange_rate` * `delivery_date` * `due_date` * `freight_amount` * `invoice_date` * `invoice_id` * `line_item`  + `line_item/amount` + `line_item/description` + `line_item/product_code` + `line_item/purchase_order` + `line_item/quantity` + `line_item/unit` + `line_item/unit_price`  * `net_amount` * `payment_terms` * `purchase_order` * `receiver_address` * `receiver_email` * `receiver_name` * `receiver_phone` * `receiver_tax_id` * `receiver_website` * `remit_to_address` * `remit_to_name` * `ship_from_address` * `ship_from_name` * `ship_to_address` * `ship_to_name` * `supplier_address` * `supplier_email` * `supplier_iban` * `supplier_name` * `supplier_payment_ref` * `supplier_phone` * `supplier_registration` * `supplier_tax_id` * `supplier_website` * `total_amount` * `total_tax_amount` * `vat`  + `vat/amount` + `vat/category_code` + `vat/tax_amount` + `vat/tax_rate` |
| **Enriched fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of enriched fields  * `supplier_address` * `supplier_name` * `supplier_phone` |
| **Normalized fields** | You can find more information in the [Enrichment & normalization](/document-ai/docs/enrichment) page.  Full list of normalized fields  * `amount_paid_since_last_invoice` * `currency` * `currency_exchange_rate` * `delivery_date` * `due_date` * `freight_amount` * `invoice_date` * `net_amount` * `total_amount` * `total_tax_amount` * `line_item/amount` * `line_item/quantity` * `line_item/unit_price` * `vat/amount` * `vat/tax_amount` * `vat/tax_rate` |
| **Uptraining** |  |
| **Labeling Instructions** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/labeling-instructions/pretrained-invoice-v1.4-2022-10-21.pdf) |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/INVOICE_PROCESSOR/google_invoice.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_invoice-processor) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-south1` * `asia-southeast1` * `australia-southeast1` * `eu` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |

  

## Classify documents

### Custom Classifier

|  |  |
| --- | --- |
| **Description** | Train a model to classify a document type from a set of classes. |
| **Category** | Classify |
| **Functions** | OCR, Classification |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `CUSTOM_CLASSIFICATION_PROCESSOR` |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-classifier-v1.5-2025-08-05` | Stable | GA | Production-ready model powered by the Gemini 2.5 Flash LLM. Also includes advanced OCR features. This pre-trained model can be used without prior training. It supports zero-shot classification and provides better support for the catch-all class. | | `pretrained-classifier-v1.6-2026-03-09` | Release Candidate | Public Preview | Release candidate powered by the Gemini 3.1 Flash LLM. **Note:** This version does not support data residency. | | `pretrained-classifier-v1.6-pro-2026-03-09` | Release Candidate | Public Preview | Release candidate powered by the Gemini 3.1 Pro LLM. **Note:** This version does not support data residency. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 200 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/CUSTOM_CLASSIFICATION_PROCESSOR/computer_vision_12.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_CUSTOM_CLASSIFICATION_PROCESSOR) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-south1` * `asia-southeast1` * `australia-southeast1` * `eu` * `europe-west2` * `europe-west3` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |
| **More information** | [Create a custom classification processor](/document-ai/docs/workbench/build-custom-classification-processor) |

  

### Custom Splitter

|  |  |
| --- | --- |
| **Description** | Train a model to split a file containing multiple documents into individual, classified documents. |
| **Category** | Classify |
| **Functions** | OCR, Classification, Splitting |
| **[Release stage](https://cloud.google.com/products#product-launch-stages)** | General availability |
| **Access status** | Public lock\_open |
| **Type in API** | `CUSTOM_SPLITTING_PROCESSOR` |
| **Notes** | * i18n can be supported through custom training options only. |
| **Supported languages** | | Language Name | BCP 47 Tag | Script | Handwriting supported | | --- | --- | --- | --- | | English | `en` | `Latn` |  | |
| **Processor versions** | | Version ID | Release Channel | Release Maturity | Description | | --- | --- | --- | --- | | `pretrained-splitter-v1.5-2025-07-14` | Stable | GA | GA model powered by the Gemini 2.5 Flash LLM. This pre-trained model can be used without prior training. It supports zero-shot splitting and classification. | | `pretrained-splitter-v1.6-2026-03-09` | Release Candidate | Public Preview | Release candidate powered by the Gemini 3.1 Flash LLM. **Note:** This version does not support data residency. | | `pretrained-splitter-v1.6-pro-2026-03-09` | Release Candidate | Public Preview | Release candidate powered by the Gemini 3.1 Pro LLM. **Note:** This version does not support data residency. |   For more information, see [Managing processor versions.](/document-ai/docs/manage-processor-versions) |
| **Quotas and limits** | |  |  | | --- | --- | | Maximum pages (online/synchronous requests): | 15 | | Maximum pages (batch/offline/asynchronous requests): | 1000 | | Maximum pages (imageless mode online/synchronous requests): | 30 |  **Note:** Specific processor limits are *in addition to* overall product [quotas and limits](/document-ai/quotas). **Note:** To extend the maximum page limit for online and synchronous requests up to 30, be sure to enable `imageless_mode` in the [ProcessRequest](/document-ai/docs/reference/rpc/google.cloud.documentai.v1#processrequest). |
| **Uptraining** |  |
| **Sample Input File** | [Open in new window.](https://storage.googleapis.com/cloud-samples-data/documentai/SampleDocuments/CUSTOM_SPLITTING_PROCESSOR/inference_cds.pdf) |
| **Sample Output** | [Open in new window.](/document-ai/docs/output#processor_CUSTOM_SPLITTING_PROCESSOR) |
| **[Supported regions](/document-ai/docs/regions)** | * `asia-south1` * `asia-southeast1` * `australia-southeast1` * `eu` * `europe-west2` * `europe-west3` * `northamerica-northeast1` * `us`  **Note:** Consult **[Supported regions](/document-ai/docs/regions)** for a full list of processor version availability by region. |
| **More information** | [Create a custom splitter processor](/document-ai/docs/workbench/build-custom-splitter-processor) |

  

## Footnotes

[†]
Identity Document Proofing works to extract and evaluate information from ID documents that contributes to identifying whether the input image represents an authentic ID.
  
  
At Google Cloud, we prioritize helping customers safely develop and implement AI solutions, and Identity Proofing has been developed in accordance with Google's AI Principles.
  
  
Based on Google's AI Principles and current product design, we strongly recommend using caution and carefully evaluating the potential benefits and risks of using Identity Document Proofing for the following:

* Decision-making without a human in the loop for predictions that can impact human rights.
* In sensitive domains including but not limited to employment, access to public services, healthcare, and safety-critical contexts.

[‡] Always use Identity Proofing as part of your broader identity-detection process and workflow.
It is important that you have a human reviewer in your workflow to verify whether the predicted signals are accurate. The Identity Proofing processor isn't meant to replace human review of IDs in a workflow, but rather to assist human reviewers in validating ID documents. The Identity Proofing processor shouldn't be used as an automated decision tool to determine whether an ID is valid. With human review, customers can achieve higher document processing accuracy and help businesses evaluate predictions using purpose-built tools to enable those reviews.
  
  
Make sure that you review regulations in the region where you are implementing this technology, and research existing industry guidance to learn about policy guidelines and common fairness issues. Read about fairness in machine learning, including ways to mitigate bias in training datasets, evaluate your custom models for disparities in performance, and other considerations as you use your custom model.
  
  
We encourage customers to keep fairness, interpretability, and privacy and security best practices in mind when implementing Identity Proofing. To learn more about how to implement responsible AI, read Google's [recommendations for Responsible AI practices](https://cloud.google.com/responsible-ai).
  
  
Refer to the blog post [Automate identity document processing with Document AI]](https://cloud.google.com/blog/topics/developers-practitioners/automate-identity-document-processing-document-ai) for more information on use cases and a sample application code repository.

[Next

Supported files

arrow\_forward](/document-ai/docs/file-types)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-07-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-07-01 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/file-types](./document-ai-docs-file-types.md)
- [https://docs.cloud.google.com/document-ai/docs/form-parser](./document-ai-docs-form-parser.md)
- [https://docs.cloud.google.com/document-ai/docs/manage-processor-versions](./document-ai-docs-manage-processor-versions.md)
- [https://docs.cloud.google.com/document-ai/docs/output](./document-ai-docs-output.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
