# Profile: talk

For spoken sources: livestreams, podcasts, interviews, Q&A clips, talks
(e.g. Anh Duy Nguyen's livestream clips). The owner keeps these for the
speaker's own voice: direct, blunt, real. So the speaker's words come first.

## Source quirks

- Auto-generated subtitles: short lines with blank lines between. Join them
  into running text before reading.
- Speech-to-text errors: fix names from context ("tấn hưng" = Tuấn Hưng,
  "Camala" = Kamala Harris, "Osama Baden" = Osama bin Laden, "đại bàn" =
  đại bàng). If you are not sure what a word was, leave that part out
  rather than guess. Write the fixes into the book file's notes.
- Clips cut from a stream: a topic can start or stop in the middle. If you
  cannot tell what the speaker is answering or talking about, skip it.
- Q&A: the speaker reads a viewer's question aloud, then answers. Questions
  often end with "anh?".

## Note forms, in this order of preference

1. **Nguyên văn** - the speaker's own sentences, copied. Only remove filler
   that carries nothing ("nó nó nó", "đó đó", "à", "tức là" said three times)
   and repeated words. Do not polish into book language, do not make it
   polite, keep his way of talking ("mấy em", "đơn giản là thế đó").
2. **Hỏi đáp** - when the answer only makes sense with the question:
   ```
   Hỏi: <the viewer's question, cleaned, one line>.
   Anh Duy: <his answer in his words, cut but not rewritten>
   ```
3. **Rút gọn** - a long answer cut down. Keep his key sentences word for
   word and drop the rest; join with "..." only where a cut would confuse.
4. **Tóm tắt** - only when an answer rambles too long to cut (more than
   ~120 words of his own that you would keep). Summarize in plain words and
   put his sharpest phrase in quotes inside it.

## Voice rules

- Swearing and insults: keep a strong word when it is the point of the
  sentence. Drop swearing used as filler, and insults thrown at a viewer
  ("mày bị ngu hả"), unless the owner asked to keep them (see the book file).
- Every note says who is speaking: "Anh Duy:" or "Theo anh Duy, ...".
  His claims are his view, not facts.
- If he states a fact that is clearly wrong and you know it well, add one
  line `Ngoài video: ...` with the right fact. Do not argue with opinions.
- No need to name him in every sentence, but the note must still stand
  alone: the topic must be clear without the video (who protests where,
  which country, which year).

## What to pick

- clear opinions with a reason ("Đi bộ đội ở Việt Nam là thiêng liêng, đi
  lính Mỹ là lợi ích"),
- short, sharp lines that sound like him,
- explanations of how a country or a system works,
- advice on how to think ("đọc hết luật rồi mới nói").

Skip: greetings, reading donations, jokes that need the video, gossip about
people with no wider point, unclear clipped parts.

## Sections

One `#` per video, named by its topic in a few words (from the file name),
not the whole long title: `# Biểu tình ở Pháp, huề cả làng`.

## Book file

One book file for the whole speaker or channel, e.g. `anh-duy-nguyen.book.md`.
List every video under `## Sources` with its position:

```
## Sources
- <file name> | done
- <file name> | char 7000
- <file name> | new
```

`next` continues the first source that is not done.
