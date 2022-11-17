# Meduzzen Test Project
Service to control user registration for  different services



## Getting Started

1. Clone the project from the Github repo :

````
git clone https://github.com/khodjiyev2o/Test_project_meduzzen
````
2. Go to the project directory  

3. Create virtual environment :

````
python3 -m venv venv
````

4. Activate virtual environment  : 

````
source\venv\bin\activate

````
if you are using Windows ,then :
````
venv\Scripts\activate
````

3.Run the server 
````
$ uvicorn main:app --reload
````
````--reload```` flag makes the server restart after code changes. Only use for development.