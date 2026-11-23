# Sharp upper-limsup density in Freeman's conjecture

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

Revision 3. License: Creative Commons Attribution 4.0 International (CC BY 4.0).

## Statements and coverage

For every positive integer triple `m,r,s` with `r != s`, put
`U=(mr,r)`, `V=(ms,s)`, `W_0=U` and
`W_(k+1)=W_k^(k+2) V^(k+1) W_k^(k+2)`.
The note proves that the limit has bounded positive digits, is not eventually
periodic, and has upper-limsup `m`-palindromic prefix density exactly one.
The upper limsup uses consecutive lengths in the complete enumeration of all
qualifying prefixes. The sharp maximum is therefore one, not the proposed
inverse golden ratio.

The note also proves the Fibonacci equality for every positive `m,r,s` with
`r != s`. All qualifying Fibonacci prefix lengths are `2(f_j-2)` for `j>=4`,
with the additional initial length one when `m=1`. This extends the classical
palindromic-prefix formula attributed to de Luca by Fischler. The classical
lower-liminf convention remains distinct.

The repeated-prefix corollary gives Freeman's `(*)_w` and `(*)_hat(w)` for
every real `w>1`, and `(**)_(w,w')` for every `w>1,w'>0` with nonempty initial
words. The endpoint `w'=0` holds when empty initial words are allowed; it is
not possible under the literal nonempty-word requirement in Definition 6.3.

The written proofs cover the parameterized density theorem, the block-code
classification, density transport, Fibonacci equality, transcendence using
Freeman's criterion, the repetition statements, and the correction to the
right-hand upper-limsup bound in Abdullah–Hamoud's Lemma 4.3.

The pinned Lean declaration
`D5.S1.Depth.ContinuedFractions.FreemanPalindromicDensityRefutation.result`
proves the negation of the universal upper bound using `(m,r,s)=(2,2,3)`:
https://github.com/the-omega-institute/trureturing/blob/aec68a61276de81e1e122880cd5921bac6e8f070/D5/S1/Depth/ContinuedFractions/FreemanPalindromicDensityRefutation.lean
The additional parameter ranges and corollaries have the written proofs in
`note.tex`; they are not assertions of that declaration.

## Rebuild the note

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, use a standard LaTeX installation with the listed packages:

```sh
pdflatex -halt-on-error -interaction=nonstopmode note.tex
pdflatex -halt-on-error -interaction=nonstopmode note.tex
```

The bibliography is embedded in `note.tex`; BibTeX is unnecessary. There are
no external figures, bibliography databases, generated tables, or TeX inputs.

## Exact finite checks

Python 3 with its standard library suffices:

```sh
python3 verify.py --output checker-reproduced.json
cmp checker-output.json checker-reproduced.json
```

The program uses exact integers and rational fractions, with no rounding.
It checks 103,760 construction-prefix positions and 120,000 Fibonacci-prefix
positions; 4,368 block words of lengths one through six over `{1,2,3}`
contribute 48,120 prefix positions. It also compares 56,470 prefixes with
direct rational continued-fraction evaluation and checks 504 root-growth
inequalities for integer exponents two through eight and stages through 80.
The full parameter lists and qualifying lengths are in `checker-output.json`.
These finite checks illustrate the statements; the infinite conclusions have
the written proofs in the note.

## Files and integrity

`note.tex` is the sole main source. `metadata.json` records the statements,
authors, license, and pinned mathematical source. `verify.py` and
`checker-output.json` contain the finite checks. `LICENSE.txt` records the
license, and `SHA256SUMS` lists the hashes of these files and this README.

After extracting the source archive, check its exact contents with:

```sh
sha256sum -c SHA256SUMS
```

## Scientific sources

- David M. Freeman, *Generalized palindromic continued fractions*,
  arXiv:1604.06755v2, Conjecture 7.1, p. 10; density definition, §6, p. 8.
  https://arxiv.org/abs/1604.06755v2
- Stéphane Fischler, *Palindromic prefixes and episturmian words*, §1,
  recalling de Luca's Fibonacci-prefix formula.
  https://arxiv.org/abs/math/0501420v3
- Boris Adamczewski and Jean-Paul Allouche, *Reversals and palindromes in
  continued fractions*, §5, Theorem 12.
  https://doi.org/10.1016/j.tcs.2007.03.017
- Duaa Abdullah and Jasem Hamoud, *On the asymptotic palindrome density of
  Fibonacci infinite words*, arXiv:2511.06485v2, Lemma 4.3, equation (7), pp. 7–8.
  https://arxiv.org/abs/2511.06485v2
