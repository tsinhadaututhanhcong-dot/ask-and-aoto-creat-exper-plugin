---
title: Tab Completion
date_created: 2026-07-01
source_url: https://antigravity.google/docs/ide/tab
description: Real-time code completion models.
tags: [concept, llms-txt, js-rendered]
platform: ide
---

* side\_navigation
* Antigravity IDE
>* Features
>* Tab

# Antigravity IDE: Tab & Navigation[link](#antigravity-ide-tab-navigation)

This guide covers the core navigation and completion tools: **Supercomplete**, **Tab-to-Jump**, and **Tab-to-Import**.

## Supercomplete[link](#supercomplete)

Supercomplete provides code suggestions in a region near your current cursor position.

![Supercomplete](assets/image/docs/editor/supercomplete.png)

### How it Works[link](#how-it-works)

* **File-Wide Suggestions**: Suggestions can modify code throughout the document, handling tasks like changing variable names or updating separate function definitions simultaneously.
* **Accepting**: Press `Tab` to accept the changes.

## Tab-to-Jump[link](#tab-to-jump)

Tab-to-Jump is a fluid navigation tool that suggests the next logical place in your document to move your cursor to.

![Tab-to-Jump](assets/image/docs/editor/tab_to_jump.png)

### How it Works[link](#how-it-works-2)

* A "Tab to jump" icon will appear offering to move your cursor to where your next logical edit will be. Pressing `Tab` instantly moves your cursor to that location.
* **Accepting**: Press `Tab` to accept the jump.

## Tab-to-Import[link](#tab-to-import)

Tab-to-Import handles missing dependencies without breaking your flow.

![Tab-to-Import](assets/image/docs/editor/tab_to_import.png)

### How it Works[link](#how-it-works-3)

* **Detection**: If you type a class or function that isn't imported, Antigravity suggests the import.
* **Action**: Press `Tab` to complete the word and instantly add the import statement to the top of the file.

## Settings[link](#settings)

In your settings, you can customize the behavior of these features:

* **Enable/Disable Features**: You can individually turn off Autocomplete, Tab-to-Jump, Supercomplete, or Tab-to-Import.
* **Tab Speed**: Controls the responsiveness of suggestions.
* `Slow`: Waits for more context before suggesting.
* `Default`: Offers a balanced pace.
* `Fast`: Provides rapid-fire suggestions.
* **Highlight Inserted Text**: When enabled, text inserted via Tab is highlighted to track changes easily.
* **Clipboard Context**: When enabled, Antigravity uses the contents of your clipboard to improve completion accuracy.
* **Allow Gitignored Files**: Enables Tab features (suggestions and jumping) within files listed in your `.gitignore` file. Tab will only ignore gitignored files if git is installed.

On this Page