## Code to accompany the paper "Teaching Autoregressive Language Models Complex Tasks By Demonstration"

Transformer models are typically trained with large numbers of training examples. 
However, by fine-tuning a sufficiently large model on appropriately structured step-by-step demonstrations, 
some tasks that can Transformers can not accomplish well even with very many training examples become possible with a relative handful. 

By way of example, GPT-Neo can be trained to solve the numbers__div_remainder task from the DeepMind Mathematics Dataset with over 80% accuracy. 
This task essentially tests the ability to conduct modulo operations with large numbers (i.e., to solve division problems and report the remainders).
Saxton et al. reported below 40% accuracy on this task when training a Tranformer with 2 million training examples. However, by fine-tuning on an appropriate training dataset,
the smallest available GPT-Neo model achieves over 80% accuracy. This is achieved merely by adjusting the input data, without altering the learning algorithm in any way.
See the paper "[Teaching Autoregressive Language Models Complex Tasks By Demonstration](http://www.twonewthings.com/Teaching_Transformers_v2.pdf)" for more information.

This repository contains training, validation, and test data associated with the experiments in the paper, as well as the code for generating it. 
A Colab notebook for fine-tuning GPT-Neo on the dataset and evaluating the results can be found [here](https://colab.research.google.com/drive/1glgRxBepDVz6Lw2_cnsWbL6xZJXAthY3). The best fine-tuned model from the paper is available [here](https://drive.google.com/drive/folders/1kVCrpN1zrL3KXsyCPAZo10q011U6qjQM?usp=sharing).

<hr>

Notes:
* If you just want the training, validation, and test files from the paper, these can be found in data/formatted/. These were generated by running demonstrator.py on the files in data/original. The files in data/original were generated by running format_benchmarks.py to extract training, validation and test data from the [DeepMind Mathematics 
dataset](https://github.com/deepmind/mathematics_dataset).
* Correct demonstrations are included after the prefixes in the test files only for reference; these are *not* to be used by the model at test time. Note that the [evaluation code](https://colab.research.google.com/drive/1glgRxBepDVz6Lw2_cnsWbL6xZJXAthY3) uses only the string preceding the "|" symbol on each line as the prefix. The model then generates a continuation, and the evaluation code uses the final answer at the end of each line of the test file ("{ final remainder is ___ }") to evaluate the correctness of the solution.