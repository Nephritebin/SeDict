## SeDict: Search your unknown words in an essay automatically.

This project is going to help you generate a pdf file automatically with a input english essay, fiction or just a sentence. The pdf file will contain the unknown words in the sentence with their meanings and examples from high-quality English-English dictionary. We hope that this project will help you to improve your English skills and save your time for English intensive reading exercises.

We use the [COCA]() dataset to check the frequency of the words, and then filter the high frequency words in default. You can also set the frequency threshold or the filtering algorithm by yourself.

### Installation
You need to install [Conda]() first. Then create a new environment and install the requirements. I also highly recommend you install [texlive](), which is used to generate the pdf file. Or you can use Overleaf for tex compiling.

```
conda create -n language python=3.8
pip install -r requirements.txt
conda install -c conda-forge weasyprint
```

### Bug Fix

```
  File "D:\Programs\Anaconda\envs\test2\lib\site-packages\weasyprint\pdf\stream.py", line 61, in __init__
    in md5(description_string, usedforsecurity=False).digest()[:6])
TypeError: openssl_md5() takes at most 1 argument (2 given)
```

```
in md5(description_string).
```