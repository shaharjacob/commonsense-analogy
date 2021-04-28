# commonsense-analogy

## Goal
Our main goal is to understand analogy, for example:  

**1) Finding a good man is like finding a needle in a haystack:**  
As Dusty Springfield knows, finding a small needle in a pile of hay takes a long time, so the task at hand is likely to be hard and tedious.  
https://examples.yourdictionary.com/analogy-ex.html  
  
**2) That's as useful as rearranging deck chairs on the Titanic:**
 It looks like you're doing something helpful but really it will make no difference in the end.  
 https://examples.yourdictionary.com/analogy-ex.html  
  
**3) DNA replication ~ a train track**  
The DNA is like a train track that gets pulled apart by the train.  
http://www.metamia.com/critique-dna-replication-like-a-train-track-1345  
  
**4) paragraph ~ a family**  
A paragraph is like a family. In a family, all the members are related. In a paragraph, all the sentences are related.  
http://www.metamia.com/critique-paragraph-like-family-6055  

**5) Sunscreen protects against the sun just as a tarpaulin protects against rain**  
&nbsp;  

## Table of content
- **main.py**: main script which is combine all the script and plot a graph.  
- **google_autocomplete.py**: Extracting information from google auto-complete.  
- **quasimodo.py**: Using quasimodo database for extracting information about connections between objects.  
- **wikifier.py**: Extracting information about the part-of-speech of the given text.  
- **dictionary.py**: Extracting information on a word such as synonyms, antonyms, meanings and examples.  
- **metamia.py**: Building a database of analogies using http://www.metamia.com  
&nbsp;  

## main.py
1) Taking a text and extract the **nouns** using wikifier part-of-speech.  
2) For each noun, which will be a **node in our graph**, extract the information from quasimodo (single subject information).  
3) For each pair of nouns, extract inforamtion from google auto-complete, with a question ('why do', 'how do'). This will be on the edges.  
4) For each pair, extract information from quasimodo. This is also will be on the edges.  

```bash
python main.py

# text for example:
'electrons revolve around the nucleus as the stars revolve around the sun'

# the output graph can be found here:
```  
[Click here!](https://github.com/shaharjacob/commonsense-analogy/blob/main/MyGraph.gv.pdf)  
&nbsp;  

## google engine
This script using the API of google auto-complete the extract information.  
We are using question, subject and object which make the results more detailed.
By default the forms is: **{question} {subject} "*" {object}**  
for example: why do horses "*" stables  
&nbsp;  
by default, the script is looking also for the plural and singular forms of the inputs.  
For example, **horses** will convert into **horse** (in addition) and **stables** into **stable**.  
&nbsp;  
in addition, the script is able to looking for **synonyms**.  
It's taking the **best 5** results according to the word vector comparison.  
more information in dictionary.py section.  
Notice that this is a very heavy to load dictionary.py.  
```bash
# using default example.yaml file without saving the results into a file
python google_autocomplete.py

# define a yaml file:
why do:
  - [horses, stables]

how do:
  - [horses, stables]


# You can use it outside the script by define a dictionary:
from google_autocomplete import process

d = {
  "why do": [
    ['horses', 'stables']
  ],
  "how do": [
    ['horses', 'stables']
  ]
}
suggestions = process(d)

# the output will be:
```  
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/google_engine_horses.png?raw=true)  
&nbsp;  

## quasimodo
This script using quasimodo database, which contains semantic information.  
We are intersting in the following fields: **subject**, **predicate**, **object**, and **score**.  
First, the script cleaning rows with low score. Then, it allow to get information about connections between object.  

```bash
# Download the .tsv file in necessary: 
https://nextcloud.mpi-klsb.mpg.de/index.php/s/Sioq6rKP8LmjMDQ/download?path=%2FLatest&files=quasimodo43.tsv

# usage
from quasimodo import Quasimodo

# heigher score_threshold -> more accurate results, but less amount.
quasimodo = Quasimodo(score_threshold=0.8)

# get information on a single subject. n_largest will take the best matches according to quasimodo score.
quasimodo.get_subject_props('horses', n_largest=10, verbose=True, plural_and_singular=True)

# so the output will be:  
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/quasimodo_get_subject_props.png?raw=true)  

```bash
# get all the connections between each pair (connection is subject-object relationship)
quasimodo.get_subject_object_props('horses', 'stables', n_largest=10, verbose=True, plural_and_singular=True)

# so the output will be:  
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/quasimodo_get_subject_object_props.png?raw=true)  

```bash
# get all the similiar properties between two subjects
quasimodo.get_similarity_between_subjects('horse', 'cow', n_largest=10, verbose=True, plural_and_singular=True)

# so the output will be:  
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/quasimodo_get_similarity_between_subjects.png?raw=true)  
&nbsp;  

## Wikifier
This script is extracting information from a text, such as part-of-speech.  
It using wikifier API for that purpose.  

**Notice**: The tool is ignoring special character inside the text, expect ','  
i.e. the output of "I lo!ve coding??" and "I love coding" will be the same.  

```bash
# usage
from wikifier import Wikifier

text_to_analyze = "I love coding but sometimes coding is very boring"
wikifier = Wikifier(text_to_analyze)
wikifier.get_part_of_speech()

# output:  
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/wikifier_get_part_of_speech2.png?raw=true)  

```bash
text_to_analyze = "sunscreen protects against the sun as a tarpaulin protects against rain"
wikifier = Wikifier(text_to_analyze)
wikifier.get_part_of_speech()

# output:  
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/wikifier_get_part_of_speech1.png?raw=true)  
&nbsp;   

## Synonyms and Antonyms
The script is getting information on a specific word,s such as **synonyms**, **antonyms**, meanings and examples.  
The main use is for synonyms. There are two classes that getting synonyms, *WordNet* and *Dictionary*. And a third class called *Mixed*, which combained both together and taking the best results.
&nbsp;  

The best results are calculate with distance function based on word-vector, using gensim package (https://radimrehurek.com/gensim).  
Because of the use of this package, script that using this file (including google_autocomplete.py) have a long pre-loaing time (aroung 10-20 seconds).
&nbsp;

**notice**: words such as "Equus caballus" or "stalking-horse" that are not contains inside the gensim corups will be ignored.  

```bash
# usage
from dictionary import Mixed

# example 1 
mixed = Mixed('horse')
mixed.getSynonyms()

# output of WordNet: horse, cavalry, knight, buck, sawbuck
# output of Dictionary: horseback, racehorse, pony, chestnut, mare
# and the mixed output:
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/dictionary_best_5_for_horse.png?raw=true)  
&nbsp;   

```bash
# example 2 
mixed = Mixed('increase')
mixed.getSynonyms()

# output of WordNet: decrease, narrow, wane, depreciate
# output of Dictionary: increase, growth, gain, addition, increment
# and the mixed output:
```
![alt text](https://github.com/shaharjacob/commonsense-analogy/blob/main/images/dictionary_best_5_for_increase.png?raw=true)  
&nbsp;  

## metamia randomizer
This site (http://www.metamia.com) has a lot of complex analogy, but a list of all the analogy isn't available (or dataset), but there is a page which return a random analogy (http://www.metamia.com/randomly-sample-the-analogy-database).  
So the script is iterate this page and parsing the analogy, and by that creates a big dataset.  

```bash
# usage (-i is the number of iteration)
python metamia.py -i 100 -o out.csv
```  
&nbsp;  

## references
- **Quasimodo**: https://quasimodo.r2.enst.fr/  
- **qa-srl**: http://qasrl.org/  
- **hayadata-lab**: http://www.hyadatalab.com/  
- **Wikifier**: http://wikifier.org/info.html/  
- **gensim**: https://radimrehurek.com/gensim/  
&nbsp;  
  
## Analogy datasets
- **metamia**: http://www.metamia.com/
- **Vecto**: https://vecto.space/  
&nbsp;  

## PDFs
**Analogy-based Detection of Morphological and Semantic Relations With Word Embeddings: What Works and What Doesn’t**:  
- https://www.aclweb.org/anthology/N16-2002.pdf

**Using Analogy To Acquire CommonsenseKnowledge from Human Contributors**:  
- https://dspace.mit.edu/handle/1721.1/87342  
  
**Reasoning and Learning by Analogy**:  
- https://psycnet.apa.org/doiLanding?doi=10.1037%2F0003-066X.52.1.32  
  
**The Analogical Mind**:  
- https://books.google.co.il/books?hl=iw&lr=&id=RfQX9wuf-2cC&oi=fnd&pg=PA23&dq=commonsense+analogy&ots=MvkNlPPSyo&sig=fsznpCd12ZuybvtaJnpqPzzvHk4&redir_esc=y#v=onepage&q=commonsense%20analogy&f=false   
&nbsp;     

## Additions
- https://examples.yourdictionary.com/analogy-ex.html  
- https://songmeanings.com
- https://www.songfacts.com

