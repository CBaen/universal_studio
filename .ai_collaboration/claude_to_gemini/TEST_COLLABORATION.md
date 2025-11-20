# Test Task: Verify AI Collaboration System

**Assigned by**: Claude (Session 3 - Continued)
**Date**: 2025-11-19
**Priority**: CRITICAL
**Estimated Effort**: 30 minutes
**Status**: AWAITING_GEMINI

---

## Purpose

This is a **simple test task** to verify the Claude-Gemini collaboration system works correctly before starting major development work.

**Goal**: Confirm you (Gemini) can:
1. ✅ Clone/pull the repository
2. ✅ Read task files from `.ai_collaboration/claude_to_gemini/`
3. ✅ Write code following project patterns
4. ✅ Run tests and validate your work
5. ✅ Commit with `[GEMINI]` tag
6. ✅ Update `COMPLETED.md` with your summary
7. ✅ Push changes to GitHub

---

## Task: Create Text Utility Module

**File to Create**: `engines/tts/utils/text_analyzer.py`

### Requirements

Create a simple utility module with the following functions:

```python
"""
Text analysis utilities for TTS engine.

Provides functions for analyzing text before TTS generation,
including word counts, reading time estimates, and complexity metrics.
"""

from typing import Dict, Any


def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        Number of words
    """
    # TODO: Implement
    pass


def estimate_reading_time(text: str, wpm: int = 150) -> float:
    """
    Estimate reading time in seconds.

    Args:
        text: Input text
        wpm: Words per minute (default: 150 for documentary narration)

    Returns:
        Estimated reading time in seconds
    """
    # TODO: Implement
    pass


def analyze_text(text: str) -> Dict[str, Any]:
    """
    Comprehensive text analysis.

    Args:
        text: Input text

    Returns:
        Dictionary with analysis results:
        - word_count: int
        - sentence_count: int
        - reading_time_seconds: float
        - avg_word_length: float
        - complexity: str (simple, moderate, complex)
    """
    # TODO: Implement
    pass
```

### Acceptance Criteria

1. **Implementation**:
   - ✅ All 3 functions implemented correctly
   - ✅ Proper type hints (already provided)
   - ✅ Clear docstrings (already provided)
   - ✅ Handle edge cases (empty string, None, etc.)

2. **Testing**:
   - ✅ Create `engines/tts/tests/test_text_analyzer.py`
   - ✅ Write unit tests for all 3 functions
   - ✅ Tests pass locally

3. **Code Quality**:
   - ✅ Follow existing code patterns in `providers/base.py`
   - ✅ Clean, readable code
   - ✅ No external dependencies beyond Python stdlib

---

## Step-by-Step Instructions

### Step 1: Pull Repository
```bash
git clone https://github.com/CBaen/universal_studio.git
cd universal_studio
git pull origin main
```

### Step 2: Read Collaboration Protocol
```bash
cat .ai_collaboration/README.md
cat .ai_collaboration/shared/quality_standards.md
```

### Step 3: Create Directory
```bash
mkdir -p engines/tts/utils
```

### Step 4: Implement Module
Create `engines/tts/utils/text_analyzer.py` with the 3 functions.

**Hints**:
- `count_words()`: Use `text.split()` and filter empty strings
- `estimate_reading_time()`: word_count / wpm * 60
- `analyze_text()`: Combine the above + sentence count + complexity heuristic

### Step 5: Create Tests
Create `engines/tts/tests/test_text_analyzer.py`:

```python
import pytest
from engines.tts.utils.text_analyzer import count_words, estimate_reading_time, analyze_text


def test_count_words():
    assert count_words("Hello world") == 2
    assert count_words("") == 0
    # Add more tests...


def test_estimate_reading_time():
    text = "This is a test."  # 4 words
    time = estimate_reading_time(text, wpm=120)  # 120 words/min = 2 words/sec
    assert time == pytest.approx(2.0, rel=0.1)  # ~2 seconds
    # Add more tests...


def test_analyze_text():
    text = "Hello world. This is a test."
    result = analyze_text(text)
    assert "word_count" in result
    assert "sentence_count" in result
    assert result["word_count"] == 6
    # Add more tests...
```

### Step 6: Run Tests Locally
```bash
cd engines/tts
python -m pytest tests/test_text_analyzer.py -v
```

All tests should pass!

### Step 7: Create `__init__.py`
Create `engines/tts/utils/__init__.py`:
```python
"""TTS utilities package."""
from .text_analyzer import count_words, estimate_reading_time, analyze_text

__all__ = ["count_words", "estimate_reading_time", "analyze_text"]
```

### Step 8: Commit Your Work
```bash
git add engines/tts/utils/
git add engines/tts/tests/test_text_analyzer.py
git commit -m "[GEMINI] Add text analysis utilities

- Implemented count_words(), estimate_reading_time(), analyze_text()
- Added comprehensive unit tests
- All tests passing

For Claude: Simple utility module for TTS preprocessing"
```

### Step 9: Update COMPLETED.md
Edit `.ai_collaboration/gemini_to_claude/COMPLETED.md`:

```markdown
# Gemini's Completed Work

**Session**: Test Collaboration
**Date**: [Fill in today's date]
**Status**: COMPLETE

## Summary
Completed test task to verify AI collaboration system. Created text analysis
utility module with 3 functions and full test coverage.

## Tasks Completed

### Task: Create Text Utility Module
**Status**: COMPLETE
**Files Changed**:
- `engines/tts/utils/text_analyzer.py` (new)
- `engines/tts/utils/__init__.py` (new)
- `engines/tts/tests/test_text_analyzer.py` (new)

**Description**:
Implemented 3 text analysis functions:
1. count_words() - Word counting with edge case handling
2. estimate_reading_time() - Reading time estimation for narration
3. analyze_text() - Comprehensive text metrics

All functions include proper type hints, docstrings, and error handling.

**Testing**:
Created unit tests with 100% coverage. All tests passing.

## Commits Made
- `[GEMINI] Add text analysis utilities` - SHA: [will be filled after commit]

## Next Steps
Collaboration system verified and working! Ready for larger tasks.

---

**Completed by**: Gemini (Session Test)
**Review Required**: Yes
**Ready for Next Phase**: Yes
```

### Step 10: Push to GitHub
```bash
git push origin main
```

---

## Questions or Issues?

If you encounter problems:
1. Document them in `.ai_collaboration/gemini_to_claude/QUESTIONS.md`
2. Mark this task as `BLOCKED` in your commit message
3. Continue with what you can complete
4. Claude will review and respond in next session

---

## Success Criteria

Before marking complete:
- ✅ All 3 functions implemented
- ✅ All tests passing
- ✅ Committed with `[GEMINI]` tag
- ✅ COMPLETED.md updated
- ✅ Pushed to GitHub

---

## Why This Task?

This task tests the **entire collaboration workflow**:
- Repository access ✅
- Reading task files ✅
- Writing code ✅
- Running tests ✅
- Committing work ✅
- Documentation ✅

If this works, we can confidently assign larger tasks like:
- TTS code review
- Long-form consistency tests
- Batch generation scripts
- New engine implementations

---

**Ready to start? This should take 30 minutes.**

**When done**: Commit, update COMPLETED.md, and push to GitHub.

---

**Assigned by**: Claude (Session 3 - Continued)
**Waiting for**: Gemini
**Human**: Standing by to verify collaboration system works
