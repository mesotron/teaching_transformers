## Code to accompany the paper "Teaching Transformers"

Transformer models are typically trained with large numbers of training examples. 
However, by fine-tuning a sufficiently large model on appropriately structured step-by-step demonstrations, 
some tasks that can Transformers can not accomplish well even with very many training examples become possible with a relative handful. 

By way of example, GPT-Neo can be trained to solve the numbers__div_remainder task from the DeepMind Mathematics Dataset with over 80% accuracy. 
This task essentially tests the ability to conduct modulo operations with large numbers (i.e., to solve division problems and report the remainders).
Saxton et al. reported below 40% accuracy on this task when training a Tranformer with 2 million training examples. However, by fine-tuning on an appropriate training dataset,
the smallest available GPT-Neo model achieves over 80% accuracy. This is achieved merely by adjusting the input data, without altering the model in any way.
See the paper "[Teaching Transformers](http://www.twonewthings.com/Teaching_Transformers_v2.pdf)" for more information

This repository contains training, validation, and test data associated with the experiments in the paper, as well as the code for generating it. 
A Colab notebook for fine-tuning GPT-Neo on the dataset and evaluating the results can be found at https://colab.research.google.com/drive/1glgRxBepDVz6Lw2_cnsWbL6xZJXAthY3.
