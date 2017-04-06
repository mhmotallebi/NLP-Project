This project aims at annotating one side of a parallel corpus givene the annotated text of the other side and outputs of the GIZA++ sentence aligner.
For example, given a English-Persian parallel corpus, alignments created using GIZA++, and Annotations of English text, this program annotates Persian side.

More precisely, final file of Giza (containing sentences and ids of corresponding persian translation of each word in each sentence), vocabulary of the Persian (containing each word and its id), tokenized persian and english texts, annotated English text (preferrably tokenized in advance) are needed. The annotated English text may differ in each project, hence may need to modify the code accordingly.
