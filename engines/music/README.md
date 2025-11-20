# Music Engine — Headless Video Production Pipeline

## Objective
Build a **production-grade music generation engine** for creating background music, intro/outro tracks, and atmospheric audio for documentary and true crime content.

## Target Quality
**Professional documentary soundtrack quality** suitable for YouTube and broadcast content.

## Architecture Philosophy
This is **not** a simple API wrapper. This is an **intelligent music synthesis engine** that:
- Combines multiple generation models (MusicGen, AudioCraft, Suno API)
- Optimizes for documentary and true crime musical styles
- Provides mood and genre control for narrative pacing
- Implements seamless looping and transitions
- Handles variable duration (5s intros to 5min background tracks)

## Key Requirements
1. **Quality**: Professional, broadcast-ready music
2. **Mood Control**: Suspenseful, mysterious, dramatic, ambient
3. **Consistency**: Musical coherence across episodes
4. **Licensing**: Royalty-free, no copyright issues
5. **Flexibility**: Variable duration and seamless loops

## Use Cases
- **Background Music**: Ambient tracks for scene narration (30s-5min)
- **Intro/Outro**: Episode theme music (10-30s)
- **Transitions**: Musical bridges between scenes (5-15s)
- **Dramatic Moments**: Tension-building music for reveals (10-60s)
- **Credits**: End credits music (30-90s)

## Directory Structure
```
music/
├── research/           # Research and benchmarks
│   ├── models/         # Model comparisons
│   ├── benchmarks/     # Quality tests
│   └── findings.md     # Research report
├── docs/               # Architecture documentation
│   ├── architecture.md # System design
│   ├── api.md          # Provider interface
│   └── licensing.md    # Copyright and licensing
├── providers/          # Implementation
│   ├── base.py         # MusicProvider abstract class
│   ├── local_musicgen.py  # MusicGen (local)
│   ├── suno_api.py     # Suno API (commercial)
│   └── hybrid.py       # Intelligent routing
├── models/             # Model weights (MusicGen checkpoints)
├── cache/              # Generated audio cache
├── tests/              # Testing suite
└── requirements.txt    # Python dependencies
```

## Research Status
**PHASE: NOT STARTED**

Priority tasks:
- [ ] Research current SOTA music models (MusicGen, AudioCraft, Suno)
- [ ] Benchmark quality for documentary/true crime style
- [ ] Analyze licensing and copyright requirements
- [ ] Design provider architecture
- [ ] Test mood and genre control

## Development Phases
1. **Research** — Identify best models for documentary music
2. **Design** — Architect hybrid local/API pipeline
3. **Implementation** — Build providers
4. **Testing** — Validate quality and mood control
5. **Optimization** — Licensing and cost efficiency

---

**Last Updated**: 2025-11-19
**Status**: Not Started — Awaiting TTS Engine completion
**Priority**: Medium (after TTS is stable)
