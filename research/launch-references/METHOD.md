# How this review works

20 October 2026. The question is which visible choices help a short product film explain a task. This is a selected reference collection, not a sample of all launches or a study of sales performance.

## Inputs

- 460 downloaded source entries, about 10 hours in total. Their original IDs have gaps; they are not numbered 1–460.
- SHA256 was recomputed for every source. All 460 hashes match the existing Watch index. All 460 files have different hashes. This rules out identical files. A separate check found two pairs of the same edit in different encodes: 027/034 and 121/122. The comparison counts each pair once, giving 458 distinct edits after these known duplicates. See [the duplicate evidence](duplicates.json); other missed duplicates remain possible.
- `sources.json` keeps public URLs, file names, hashes, Watch IDs and fresh ffprobe results. Two files, 440 and 508, contain no audio stream. That says nothing about sound on another version of those posts.
- The local archive contains 36,274 chronological samples and 1,421 contact sheets. Most samples are one second apart. A prepared sheet is not a completed review.

The collection includes feature demos, brand films, event ads, hardware demonstrations and longer product explanations. Of the 458 edits after known duplicates, 51 are at most 30s, 153 are over 30–60s, 195 are over 60–120s and 59 are longer than two minutes. The median is about 66.4s. Do not treat the whole collection as 20-second launch clips or copy the pacing of a long demo into a short film.

“Still unclear” names what the sampled film does not establish. That is not always a flaw: an event announcement or brand film may not aim to teach a product task. Judge the finding against the film's purpose before reusing it as a rule.

The downloaded films and large evidence images stay in the local archive. This repository contains original analysis and source references. Public availability is not a licence to reuse a film's footage, music, logo or design assets.

## Reviewer and tools

Three GPT-6 Astra agents review separate source groups. They inspect every chronological sheet they list as reviewed, read short sections in order, and use denser local windows for important unclear motion. Watch provides indexed source frames, OCR and transcript context. Its `get_moment` returns existing samples; it does not promise a new high-frame-rate clip. Local ffmpeg supplies closer samples when needed.

Watch's automatic cloud vision backend was configured as Claude Sonnet 5 during setup. This pass uses Astra as the host reviewer and does not use that backend for its authored findings. The model name on a host is different from the model inside a tool. Every report names its actual scope.

Source hash checks, metadata probes and report formatting are local operations. Astra host usage is not recorded as a per-film API bill. Cost is unavailable, not zero. This pass starts no new paid audio-model requests.

## What the evidence can support

| Input | Useful for | Does not establish |
| --- | --- | --- |
| Chronological sampled frames | Story order, layouts, visible text, object states, materials | Every brief insert, exact easing or continuous movement |
| Denser sampled window | Closer transition and movement evidence at its stated rate | Events between its frames or sub-frame timing |
| ASR draft | Candidate spoken words and script structure | Heard voice delivery, music, effects or reliable silence |
| Local waveform / spectral measurements | Level changes, candidate acoustic attacks, signal timing | A drum, click, effect, musical genre or artistic sync |
| ffprobe | Stored streams, dimensions, frame rate, codecs and duration | Visual quality, listening quality or product truth |
| Astra interpretation | A proposed reading of the story and useful experiments | Actual new-viewer comprehension, retention or conversion |

Scene boundaries from one-second samples are approximate. Reports can join repeated states into a longer scene while keeping its source range. Closer windows keep the original source times. Overlap between inspected chunks is counted once.

Contact-sheet headers contain the source title. Reviewers must base product claims on the pictures or clearly marked ASR, but this is not a blind test with an unfamiliar viewer. The product-clear time is a reviewer estimate, not a measured comprehension time.

## Sound remains open

Earlier sound trials did not pass the required control set. They are separate from this Astra pass:

| Setup | Controls passed | Important failure |
| --- | --- | --- |
| Gemini Flash, video and audio | 2 of 3 | Missed delayed tones |
| Gemini 3.1 Pro Preview, video and audio | 1 of 3 | Added tones at visual cuts and in a zero-sample silent file |
| Gemini 3.1 Pro Preview, audio only | 0 of 3 | Incorrect tone timing and invented breathing/hiss in silence |

These are small setup-specific checks, not a general ranking of the models. Local ASR and sound-class candidates also do not replace listening. This review therefore leaves voice character, music style, added effects, effect counts and beat sync unverified unless an individual finding has a separate valid source. Unknown is never counted as absent.

[Stored control results](audio-controls.json) keep the expected and returned event times. The original prompts, media and raw model replies remain in the archive paths named there. The sound tests were done before this review and are not counted as new work in it.

## Reading the outputs

- `reviews/NNN.md`: a short verdict, timed scenes, sound limits, Q01–Q25 and two proposed experiments.
- `data/NNN.json`: the authored findings used to build that report. Archive-relative evidence paths show what was inspected; the media are not bundled.
- `COMPARISON.md` and `comparison.csv`: one row for each distinct reviewed edit. Same-edit copies link to their canonical review.
- `ELEMENTS.md`: positive examples of UI, motion and texture, with report links. Counts are discovery counts, not an exhaustive prevalence study.
- `coverage.json`: the actual completed and pending source IDs, with distinct edits and covered copies counted separately. A table with 460 source rows alone does not mean 460 reviews are complete.

Run `python3 -m unittest -q test_build.py` and `python3 build.py` in this directory to check the data and rebuild tables. The checks catch missing categories, source mismatches, coverage gaps and unanchored elements. A person/model still has to check the meaning of each finding against the visual evidence.

[Parent spot checks](quality-review.json) record the source sheets and closer windows checked again, including corrected interpretations. This is a selected second check, not a second full review of all films.

Workflow rules are proposals drawn from cited examples. They are not proof that a new film built with those rules is good. Its own product clarity, phone-size frames, movement, sound and final encode still need review.
