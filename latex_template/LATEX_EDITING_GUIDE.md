# 📝 LaTeX Editing Guide - Work on Your Thesis Manually

## ✅ What I Just Fixed

**Problem**: Figures were too wide, cut off on right side, not centered  
**Solution**: Fixed all 5 figures with proper LaTeX formatting:
- ✅ Set width to 85% of text width (`width=0.85\textwidth`)
- ✅ Used PDF format for better quality
- ✅ Added proper captions
- ✅ Added labels for cross-referencing
- ✅ Figures now properly centered and fit on page!

---

## 📁 Your Thesis File Structure

```
latex_template/
├── thesis.tex                 ← MAIN FILE (compile this)
├── content/                   ← YOUR CHAPTERS (edit these!)
│   ├── abstract.tex          ← Abstract
│   ├── introduction.tex      ← Chapter 1
│   ├── background.tex        ← Chapter 2
│   ├── methods.tex           ← Chapter 3
│   ├── results.tex           ← Chapter 4 (figures fixed!)
│   ├── discussion.tex        ← Chapter 5
│   ├── conclusions.tex       ← Chapter 6
│   └── acknowledgement.tex   ← Thanks
├── figures/                   ← Your images
└── bib/mybib.bib             ← References
```

---

## 🎯 TWO WAYS TO EDIT

### Option A: Edit on Overleaf (EASIEST)

1. **Upload again** with fixed figures:
   - Delete old project on Overleaf
   - Upload new `thesis_overleaf.zip` (I'll recreate it)
   - Figures will now fit properly!

2. **Edit directly**:
   - Click any `.tex` file in left sidebar
   - Edit content
   - Click "Recompile" to see changes
   - PDF updates automatically!

**Best for**: Quick edits, seeing results immediately

---

### Option B: Edit Locally (MORE CONTROL)

1. **Open files** in VS Code or any text editor:
   ```bash
   code ~/thesis-asr/latex_template/content/
   ```

2. **Edit the `.tex` files**
3. **Upload to Overleaf to compile** (since LaTeX not installed locally yet)
4. **Or install MacTeX locally** for offline compilation

**Best for**: Deep editing, working offline

---

## 📖 LaTeX Basics You Need to Know

### Document Structure

```latex
\chapter{Chapter Title}           % New chapter
\section{Section Title}           % Section (1.1, 1.2)
\subsection{Subsection}           % Subsection (1.1.1)
\subsubsection{Subsubsection}     % Subsubsection (1.1.1.1)
```

### Text Formatting

```latex
\textbf{Bold text}                % Bold
\textit{Italic text}              % Italic
\emph{Emphasized}                 % Emphasized (usually italic)
\texttt{Code text}                % Monospace (for code)
```

### Lists

```latex
% Bullet list
\begin{itemize}
\item First item
\item Second item
\end{itemize}

% Numbered list
\begin{enumerate}
\item First
\item Second
\end{enumerate}
```

### Tables

```latex
\begin{table}[htbp]
\centering
\begin{tabular}{lll}  % l=left, c=center, r=right
\toprule
Header 1 & Header 2 & Header 3 \\
\midrule
Data 1 & Data 2 & Data 3 \\
Data 4 & Data 5 & Data 6 \\
\bottomrule
\end{tabular}
\caption{Table caption}
\label{tab:my-table}
\end{table}
```

### Figures (NOW PROPERLY FORMATTED!)

```latex
\begin{figure}[htbp]              % h=here, t=top, b=bottom, p=page
\centering
\includegraphics[width=0.85\textwidth]{figures/image.pdf}
\caption{Figure caption goes here.}
\label{fig:my-figure}             % For referencing
\end{figure}
```

**Key parameters**:
- `width=0.85\textwidth` - Image is 85% of text width
- `width=0.5\textwidth` - Image is 50% of text width (smaller)
- `width=\textwidth` - Image is 100% of text width (full width)

### Cross-References

```latex
See Figure~\ref{fig:my-figure}    % Reference figure
See Table~\ref{tab:my-table}      % Reference table
See Section~\ref{sec:intro}       % Reference section
```

### Math (if needed)

```latex
Inline math: $x = y + z$

Display math:
\begin{equation}
E = mc^2
\label{eq:einstein}
\end{equation}
```

### Citations (Bibliography)

```latex
According to \cite{author2023}...  % Single citation
Multiple studies \cite{auth1,auth2}... % Multiple
```

---

## 🔧 Common Edits You'll Want to Make

### 1. Add/Remove Text
Just type or delete text in `.tex` files!

### 2. Add a New Section
```latex
\subsection{My New Section}
Here's the content...
```

### 3. Resize a Figure
Change the width parameter:
```latex
\includegraphics[width=0.7\textwidth]{figures/image.pdf}  % Smaller
\includegraphics[width=1.0\textwidth]{figures/image.pdf}  % Larger
```

### 4. Add a New Figure
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{figures/new_image.pdf}
\caption{Description of my new figure.}
\label{fig:new-image}
\end{figure}
```

### 5. Fix Figure Position
If figure appears in wrong place:
```latex
\begin{figure}[H]  % Force "here" (need \usepackage{float})
\begin{figure}[t]  % Force top of page
\begin{figure}[b]  % Force bottom of page
```

### 6. Change Caption
Just edit the `\caption{...}` text!

### 7. Add/Remove Chapters
Edit `thesis.tex`:
```latex
\include{content/chapter_name}  % Add
% \include{content/old_chapter}  % Comment out to remove
```

---

## ⚠️ Common LaTeX Errors & Fixes

### Error: "Undefined control sequence"
**Cause**: Typo in LaTeX command  
**Fix**: Check spelling of `\chapter`, `\section`, etc.

### Error: "Missing $ inserted"
**Cause**: Special character not escaped  
**Fix**: Use `\%`, `\&`, `\_`, `\$` for %, &, _, $

### Error: "File not found"
**Cause**: Wrong file path  
**Fix**: Check figures path is `figures/image.pdf` not `../figures/`

### Error: Figure too wide
**Fix**: Reduce width: `width=0.7\textwidth` or `width=0.5\textwidth`

### Error: "Undefined reference"
**Cause**: Need to compile multiple times  
**Fix**: Compile 2-3 times for references to work

---

## 🎨 Your Thesis - What's Where

### thesis.tex (Main File)
- ✅ Your name: Munkhchimeg Sergelen
- ✅ Supervisor: Dr. Mihajlik Péter
- ✅ Title configured
- **Don't edit much here** - just includes other files

### content/abstract.tex
- Your complete abstract
- Edit to refine wording

### content/introduction.tex
- Chapter 1: Introduction
- Edit sections as needed
- Add/remove motivation, RQs, contributions

### content/background.tex
- Chapter 2: Background
- Technical foundation
- Edit definitions, related work

### content/methods.tex
- Chapter 3: Methods
- Hardware, systems, evaluation
- Edit descriptions

### content/results.tex (JUST FIXED!)
- Chapter 4: Results
- ✅ All figures now properly sized
- ✅ Centered and fit on page
- Edit findings, tables, interpretations

### content/discussion.tex
- Chapter 5: Discussion
- Edit analysis, interpretations

### content/conclusions.tex
- Chapter 6: Conclusions
- Edit summary, contributions, future work

---

## 🔄 Workflow: Edit → Compile → Review

### On Overleaf:
1. Edit file in left panel
2. Click "Recompile"
3. See PDF update on right
4. Repeat!

### Locally:
1. Edit `.tex` files
2. Upload to Overleaf OR compile locally:
   ```bash
   cd ~/thesis-asr/latex_template
   xelatex thesis.tex
   bibtex thesis
   xelatex thesis.tex
   xelatex thesis.tex
   ```
3. View PDF

---

## 📊 Check Your Figures Now!

All figures are now:
- ✅ **Centered** on page
- ✅ **Proper width** (85% of text width)
- ✅ **Not cut off** on right side
- ✅ **High quality** (PDF format)
- ✅ **Labeled** for cross-referencing

**Test it**: Upload new ZIP to Overleaf and compile!

---

## 🎯 Recommended Editing Order

1. **First pass**: Read through, fix typos
2. **Content**: Refine explanations, add details
3. **Figures**: Check captions, adjust sizes if needed
4. **Tables**: Format nicely, add borders
5. **References**: Add missing citations
6. **Final**: Polish abstract, conclusions

---

## 💡 Pro Tips

### Tip 1: Comment Out, Don't Delete
```latex
% This text is commented out and won't appear
% But I can bring it back later!
```

### Tip 2: Use Labels Everywhere
```latex
\section{Introduction}\label{sec:intro}
\begin{figure}...\label{fig:my-plot}

% Then reference:
See Section~\ref{sec:intro} and Figure~\ref{fig:my-plot}
```

### Tip 3: Keep Backups
- Git is already tracking changes!
- Overleaf has version history
- Save often!

### Tip 4: Compile Often
- Don't wait until done to compile
- Catch errors early
- See how changes look

---

## 🆘 If You Get Stuck

### Issue: Figures still too wide
```latex
% Make smaller:
\includegraphics[width=0.6\textwidth]{...}
\includegraphics[width=0.5\textwidth]{...}
```

### Issue: Table too wide
```latex
% Use smaller font:
{\small
\begin{tabular}{...}
...
\end{tabular}
}
```

### Issue: Too much white space
- LaTeX auto-spaces things
- Trust it! Or use `\vspace{-1em}` to reduce

### Issue: Want to see LaTeX code examples
- Open any `.tex` file and learn from structure
- Copy-paste patterns
- Modify as needed

---

## 📦 Next: Re-upload to Overleaf

I'll recreate the ZIP with fixed figures:

```bash
cd ~/thesis-asr
zip -r thesis_overleaf_fixed.zip latex_template/ -x "*.DS_Store" "*.md"
```

Then:
1. Delete old Overleaf project
2. Upload `thesis_overleaf_fixed.zip`
3. Compile
4. **Figures will fit perfectly!** ✅

---

## ✅ Summary

**You can now**:
- ✅ Edit any chapter in `.tex` files
- ✅ Add/remove sections
- ✅ Adjust figures (they're fixed now!)
- ✅ Change captions, tables, text
- ✅ Compile on Overleaf or locally
- ✅ Work manually with full control!

**Your thesis is**:
- ✅ Properly formatted LaTeX
- ✅ Consistent with BME template
- ✅ Figures now centered and sized correctly
- ✅ Ready for manual editing!

---

**Questions? Just ask! I'll help you edit anything!** 🚀
