# Quality Standards - Headless Video Production Pipeline

**Owner**: @CBaen (Human)
**Last Updated**: 2025-11-19 (Session 3)
**Status**: NON-NEGOTIABLE REQUIREMENTS

---

## User's Explicit Requirements

### Philosophy

> "Quality is the most important... we will never choose the quicker or easier option"
>
> "None of what you're building is speed over quality prototyping and we don't fast track anything. The longest, most extensive design with the highest quality is the most important."

**Interpretation**:
- Quality is the ONLY metric
- Speed, cost, complexity are irrelevant
- No shortcuts or "good enough" solutions
- Extensive, thorough design over rapid iteration

---

## TTS Engine Quality Requirements

### Minimum Quality Threshold

**90/100 vs. ElevenLabs (94/100)**

This is **non-negotiable**. Any engine scoring below 90/100 is rejected for production use.

**Scoring calibration**:
- Piper: 72/100 ❌ (Prototyping only)
- Chatterbox: 89/100 ❌ (Below threshold)
- **Higgs Audio V2: 92/100** ✅ (Production approved)

### Voice Profile: Freeman + Attenborough Blend

**Required Characteristics**:

| Attribute | Specification | How to Verify |
|-----------|---------------|---------------|
| **Pitch** | 95-120 Hz (deep but not extreme) | Spectral analysis (librosa.yin) |
| **Pacing** | 135-155 WPM with dramatic variation | Word count / duration |
| **Timbre** | Warm with crystal clarity | Chest-forward resonance, clear articulation |
| **Emotion** | Authoritative wonder, trustworthy storytelling | Subjective human assessment |
| **Resonance** | Chest-forward, deep | Spectral centroid analysis |
| **Clarity** | Crystal clear articulation (Attenborough trait) | No mumbling, clear consonants |

**Reference Examples**:
- Morgan Freeman: Planet Earth narration
- David Attenborough: Blue Planet narration
- Ideal: Blend of both (Freeman's warmth + Attenborough's clarity)

### Use Cases

**Primary**: Documentary narration
- Long-form content (9+ hours)
- Consistent voice across 3000+ scenes
- Professional broadcast quality
- No voice drift over time

**Secondary**: Human conversation-grade production
- Multi-story formats
- Emotional range (neutral, dramatic, investigative, emotional)
- Natural prosody and pacing

### Quality Validation Criteria

Before declaring audio "production ready", verify:

**Objective Metrics** (measurable):
- [ ] Pitch range: 95-120 Hz ±10 Hz
- [ ] Speaking rate: 135-155 WPM ±10 WPM
- [ ] Sample rate: ≥22050 Hz
- [ ] Bit depth: 16-bit or higher
- [ ] No clipping (peak amplitude < 0 dB)
- [ ] No artifacts (robotic sound, clicks, pops)

**Subjective Metrics** (human judgment):
- [ ] Overall quality: 90+/100 vs. ElevenLabs
- [ ] Voice similarity to reference: ≥90%
- [ ] Timbre: Warm, authoritative, clear
- [ ] Emotion: Appropriate to scene content
- [ ] Consistency: Same voice across all scenes
- [ ] Naturalness: No uncanny valley effect

**Long-Form Metrics** (9+ hour content):
- [ ] Voice consistency: <5% drift over 3000 scenes
- [ ] Volume consistency: ±3 dB max variance
- [ ] Pacing consistency: ±10 WPM variance
- [ ] No quality degradation over time

---

## Code Quality Standards

### All Code Must Have

**1. Tests**
- Unit tests for all functions
- Integration tests for providers
- Edge case coverage
- Test coverage ≥80%

**2. Documentation**
- Module-level docstrings
- Function-level docstrings (Google style)
- Type hints on all parameters and returns
- Inline comments for complex logic

**3. Error Handling**
- All failure modes anticipated
- Clear, actionable error messages
- Graceful degradation where possible
- Logging for debugging

**4. Performance**
- No obvious inefficiencies
- Caching where appropriate
- Lazy loading for large resources
- Memory leak prevention

### Code Review Checklist

Before committing:
- [ ] Code follows existing patterns
- [ ] No magic numbers (use constants)
- [ ] No hardcoded paths (use Path objects)
- [ ] No secrets in code (use env vars)
- [ ] Commits are atomic and focused
- [ ] Commit messages are descriptive
- [ ] No commented-out code
- [ ] No debug print statements

---

## AI Collaboration Standards

### What Requires Human Approval

**Major Changes**:
- ❌ Architectural redesign
- ❌ Changing quality thresholds
- ❌ Adding paid dependencies
- ❌ Removing existing functionality
- ❌ Changing voice profile specifications

**Auto-Approved**:
- ✅ Bug fixes
- ✅ Documentation improvements
- ✅ Test additions
- ✅ Performance optimizations (if no quality impact)
- ✅ New features (if additive, not breaking)

### Quality Gates

**Before marking work "complete"**:
1. All tests pass
2. No reduction in quality metrics
3. Documentation updated
4. Code reviewed (by other AI if possible)
5. Commit messages clear
6. No known bugs or blockers

---

## Failure Modes to Avoid

### Historical Mistakes (Learn From These)

**Session 1-2 Lessons**:
1. ❌ Assuming "3-tier hybrid" when user needs "single best engine"
   - **Fix**: Focus on Higgs only for production

2. ❌ Framing work as "prototyping tier"
   - **Fix**: All production code is permanent, not throwaway

3. ❌ Chatterbox (89/100) was explored despite being below 90+ threshold
   - **Fix**: Immediately reject any solution below quality requirement

**General Anti-Patterns**:
- ❌ "Good enough for now" thinking
- ❌ Speed over quality tradeoffs
- ❌ Deferring quality validation to later
- ❌ Assuming user will compromise on requirements
- ❌ Building features user didn't request

---

## Success Definition

**TTS Engine is "Production Ready" when**:

1. ✅ Generated audio achieves 90+/100 quality (human validated)
2. ✅ Voice matches Freeman + Attenborough specifications
3. ✅ Consistency across 100+ scenes validated (no drift)
4. ✅ All tests passing (unit, integration, long-form)
5. ✅ Documentation complete (setup, troubleshooting, API)
6. ✅ Human has successfully generated audio and approved quality
7. ✅ Caching working (100% hit rate for repeated text)
8. ✅ No known bugs or blockers

**Not Ready If**:
- ⚠️ Quality unvalidated by human ears
- ⚠️ Voice cloning untested with real reference audio
- ⚠️ Long-form consistency untested (>100 scenes)
- ⚠️ Colab setup not completed
- ⚠️ Any quality metric below threshold

---

## Priority Framework

When choosing between options:

**Always Choose**:
1. **Quality** > Speed
2. **Thoroughness** > Convenience
3. **Long-term robustness** > Quick fix
4. **User requirements** > AI assumptions
5. **Production-grade** > Prototype-grade

**Question to Ask**:
> "Does this meet the user's requirement for 'the longest, most extensive design with the highest quality'?"

If answer is no: **Don't do it.**

---

**These standards are immutable. If unclear, ask the human.**

**Last Reviewed**: Session 3 (Claude)
**Next Review**: After Gemini's session
