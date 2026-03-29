# AGENTS

This document defines the AI agents used in the Financing project and their roles, responsibilities, and capabilities.

## Overview

The Financing project leverages AI agents for various aspects of development, testing, and code generation. Each agent has a specific domain of expertise and defined responsibilities.

## Agent Definitions

### 1. Orchestrator Agent (Sisyphus)

**Role:** Primary task coordination and execution agent

**Responsibilities:**
- Coordinate overall project tasks
- Delegate specialized work to domain-specific agents
- Manage task execution flow
- Ensure task completion and verification

**Capabilities:**
- Intent recognition and task classification
- Multi-step task orchestration
- Parallel execution of independent tasks
- Session management for continuity

**Domain:** Project-wide orchestration

---

### 2. Explore Agent

**Role:** Codebase exploration and pattern discovery

**Responsibilities:**
- Search and analyze codebase structure
- Find implementation patterns across the codebase
- Identify code conventions and styles
- Locate specific functionality and modules

**Capabilities:**
- Contextual grep for codebases
- Pattern discovery and matching
- File structure analysis
- Multi-angle codebase exploration

**Domain:** Internal codebase analysis

**Use Cases:**
- Finding existing implementations
- Understanding code structure
- Locating specific features
- Pattern matching

---

### 3. Librarian Agent

**Role:** External reference research and documentation lookup

**Responsibilities:**
- Search official documentation for libraries
- Find production-ready examples from open-source projects
- Research best practices for unfamiliar technologies
- Retrieve library API references

**Capabilities:**
- GitHub CLI for OSS examples
- Context7 documentation queries
- Web search for current best practices
- Cross-repository analysis

**Domain:** External resources and documentation

**Use Cases:**
- Learning unfamiliar APIs
- Finding production patterns
- Researching security best practices
- Looking up library documentation

---

### 4. Oracle Agent

**Role:** High-IQ read-only consultant

**Responsibilities:**
- Complex architecture design consultation
- Debugging challenging issues
- Multi-system tradeoff analysis
- Security and performance evaluation

**Capabilities:**
- Deep reasoning and analysis
- Architecture decision support
- Problem diagnosis
- Read-only consultation

**Domain:** Architecture, debugging, complex decisions

**Use Cases:**
- Architecture design questions
- After 2+ failed fix attempts
- Unfamiliar code patterns
- Multi-system tradeoffs
- Security/performance concerns

**Constraints:**
- Read-only (no code changes)
- Consultation-only (not for trivial tasks)
- Used sparingly (expensive resource)

---

### 5. Metis Agent

**Role:** Pre-planning and requirements analysis

**Responsibilities:**
- Analyze complex tasks for hidden intentions
- Identify ambiguities in requirements
- Catch potential AI failure points
- Scope clarification

**Capabilities:**
- Requirement analysis
- Ambiguity detection
- Risk assessment
- Scope definition

**Domain:** Task planning and analysis

**Use Cases:**
- Complex task planning
- Ambiguous requirements
- Multi-layered tasks
- Pre-implementation analysis

---

### 6. Momus Agent

**Role**: Work plan review and quality assurance

**Responsibilities:**
- Evaluate work plans for clarity
- Assess plan verifiability
- Check completeness of implementation plans
- Identify gaps in documentation

**Capabilities:**
- Plan quality assessment
- Gap detection
- Clarity verification
- Completeness checking

**Domain:** Plan review and QA

**Use Cases:**
- Work plan evaluation
- Implementation plan review
- Documentation gap analysis
- Quality assurance

---

### 7. Build Agent

**Role:** Implementation and code generation

**Responsibilities:**
- Write production code following project conventions
- Implement features based on specifications
- Ensure code quality and testing
- Match existing codebase patterns

**Capabilities:**
- Code generation
- Implementation from specs
- Test writing
- Pattern matching

**Domain:** Code implementation

**Use Cases:**
- Feature implementation
- Code refactoring
- Test writing
- Bug fixes

---

## Agent Collaboration Patterns

### Standard Discovery Pattern

```
User Request → Orchestrator
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Explore Agent      Librarian Agent
    │                   │
Internal Research  External Research
    └─────────┬─────────┘
              ↓
        Synthesize
              ↓
        Execute
```

### Complex Task Pattern

```
User Request → Metis (Pre-planning)
              ↓
        Work Plan
              ↓
        Momus (Plan Review)
              ↓
        Orchestrator
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Explore Agent      Librarian Agent
    │                   │
    └─────────┬─────────┘
              ↓
        Build Agent (Implementation)
              ↓
        Oracle (Review if needed)
```

### Debugging Pattern

```
Issue Found → Build Agent (2+ attempts fail)
              ↓
        Oracle (Diagnosis)
              ↓
        Build Agent (Fix)
              ↓
        Verification
```

## Agent Selection Guidelines

### When to Use Explore Agent

- Need to understand existing code structure
- Looking for patterns in the codebase
- Finding implementations of specific features
- Mapping module dependencies

### When to Use Librarian Agent

- Working with unfamiliar libraries
- Need official API documentation
- Looking for production examples
- Researching best practices

### When to Use Oracle Agent

- Architecture decisions involving tradeoffs
- After 2+ failed implementation attempts
- Security or performance concerns
- Unfamiliar complex patterns

### When to Use Metis Agent

- Complex, multi-layered tasks
- Ambiguous or unclear requirements
- Tasks with multiple potential interpretations
- Pre-planning needed

### When to Use Momus Agent

- Reviewing work plans before implementation
- Checking completeness of specifications
- Evaluating documentation clarity
- Quality assurance of plans

### When to Use Build Agent

- Writing production code
- Implementing features
- Writing tests
- Making code changes

## Agent Configuration

### Parallel Execution

Agents can be executed in parallel for independent tasks:

```python
# Fire multiple exploration agents simultaneously
task(agent="explore", prompt="Find auth implementations")
task(agent="explore", prompt="Find error handling patterns")
task(agent="librarian", prompt="Research JWT best practices")

# Continue with other work while agents run
```

### Session Continuity

Sessions can be continued with preserved context:

```python
# First task
result = task(category="quick", prompt="Fix type error")
session_id = result.session_id

# Continue with full context preserved
task(session_id=session_id, prompt="Also: check related code")
```

### Background Tasks

Agents can run in background for long-running tasks:

```python
# Fire agent in background
task_id = task(agent="explore", prompt="Search entire codebase",
              run_in_background=True)

# Continue with other work
# System notifies when complete

# Collect results
background_output(task_id)
```

## Agent Costs

| Agent | Cost | Usage |
|-------|------|-------|
| Explore | FREE | Contextual grep, codebase analysis |
| Librarian | CHEAP | Documentation, OSS examples |
| Build | MEDIUM | Implementation, code generation |
| Metis | EXPENSIVE | Pre-planning, requirement analysis |
| Momus | EXPENSIVE | Plan review, QA |
| Oracle | EXPENSIVE | Architecture, complex debugging |

**Guideline:** Use agents progressively—start with free/cheap agents, escalate to expensive agents only when needed.

## Anti-Patterns

### ❌ Don't: Duplicate Work

After delegating to Explore/Librarian, don't manually search the same topics.

```python
# WRONG
task(agent="explore", prompt="Find auth patterns")
grep("auth")  # Don't do this!
```

### ❌ Don't: Use Oracle for Trivial Tasks

```python
# WRONG
task(agent="oracle", prompt="How to print in Python?")
```

### ❌ Don't: Poll Background Tasks

```python
# WRONG
task_id = task(agent="oracle", prompt="Analyze architecture", run_in_background=True)
background_output(task_id)  # Don't poll - wait for notification
```

### ✅ Do: Continue Non-Overlapping Work

```python
# CORRECT
task(agent="explore", prompt="Find auth patterns")
# Work on different file while searching
```

## Best Practices

1. **Start with Explore/Librarian** for discovery before implementation
2. **Use Metis for complex tasks** to clarify requirements first
3. **Consult Oracle sparingly** - it's expensive and read-only
4. **Continue sessions** instead of starting fresh for follow-ups
5. **Run independent tasks in parallel** for efficiency
6. **Let background tasks complete** without polling
7. **Review plans with Momus** before major implementations

## Agent-Driven Development Workflow

1. **Discovery Phase**
   - Explore Agent: Understand existing code
   - Librarian Agent: Research external references

2. **Planning Phase**
   - Metis Agent: Analyze requirements and scope
   - Momus Agent: Review and validate plan

3. **Implementation Phase**
   - Build Agent: Write code
   - Oracle Agent: Consult on complex issues (if needed)

4. **Review Phase**
   - Oracle Agent: Architecture review (if needed)
   - Build Agent: Verification and testing

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial agent definitions for Financing project |
