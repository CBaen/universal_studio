# Current Task for Gemini

**Assigned by**: Claude (Session 3)
**Date**: 2025-11-19
**Priority**: HIGH
**Status**: AWAITING_GEMINI
**Estimated Effort**: 2-4 hours

---

## Context: What Claude Built (Sessions 1-3)

I completed the TTS engine architecture for production-quality documentary narration:

**Session 1**: Research (12 TTS models analyzed)
**Session 2**: Piper implementation (72/100 quality - prototyping only)
**Session 3**: Higgs Audio V2 setup (92/100 quality - production ready)

**Files created**:
- `engines/tts/providers/colab_higgs.py` (Higgs provider - 291 lines)
- `engines/tts/colab/higgs_audio_worker.ipynb` (Colab notebook)
- `engines/tts/test_higgs_provider.py` (Integration tests)
- `engines/tts/HIGGS_SETUP_GUIDE.md` (Comprehensive guide)
- `engines/tts/SESSION_3_HIGGS_SETUP.md` (Session summary)

**Status**: All code complete, ready for deployment testing

---

## Your Task: Create Supporting Infrastructure

Since you **cannot** access Google Colab or generate actual audio, focus on tasks you **can** complete autonomously:

### Task 1: Create Long-Form Consistency Test (HIGH PRIORITY)

**File**: `engines/tts/test_long_form_consistency.py`

**Purpose**: Test voice consistency across 100+ scenes (simulate 9-hour content)

**Requirements**:
```python
"""
Test voice consistency for long-form content (9+ hours)

Simulates generating 100-200 scenes and checks for:
- Voice drift (spectral analysis)
- Quality degradation over time
- Cache efficiency
- Memory usage

Note: This test will only work AFTER human completes Colab setup.
Until then, use mock data or Piper for simulation.
"""

def test_voice_drift():
    # Generate 100 scenes with same voice
    # Compare spectral characteristics of scene 1 vs scene 100
    # Flag if drift > 5%
    pass

def test_cache_efficiency():
    # Test that repeated text returns cached audio (0.0s generation)
    # Verify 100% cache hit rate for duplicates
    pass

def test_memory_usage():
    # Monitor memory over 200-scene generation
    # Ensure no memory leaks
    pass
```

**Deliverable**: Working test file with detailed documentation

---

### Task 2: Create Temperature Comparison Script (MEDIUM PRIORITY)

**File**: `engines/tts/research/compare_temperatures.py`

**Purpose**: Test different temperature settings (0.2, 0.3, 0.4, 0.5) and document impact on voice quality

**Requirements**:
```python
"""
Compare Higgs temperature settings for optimal quality

Tests same text with different temperatures:
- 0.2 (very consistent, low variation)
- 0.3 (balanced - recommended)
- 0.4 (natural variation)
- 0.5 (maximum expressiveness)

Generates comparison report for human to review.
"""

temperatures = [0.2, 0.3, 0.4, 0.5]
test_text = "In a world where true crime narratives captivate millions..."

for temp in temperatures:
    # Generate audio with each temperature
    # Save to separate files
    # Document generation time, perceived quality notes
    pass
```

**Deliverable**: Script + markdown report template

---

### Task 3: Enhance HIGGS_SETUP_GUIDE.md (LOW PRIORITY)

**File**: `engines/tts/HIGGS_SETUP_GUIDE.md`

**Improvements needed**:
1. Add troubleshooting section for "Voice doesn't match reference"
2. Add examples of good vs bad reference audio characteristics
3. Add section on pitch analysis (how to verify 95-120 Hz)
4. Add flowchart for quality validation decision tree
5. Add "Common Mistakes" section based on predicted issues

**Deliverable**: Enhanced guide with new sections

---

### Task 4: Create Batch Generation Script (MEDIUM PRIORITY)

**File**: `engines/tts/batch_generate.py`

**Purpose**: Generate multiple scenes efficiently from JSON input

**Requirements**:
```python
"""
Batch audio generation from scene list

Input: scenes.json
[
  {"id": "scene_001", "text": "...", "emotion": "neutral"},
  {"id": "scene_002", "text": "...", "emotion": "dramatic"}
]

Output: cache/higgs/scene_001.wav, scene_002.wav, etc.
Generates progress report and timing metrics.
"""

def load_scenes(json_path):
    pass

def generate_batch(scenes, provider):
    # Generate all scenes
    # Track progress
    # Report failures
    # Generate summary report
    pass
```

**Deliverable**: Working batch script + example scenes.json

---

### Task 5: Code Review of HiggsAudioProvider (HIGH PRIORITY)

**File**: `engines/tts/providers/colab_higgs.py`

**Review for**:
- **Bugs**: Logic errors, edge cases
- **Error handling**: Are all failure modes covered?
- **Type hints**: Are they complete and accurate?
- **Documentation**: Are docstrings clear?
- **Performance**: Any obvious optimizations?
- **Security**: Any risks (e.g., URL injection)?

**Deliverable**: Create `engines/tts/CODE_REVIEW_HIGGS.md` with findings and suggested fixes

---

### Task 6: Create Troubleshooting Runbook (MEDIUM PRIORITY)

**File**: `engines/tts/TROUBLESHOOTING.md`

**Content**:
```markdown
# TTS Engine Troubleshooting

## Issue: "Connection refused to Colab worker"
**Symptoms**: ...
**Causes**: ...
**Solutions**: ...

## Issue: "Voice quality below 90/100"
**Symptoms**: ...
**Causes**: ...
**Solutions**: ...

## Issue: "Generation timeout after 5 minutes"
**Symptoms**: ...
**Causes**: ...
**Solutions**: ...

[etc. - create 10+ common issues with solutions]
```

**Deliverable**: Comprehensive troubleshooting guide

---

## What You CANNOT Do (Human Required)

- ❌ Obtain reference audio (Freeman + Attenborough voice)
- ❌ Upload notebook to Google Colab
- ❌ Run Colab cells to test Higgs
- ❌ Test HiggsAudioProvider (requires running Colab worker)
- ❌ Listen to audio quality and make 90+ judgment

**Why this matters**: These tasks require human senses or platform access you don't have.

---

## Success Criteria

Before marking your work complete:

- ✅ All 6 tasks completed
- ✅ All new files have tests (if applicable)
- ✅ All new files have comprehensive docstrings
- ✅ Code follows existing patterns in `providers/base.py` and `providers/local_piper.py`
- ✅ Documentation is clear and actionable
- ✅ Commit messages follow `[GEMINI]` format (see `.ai_collaboration/README.md`)
- ✅ Updated `gemini_to_claude/COMPLETED.md` with your work summary
- ✅ Updated `shared/project_status.md` with new state

---

## Deliverables Checklist

When you're done, you should have committed:

- [ ] `test_long_form_consistency.py` (Task 1)
- [ ] `research/compare_temperatures.py` (Task 2)
- [ ] Enhanced `HIGGS_SETUP_GUIDE.md` (Task 3)
- [ ] `batch_generate.py` (Task 4)
- [ ] `CODE_REVIEW_HIGGS.md` (Task 5)
- [ ] `TROUBLESHOOTING.md` (Task 6)
- [ ] `gemini_to_claude/COMPLETED.md` (Your work summary)
- [ ] Updated `shared/project_status.md`

---

## Questions? Blockers?

If you encounter issues:
1. Document in `gemini_to_claude/QUESTIONS.md`
2. Mark task status as `BLOCKED` in commit message
3. Continue with tasks you can complete
4. Human/Claude will address in next session

---

## Context Files You Need

Read these files first to understand the project:

**Critical**:
- `engines/tts/providers/base.py` - Base interfaces you must follow
- `engines/tts/providers/local_piper.py` - Example provider implementation
- `engines/tts/providers/colab_higgs.py` - The file you're reviewing/extending

**Important**:
- `engines/tts/SESSION_3_HIGGS_SETUP.md` - What Claude did in Session 3
- `engines/tts/HIGGS_SETUP_GUIDE.md` - User-facing setup instructions
- `engines/tts/research/findings.md` - TTS model research (780 lines)

**Reference**:
- `.ai_collaboration/shared/quality_standards.md` - User requirements
- `.ai_collaboration/shared/project_status.md` - Current state

---

## Timeline

**Expected completion**: 1 session (2-4 hours of work)

**Priority order**:
1. Task 5 (Code Review) - Critical for quality
2. Task 1 (Long-form test) - Critical for production readiness
3. Task 4 (Batch generation) - High value for user
4. Task 2 (Temperature comparison) - Useful optimization
5. Task 6 (Troubleshooting) - Helpful but not blocking
6. Task 3 (Documentation) - Nice to have

---

**Ready to start? Read the context files, then begin with Task 5 (Code Review).**

**When done**: Commit with `[GEMINI]` tag and update `gemini_to_claude/COMPLETED.md`

---

**Assigned by**: Claude (Session 3)
**Waiting for**: Gemini (Session 4)
**Human blocker**: Reference audio + Colab setup
