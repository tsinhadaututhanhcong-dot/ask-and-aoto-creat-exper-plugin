---
type: Reference
title: "Custom splitter  |  Document AI  |  Google Cloud Documentation"
description: "**Source:** [https://docs.cloud.google.com/document-ai/docs/custom-splitter](https://docs.cloud.google.com/document-ai/docs/custom-splitter)"
timestamp: 2026-07-06T03:34:16Z
---
# Custom splitter  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/custom-splitter](https://docs.cloud.google.com/document-ai/docs/custom-splitter)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.



# Custom splitter

Custom splitter is designed to be used to split composite documents (documents made
up of multiple classes) into a number of single class documents by identifying
each logical document. For example, a mortgage package contains multiple classes
within it such as application, income verification, and photo ID. Custom splitter
processors can be used out of the box, or trained from the ground up using your own
documents and custom classes.

**Note:** A logical document is a unique type of document within a single packed PDF
that might contain invoices, expenses, IDs, or contracts.

## Splitter description and usage

You can create custom splitters that are specifically suited to your documents
and trained and evaluated with your data, or deploy pretrained models with
generative AI. These processors identify classes of documents from a user-defined
set of classes. You can then use these processors on your documents.
You typically would use a custom splitter on files that are composed of different
types of logical documents, then use the class identification of each to pass
the documents to an appropriate extraction processor to extract the entities.

**Note:** The custom splitter only predicts the pages that make up various documents
within the composite file and the class of each identified document. In the Document AI
Toolbox SDK, there is code to physically separate out each identified logical
document.

Because ML models are not perfect and have a certain error rate, and because errors
in splitting are typically very problematic (a bad split makes two documents wrong
and causes extraction errors), a best practice is to always have a human review
step after the splitting prediction but before the actual file split. Based on
business requirements, there are alternatives to always doing human review:

* Use confidence scores in the prediction to decide whether to bypass human review
  (if high enough). That confidence score threshold should be determined based on
  historical data about error rates at given confidence scores. This should be a
  business decision based on the business process tolerance for errors and requirement
  to bypass human review.
* In some use cases, the split documents can be routed directly to the appropriate
  extractor according to the predicted class. Then, if the extraction is incomplete
  or has low confidence scores, isolate the split documents and trigger the
  original composite document and split decision to then be reviewed. This has
  rather complex workflow requirements.

## Custom splitter model versions

The following models are available for custom splitter. To change model
versions, see [Manage processor versions](/document-ai/docs/manage-processor-versions).

Version 1.5 supports confidence scores.

| Model version | Description | Release channel | Release date |
| --- | --- | --- | --- |
| `pretrained-splitter-v1.5-2025-07-14` | GA model powered by the Gemini 2.5 Flash LLM. This pre-trained model can be used without prior training. It supports zero-shot splitting and classification. | Stable | July 14, 2025 |
| `pretrained-splitter-v1.6-2026-03-09` | Release candidate powered by the Gemini 3.1 Flash LLM. **Note:** This version does not support data residency. | Release Candidate | March 9, 2026 |
| `pretrained-splitter-v1.6-pro-2026-03-09` | Release candidate powered by the Gemini 3.1 Pro LLM. **Note:** This version does not support data residency. | Release Candidate | March 9, 2026 |

To make a Quota Increase Request (QIR) for the default processor quota, follow
the steps to
[request a quota adjustment](/docs/quotas/view-manage#requesting_higher_quota).

## Decide on a custom splitter version

When using custom splitter, train on your own data or use a pre-trained version with generative AI, such as `pretrained-splitter-v1.5-2025-07-14`.

The training process can take several hours, but lets you adjust the model to
the specifics of your data. Pre-trained versions are based on Gemini
models. They can be brought to production in less time or used to quickly
iterate and test labeling schema. They don't require a training dataset.

The following guide applies to both versions, and will call out the different
steps for each when they vary.

## Create a custom splitter in Google Cloud console

This quickstart guide describes how to use Document AI to create and train
a custom splitter that splits and classifies procurement documents. Most of the
document prep is done, so that you can focus on creating a custom splitter.

A typical workflow to create and use a custom splitter trained base version is as follows:

1. Create a custom splitter in Document AI.
2. Create a dataset using an empty Cloud Storage bucket.
3. Define and create the processor schema (classes).
4. Import documents.
5. Assign documents to the training and test sets.
6. Annotate documents manually in Document AI or with labeling tasks.
7. Train the processor.
8. Evaluate the processor.
9. Deploy the processor.
10. Test the processor.
11. Use the processor on your documents.

A typical workflow to create and use a custom splitter pre-trained version is as
follows:

1. Create a custom splitter in Document AI.
2. Create a dataset using an empty Cloud Storage bucket.
3. Select a pre-trained model version
4. Define and create the processor schema (classes).
5. (Optionally) Import documents.
6. (Optionally if you want to evaluate its performance) Assign documents to the
   test sets
7. (Optionally) Evaluate the processor.
8. Test the processor.
9. Deploy the processor.
10. Use the processor on your documents.

---

To follow step-by-step guidance for this task directly in the
Google Cloud console, click **Guide me**:

[Guide me](https://console.cloud.google.com/ai/document-ai?tutorial=document-ai--documentai-workbench_custom_splitter_console)

---

## Before you begin

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
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required-roles). If you created a new
  project, then you already have the required permissions.
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- Enable the Document AI, Cloud Storage APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](/iam/docs/granting-changing-revoking-access).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=documentai.googleapis.com,storage.googleapis.com)

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
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required-roles). If you created a new
  project, then you already have the required permissions.
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- Enable the Document AI, Cloud Storage APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](/iam/docs/granting-changing-revoking-access).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=documentai.googleapis.com,storage.googleapis.com)

### Required roles

To get the permissions that
you need to create a custom splitter,
ask your administrator to grant you the
following IAM roles on your project:

* [Document AI Administrator](/iam/docs/roles-permissions/clouddocumentai#documentai.admin)  (`roles/documentai.admin`)
* [Storage Admin](/iam/docs/roles-permissions/storage#storage.admin)  (`roles/storage.admin`)

For more information about granting roles, see [Manage access to projects, folders, and organizations](/iam/docs/granting-changing-revoking-access).

You might also be able to get
the required permissions through [custom
roles](/iam/docs/creating-custom-roles) or other [predefined
roles](/iam/docs/roles-overview#predefined).

**Note:** If you want to access input files stored in a different project, then you
need to grant additional roles to the Document AI service agent. For
more information, see [Cross project file access
setup](/document-ai/docs/setup#cross_project_file_access_setup).

## Create a processor

1. In the Google Cloud console, in the Document AI section, go to the **Workbench** page.

   [Workbench](https://console.cloud.google.com/ai/document-ai/workbench)
2. For **Custom Document Splitter**, select
   **Create processor**.
   ![custom-splitter-1](/static/document-ai/docs/images/create/custom-splitter-1.png)
3. In the **Create processor** menu, enter a name for your processor, such as `my-custom-document-splitter`.

   ![custom-splitter-2](/static/document-ai/docs/images/create/custom-splitter-2.png)
4. Select the region closest to you.
5. Select **Create**. The **Processor Details** tab appears.

## Configure dataset

In order to train this new processor, you must create a dataset with training and
testing data to help the processor identify the documents that you want to split and classify.

This dataset requires a new location for it. This can be an empty [Cloud Storage bucket](/storage)
or folder, or you can allow a **Google-Managed** (internal) location.

* If you want **Google-managed storage**, select that option.
* If you want to use your own storage in order to use Customer-Managed Encryption Keys (CMEK),
  select **I'll specify my own storage location** and follow the later procedure.

![custom-splitter-3](/static/document-ai/docs/images/create/custom-splitter-3.png)

**Note:** Folders for datasets must be treated as read-only. Don't change or add anything.

## Create a Cloud Storage bucket for the dataset

**Note:** Don't use the same bucket where your documents are stored.

1. Go to your processor's
   **Train**
   tab.
2. Select **Set dataset location**. You are prompted to select or create an empty
   Cloud Storage bucket or folder.

   ![custom-splitter-4](/static/document-ai/docs/images/create/custom-splitter-4.png)
3. Select **Browse** to open **Select folder**.
4. Select the **Create a new bucket** icon and follow the prompts to create a new
   bucket. After you create the bucket, the **Select folder** page
   appears for it. For more information on creating a Cloud Storage bucket, refer to
   [Cloud Storage buckets](/storage/docs/creating-buckets).

   **Note:** A bucket is the top-level storage entity, in which you can nest folders.
   Instead of creating and selecting a bucket, you can also create and select an empty
   folder inside an existing bucket. For more information, see
   [Cloud Storage simulated folders](/storage/docs/objects#simulated-folders).
5. On the **Select folder** page for your bucket, choose the **Select button** at
   the bottom of the dialog.

   ![custom-splitter-5](/static/document-ai/docs/images/create/custom-splitter-5.png)

Make sure the destination path is populated with the bucket name you selected.
Select **Create dataset**. The dataset might take up to several minutes to create.

## (Optional) Select a pre-trained model version

If you have decided to use a pre-trained model, you must first select it in the
**Deploy and use** section. You can ignore the sections after the next one, "Define processor schema."

1. Navigate to **Deploy and use**

   ![custom-splitter-15](/static/document-ai/docs/images/create/custom-splitter-15.png)
2. Click the **Manage versions** drop-down.
3. Select the chosen processor version.

**Tip:** You can see a list of pre-trained and trained versions you've
worked on in the **Versions** section, including which are deployed
check\_circle
 and which is the default
radio\_button\_unchecked
star
.

## Define processor schema

You can create the processor schema either before or after you import documents
into your dataset. The schema provides labels that you use to annotate documents.

1. On the **Build** tab, select **Manage dataset**. The manage dataset page opens.
2. Select 
   **Edit Schema**.
3. Select 
   **Create label**
   and enter the name for the label. Select **Create**. Refer to [Define processor
   schema](/document-ai/docs/workbench/label-documents#define_processor_schema) for
   detailed instructions on creating and editing a schema.

   **Note:** Once the processor is trained, labels cannot be deleted. Instead, you can
   disable any label you don't want to use.**Tip:** [Add a description
   prompt](/document-ai/docs/label-documents#add_a_description_prompt) to improve
   training performance.
4. Create each of the following labels for the processor schema.

   * `bank_statement`
   * `form_1040`
   * `form_w2`
   * `form_w9`
   * `paystub`
5. Select
   **Save** when the labels are complete.

   ![custom-splitter-6](/static/document-ai/docs/images/create/custom-splitter-6.png)

## Import an unlabeled document into a dataset

The next step is to begin importing unlabeled documents into your dataset and
label them. A recommended alternative is to import documents organized in folders
by class, if available.

If working on your own project, you determine how to label your data. Refer to
[Labeling options](/document-ai/docs/workbench/label-documents#labeling_options).

Document AI custom processors require a minimum of 10 documents in the training
and test sets, along with 10 instances of each label in each set. We recommend at
least 50 documents in each set, with 50 instances of each label for best performance.
In general, more training data produces higher accuracy.

1. On the **Train** tab, select
   **Import documents**.

   ![custom-splitter-7](/static/document-ai/docs/images/create/custom-splitter-7.png)
2. For this example, enter this path in
   **Source path**. This contains one document PDF.

   ```
   cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-Unlabeled
   ```
3. Set the
   **Document label**
   as **None**.
4. Set the
   **Dataset split**
   dropdown to **Unassigned**.

   The document in this folder is not given a label or assigned to the testing or
   training set by default.
5. Select
   **Import**.
   Document AI reads the documents from the bucket into the dataset. It does
   not modify the import bucket or read from the bucket after the import is complete.

When you import documents, you can optionally assign the documents to the
**Training** or **Test** set when imported, or wait to assign them later.

If you want to delete a document or documents that you have imported, select
them on the **Train** tab, and select **Delete**.

For more information about preparing your data for import, refer to the
[Data preparation guide](/document-ai/docs/workbench/create-dataset).

## Optional: Batch label documents at import

You can label all documents that are in a particular directory at import to save
time with labeling.
If you have your training documents organized by class in folders, then you can
use the **Document label** field to specify the class for those documents and avoid manual labeling of each document.

![custom-splitter-8](/static/document-ai/docs/images/create/custom-splitter-8.png)

In the image **Bank\_statements** and **Invoice** are available defined labels
(document classes) you can select. Or you can use `CREATE LABEL` and define a new
class.

1. Click **Import documents**.
2. Enter the following path in **Source path**. This bucket contains unlabeled
   documents in PDF format.

   `cloud-samples-data/documentai/Custom/Patents/PDF-CDC-BatchLabel`
3. From the **Data split** list, select **Auto-split**. This automatically splits
   the documents to have 80% in the training set, and 20% in the test set.
4. In the **Apply labels** section, select **Choose label**.
5. For these sample documents, select other.
6. Click **Import** and wait for the documents to import. You can leave this page
   and return later.

## Label a document

The process of applying labels to a document is known as *annotation*.

1. Return to the **Train** tab, and select
   a document
   to open the **Label management** console.
2. This document contains multiple page groups that need to be identified and
   labeled. First, you need to identify the split points. Move your mouse in between
   pages **1** and **2** in the image view and select on the
   **+** symbol.

   ![custom-splitter-9](/static/document-ai/docs/images/create/custom-splitter-9.png)
3. Create split points before the following page numbers: **2**, **3**, **4**, **5**.

   Your console should look like this when finished.
   ![custom-splitter-10](/static/document-ai/docs/images/create/custom-splitter-10.png)

   **Note:** You can do step 4 (setting the document type) as soon as the logical document
   is split.
4. In the **Document type** dropdown, select the appropriate label for each page group.

   | **Page(s)** | **Document type** |
   | --- | --- |
   | 1 | `paystub` |
   | 2 | `form_w9` |
   | 3 | `bank_statement` |
   | 4 | `form_w2` |
   | 5 & 6 | `form_1040` |

   The labeled document should look like this when complete:
   ![custom-splitter-11](/static/document-ai/docs/images/create/custom-splitter-11.png)
5. Select
   **Mark as Labeled**
   when you have finished annotating the document.

   On the **Train** tab, the left-hand panel shows that 1 document has been
   labeled.

## Assign annotated document to the training set

Now that you have labeled this example document, you can assign it to the training set.

1. On the **Train** tab, select the
   **Select All**
   checkbox.
2. From the
   **Assign to Set**
   list, select **Training**.

In the left-hand panel, you can find that 1 document has been assigned to the training set.

## Import data with batch labeling

Next, you import unlabeled PDF files that are sorted into different Cloud Storage
folders by their type. Batch labeling helps save time on labeling by assigning a
label at import time based on the path.

1. On the **Train** tab, select
   **Import documents**.
2. Enter the following path in
   **Source path**. This folder contains PDFs of bank statements.

   ```
   cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-CDS-BatchLabel/bank-statement
   ```
3. Set the
   **Document label**
   as `bank_statement`.
4. Set, in the
   **Dataset split**
   menu, to **Auto-split**. This automatically splits the documents to have 80%
   in the training set and 20% in the test set.
5. Select
   **Add Another Folder**
   to add more folders.
6. Repeat the previous steps with the following paths and document labels:

   | **Bucket path** | **Document label** |
   | --- | --- |
   | `cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-CDS-BatchLabel/1040` | `form_1040` |
   | `cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-CDS-BatchLabel/w2` | `form_w2` |
   | `cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-CDS-BatchLabel/w9` | `form_w9` |
   | `cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-CDS-BatchLabel/paystub` | `paystub` |

   The console should look like this when complete:
   ![custom-splitter-12](/static/document-ai/docs/images/create/custom-splitter-12.png)
7. Select
   **Import**.
   The import takes several minutes.

When the import is finished, find the documents on the **Train** tab.

## Import prelabeled data

In this guide, you are provided with prelabeled data in the [`Document`](/document-ai/docs/reference/rest/v1/Document) format as JSON files.

This is the same format that Document AI outputs when processing a document or [exporting a dataset](/document-ai/docs/workbench/label-documents#export_dataset).

1. On the **Train** tab, select
   **Import documents**.
2. Enter the following path in
   **Source path**.

   ```
   cloud-samples-data/documentai/Custom/Lending-Splitter/JSON-Labeled
   ```
3. Set the
   **Document label**
   as **None**.
4. Set the
   **Dataset split**
   dropdown to **Auto-split**.
5. Select
   **Import**.

When the import is finished, find the documents on the **Train** tab.

## Train the processor

Now that you have imported the training and test data, you can train the processor. Because training might take several hours, make sure you have set up the processor with the appropriate data and labels before you begin training.

1. Select
   **Train New Version**.
2. In the
   **Version name** field, enter a name for this processor version, such as `my-cds-version-1`.
3. (Optional) Select **View Label Stats** to find information about the document labels. That can help determine your coverage. Select **Close** to return to the training setup.

   ![custom-splitter-13](/static/document-ai/docs/images/create/custom-splitter-13.png)
4. Select
   **Start training**
   You can check the status on the right-hand panel.

## Deploy the processor version

1. After training is complete, navigate to the
   **Manage Versions**
   tab. You can view details about the version you just trained.
2. Select the
   three vertical dots
   on the right of the version you want to deploy, and select **Deploy version**.
3. Select
   **Deploy**
   from the popup window.

   Deployment takes a few minutes to complete.

## Evaluate and test the processor

1. After deployment is complete, navigate to the
   **Evaluate & Test**
   tab.

   On this page, you can view evaluation metrics including the F1 score, precision
   and recall for the full document, and individual labels.
   For more information about evaluation and statistics, refer to [Evaluate processor](/document-ai/docs/workbench/evaluate).
2. Download a document that has not been involved in previous training or testing
   so that you can use it to evaluate the processor version. If using your own data,
   you would use a document set aside for this purpose.

   [file\_download
   Download PDF](https://storage.googleapis.com/cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-Inference/inference_cds.pdf)
3. Select
   **Upload Test Document** and select
   the document you just downloaded.

   The **Custom splitter analysis** page opens. The screen output demonstrate how
   well the document was split and classified.

   The console should look like this when complete:
   ![custom-splitter-14](/static/document-ai/docs/images/create/custom-splitter-14.png)

   You can also re-run the evaluation against a different test set or processor
   version.

## (Optional) Import data with auto-labeling

After deploying a trained processor version, you can use [Auto-labeling](/document-ai/docs/workbench/label-documents#auto-label) to save time on labeling when importing new documents.

1. On the **Train** tab, select
   **Import documents**.
2. Enter the following path in
   **Source path**. This folder contains unlabeled PDFs of multiple document types.

   ```
   cloud-samples-data/documentai/Custom/Lending-Splitter/PDF-CDS-AutoLabel
   ```
3. Set the
   **Document label**
   as **Auto-label**.
4. Set the
   **Dataset split**
   dropdown to **Auto-split**.
5. In the **Auto-labeling** section, set the
   **Version**
   as the version you previously trained.

   * For example: `2af620b2fd4d1fcf`
6. Select
   **Import**
   and wait for the documents to import.
7. You cannot use autolabeled documents for training or testing without marking them as labeled. Go to the
   **Auto-labeled**
   section to view the autolabeled documents.
8. Select the first document to enter the labeling console.
9. Verify the label to ensure it's correct, and adjust if not.
10. Select **Mark as Labeled** when finished.
11. Repeat the label verification for each autolabeled document.
12. Return to the **Train** page and select **Train New Version** to use the data for training.

## Use the processor

You have successfully created and trained a custom splitter processor.

You can manage your custom-trained processor versions just like any other processor
version. For more information, refer to [Managing processor versions](/document-ai/docs/manage-processor-versions).

Once deployed, you can
[Send a processing request](/document-ai/docs/send-request) to your custom
processor, and the
[response can be handled the same as other splitter processors](/document-ai/docs/splitters).

## Clean up

To avoid incurring charges to your Google Cloud account for
the resources used on this page, follow these steps.

To avoid unnecessary Google Cloud charges, use the
[Google Cloud console](https://console.cloud.google.com/) to delete your processor and project if you don't need
them.

If you created a new project to learn about Document AI and you no
longer need the project, [delete the project](https://console.cloud.google.com/cloud-resource-manager).

If you used an existing Google Cloud project, delete the resources you
created to avoid incurring charges to your account:

1. In the Google Cloud console navigation menu, select **Document AI** and select **My Processors**.
2. Select **More actions** in the same row as the processor you want to delete.
3. Select **Delete processor**, type the processor name, then select **Delete** again to confirm.

## What's next

[Previous

arrow\_back

Custom classifier](/document-ai/docs/custom-classifier)

[Next

Document splitters behavior

arrow\_forward](/document-ai/docs/splitters)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/custom-classifier](./document-ai-docs-custom-classifier.md)
- [https://docs.cloud.google.com/document-ai/docs/label-documents](./document-ai-docs-label-documents.md)
- [https://docs.cloud.google.com/document-ai/docs/manage-processor-versions](./document-ai-docs-manage-processor-versions.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/send-request](./document-ai-docs-send-request.md)
- [https://docs.cloud.google.com/document-ai/docs/setup](./document-ai-docs-setup.md)
