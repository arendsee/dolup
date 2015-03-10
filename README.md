dolup
=====

Download or list UniProt proteomes descending from an ancestral node

Examples
========

List all options
```bash
$ dolup -h
```

List all taxon ids in the Nematoda phylum

```bash
$ dolup 6231
6253
6279
135651
6238
6239
281687
31234
7209
6282
54126
6334
6293
```

List only the reference species
```bash
$ dolup -r 6231
6238
6239
281687
54126
```

Download all reference species
```bash
$ dolup -rd 6231
Retrieving 6238.faa
Retrieving 6239.faa
Retrieving 281687.faa
Retrieving 54126.faa
```

Do the same but politely cache the results
```bash
$ dolup -rd --cache /tmp/uniprot-cache 6231
```
