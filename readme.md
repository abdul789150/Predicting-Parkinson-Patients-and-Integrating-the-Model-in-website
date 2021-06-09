## Breif Description about Problem Statment and its Solution
The Machine Learning model which is presented in this notebook is for detecting patients with Parkinson disease.
I have used the data set from `UCI Machine Learning Repository`.

This dataset is composed of a range of biomedical voice measurements from 31 people, 23 with Parkinson's disease (PD). Each column in the table is a particular voice measure, and each row corresponds one of 195 voice recording from these individuals (`name` column). In this dataset the targeted values in given in `status column`, according to `status column` **0 indicates healthy** and **1 indicates Parkinson patient**.


The process for creating the ML model is breifly explained in the ste

- **Step1:** `Reading dataset`
    - In the first step we will read the dataset which is stored in `parkinsons.data` file. For reading the dataset we will use `pandas` library.  
    

- **Step2:** `Data Cleaning`
    - Now after step 1, we will explore the dataset to find if that dataset has any missing values or not, missing values in the dataset decreases the accuracy of the model and also makes it worse. And after that we will split our features and target label (class column) for the dataset, in our case `status` is the column in which target labels/ classses exits so that's why we will split this column from features.


- **Step3:** `Feature Analysis`
    - In this step we will use correlation analysis to analyze all the features which are given in the dataset. Then on the basis of correlation analysis result we will remove the columns with less score. And after that we will also remove `name` column because `name` colun just contains the name or id of the patient and that is not useful to predict any value. 
  
  
- **Step4:** `Data Transformation`
    - Now we will split the data into two subsets `Training` and `Testing`, we will take **20%** as testing data and **80%** as training data. Now we have two subsets of dataset, we know that Neural Networks accepts only vectors as input, so for this purpose we will transform our data into vector form by using `numpy` library. 
    
    
- **Step5:** `Neural Network`
    - In this step we will implement `Neural Network`, in the steps given below I have defined the steps which are required to define and train the neural network model:
    - We will define a `Neural Network` architecture which we will use to detect healthy/sick patients.
    - We will use `cross validation` technique to prevent overfitting.
    - We will also use `Dropout Layers`, this method also prevents overfitting.
    - After all these steps we will train and test the model.
    
    
- **Step6:** `Saving information`
    - In the last step we will need to save some of the information in files. We will store the `Neural Network model` and `weights` of the model, by the help of this step we don't need t train the model again and again for usage, we will just read the trainned model from the file and it will predict results for us.
    

## How you can run the web project for parkinson patient detection
For running this project you will need following things

- installation of django ( pip install django) 
- installation of mysql client for django
- install xampp ( lampp if using linux )

Then start xampp, and run phpmyadmin, and database, after that open up the browser and goto "localhost/phpmyadmin", now here create a new database with the name "parkinson_db"

 
Then first go inside the directory ```parkinson``` where you can find "migrations.py" file, open the terminal/command line within that directory and run the following commands

- python manage.py makemigrations
- python manage.py migrate

Then for loading FAQ's into database run the following commands

- python manage.py loaddata /path-to/fixtures/topic.json
- python manage.py loaddata /path-to/fixtures/faq.json 

After all that run the command below to run the website

- python manage.py runserver
