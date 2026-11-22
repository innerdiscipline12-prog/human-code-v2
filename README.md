# The Human Code — V3

The Human Code is a black-and-gold psychological content engine.

## V3 content pipeline

Topic → Angle → Hook → Escalating 7-point narrative → Payoff → Originality check → Visual render

### Retention design

Each seven-point narrative is deliberately structured to create forward momentum:

1. Hook / pattern interrupt
2. Curiosity
3. Tension
4. Escalation
5. Reframe
6. Consequence
7. Payoff

The engine favors concise psychological statements and avoids flat motivational endings.

### Originality protection

The state file now keeps recent narrative signatures. Candidate narratives are rejected when their semantic token similarity to recent content is too high. Topic repetition is also lightly penalized.

### Validation

Every production workflow run first executes:

`python src/generate.py --stress-test 20`

The 20-generation gate checks:

- seven unique points per post
- semantic duplicate protection
- minimum impact score
- consecutive-run uniqueness

Only after the gate passes does the workflow generate the production asset.

### Visual identity

- 1080×1350
- black background
- gold primary typography
- white body text
- Montserrat Bold
- THE HUMAN CODE watermark
- existing cover/list-post structure preserved

### Future learning loop

The V3 content layer is intentionally separated from publishing and analytics so future Facebook/Instagram feedback can learn which topics, angles, hooks and narrative structures produce stronger watch time, retention, replays and completion.
