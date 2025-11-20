# Headless Video Production Pipeline

**Owner**: @CBaen
**Repository**: https://github.com/CBaen/universal_studio
**Status**: 🟡 In Development - TTS Engine Phase

---

## Project Overview

Automated video production pipeline for creating high-quality documentary and narrative content. Current focus: Production-grade Text-to-Speech (TTS) engine achieving 90+ quality (vs. ElevenLabs 94/100).

**Quality Philosophy**: "Quality is the most important... we will never choose the quicker or easier option"

---

## Current Component: TTS Engine

**Target**: 92/100 quality with Freeman + Attenborough blend voice
**Status**: Code complete, awaiting Colab deployment and quality validation

### Architecture
- **Tier 1 (Piper)**: Fast prototyping (72/100 quality, <1s generation)
- **Tier 3 (Higgs Audio V2)**: Production quality (92/100, zero-shot voice cloning)

### Quick Start

**For Users**:
```bash
# 1. Install dependencies
pip install -r engines/tts/requirements.txt

# 2. Test Piper (prototyping tier)
cd engines/tts
python test_provider.py

# 3. For production quality, follow Colab setup
# See: engines/tts/HIGGS_SETUP_GUIDE.md
```

**For Production (Higgs V2)**:
1. Read `engines/tts/HIGGS_SETUP_GUIDE.md`
2. Obtain reference audio (Freeman + Attenborough voice)
3. Upload `colab/higgs_audio_worker.ipynb` to Google Colab
4. Follow Phase 1-6 instructions

---

## AI Collaboration Workspace

This project uses **asynchronous AI collaboration** through GitHub:

- **Claude (Anthropic)**: Primary development (Sessions 1-3)
- **Gemini (Google)**: Code review, testing, supporting infrastructure

**Communication Directory**: `.ai_collaboration/`
- Tasks assigned in `claude_to_gemini/CURRENT_TASK.md`
- Work completed in `gemini_to_claude/COMPLETED.md`
- Project status in `shared/project_status.md`

See `.ai_collaboration/README.md` for collaboration protocol.

---

## Project Structure

```
headless_video_production_pipeline_codebase/
├── .ai_collaboration/           # AI-to-AI communication
│   ├── claude_to_gemini/        # Tasks for Gemini
│   ├── gemini_to_claude/        # Gemini's responses
│   └── shared/                  # Shared documentation
│
├── engines/
│   └── tts/                     # Text-to-Speech engine
│       ├── providers/           # TTS provider implementations
│       ├── models/              # Piper voice models (*.onnx)
│       ├── cache/               # Generated audio cache
│       ├── colab/               # Google Colab notebooks
│       ├── research/            # Research and benchmarks
│       └── *.md                 # Documentation
│
├── colab/                       # Google Colab notebooks
│   └── higgs_audio_worker.ipynb # Higgs V2 production worker
│
└── README.md                    # This file
```

---

## Documentation

### For Users
- **Setup**: `engines/tts/HIGGS_SETUP_GUIDE.md` (comprehensive Colab setup)
- **Quick Start**: `engines/tts/QUICK_START.md` (Piper prototyping)
- **Troubleshooting**: `engines/tts/TROUBLESHOOTING.md` (common issues)

### For Developers
- **Architecture**: `engines/tts/research/findings.md` (12-model analysis)
- **Session Logs**: `engines/tts/SESSION_*.md` (detailed session notes)
- **API Reference**: `engines/tts/providers/base.py` (AudioProvider interface)

### For AI Contributors
- **Collaboration Protocol**: `.ai_collaboration/README.md`
- **Current Tasks**: `.ai_collaboration/claude_to_gemini/CURRENT_TASK.md`
- **Quality Standards**: `.ai_collaboration/shared/quality_standards.md`
- **Project Status**: `.ai_collaboration/shared/project_status.md`

---

## Current Status (Session 3)

**Completed**:
- ✅ TTS research (12 models evaluated)
- ✅ Piper implementation (72/100 quality, prototyping tier)
- ✅ Higgs Audio V2 setup (92/100 quality, production tier)
- ✅ Colab notebook created
- ✅ Comprehensive documentation

**Pending**:
- ⏳ Reference audio acquisition (human task)
- ⏳ Colab deployment and testing (human task)
- ⏳ Quality validation (90+ requirement)
- ⏳ Long-form consistency testing (100+ scenes)
- ⏳ Production integration

**Blocker**: Human must obtain reference audio and run Colab notebook

---

## Quality Requirements

**Minimum**: 90/100 vs. ElevenLabs (94/100)

**Voice Profile** (Freeman + Attenborough blend):
- Pitch: 95-120 Hz (deep, authoritative)
- Pacing: 135-155 WPM with dramatic variation
- Timbre: Warm with crystal clarity
- Emotion: Authoritative wonder, trustworthy storytelling

**Use Cases**:
- Documentary narration (9+ hour long-form content)
- Human conversation-grade production
- Professional broadcast quality

---

## Contributing

### For AIs
See `.ai_collaboration/README.md` for collaboration protocol.

**Commit Format**:
```
[AI_NAME] Brief description

- Detailed change 1
- Detailed change 2

For [Other AI/Human]: [pointer to task or notes]
```

### For Humans
1. Read current project status: `.ai_collaboration/shared/project_status.md`
2. Review open questions: `.ai_collaboration/gemini_to_claude/QUESTIONS.md`
3. Check current tasks: `.ai_collaboration/claude_to_gemini/CURRENT_TASK.md`
4. Make changes and commit with descriptive messages

---

## License

[To be determined]

---

## Contact

**Owner**: @CBaen
**Repository Issues**: https://github.com/CBaen/universal_studio/issues

---

**Last Updated**: 2025-11-19 (Session 3 - Claude)
**Next Session**: Gemini (code review and testing infrastructure)
