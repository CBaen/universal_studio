# AI Collaboration Workspace

**Purpose**: Asynchronous collaboration between Claude (Anthropic) and Gemini (Google) on the Headless Video Production Pipeline project.

**Owner**: @CBaen (Human)
**Repository**: https://github.com/CBaen/universal_studio

---

## How This Works

### Workflow
1. **Claude** writes code, commits to repo, leaves tasks in `claude_to_gemini/`
2. **Gemini** pulls repo, reads tasks, completes work, commits back
3. **Gemini** leaves notes/questions in `gemini_to_claude/`
4. **Claude** reviews Gemini's work in next session, continues iteration
5. **Human** reviews both AI contributions via GitHub commits

### Directory Structure

```
.ai_collaboration/
├── README.md                    (This file - collaboration rules)
├── claude_to_gemini/            (Tasks Claude assigns to Gemini)
│   ├── CURRENT_TASK.md          (Active task for Gemini)
│   ├── task_queue.md            (Backlog of tasks)
│   └── context/                 (Context files Gemini needs)
├── gemini_to_claude/            (Gemini's responses and questions)
│   ├── COMPLETED.md             (What Gemini finished)
│   ├── QUESTIONS.md             (Questions for Claude/Human)
│   └── work_log.md              (Gemini's work journal)
└── shared/                      (Shared documentation)
    ├── project_status.md        (Current project state)
    ├── decisions.md             (Key architectural decisions)
    └── quality_standards.md     (Quality requirements)
```

---

## Communication Protocol

### For Claude

**Before committing**:
1. Write clear task description in `claude_to_gemini/CURRENT_TASK.md`
2. Update `shared/project_status.md` with latest state
3. Commit all code changes with descriptive messages
4. Tag commits with `[CLAUDE]` prefix

**Commit message format**:
```
[CLAUDE] Brief description

- Detailed change 1
- Detailed change 2

For Gemini: [pointer to task file or inline instructions]
```

### For Gemini

**Before committing**:
1. Read `claude_to_gemini/CURRENT_TASK.md`
2. Complete assigned work
3. Document work in `gemini_to_claude/COMPLETED.md`
4. Update `shared/project_status.md`
5. Move completed task to `gemini_to_claude/work_log.md`
6. Tag commits with `[GEMINI]` prefix

**Commit message format**:
```
[GEMINI] Brief description

- Detailed change 1
- Detailed change 2

Status: [COMPLETE | BLOCKED | IN_PROGRESS]
Notes: [any context for Claude/Human]
```

### For Humans

**Reviewing AI work**:
- Check commit history for `[CLAUDE]` and `[GEMINI]` tags
- Read `gemini_to_claude/QUESTIONS.md` for blockers
- Review `shared/project_status.md` for current state
- Provide direction in issues or direct file edits

---

## Quality Standards

All AI contributors must follow:
- **User's requirement**: 90+ quality (documented in `shared/quality_standards.md`)
- **Testing**: All code must have tests
- **Documentation**: All functions must have docstrings
- **Commits**: Small, atomic commits with clear messages
- **No breaking changes**: Without explicit approval

---

## Conflict Resolution

If Claude and Gemini disagree:
1. Document disagreement in `shared/decisions.md`
2. Present options to human owner
3. Human makes final decision
4. Losing AI acknowledges and adapts

---

## Current Project: TTS Engine (92/100 Quality)

**Status**: Session 3 complete, ready for Colab deployment
**Owner AI**: Claude (Sessions 1-3)
**Next AI**: Gemini (Session 4)
**Blocker**: Human must obtain reference audio and run Colab

See `claude_to_gemini/CURRENT_TASK.md` for details.

---

**Last Updated**: 2025-11-19 by Claude
**Session**: 3
**Human Approval**: Required for major architectural changes
