# lastBench

AI-first learning platform for structured courses, progress tracking, quizzes, exercises, and sandbox labs for hands-on practice.

## Overview

lastBench is a modern learning platform designed to host curated learning content and turn passive study into active practice.

The platform is intended to support:

- structured courses and learning paths
- module and lesson-based navigation
- learner progress tracking
- quizzes and exercises
- sandbox/lab-based hands-on practice
- admin-driven content management
- basic analytics for learner activity and course performance

The goal is to create a focused system where learners can study, practice, track progress, and improve in one place.

## Core Features

### Learning Experience
- Course catalog
- Course -> Module -> Lesson hierarchy
- Rich lesson content
- Continue-learning flow
- Progress indicators at lesson, module, and course level

### Assessments
- Quiz support
- Exercise activities
- Attempt tracking
- Score history
- Pass/fail evaluation

### Sandbox / Labs
- Hands-on practice environment
- Task-based lab activities
- Starter templates
- Output/result tracking
- Extensible sandbox architecture

### Admin Capabilities
- Create and manage courses
- Organize modules and lessons
- Create quizzes and sandbox tasks
- Publish or unpublish content
- View learner activity and summaries

### Analytics
- Enrollments overview
- Completion tracking
- Quiz attempt summaries
- Course progress visibility

## Proposed Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend
- FastAPI
- Python

### Data and Infrastructure
- PostgreSQL
- Docker Compose
- Redis (optional, only if needed)
- Object storage for assets and resources

## Architecture Direction

lastBench is planned as a modular monolith for the initial version.

This approach is chosen to keep development fast, maintainable, and practical while still allowing future separation of services if scale or complexity requires it.

Planned logical modules include:

- Auth and User Management
- Courses and Content Management
- Enrollment
- Progress Tracking
- Quiz and Exercise Engine
- Sandbox / Lab Engine
- Analytics
- Admin Dashboard

## Initial Product Scope

The first MVP will focus on:

- authentication
- course management
- learner dashboard
- lesson delivery
- progress tracking
- quizzes
- basic sandbox/lab support
- admin panel
- analytics basics

## Project Structure

Planned structure:

```text
/
  README.md
  docker-compose.yml
  .env.example
  /docs
  /apps
    /web
    /api
  /scripts
  /packages
```

## Planned User Roles

### Admin
Manages courses, lessons, quizzes, sandbox tasks, and platform visibility.

### Learner
Consumes content, completes activities, uses the sandbox, and tracks progress.

### Reviewer / Mentor
Optional future role for reviewing practical submissions and providing feedback.

## Roadmap

### Phase 1
- Repo setup
- App scaffolding
- Authentication
- Database schema
- Basic frontend/backend integration

### Phase 2
- Course, module, and lesson management
- Learner navigation
- Enrollment flow
- Progress tracking

### Phase 3
- Quiz engine
- Exercise support
- Sandbox MVP

### Phase 4
- Admin analytics
- Improved UX
- Content publishing workflow
- Hardening and tests

## Vision

lastBench aims to become a practical learning platform where content, assessment, and experimentation exist together, making learning measurable, interactive, and project-driven.

## Status

Project status: Planning / Initial Setup
