# Note

Dear CS4487er,

Please be informed that:

1. The test codes of the course project should be submitted as an ipynb file (Do not include other unnecessary codes and files) and MUST be easy for TAs to run. Here we provide a template for reference：

```
def test(model, data_path):
      Accuracy, Recall, Precision, AUC = 0, 0, 0
      """
      You need to finish this function.
      """
      return Accuracy, Recall, Precision, AUC
```

2. The data to be released this late week should be split in your way and placed in the following structure before you start your course project. Correspondingly, the dataset loader in your submitted test code should be written in consistency with this data structure.

```
|--- data
	|--- train
		|---0001.png
		|---...
	|--- val
		|---...
	|--- test
		|---...
```

3. Since test sets will NOT be released to the students, each group has THREE chances before the due date (Dec. 4, 2022, 11:59 pm) to get access to the test sets for ranking.

4. Some useful resources to get started can be found at 

   https://github.com/HongguLiu/Deepfake-Detection

   https://pytorch.org/tutorials/beginner/basics/data_tutorial.html

   https://learn.microsoft.com/en-us/windows/ai/windows-ml/tutorials/pytorch-train-model
   
   https://www.kaggle.com/code/basu369victor/pytorch-tutorial-the-classification/notebook.

5. Pretrained models are allowed as long as they are not pre-trained on the exact task of DeepFake detection. In other words, you cannot use other DeepFake datasets to train or finetune your models.

6. Please send your test codes to any of the following emails: * and *.

Should you have any questions, feel free to contact our TA team.

Regards,

CS4487 TA Team