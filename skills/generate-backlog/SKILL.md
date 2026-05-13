---
name: generate-backlog
description: Generate migration backlog from migration plan. Use when the user wants to create user stories, generate task backlog, populate kanban boards, or break down migration work into trackable items.
---

Generate and sync Kanban tickets from migration plan.

## Parameters

- `--plan` (required): Path to migration plan JSON
- `--kanban-platform` (required): Platform (jira, linear, github-projects)
- `--project-id` (optional): Project/board ID

## Description

Creates tickets on Kanban board from user stories and maintains synchronization.

## Actions

1. Load migration plan
2. Connect to Kanban platform API
3. Create tickets for each story
4. Set labels, priorities, dependencies
5. Return ticket mapping

## Outputs

JSON mapping of story IDs to Kanban ticket IDs.
